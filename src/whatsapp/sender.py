import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class WhatsAppSender:
    """
    Clase encargada de enviar mensajes a un grupo de WhatsApp
    usando WhatsApp Web + Selenium
    """

    def __init__(self):
        self.nombre_grupo = os.getenv("WHATSAPP_GRUPO_NOMBRE")
        self.perfil_path = os.getenv("WHATSAPP_PERFIL_PATH")

        if not self.nombre_grupo:
            raise ValueError("WHATSAPP_GRUPO_NOMBRE no definido")

        self.driver = self._crear_driver()

    def _crear_driver(self):
        """
        Configura Chrome con perfil persistente
        """
        opciones = Options()
        opciones.add_argument(f"--user-data-dir={self.perfil_path}")
        opciones.add_argument("--profile-directory=Default")
        opciones.add_argument("--start-maximized")

        servicio = Service(ChromeDriverManager().install())

        return webdriver.Chrome(service=servicio, options=opciones)

    def enviar_mensaje(self, mensaje: str):
        """
        Abre WhatsApp Web, busca el grupo y envía el mensaje
        """
        self.driver.get("https://web.whatsapp.com")

        # Esperar carga inicial / login
        time.sleep(15)

        self._abrir_chat_grupo()
        self._escribir_mensaje(mensaje)

        time.sleep(5)
        self.driver.quit()

    def _abrir_chat_grupo(self):
        """
        Busca y abre el chat del grupo
        """
        buscador = self.driver.find_element(
            By.XPATH,
            '//div[@contenteditable="true"][@data-tab="3"]'
        )

        buscador.click()
        buscador.send_keys(self.nombre_grupo)
        time.sleep(2)
        buscador.send_keys(Keys.ENTER)

        time.sleep(2)

    def _escribir_mensaje(self, mensaje: str):
        """
        Escribe y envía el mensaje en el chat activo
        """
        caja_mensaje = self.driver.find_element(
            By.XPATH,
            '//div[@contenteditable="true"][@data-tab="10"]'
        )

        for linea in mensaje.split("\n"):
            caja_mensaje.send_keys(linea)
            caja_mensaje.send_keys(Keys.SHIFT, Keys.ENTER)

        caja_mensaje.send_keys(Keys.ENTER)
