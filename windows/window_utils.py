import time

import pyautogui
import win32con
import win32gui
import win32com.client


def janela_esta_visivel(hwnd):
    return bool(hwnd and win32gui.IsWindow(hwnd) and win32gui.IsWindowVisible(hwnd))


def aguardar_janela_sumir(hwnd, timeout=1.5):
    inicio = time.time()

    while time.time() - inicio < timeout:
        if not janela_esta_visivel(hwnd):
            return True

        time.sleep(0.1)

    return False


def focar_hwnd(hwnd):
    if not hwnd:
        return False

    try:
        shell = win32com.client.Dispatch("WScript.Shell")
        shell.SendKeys("%")

        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(hwnd)

        time.sleep(0.2)

        return True

    except Exception:
        return False


def obter_titulo_janela_ativa():
    hwnd = win32gui.GetForegroundWindow()
    titulo = win32gui.GetWindowText(hwnd)
    classe = win32gui.GetClassName(hwnd)

    return titulo, classe


def listar_controles_filhos(hwnd_pai):
    controles = []

    def procurar(hwnd, _):
        controles.append(hwnd)

    win32gui.EnumChildWindows(hwnd_pai, procurar, None)

    return controles


def obter_texto_janela(hwnd):
    textos = []

    try:
        texto_pai = win32gui.GetWindowText(hwnd).strip()

        if texto_pai:
            textos.append(texto_pai)

        def procurar_filho(hwnd_filho, _):
            texto = win32gui.GetWindowText(hwnd_filho).strip()

            if texto:
                textos.append(texto)

        win32gui.EnumChildWindows(hwnd, procurar_filho, None)

    except Exception:
        pass

    textos_limpos = []

    for texto in textos:
        if texto not in textos_limpos:
            textos_limpos.append(texto)

    return " | ".join(textos_limpos)


def encontrar_controle_por_classe_instancia(hwnd_pai, classe_controle, instancia):
    controles = listar_controles_filhos(hwnd_pai)

    encontrados = [
        hwnd
        for hwnd in controles
        if win32gui.GetClassName(hwnd) == classe_controle
    ]

    if len(encontrados) < instancia:
        return None

    return encontrados[instancia - 1]


def clicar_controle(hwnd_controle):
    if not hwnd_controle:
        return False

    left, top, right, bottom = win32gui.GetWindowRect(hwnd_controle)

    x = left + ((right - left) // 2)
    y = top + ((bottom - top) // 2)

    pyautogui.click(x, y)

    return True


def setar_texto_controle(hwnd_controle, texto):
    if not hwnd_controle:
        return False

    win32gui.SendMessage(
        hwnd_controle,
        win32con.WM_SETTEXT,
        0,
        str(texto),
    )

    return True