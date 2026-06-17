"""SQL Query Registry.

Store SQL statements used by repository modules to keep database access
organized and separated from automation logic.

Developed by: Giovane Rodrigues
Updated by: Giovane Rodrigues
Last Modified: 2026-06-17
Version: 1.0
"""


BUSCAR_ESTABELECIMENTOS = """
     SELECT
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
            GROUP BY
                u_tempresa.estab
            ORDER BY
                u_tempresa.estab
"""