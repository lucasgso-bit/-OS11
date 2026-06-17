"""Manage establishment queries."""

from database.queries import BUSCAR_ESTABELECIMENTOS


def buscar_estabelecimentos(conexao):
    cursor = conexao.cursor()

    try:
        cursor.execute(BUSCAR_ESTABELECIMENTOS)

        resultados = cursor.fetchall()

        return [linha[0] for linha in resultados]

    finally:
        cursor.close()