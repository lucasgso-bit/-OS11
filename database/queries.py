"""SQL Query Registry.

Store SQL statements used by repository modules to keep database access
organized and separated from automation logic.

Developed by: Giovane Rodrigues
Updated by: Giovane Rodrigues
Last Modified: 2026-06-17
Version: 1.0
"""


BUSCAR_ESTABELECIMENTOS = """
    SELECT DISTINCT
        u_tempresa.estab
    FROM
        u_tempresa
        INNER JOIN filial
            ON filial.estab = u_tempresa.estab
        INNER JOIN cidade
            ON cidade.cidade = filial.cidade
    WHERE
        u_tempresa.graos = 'S'
        AND u_tempresa.ativo = 'S'
        AND u_tempresa.exvenda = 'N'
        AND cidade.uf = 'SP'
        -- AND u_tempresa.estab >= 47
    ORDER BY
        u_tempresa.estab
"""


BUSCAR_ROBOT_LOG_STATUS = """
    SELECT
        STATUS
    FROM
        U_ROBOT_LOG
    WHERE
        U_ROBOT_ID = :u_robot_id
"""


ATUALIZAR_ROBOT_LOG_EXECUTANDO = """
    UPDATE U_ROBOT_LOG
       SET STATUS = 'EXECUTANDO',
           DATAINICIO = SYSDATE,
           DATAFIM = NULL,
           OBSERVACAO = NULL
     WHERE U_ROBOT_ID = :u_robot_id
       AND STATUS = 'PENDENTE'
"""


ATUALIZAR_ROBOT_LOG_CONCLUIDO = """
    UPDATE U_ROBOT_LOG
       SET STATUS = 'CONCLUIDO',
           DATAFIM = SYSDATE
     WHERE U_ROBOT_ID = :u_robot_id
       AND STATUS = 'EXECUTANDO'
"""


ATUALIZAR_ROBOT_LOG_ERRO = """
    UPDATE U_ROBOT_LOG
       SET STATUS = 'ERRO',
           OBSERVACAO = :mensagem_erro,
           DATAFIM = SYSDATE
     WHERE U_ROBOT_ID = :u_robot_id
       AND STATUS = 'EXECUTANDO'
"""