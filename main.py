import sys

import pyautogui

from agro.app import abrir_agro
from agro.estabelecimento import trocar_estabelecimento
from agro.taxa_servico import (
    abrir_tela_taxa_servico,
    fechar_tela_taxa_servico_ctrl_f4,
    preencher_cobranca_taxa_servico,
)
from config import get_settings, validar_configuracao
from database.oracle_client import (
    fechar_conexao_oracle,
    get_connection,
    init_oracle_client,
)
from repositories.estabelecimento_repository import buscar_estabelecimentos


def main():
    conexao = None
    settings = get_settings()

    pyautogui.PAUSE = settings.pyautogui_pause

    if not validar_configuracao(settings):
        sys.exit(1)

    try:
        print("Tentando conectar no Oracle...")
        print("DSN usado:", settings.dsn_oracle)

        init_oracle_client(settings)
        conexao = get_connection(settings)

        print("Conectado ao Oracle com sucesso.")

    except Exception as erro:
        print("Erro ao conectar no Oracle.")
        print(erro)
        sys.exit(1)

    try:
        estabelecimentos = buscar_estabelecimentos(conexao)

        print(f"Estabelecimentos encontrados na consulta: {len(estabelecimentos)}")

        if not estabelecimentos:
            print("Nenhum estabelecimento encontrado na consulta. Agro não será aberto.")

            if conexao:
                fechar_conexao_oracle(conexao)
                conexao = None

            return

        for estab in estabelecimentos:
            print("ESTAB encontrado:", estab)

        fechar_conexao_oracle(conexao)
        conexao = None

    except Exception as erro:
        print("Erro ao buscar estabelecimentos.")
        print(erro)

        if conexao:
            fechar_conexao_oracle(conexao)
            conexao = None

        return

    print("Fluxo iniciado para os ESTAB retornados pela consulta.")
    print("Será preenchido somente o SERVICO:", settings.servico_fixo)

    if not abrir_agro(settings):
        print("Erro ao abrir Agro.")
        return

    for indice, estab in enumerate(estabelecimentos, start=1):
        sucesso_estab = False

        try:
            print("-" * 50)
            print(f"Processando ESTAB {indice} de {len(estabelecimentos)}:", estab)

            print("Limpando tela de taxa antes de trocar ESTAB...")

            try:
                fechar_tela_taxa_servico_ctrl_f4(timeout=2)
            except Exception as erro_limpeza_inicial:
                print("Erro ao tentar limpar tela de taxa antes de trocar ESTAB.")
                print(erro_limpeza_inicial)

            print("Trocando estabelecimento para:", estab)

            if not trocar_estabelecimento(estab):
                print(f"Erro ao trocar estabelecimento para ESTAB {estab}.")
                print("Indo para o próximo ESTAB.")
                continue

            print("Abrindo/focando tela de taxa de serviço...")

            if not abrir_tela_taxa_servico():
                print(f"Erro ao abrir/focar a tela de taxa de serviço no ESTAB {estab}.")
                print("Indo para o próximo ESTAB.")
                continue

            sucesso_estab = preencher_cobranca_taxa_servico(
                servico=settings.servico_fixo,
            )

            if not sucesso_estab:
                print(f"Erro ao executar consulta/processamento da taxa de serviço no ESTAB {estab}.")
                print("Indo para o próximo ESTAB.")
                continue

            print("ESTAB processado com sucesso:", estab)

        except Exception as erro:
            print(f"Erro inesperado ao processar ESTAB {estab}.")
            print(erro)
            print("Indo para o próximo ESTAB.")

        finally:
            print(f"Limpando tela após ESTAB {estab}...")

            try:
                fechar_tela_taxa_servico_ctrl_f4(timeout=2)
            except Exception as erro_limpeza_final:
                print("Erro ao tentar limpar/fechar tela de taxa após o ESTAB.")
                print(erro_limpeza_final)

            print(f"Finalizado bloco do ESTAB {estab}. Sucesso:", sucesso_estab)

    if conexao:
        fechar_conexao_oracle(conexao)
        conexao = None

    print("Fluxo finalizado.")


if __name__ == "__main__":
    main()