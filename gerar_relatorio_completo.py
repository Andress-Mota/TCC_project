#!/usr/bin/env python3
"""TCC FATEC-GT 2026 — Script principal FINAL 200+"""
from tcc_parte1 import PDF, capa, verso, resumo, listas, sumario
from tcc_parte2 import introducao, cap1_s1, cap1_knn, cap1_svm
from tcc_parte3 import cap1_rf_lr_nb, cap1_ensemble, cap1_cnn, cap1_hog, cap1_metricas
from tcc_parte4 import cap2, cap3_inicio
from tcc_parte5 import cap3_db, cap3_api, cap3_ml_module, cap3_cnn_front
from tcc_parte6 import cap3_sec, cap4, conclusao, referencias, apendices
from tcc_parte7 import (cap_trabalhos_relacionados, cap1_extra,
                        cap3_extra, cap4_extra, apendice_c)
from tcc_parte8 import (cap1_exemplos_praticos, cap2_extra,
                        cap3_frontend_extra, cap4_discussao_expandida,
                        apendice_d)
from tcc_parte9 import (estado_arte_completo, cap1_matematica_extra,
                        cap3_auth_extra, glossario,
                        cap4_por_algoritmo, apendice_e)
from tcc_parte10 import (cap1_teoria_aprendizado, cap2_design_experimento,
                         cap3_seguranca_aprofundada,
                         cap4_analise_knn_parametros_extra,
                         cap3_testes_sistema, cap_consideracoes_extra)
from tcc_parte11 import (tutorial_uso_sistema, cap1_revisao_hist,
                         cap3_banco_extra, cap4_resultados_extras)

OUTPUT = r"c:\Users\andre\Documents\TCC project\RELATORIO_TCC_FATEC_COMPLETO.pdf"

def main():
    pdf = PDF()

    print("[ 1/7 ] Pre-textuais...")
    capa(pdf); verso(pdf); resumo(pdf); listas(pdf); sumario(pdf)

    print("[ 2/7 ] Introducao...")
    introducao(pdf)

    print("[ 3/7 ] Capitulo 1 — Referencial Teorico...")
    cap1_s1(pdf); cap1_knn(pdf); cap1_svm(pdf)
    cap1_rf_lr_nb(pdf); cap1_ensemble(pdf)
    cap1_cnn(pdf); cap1_hog(pdf); cap1_metricas(pdf)
    cap1_extra(pdf)
    cap1_exemplos_praticos(pdf)
    cap1_matematica_extra(pdf)
    cap1_teoria_aprendizado(pdf)
    cap1_revisao_hist(pdf)
    estado_arte_completo(pdf)

    print("[ 4/7 ] Capitulo 2 — Metodologia...")
    cap2(pdf); cap2_extra(pdf); cap2_design_experimento(pdf)
    cap_trabalhos_relacionados(pdf)

    print("[ 5/7 ] Capitulo 3 — Sistema...")
    cap3_inicio(pdf); cap3_db(pdf); cap3_api(pdf)
    cap3_ml_module(pdf); cap3_cnn_front(pdf); cap3_sec(pdf)
    cap3_extra(pdf); cap3_frontend_extra(pdf); cap3_auth_extra(pdf)
    cap3_seguranca_aprofundada(pdf); cap3_testes_sistema(pdf)
    cap3_banco_extra(pdf)

    print("[ 6/7 ] Capitulo 4 — Resultados...")
    cap4(pdf); cap4_extra(pdf)
    cap4_discussao_expandida(pdf); cap4_por_algoritmo(pdf)
    cap4_analise_knn_parametros_extra(pdf)
    cap4_resultados_extras(pdf)

    print("[ 7/7 ] Consideracoes Finais, Referencias e Apendices...")
    conclusao(pdf); cap_consideracoes_extra(pdf)
    referencias(pdf); glossario(pdf)
    apendices(pdf); apendice_c(pdf); apendice_d(pdf)
    apendice_e(pdf); tutorial_uso_sistema(pdf)

    pdf.output(OUTPUT)
    print(f"\n{'='*60}")
    print(f"PDF gerado: {OUTPUT}")
    print(f"Total de paginas: {pdf.page}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
