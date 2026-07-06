echo ## Ir a la carpeta del archivo ##
cd "C:\Users\dmefr\OneDrive\Escritorio\Proyecto_Python_Selenium\src"

echo ## Ejecucion del Archivo desde la Consola ##
python -m pytest Test\prueba_allure#2.py --alluredir report\reportsAllure\allure-results

echo ## Fin de la ejecucion del archivo ##
pause
allure generate report\reportsAllure\allure-results --output report\reportsAllure\allure-report --clean

pause

