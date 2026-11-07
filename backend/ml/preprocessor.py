import cv2
import numpy as np
import os
import logging
from skimage.feature import hog

log = logging.getLogger(__name__)

IMG_SIZE = (128, 128)
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}


def extract_hog(img_gray):
    features, _ = hog(
        img_gray,
        orientations=9,
        pixels_per_cell=(16, 16),
        cells_per_block=(2, 2),
        visualize=True
    )
    return features


def load_images_from_folder(dataset_path):
    log.info("=== CARREGAMENTO DO DATASET ===")
    log.info(f"Pasta: {dataset_path}")

    X, y = [], []
    classes = sorted([
        d for d in os.listdir(dataset_path)
        if os.path.isdir(os.path.join(dataset_path, d))
    ])

    if len(classes) < 2:
        raise ValueError("O dataset precisa ter ao menos 2 subpastas (classes).")

    log.info(f"Classes encontradas ({len(classes)}): {classes}")

    skipped_total = 0
    for label, class_name in enumerate(classes):
        class_path = os.path.join(dataset_path, class_name)
        loaded = 0
        skipped = 0
        for fname in os.listdir(class_path):
            ext = os.path.splitext(fname)[1].lower()
            if ext not in SUPPORTED_EXTENSIONS:
                skipped += 1
                continue
            img_path = os.path.join(class_path, fname)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None:
                log.warning(f"  Nao foi possivel ler: {fname}")
                skipped += 1
                continue
            img = cv2.resize(img, IMG_SIZE)
            X.append(extract_hog(img))
            y.append(label)
            loaded += 1

        if loaded == 0:
            raise ValueError(f"Nenhuma imagem válida encontrada em: {class_path}")

        log.info(f"  [{label}] {class_name}: {loaded} imagens carregadas"
                 + (f" ({skipped} ignoradas)" if skipped else ""))
        skipped_total += skipped

    log.info(f"Total: {len(X)} imagens | {len(classes)} classes"
             + (f" | {skipped_total} arquivos ignorados" if skipped_total else ""))
    log.info("Extraindo features HOG...")
    return np.array(X), np.array(y), classes


def preprocess_single_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise ValueError(f"Não foi possível carregar: {img_path}")
    img = cv2.resize(img, IMG_SIZE)
    return extract_hog(img).reshape(1, -1)
