import os
import subprocess
import time

import pyautogui

from indetificador import focar_janela_por_titulo
from windows.alerts import confirmar_todas_atencoes


def abrir_agro(settings):
    subprocess.run(
        ["taskkill", "/F", "/IM", settings.processo_agro],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    time.sleep(0.8)

    try:
        os.startfile(settings.caminho_agro)
        print("Agro aberto com sucesso.")

    except Exception as erro:
        print("Erro ao abrir o Agro.")
        print(erro)
        return False

    try:
        focar_janela_por_titulo("Seleção de Usuário")
        time.sleep(2)

        print("Voltando para o campo de usuário com SHIFT + TAB...")
        pyautogui.hotkey("shift", "tab")
        time.sleep(0.3)

        print("Digitando usuário do Agro...")
        pyautogui.write(settings.usuario_agro)
        time.sleep(0.3)

        print("Indo para o campo de senha com TAB...")
        pyautogui.press("tab")
        time.sleep(0.3)

        print("Digitando senha do Agro...")
        pyautogui.write(settings.senha_agro)
        time.sleep(0.3)

        print("Confirmando login com ENTER...")
        pyautogui.press("enter")
        time.sleep(1)

        confirmar_todas_atencoes(timeout_primeira=1.5)

        print("Enviando ENTER adicional após login...")
        pyautogui.press("enter")
        time.sleep(0.8)

    except Exception as erro:
        print("Erro ao focar/preencher a tela de usuário.")
        print(erro)
        return False

    confirmar_todas_atencoes(timeout_primeira=1.5)

    try:
        focar_janela_por_titulo("Seleção de Estabelecimento para Trabalho")
        time.sleep(0.8)

        print("Tela de estabelecimento apareceu. Confirmando com ENTERs e tratando Atenção/Erro.")

        for tentativa in range(2):
            print(f"ENTER na tela de estabelecimento {tentativa + 1}/2...")
            pyautogui.press("enter")
            time.sleep(0.8)
            confirmar_todas_atencoes(timeout_primeira=1.2)

        print("Tela de estabelecimento confirmada.")

    except Exception:
        print("Tela de estabelecimento não apareceu. Continuando para AGRO-AG.")

    confirmar_todas_atencoes(timeout_primeira=1.5)

    try:
        focar_janela_por_titulo("AGRO-AG")
        time.sleep(1)

        print("Tela principal AGRO-AG focada.")
        return True

    except Exception as erro:
        print("Erro ao focar a tela principal AGRO-AG.")
        print(erro)
        return False
