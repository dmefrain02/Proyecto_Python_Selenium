from behave import given, when, then
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import allure
import os
from datetime import datetime
#import src.Functions_Utilitaries.functions as func

@given('el usuario abre el navegador de pruebas')
def step_open_navegador(context):
    options = Options()
    prefs = {
        "profile.default_content_settings.popups": 0,
        "directory_upgrade":True
    }
    options.add_experimental_option("prefs",prefs)
    options.add_argument('start-maximized')
    #options.add_argument("--headless")
    service = ChromeService(executable_path=ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=options)

@when('ingresa a la pagina de Mercado Libre')
def step_ingresa_pagina(context):
    context.driver.get("https://www.mercadolibre.co.cr/")

    # # 📂 Carpeta para capturas (dentro de report para que HTML la encuentre)
    # screenshot_dir = r"../img/screenshots"
    # os.makedirs(screenshot_dir, exist_ok=True)
    # # 📄 Nombre único con timestamp
    # timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # file_name = f"screenshot_{timestamp}.png"
    # file_path = os.path.join(screenshot_dir, file_name)
    # # 📷 Guardar para HTML
    # context.driver.save_screenshot(file_path)
    # # Ruta para enlace HTML (relativa al HTML report)
    # href_path = f"{screenshot_dir}/{file_name}".replace("\\", "/")
    # # Enlace visible en behave-html-formatter
    # print(f'<a href="{href_path}" target="_blank">Ver captura</a>')
    # # 🖼 Adjuntar a Allure
    # with open(file_path, "rb") as img_file:
    #     allure.attach(
    #         img_file.read(),
    #         name=f"Captura {timestamp}",
    #         attachment_type=allure.attachment_type.PNG
    #     )
    # time.sleep(2)
    #func.add_screenshot_to_allure(context, name="Captura de pantalla",attachment_type=allure.attachment_type.PNG)
    screenshot = context.driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name="Captura de pantalla",
        attachment_type=allure.attachment_type.PNG
    )
    time.sleep(2)

@when('usuario busca el producto {Articulo}')
def step_buscar_producto(context, Articulo):
    text_busqueda = context.driver.find_element(By.XPATH,"//input[@id='cb1-edit']").send_keys(Articulo)
    screenshot = context.driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name="Captura de pantalla",
        attachment_type=allure.attachment_type.PNG
    )
    time.sleep(2)

@when('usuario presiona la tecla Enter')
def step_presiona_enter(context):
    context.driver.find_element(By.XPATH,"//input[@id='cb1-edit']").send_keys(Keys.ENTER)
    screenshot = context.driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name="Captura de pantalla",
        attachment_type=allure.attachment_type.PNG
    )
    time.sleep(2)

@then('verifica que se muestran los resultados de la búsqueda con el elemento buscado "{ElementoBusqueda}" y el texto esperado "{TextoEsperado}"')
def step_verifica_elemento(context, ElementoBusqueda, TextoEsperado):

    screenshot = context.driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name="Captura de pantalla",
        attachment_type=allure.attachment_type.PNG
    )
    time.sleep(2)
    
    elemento_destino = context.driver.find_element(By.XPATH,ElementoBusqueda)
    assert TextoEsperado in elemento_destino.text, f'El texto esperado "{TextoEsperado}" no se encontró en el elemento.'
    context.driver.quit()