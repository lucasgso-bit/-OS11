import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    usuario_oracle: str
    senha_oracle: str
    host_oracle: str
    porta_oracle: int
    service_name: str
    client_path: str
    caminho_agro: str
    processo_agro: str
    usuario_agro: str
    senha_agro: str
    servico_fixo: int
    pyautogui_pause: float

    @property
    def dsn_oracle(self):
        return f"{self.host_oracle}:{self.porta_oracle}/{self.service_name}"


def get_env(nome, padrao=""):
    return os.getenv(nome, padrao).strip()


def get_int_env(nome, padrao):
    return int(get_env(nome, str(padrao)))


def get_float_env(nome, padrao):
    return float(get_env(nome, str(padrao)))


def get_settings():
    return Settings(
        usuario_oracle=get_env("USUARIO_ORACLE"),
        senha_oracle=get_env("SENHA_ORACLE"),
        host_oracle=get_env("HOST_ORACLE"),
        porta_oracle=get_int_env("PORTA_ORACLE", 1521),
        service_name=get_env("SERVICE_NAME"),
        client_path=get_env("CLIENT_PATH"),
        caminho_agro=get_env("CAMINHO_AGRO"),
        processo_agro=get_env("PROCESSO_AGRO", "Agro3C.exe"),
        usuario_agro=get_env("USUARIO_AGRO"),
        senha_agro=get_env("SENHA_AGRO"),
        servico_fixo=get_int_env("SERVICO_FIXO", 30),
        pyautogui_pause=get_float_env("PYAUTOGUI_PAUSE", 0.05),
    )


def validar_configuracao(settings):
    variaveis_obrigatorias = {
        "USUARIO_ORACLE": settings.usuario_oracle,
        "SENHA_ORACLE": settings.senha_oracle,
        "HOST_ORACLE": settings.host_oracle,
        "SERVICE_NAME": settings.service_name,
        "CLIENT_PATH": settings.client_path,
        "CAMINHO_AGRO": settings.caminho_agro,
        "USUARIO_AGRO": settings.usuario_agro,
        "SENHA_AGRO": settings.senha_agro,
    }

    variaveis_faltando = [
        nome
        for nome, valor in variaveis_obrigatorias.items()
        if not str(valor).strip()
    ]

    if variaveis_faltando:
        print("Variáveis obrigatórias ausentes no arquivo .env:")

        for nome in variaveis_faltando:
            print("-", nome)

        return False

    return True