import time

import pyautogui
import win32con
import win32gui

from windows.alerts import (
    aguardar_alerta_32770,
    aviso_eh_final,
    confirmar_alerta_somente_enter,
    confirmar_todas_atencoes,
)
from windows.window_utils import (
    aguardar_janela_sumir,
    clicar_controle,
    encontrar_controle_por_classe_instancia,
    focar_hwnd,
    obter_texto_janela,
    setar_texto_controle,
)


TITULO_AGRO = "AGRO-AG"
CLASSE_AGRO = "TVsMenu"

TITULO_TAXA_SERVICO = "Cobrança de Taxas de Serviço"
CLASSE_TAXA_SERVICO = "TFCobTxServico"

PESQUISA_TAXA_SERVICO = "cobrança taxas de serviços"


def encontrar_tela_agro_principal():
    hwnd_encontrado = None

    def procurar(hwnd, _):
        nonlocal hwnd_encontrado

        if hwnd_encontrado:
            return

        if not win32gui.IsWindowVisible(hwnd):
            return

        titulo = win32gui.GetWindowText(hwnd).strip()
        classe = win32gui.GetClassName(hwnd).strip()

        if TITULO_AGRO in titulo and classe == CLASSE_AGRO:
            hwnd_encontrado = hwnd

    win32gui.EnumWindows(procurar, None)

    return hwnd_encontrado


def focar_tela_agro_principal(timeout=10):
    inicio = time.time()

    while time.time() - inicio < timeout:
        hwnd = encontrar_tela_agro_principal()

        if hwnd:
            try:
                if win32gui.IsIconic(hwnd):
                    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                    time.sleep(0.5)
                else:
                    win32gui.ShowWindow(hwnd, win32con.SW_SHOW)
                    time.sleep(0.2)

                win32gui.BringWindowToTop(hwnd)
                time.sleep(0.2)

                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.4)

                hwnd_ativo = win32gui.GetForegroundWindow()
                titulo_ativo = win32gui.GetWindowText(hwnd_ativo).strip()
                classe_ativo = win32gui.GetClassName(hwnd_ativo).strip()

                print("Janela ativa:", titulo_ativo, "| Classe:", classe_ativo)

                if hwnd_ativo == hwnd or classe_ativo == CLASSE_AGRO:
                    return hwnd

            except Exception as erro:
                print("Erro ao focar AGRO-AG sem minimizar:")
                print(erro)

        time.sleep(0.3)

    return None


def pesquisar_taxa_servico_ctrl_f11(timeout=15):
    inicio = time.time()

    while time.time() - inicio < timeout:
        hwnd_agro = encontrar_tela_agro_principal()

        if not hwnd_agro:
            print("Janela AGRO-AG ainda não encontrada.")
            time.sleep(0.3)
            continue

        hwnd_pesquisa = encontrar_controle_por_classe_instancia(
            hwnd_agro,
            "TLabeledEdit",
            1,
        )

        if not hwnd_pesquisa:
            print("Campo TLabeledEdit INSTANCE 1 ainda não encontrado.")
            time.sleep(0.2)
            continue

        print("Campo de pesquisa TLabeledEdit encontrado.")
        print("HWND campo pesquisa:", hwnd_pesquisa)

        clicar_controle(hwnd_pesquisa)
        time.sleep(0.4)

        print("Limpando campo de pesquisa...")
        setar_texto_controle(hwnd_pesquisa, "")
        time.sleep(0.4)

        print("Digitando pesquisa:", PESQUISA_TAXA_SERVICO)
        setar_texto_controle(hwnd_pesquisa, PESQUISA_TAXA_SERVICO)
        time.sleep(0.8)

        try:
            texto_digitado = win32gui.GetWindowText(hwnd_pesquisa).strip()
            print("Texto atual no campo de pesquisa:", texto_digitado)
        except Exception:
            print("Não foi possível validar texto do campo. Vai seguir mesmo assim.")

        print("Selecionando rotina encontrada com DOWN + ENTER...")

        pyautogui.press("down")
        time.sleep(0.3)

        pyautogui.press("enter")
        time.sleep(2)

        print("Validando se abriu a tela correta...")

        if focar_tela_taxa_servico(timeout=10):
            print("Tela correta aberta:", TITULO_TAXA_SERVICO)
            return True

        hwnd_ativo = win32gui.GetForegroundWindow()
        titulo_ativo = win32gui.GetWindowText(hwnd_ativo).strip()
        classe_ativo = win32gui.GetClassName(hwnd_ativo).strip()

        print("A tela correta não abriu.")
        print("Janela ativa atual:", titulo_ativo, "| Classe:", classe_ativo)
        print("Provavelmente selecionou rotina errada na pesquisa.")

        return False

    print("Campo TLabeledEdit INSTANCE 1 não encontrado na tela AGRO-AG.")
    return False


def encontrar_tela_taxa_servico():
    hwnd_encontrado = None

    def procurar(hwnd, _):
        nonlocal hwnd_encontrado

        if hwnd_encontrado:
            return

        if not win32gui.IsWindowVisible(hwnd):
            return

        titulo = win32gui.GetWindowText(hwnd).strip()
        classe = win32gui.GetClassName(hwnd).strip()

        if titulo == TITULO_TAXA_SERVICO and classe == CLASSE_TAXA_SERVICO:
            hwnd_encontrado = hwnd

    win32gui.EnumWindows(procurar, None)

    return hwnd_encontrado


def focar_tela_taxa_servico(timeout=5):
    inicio = time.time()

    while time.time() - inicio < timeout:
        hwnd = encontrar_tela_taxa_servico()

        if hwnd:
            if focar_hwnd(hwnd):
                time.sleep(0.25)
                return hwnd

        time.sleep(0.2)

    return None


def obter_textos_janela(hwnd):
    textos = []

    try:
        texto = win32gui.GetWindowText(hwnd).strip()

        if texto:
            textos.append(texto)

    except Exception:
        pass

    def procurar_filhos(hwnd_filho, _):
        try:
            texto_filho = win32gui.GetWindowText(hwnd_filho).strip()

            if texto_filho:
                textos.append(texto_filho)

        except Exception:
            pass

    try:
        win32gui.EnumChildWindows(hwnd, procurar_filhos, None)
    except Exception:
        pass

    return textos


def janela_contem_texto(hwnd, textos_procurados):
    textos_janela = obter_textos_janela(hwnd)
    texto_completo = " ".join(textos_janela).lower()

    for texto in textos_procurados:
        if texto.lower() in texto_completo:
            return True

    return False


def encontrar_janela_processamento_taxa():
    hwnd_encontrado = None

    textos_processamento = (
        "processando taxas de serviço",
        "aguarde",
    )

    def procurar_top_level(hwnd, _):
        nonlocal hwnd_encontrado

        if hwnd_encontrado:
            return

        if not win32gui.IsWindowVisible(hwnd):
            return

        if janela_contem_texto(hwnd, textos_processamento):
            hwnd_encontrado = hwnd

    win32gui.EnumWindows(procurar_top_level, None)

    if hwnd_encontrado:
        return hwnd_encontrado

    hwnd_taxa = encontrar_tela_taxa_servico()

    if not hwnd_taxa:
        return None

    def procurar_filhos_taxa(hwnd_filho, _):
        nonlocal hwnd_encontrado

        if hwnd_encontrado:
            return

        if not win32gui.IsWindowVisible(hwnd_filho):
            return

        if janela_contem_texto(hwnd_filho, textos_processamento):
            hwnd_encontrado = hwnd_filho

    try:
        win32gui.EnumChildWindows(hwnd_taxa, procurar_filhos_taxa, None)
    except Exception:
        pass

    return hwnd_encontrado


def confirmar_atencao_se_estiver_aberta(timeout=0.2):
    hwnd_alerta, titulo_alerta, classe_alerta = aguardar_alerta_32770(timeout=timeout)

    if not hwnd_alerta:
        return False

    titulo_normalizado = str(titulo_alerta or "").strip().lower()
    classe_normalizada = str(classe_alerta or "").strip()

    if not titulo_normalizado.startswith("aten"):
        print("Alerta encontrado, mas não é Atenção. Não vou confirmar aqui.")
        print("Título:", titulo_alerta)
        print("Classe:", classe_alerta)
        print("HWND:", hwnd_alerta)
        return False

    print("Tela Atenção detectada durante espera/processamento.")
    print("Título:", titulo_alerta)
    print("Classe:", classe_normalizada)
    print("HWND:", hwnd_alerta)

    print("Enviando ENTER imediato, sem refocar...")
    pyautogui.press("enter")
    time.sleep(0.7)

    if aguardar_janela_sumir(hwnd_alerta, timeout=1.2):
        print("Tela Atenção fechada com ENTER imediato.")
        return True

    print("ENTER imediato não fechou. Tentando função confirmar_alerta_somente_enter...")
    return confirmar_alerta_somente_enter(hwnd_alerta)


def aguardar_processamento_taxa_finalizar(timeout_aparecer=5, timeout_finalizar=300):
    print("Verificando se apareceu tela de processamento da taxa...")

    confirmar_atencao_se_estiver_aberta(timeout=0.2)

    inicio_aparecer = time.time()
    hwnd_processamento = None

    while time.time() - inicio_aparecer < timeout_aparecer:
        if confirmar_atencao_se_estiver_aberta(timeout=0.2):
            print("Atenção confirmada durante espera do processamento aparecer.")
            return True

        hwnd_processamento = encontrar_janela_processamento_taxa()

        if hwnd_processamento:
            break

        time.sleep(0.2)

    if not hwnd_processamento:
        print("Tela de processamento da taxa não apareceu.")
        confirmar_atencao_se_estiver_aberta(timeout=0.5)
        return True

    print("Tela de processamento da taxa encontrada. Aguardando finalizar...")
    print("HWND processamento:", hwnd_processamento)

    inicio_finalizar = time.time()

    while time.time() - inicio_finalizar < timeout_finalizar:
        if confirmar_atencao_se_estiver_aberta(timeout=0.2):
            print("Atenção confirmada durante processamento da taxa.")
            return True

        hwnd_processamento = encontrar_janela_processamento_taxa()

        if not hwnd_processamento:
            print("Processamento da taxa finalizado.")
            time.sleep(0.8)

            confirmar_atencao_se_estiver_aberta(timeout=0.8)

            return True

        time.sleep(1)

    print("Tempo limite aguardando processamento da taxa finalizar.")
    return False


def aguardar_tela_taxa_ativa(timeout=30):
    inicio = time.time()

    while time.time() - inicio < timeout:
        confirmar_atencao_se_estiver_aberta(timeout=0.2)

        hwnd = win32gui.GetForegroundWindow()
        titulo = win32gui.GetWindowText(hwnd).strip()
        classe = win32gui.GetClassName(hwnd).strip()

        if titulo == TITULO_TAXA_SERVICO and classe == CLASSE_TAXA_SERVICO:
            time.sleep(0.5)
            return True

        hwnd_taxa = encontrar_tela_taxa_servico()

        if hwnd_taxa:
            focar_hwnd(hwnd_taxa)
            time.sleep(0.3)

            hwnd_ativo = win32gui.GetForegroundWindow()
            titulo_ativo = win32gui.GetWindowText(hwnd_ativo).strip()
            classe_ativo = win32gui.GetClassName(hwnd_ativo).strip()

            if titulo_ativo == TITULO_TAXA_SERVICO and classe_ativo == CLASSE_TAXA_SERVICO:
                time.sleep(0.5)
                return True

        time.sleep(0.2)

    return False


def fechar_tela_taxa_servico_ctrl_f4(timeout=2):
    hwnd_taxa = focar_tela_taxa_servico(timeout=timeout)

    if not hwnd_taxa:
        print("Tela Cobrança de Taxas de Serviço não está aberta. Nada para fechar.")
        confirmar_atencao_se_estiver_aberta(timeout=0.5)
        return True

    print("Fechando Cobrança de Taxas de Serviço com CTRL + F4...")

    pyautogui.hotkey("ctrl", "f4")
    time.sleep(0.8)

    confirmar_todas_atencoes(timeout_primeira=1.2)

    if aguardar_janela_sumir(hwnd_taxa, timeout=2):
        print("Tela Cobrança de Taxas de Serviço fechada.")
        return True

    print("A tela Cobrança de Taxas de Serviço continuou aberta após CTRL + F4.")

    return False


def formatar_valor_tela(valor):
    if valor is None:
        return ""

    if isinstance(valor, float) and valor.is_integer():
        return str(int(valor))

    return str(valor).strip()


def preencher_campo(
    hwnd_janela,
    nome_campo,
    valor,
    classe_controle,
    instancia,
    pressionar_enter=True,
):
    valor_texto = formatar_valor_tela(valor)

    if valor_texto == "":
        print(f"{nome_campo} não foi preenchido.")
        return False

    hwnd_controle = encontrar_controle_por_classe_instancia(
        hwnd_janela,
        classe_controle,
        instancia,
    )

    if not hwnd_controle:
        print(f"Controle do campo {nome_campo} não encontrado.")
        return False

    clicar_controle(hwnd_controle)
    time.sleep(0.15)

    setar_texto_controle(hwnd_controle, valor_texto)
    time.sleep(0.25)

    if pressionar_enter:
        pyautogui.press("enter")
        time.sleep(0.35)
        confirmar_todas_atencoes(timeout_primeira=0.8)

    return True


def preparar_consulta_servico():
    print("Executando navegação após digitar SERVICO...")
    print("Sequência segura: 5x SHIFT + TAB, RIGHT, CTRL + P, 2x TAB")

    if not focar_tela_taxa_servico(timeout=5):
        print("Não foi possível focar a tela Cobrança de Taxas de Serviço.")
        return False

    time.sleep(0.5)

    for tentativa in range(5):
        print(f"Enviando SHIFT + TAB antes do RIGHT {tentativa + 1}/5...")
        pyautogui.hotkey("shift", "tab")
        time.sleep(0.25)

    print("Enviando RIGHT...")
    pyautogui.press("right")
    time.sleep(0.5)

    print("Enviando CTRL + P...")
    pyautogui.hotkey("ctrl", "p")

    if not aguardar_processamento_taxa_finalizar(
        timeout_aparecer=5,
        timeout_finalizar=300,
    ):
        print("Processamento após CTRL + P não finalizou.")
        return False

    confirmar_todas_atencoes(timeout_primeira=1.5)

    if not aguardar_tela_taxa_ativa(timeout=30):
        print("Tela Cobrança de Taxas de Serviço não ficou ativa após CTRL + P.")
        return False

    if not focar_tela_taxa_servico(timeout=5):
        print("Perdeu o foco da tela Cobrança de Taxas de Serviço após CTRL + P.")
        return False

    print("Aguardando estabilização antes dos TABs...")
    time.sleep(1)

    print("Enviando TAB 1 depois do CTRL + P...")
    pyautogui.keyDown("tab")
    time.sleep(0.2)
    pyautogui.keyUp("tab")
    time.sleep(0.6)

    print("Enviando TAB 2 depois do CTRL + P...")
    pyautogui.keyDown("tab")
    time.sleep(0.2)
    pyautogui.keyUp("tab")
    time.sleep(0.6)

    print("TABs enviados. Aguardando antes do CTRL + ESPAÇO...")
    time.sleep(2)

    return True


def enviar_ctrl_espaco():
    print("Enviando CTRL + ESPAÇO...")

    pyautogui.keyDown("ctrl")
    time.sleep(0.2)
    pyautogui.press("space")
    time.sleep(0.2)
    pyautogui.keyUp("ctrl")


def enviar_alt_g():
    print("Enviando ALT + G...")

    pyautogui.keyDown("alt")
    time.sleep(0.2)
    pyautogui.press("g")
    time.sleep(0.2)
    pyautogui.keyUp("alt")


def processar_servico_ate_aviso(max_tentativas=300):
    for tentativa in range(1, max_tentativas + 1):
        print(f"Tentativa {tentativa}/{max_tentativas} no ESTAB atual.")

        if tentativa == 1:
            print("Primeira tentativa após os TABs. Não vou refocar antes do CTRL + ESPAÇO.")
            time.sleep(1)
        else:
            print("Tentativa após alerta. Focando a tela de taxa antes de repetir.")

            hwnd_taxa = focar_tela_taxa_servico(timeout=5)

            if not hwnd_taxa:
                print("Não conseguiu focar a tela de taxa. Vou continuar mesmo assim.")

            time.sleep(1)

        confirmar_atencao_se_estiver_aberta(timeout=0.2)

        enviar_ctrl_espaco()

        print("Aguardando marcação da linha antes do ALT + G...")
        time.sleep(1.5)

        confirmar_atencao_se_estiver_aberta(timeout=0.2)

        enviar_alt_g()

        print("Aguardando processamento após ALT + G...")

        if not aguardar_processamento_taxa_finalizar(
            timeout_aparecer=5,
            timeout_finalizar=300,
        ):
            print("Processamento após ALT + G não finalizou.")
            return False

        print("Aguardando alerta após processamento...")
        hwnd_alerta, titulo_alerta, classe_alerta = aguardar_alerta_32770(timeout=8)

        if not hwnd_alerta:
            print("Nenhuma tela apareceu após ALT + G.")
            print("Vai focar a tela e repetir CTRL + ESPAÇO e ALT + G no mesmo ESTAB.")

            hwnd_taxa = focar_tela_taxa_servico(timeout=5)

            if not hwnd_taxa:
                print("Não conseguiu focar a tela de taxa, mas vai repetir mesmo assim.")

            time.sleep(1)
            continue

        print("Tela encontrada:")
        print("Título:", titulo_alerta)
        print("Classe:", classe_alerta)
        print("HWND:", hwnd_alerta)

        texto_alerta = obter_texto_janela(hwnd_alerta)
        print("Texto:", texto_alerta)

        if aviso_eh_final(hwnd_alerta, titulo_alerta, classe_alerta):
            print("Aviso final encontrado.")
            print("Esse aviso indica que não há mais nota no ESTAB atual.")
            print("Confirmando com ENTER e trocando para o próximo ESTAB.")

            confirmar_alerta_somente_enter(hwnd_alerta)

            time.sleep(1)

            hwnd_taxa = focar_tela_taxa_servico(timeout=5)

            if not hwnd_taxa:
                print("Não conseguiu focar Cobrança de Taxas de Serviço antes do CTRL + F4.")
                print("Tentando fechar com CTRL + F4 mesmo assim.")

            time.sleep(0.5)

            print("Fechando Cobrança de Taxas de Serviço com CTRL + F4...")
            pyautogui.hotkey("ctrl", "f4")
            time.sleep(1.2)

            confirmar_todas_atencoes(timeout_primeira=1.2)

            print("ESTAB finalizado. Próximo ESTAB será processado.")
            return True

        print("Tela diferente do aviso final.")
        print("Confirmando com ENTER.")

        confirmar_alerta_somente_enter(hwnd_alerta)

        print("Esperando 1 segundo após ENTER.")
        time.sleep(1)

        print("Focando de volta na tela Cobrança de Taxas de Serviço.")
        hwnd_taxa = focar_tela_taxa_servico(timeout=5)

        if not hwnd_taxa:
            print("Não conseguiu focar a tela de taxa, mas vai repetir mesmo assim.")

        time.sleep(0.5)

        print("Vai repetir CTRL + ESPAÇO e ALT + G no mesmo ESTAB.")
        continue

    print("Limite de tentativas atingido sem aparecer o aviso final.")

    return False


def preencher_cobranca_taxa_servico(servico):
    hwnd_janela = encontrar_tela_taxa_servico()

    if not hwnd_janela:
        hwnd_janela = focar_tela_taxa_servico(timeout=10)

    if not hwnd_janela:
        print("Janela TFCobTxServico não encontrada.")
        return False

    focar_hwnd(hwnd_janela)
    time.sleep(0.5)

    print("Preenchendo janela TFCobTxServico somente com SERVICO...")

    if not preencher_campo(
        hwnd_janela=hwnd_janela,
        nome_campo="SERVICO",
        valor=servico,
        classe_controle="TVsNumRight",
        instancia=12,
        pressionar_enter=False,
    ):
        return False

    print("SERVICO preenchido:", servico)

    if not preparar_consulta_servico():
        print("Falha ao preparar consulta depois do SERVICO.")
        return False

    sucesso = processar_servico_ate_aviso()

    if not sucesso:
        print("Falha no processamento do ESTAB atual.")
        return False

    print("ESTAB finalizado com aviso e tela fechada.")

    return True


def abrir_tela_taxa_servico():
    if focar_tela_taxa_servico(timeout=1):
        print("Tela de taxa de serviço já está aberta. Reutilizando tela focada.")
        return True

    print("Focando na tela AGRO-AG sem minimizar...")

    hwnd_agro = focar_tela_agro_principal(timeout=10)

    if not hwnd_agro:
        print("Não foi possível focar a tela AGRO-AG.")
        return False

    time.sleep(0.8)

    print("Abrindo pesquisa de rotina pelo CTRL + F11...")

    pyautogui.keyDown("ctrl")
    time.sleep(0.15)
    pyautogui.press("f11")
    time.sleep(0.15)
    pyautogui.keyUp("ctrl")

    time.sleep(1.5)

    confirmar_todas_atencoes(timeout_primeira=1.2)

    if not pesquisar_taxa_servico_ctrl_f11(timeout=15):
        print("Erro ao pesquisar/abrir rotina de taxa de serviço pelo CTRL + F11.")
        return False

    confirmar_todas_atencoes(timeout_primeira=1.5)

    if focar_tela_taxa_servico(timeout=10):
        print("Tela Cobrança de Taxas de Serviço aberta com sucesso.")
        return True

    print("Erro ao abrir/focar a tela Cobrança de Taxas de Serviço pelo CTRL + F11.")
    return False