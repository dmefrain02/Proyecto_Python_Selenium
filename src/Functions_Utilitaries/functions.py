import allure
import time
import os
from datetime import datetime

def add_screenshot(context, name = "Captura de pantalla"):
    screenshoot = context.driver.get_screenshot_as_png()
    allure.attach(
        screenshoot,
        name,
        attachment_type=allure.attachment_type.PNG
    )
    time.sleep(2)

def screenshot_test(context, screenshoot_dir = "../img/"):
    os.makedirs(screenshoot_dir, exist_ok = True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"screenshot_{timestamp}.png"
    file_path = os.path.join(screenshoot_dir,file_name)
    context.driver.save_screenshot(file_path)

def evidencia(context, nombre):
    #Genera la evidencia en Allure y en la carpeta img con una sola llamada
    add_screenshot(context, nombre)
    return screenshot_test(context, nombre)


def evidencia_de_fallo(context, nombre_caso):
    try:
        add_screenshot(context, f"Fallo en {nombre_caso}")
        screenshot_test(context, f"fallo_{nombre_caso}")
    except Exception as error:
        print(f"No se pudo tomar la captura del fallo: {error}")


def con_evidencia(funcion):
    #Toma la captura en el momento del error, antes de que el tearDown
    #cierre el navegador, y vuelve a lanzar la excepcion
    def envoltura(self, *args, **kwargs):
        try:
            return funcion(self, *args, **kwargs)
        except Exception:
            evidencia_de_fallo(self, funcion.__name__)
            raise
    envoltura.__name__ = funcion.__name__
    envoltura.__doc__ = funcion.__doc__
    return envoltura