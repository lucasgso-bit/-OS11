import sys

import pyautogui

from agro.app import abrir_agro
from agro.estabelecimento import trocar_estabelecimento
from agro.taxa_servico import (
    abrir_tela_taxa_servico,
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
        fechar_conexao_oracle(conexao)
        conexao = None
        return

    print("Fluxo iniciado para os ESTAB retornados pela consulta.")
    print("Será preenchido somente o SERVICO:", settings.servico_fixo)

    if not abrir_agro(settings):
        return

    for indice, estab in enumerate(estabelecimentos, start=1):
        try:
            print("-" * 50)
            print(f"Processando ESTAB {indice} de {len(estabelecimentos)}:", estab)

            if not trocar_estabelecimento(estab):
                print("Erro ao trocar estabelecimento. Indo para o próximo ESTAB.")
                continue

            print("Abrindo/focando tela de taxa de serviço...")

            if not abrir_tela_taxa_servico():
                print("Erro ao abrir/focar a tela de taxa de serviço. Indo para o próximo ESTAB.")
                continue

            sucesso = preencher_cobranca_taxa_servico(
                servico=settings.servico_fixo,
            )

            if not sucesso:
                print("Erro ao executar consulta/processamento da taxa de serviço. Indo para o próximo ESTAB.")
                continue

            print("ESTAB processado com sucesso:", estab)

        except Exception as erro:
            print("Erro inesperado ao processar este ESTAB.")
            print(erro)
            print("Indo para o próximo ESTAB.")
            continue

    if conexao:
        fechar_conexao_oracle(conexao)

    print("Fluxo finalizado.")


if __name__ == "__main__":
    main()  