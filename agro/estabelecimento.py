import time

import pyautogui

from agro.taxa_servico import fechar_tela_taxa_servico_ctrl_f4
from indetificador import focar_janela_por_titulo
from windows.alerts import confirmar_todas_atencoes
from windows.window_utils import obter_titulo_janela_ativa


def enviar_shift_f12():
    print("Enviando SHIFT + F12...")

    focar_janela_por_titulo("AGRO-AG")
    time.sleep(0.3)

    pyautogui.hotkey("shift", "f12")
    time.sleep(0.8)

    return True


def enviar_ctrl_tab():
    print("Enviando CTRL + TAB...")

    pyautogui.hotkey("ctrl", "tab")
    time.sleep(0.5)

    return True


def formatar_valor_tela(valor):
    if valor is None:
        return ""

    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))

    return str(valor).strip()


def trocar_estabelecimento(estab):
    estab_texto = formatar_valor_tela(estab)

    if estab_texto == "":
        print("ESTAB vazio. Não foi possível trocar estabelecimento.")
        return False

    print("Trocando estabelecimento para:", estab_texto)

    if not fechar_tela_taxa_servico_ctrl_f4(timeout=1):
        print("Não foi possível fechar a tela de taxa antes da troca de estabelecimento.")
        return False

    focar_janela_por_titulo("AGRO-AG")
    time.sleep(0.8)

    titulo_ativo, classe_ativa = obter_titulo_janela_ativa()
    print("Janela ativa antes do SHIFT+F12:", titulo_ativo, "| Classe:", classe_ativa)

    if not enviar_shift_f12():
        print("Falha ao enviar SHIFT + F12.")
        return False

    confirmar_todas_atencoes(timeout_primeira=1.5)
    time.sleep(0.5)

    if not enviar_ctrl_tab():
        print("Falha ao enviar CTRL + TAB.")
        return False

    time.sleep(0.5)

    titulo_ativo, classe_ativa = obter_titulo_janela_ativa()
    print("Janela ativa antes de digitar ESTAB:", titulo_ativo, "| Classe:", classe_ativa)

    print("Digitando ESTAB:", estab_texto)
    pyautogui.write(estab_texto)
    time.sleep(0.4)

    for tentativa in range(4):
        print(f"Confirmando ESTAB com ENTER {tentativa + 1}/4...")
        pyautogui.press("enter")
        time.sleep(0.8)
        confirmar_todas_atencoes(timeout_primeira=1.2)

    focar_janela_por_titulo("AGRO-AG")
    time.sleep(0.8)

    print("ESTAB informado com sucesso:", estab_texto)

    return True
