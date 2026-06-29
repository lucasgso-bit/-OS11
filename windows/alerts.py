import time

import pyautogui
import win32con
import win32gui

from utils.text import normalizar_texto
from windows.window_utils import (
    aguardar_janela_sumir,
    focar_hwnd,
)


def aviso_eh_final(hwnd_alerta, titulo_alerta, classe_alerta):
    titulo_normalizado = normalizar_texto(titulo_alerta)
    classe_normalizada = str(classe_alerta or "").strip()

    if titulo_normalizado == "aviso" and classe_normalizada == "#32770":
        print("Aviso final identificado por título e classe.")
        print("Título:", titulo_alerta)
        print("Classe:", classe_alerta)
        print("HWND:", hwnd_alerta)
        return True

    return False


def aguardar_alerta_32770(timeout=2):
    inicio = time.time()

    while time.time() - inicio < timeout:
        hwnd_encontrado = None
        titulo_encontrado = ""
        classe_encontrada = ""

        def procurar(hwnd, _):
            nonlocal hwnd_encontrado, titulo_encontrado, classe_encontrada

            if hwnd_encontrado:
                return

            if not win32gui.IsWindowVisible(hwnd):
                return

            titulo = win32gui.GetWindowText(hwnd).strip()
            classe = win32gui.GetClassName(hwnd).strip()
            titulo_normalizado = normalizar_texto(titulo)

            titulo_eh_alerta = titulo_normalizado in (
                "atencao",
                "aviso",
                "erro",
            )

            classe_eh_alerta = classe in (
                "#32770",
                "TMessageForm",
            )

            if titulo_eh_alerta and classe_eh_alerta:
                hwnd_encontrado = hwnd
                titulo_encontrado = titulo
                classe_encontrada = classe

        win32gui.EnumWindows(procurar, None)

        if hwnd_encontrado:
            return hwnd_encontrado, titulo_encontrado, classe_encontrada

        time.sleep(0.1)

    return None, "", ""


def enviar_enter_teclado():
    print("Enviando ENTER direto pelo teclado...")

    pyautogui.keyDown("enter")
    time.sleep(0.08)
    pyautogui.keyUp("enter")
    time.sleep(0.7)


def enviar_enter_direto_no_hwnd(hwnd_alerta):
    if not hwnd_alerta:
        return False

    try:
        print("Enviando ENTER direto no HWND:", hwnd_alerta)

        win32gui.PostMessage(
            hwnd_alerta,
            win32con.WM_KEYDOWN,
            win32con.VK_RETURN,
            0,
        )
        time.sleep(0.1)

        win32gui.PostMessage(
            hwnd_alerta,
            win32con.WM_KEYUP,
            win32con.VK_RETURN,
            0,
        )
        time.sleep(0.8)

        return True

    except Exception as erro:
        print("Erro ao enviar ENTER direto no HWND.")
        print(erro)
        return False


def focar_alerta_somente_se_precisar(hwnd_alerta):
    if not hwnd_alerta:
        return False

    try:
        if not win32gui.IsWindow(hwnd_alerta):
            print("HWND do alerta não existe mais.")
            return False

        if not win32gui.IsWindowVisible(hwnd_alerta):
            print("HWND do alerta não está visível.")
            return False

        print("Tentando focar alerta porque ENTER direto não fechou.")

        if win32gui.IsIconic(hwnd_alerta):
            win32gui.ShowWindow(hwnd_alerta, win32con.SW_RESTORE)
            time.sleep(0.2)

        win32gui.ShowWindow(hwnd_alerta, win32con.SW_SHOW)
        time.sleep(0.2)

        win32gui.BringWindowToTop(hwnd_alerta)
        time.sleep(0.2)

        focar_hwnd(hwnd_alerta)
        time.sleep(0.3)

        return True

    except Exception as erro:
        print("Erro ao focar alerta.")
        print(erro)
        return False


def confirmar_alerta_somente_enter(hwnd_alerta):
    if not hwnd_alerta:
        return False

    try:
        titulo = win32gui.GetWindowText(hwnd_alerta).strip()
        classe = win32gui.GetClassName(hwnd_alerta).strip()
    except Exception:
        titulo = ""
        classe = ""

    print("Confirmando alerta somente com ENTER:", titulo, "| Classe:", classe)
    print("HWND alerta:", hwnd_alerta)

    # 1) Primeiro tenta ENTER direto, sem focar nada.
    # Isso é para o caso da tela Atenção já estar ativa.
    for tentativa in range(1, 4):
        print(f"Tentativa ENTER direto pelo teclado {tentativa}/3...")

        enviar_enter_teclado()

        if aguardar_janela_sumir(hwnd_alerta, timeout=1.2):
            print("Alerta confirmado com ENTER direto pelo teclado.")
            return True

    # 2) Se não fechou, aí sim tenta focar o alerta e mandar ENTER.
    for tentativa in range(1, 4):
        print(f"Tentativa ENTER após foco no alerta {tentativa}/3...")

        focar_alerta_somente_se_precisar(hwnd_alerta)
        enviar_enter_teclado()

        if aguardar_janela_sumir(hwnd_alerta, timeout=1.2):
            print("Alerta confirmado com ENTER após foco.")
            return True

    # 3) Último recurso: ENTER direto no HWND.
    for tentativa in range(1, 4):
        print(f"Tentativa ENTER direto no HWND {tentativa}/3...")

        enviar_enter_direto_no_hwnd(hwnd_alerta)

        if aguardar_janela_sumir(hwnd_alerta, timeout=1.5):
            print("Alerta confirmado com ENTER direto no HWND.")
            return True

    print("Não foi possível confirmar alerta com ENTER.")
    return False


def confirmar_alerta_enter_ou_alt_o(hwnd_alerta):
    print("Função confirmar_alerta_enter_ou_alt_o chamada.")
    print("ALT + O está desativado. Será usado somente ENTER.")

    return confirmar_alerta_somente_enter(hwnd_alerta)


def confirmar_todas_atencoes(timeout_primeira=1.5, max_tentativas=3):
    encontrou = False

    for tentativa in range(max_tentativas):
        timeout = timeout_primeira if tentativa == 0 else 0.5

        hwnd_alerta, titulo_alerta, classe_alerta = aguardar_alerta_32770(timeout=timeout)

        if not hwnd_alerta:
            break

        print("Alerta encontrado em confirmar_todas_atencoes.")
        print("Título:", titulo_alerta)
        print("Classe:", classe_alerta)
        print("HWND:", hwnd_alerta)

        confirmar_alerta_somente_enter(hwnd_alerta)

        encontrou = True
        time.sleep(0.2)

    return encontrou