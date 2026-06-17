import oracledb


def init_oracle_client(settings):
    try:
        oracledb.init_oracle_client(lib_dir=settings.client_path)
    except Exception as erro:
        if "has already been initialized" not in str(erro):
            raise


def get_connection(settings):
    return oracledb.connect(
        user=settings.usuario_oracle,
        password=settings.senha_oracle,
        dsn=settings.dsn_oracle,
    )


def fechar_conexao_oracle(conexao):
    if not conexao:
        return

    try:
        conexao.close()
        print("Conexão Oracle fechada.")

    except oracledb.DatabaseError as erro:
        mensagem = str(erro)

        if (
            "DPY-4011" in mensagem
            or "DPI-1080" in mensagem
            or "ORA-03113" in mensagem
        ):
            print("Conexão Oracle já estava fechada pelo banco/rede. Ignorando fechamento.")
            return

        raise
