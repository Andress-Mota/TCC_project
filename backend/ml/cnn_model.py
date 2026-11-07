import io
import random
import logging
import numpy as np
import cv2
from PIL import Image

log = logging.getLogger(__name__)

try:
    import torch
    import torch.nn as nn
    from torchvision.models import efficientnet_b0, EfficientNet_B0_Weights
    import torchvision.transforms as T
    from torch.utils.data import DataLoader, Subset
    from torchvision.datasets import ImageFolder
    _TORCH_OK = True
except ImportError:
    _TORCH_OK = False

_DEVICE = 'cpu'
if _TORCH_OK:
    try:
        _DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
    except Exception:
        _DEVICE = 'cpu'

_TRANSFORM_VAL = None
_TRANSFORM_TRAIN = None

if _TORCH_OK:
    _TRANSFORM_VAL = T.Compose([
        T.Resize(256),
        T.CenterCrop(224),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])
    _TRANSFORM_TRAIN = T.Compose([
        T.Resize(256),
        T.RandomCrop(224),
        T.RandomHorizontalFlip(),
        T.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.1),
        T.ToTensor(),
        T.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ])


class _GradCAM:
    def __init__(self, model):
        self.model  = model
        self._grads = None
        self._acts  = None
        target      = model.features[-1]
        self._fwd   = target.register_forward_hook(self._save_act)
        self._bwd   = target.register_full_backward_hook(self._save_grad)

    def _save_act(self, module, inp, out):
        self._acts = out.detach()

    def _save_grad(self, module, grad_in, grad_out):
        self._grads = grad_out[0].detach()

    def generate(self, img_tensor):
        self.model.eval()
        with torch.set_grad_enabled(True):
            out   = self.model(img_tensor)
            probs = torch.softmax(out, dim=1)
            idx   = probs.argmax(1).item()
            conf  = probs[0, idx].item()
            self.model.zero_grad()
            out[0, idx].backward()

        w   = self._grads.mean(dim=(2, 3), keepdim=True)
        cam = torch.relu((w * self._acts).sum(dim=1)).squeeze().cpu().numpy()
        mn  = cam.min()
        mx  = cam.max()
        if mx > mn:
            cam = (cam - mn) / (mx - mn)
        else:
            cam = np.zeros_like(cam)
        return cam, idx, conf

    def remove(self):
        self._fwd.remove()
        self._bwd.remove()


def _build_model(num_classes):
    model = efficientnet_b0(weights=EfficientNet_B0_Weights.IMAGENET1K_V1)
    in_f  = model.classifier[1].in_features
    model.classifier[1] = nn.Linear(in_f, num_classes)
    return model.to(_DEVICE)


def train_cnn(dataset_path, classes, callback=None, epochs=8):
    """
    Fine-tunes EfficientNet-B0 on dataset_path.
    callback(pct_0_100, msg) called each batch.
    Returns (model, val_accuracy).
    """
    if not _TORCH_OK:
        raise RuntimeError('torch/torchvision não instalado. Execute: pip install torch torchvision')

    import torch.optim as optim
    from torch.optim.lr_scheduler import OneCycleLR

    num_classes = len(classes)
    log.info(f"[CNN] Iniciando treino — {num_classes} classes | device={_DEVICE} | epochs={epochs}")

    ds_train = ImageFolder(dataset_path, transform=_TRANSFORM_TRAIN)
    ds_val   = ImageFolder(dataset_path, transform=_TRANSFORM_VAL)

    indices = list(range(len(ds_train)))
    rng = random.Random(42)
    rng.shuffle(indices)
    n_val     = max(1, int(len(indices) * 0.2))
    val_idx   = indices[:n_val]
    train_idx = indices[n_val:]

    train_ds = Subset(ds_train, train_idx)
    val_ds   = Subset(ds_val,   val_idx)

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True,  num_workers=0, pin_memory=False)
    val_loader   = DataLoader(val_ds,   batch_size=32, shuffle=False, num_workers=0, pin_memory=False)

    model     = _build_model(num_classes)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-4)
    scheduler = OneCycleLR(optimizer, max_lr=1e-3,
                           steps_per_epoch=len(train_loader), epochs=epochs)

    total_batches = epochs * len(train_loader)
    step = 0

    for epoch in range(epochs):
        model.train()
        running_loss = 0.0
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(_DEVICE), labels.to(_DEVICE)
            optimizer.zero_grad()
            loss = criterion(model(imgs), labels)
            loss.backward()
            optimizer.step()
            scheduler.step()
            running_loss += loss.item()
            step += 1
            if callback:
                pct = int(step / total_batches * 100)
                callback(pct, f'CNN — época {epoch + 1}/{epochs} ({pct}%)')

        avg_loss = running_loss / len(train_loader)
        log.info(f"[CNN] Época {epoch + 1}/{epochs} — loss: {avg_loss:.4f}")

    model.eval()
    correct = total = 0
    with torch.no_grad():
        for imgs, labels in val_loader:
            imgs, labels = imgs.to(_DEVICE), labels.to(_DEVICE)
            preds   = model(imgs).argmax(1)
            total   += labels.size(0)
            correct += (preds == labels).sum().item()

    val_acc = correct / total if total else 0.0
    log.info(f"[CNN] Validação final: {val_acc * 100:.2f}%")
    return model, val_acc


def save_cnn(model, classes, path):
    torch.save({'state_dict': model.state_dict(), 'classes': classes}, path)
    log.info(f"[CNN] Modelo salvo: {path}")


def gradcam_overlay(model_path, img_bytes, classes):
    """
    Generates a Grad-CAM heatmap overlaid on the original image.
    Returns (pred_class: str, confidence: float, jpeg_bytes: bytes).
    """
    if not _TORCH_OK:
        raise RuntimeError('torch/torchvision não instalado.')

    num_classes = len(classes)
    ckpt  = torch.load(model_path, map_location=_DEVICE, weights_only=False)
    model = _build_model(num_classes)
    model.load_state_dict(ckpt['state_dict'])
    loaded_classes = ckpt.get('classes', classes)
    model.eval()

    img_pil    = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    img_tensor = _TRANSFORM_VAL(img_pil).unsqueeze(0).to(_DEVICE)

    cam_gen = _GradCAM(model)
    cam, idx, conf = cam_gen.generate(img_tensor)
    cam_gen.remove()

    pred_class = loaded_classes[idx] if idx < len(loaded_classes) else classes[idx]

    img_np  = np.array(img_pil)
    h, w    = img_np.shape[:2]
    cam_up  = cv2.resize(cam, (w, h))
    heatmap = cv2.applyColorMap(np.uint8(cam_up * 255), cv2.COLORMAP_JET)
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
    overlay = cv2.addWeighted(img_bgr, 0.55, heatmap, 0.45, 0)

    ok, buf = cv2.imencode('.jpg', overlay, [cv2.IMWRITE_JPEG_QUALITY, 88])
    if not ok:
        raise RuntimeError('Falha ao codificar imagem Grad-CAM')

    return pred_class, conf, bytes(buf)
