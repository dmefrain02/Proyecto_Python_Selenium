from behave import given, when, then
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys

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
def step_ingresa_pagin(context):
    context.driver.get("https://www.mercadolibre.co.cr/")
    time.sleep(2)

@when('usuario busca el producto {Articulo}')
def step_buscar_producto(context, Articulo):
    text_busqueda = context.driver.find_element(By.XPATH,"//input[@id='cb1-edit']").send_keys(Articulo)
    time.sleep(2)

@when('usuario presiona la tecla Enter')
def step_presiona_enter(context):
    context.driver.find_element(By.XPATH,"//input[@id='cb1-edit']").send_keys(Keys.ENTER)
    time.sleep(2)

@then('verifica que se muestran los resultados de la búsqueda')
def step_verifica_elemento(context):
    context.driver.quit()