"""Manage robot execution log updates."""

from database.queries import (
    ATUALIZAR_ROBOT_LOG_CONCLUIDO,
    ATUALIZAR_ROBOT_LOG_ERRO,
    ATUALIZAR_ROBOT_LOG_EXECUTANDO,
)


def marcar_robot_como_executando(conexao, u_robot_id):
    """Mark robot log as running."""
    cursor = conexao.cursor()

    try:
        cursor.execute(
            ATUALIZAR_ROBOT_LOG_EXECUTANDO,
            {
                "u_robot_id": u_robot_id,
            },
        )

        linhas_afetadas = cursor.rowcount
        conexao.commit()

        if linhas_afetadas == 0:
            print("Nenhum registro encontrado na U_ROBOT_LOG para marcar como EXECUTANDO.")
            print("U_ROBOT_ID:", u_robot_id)
            return False

        print("U_ROBOT_LOG atualizado para EXECUTANDO.")
        print("U_ROBOT_ID:", u_robot_id)

        return True

    except Exception as erro:
        conexao.rollback()
        print("Erro ao marcar U_ROBOT_LOG como EXECUTANDO.")
        print(erro)
        return False

    finally:
        cursor.close()


def marcar_robot_como_concluido(conexao, u_robot_id):
    """Mark robot log as completed."""
    cursor = conexao.cursor()

    try:
        cursor.execute(
            ATUALIZAR_ROBOT_LOG_CONCLUIDO,
            {
                "u_robot_id": u_robot_id,
            },
        )

        linhas_afetadas = cursor.rowcount
        conexao.commit()

        if linhas_afetadas == 0:
            print("Nenhum registro encontrado na U_ROBOT_LOG para marcar como CONCLUIDO.")
            print("U_ROBOT_ID:", u_robot_id)
            return False

        print("U_ROBOT_LOG atualizado para CONCLUIDO.")
        print("U_ROBOT_ID:", u_robot_id)

        return True

    except Exception as erro:
        conexao.rollback()
        print("Erro ao marcar U_ROBOT_LOG como CONCLUIDO.")
        print(erro)
        return False

    finally:
        cursor.close()


def marcar_robot_como_erro(conexao, u_robot_id, mensagem_erro="Erro na execução do robô."):
    """Mark robot log as error."""
    cursor = conexao.cursor()

    try:
        cursor.execute(
            ATUALIZAR_ROBOT_LOG_ERRO,
            {
                "u_robot_id": u_robot_id,
                "mensagem_erro": str(mensagem_erro)[:4000],
            },
        )

        linhas_afetadas = cursor.rowcount
        conexao.commit()

        if linhas_afetadas == 0:
            print("Nenhum registro encontrado na U_ROBOT_LOG para marcar como ERRO.")
            print("U_ROBOT_ID:", u_robot_id)
            return False

        print("U_ROBOT_LOG atualizado para ERRO.")
        print("U_ROBOT_ID:", u_robot_id)
        print("ERRO:", mensagem_erro)

        return True

    except Exception as erro:
        conexao.rollback()
        print("Erro ao marcar U_ROBOT_LOG como ERRO.")
        print(erro)
        return False

    finally:
        cursor.close()