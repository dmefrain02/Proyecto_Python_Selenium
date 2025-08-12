import allure
import time
def add_screenshot_to_allure(context, name="Captura de pantalla", attachment_type=allure.attachment_type.PNG):
    screenshot = context.driver.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name=name,
        attachment_type=allure.attachment_type.PNG
    )
    time.sleep(2)