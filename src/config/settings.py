from pathlib import Path
from dotenv import load_dotenv
import os


class Settings:
    """
    Clase centralizada de configuración del proyecto.
    Responsable de:
    - Resolver la raíz del proyecto
    - Cargar variables de entorno
    - Resolver rutas y valores del .env
    """

    # Raíz del proyecto (calculada una sola vez)
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # Cargar variables de entorno al importar la clase
    load_dotenv(BASE_DIR / ".env")

    @classmethod
    def valor(cls, variable: str) -> str:
        """
        Obtiene una variable de entorno como string.
        """
        valor = os.getenv(variable)
        if not valor:
            raise ValueError(f"Variable de entorno '{variable}' no definida")
        return valor

    @classmethod
    def ruta(cls, variable: str) -> Path:
        """
        Obtiene una variable de entorno que representa una ruta
        y la convierte en ruta absoluta basada en BASE_DIR.
        """
        return cls.BASE_DIR / cls.valor(variable)
