echo ## Ir a la carpeta del archivo ##
cd "C:\Users\dmefr\OneDrive\Escritorio\Proyecto_Python_Selenium\src"

echo ## Ejecucion del Archivo desde la Consola ##
python -m pytest Test\Simulacion#3\prueba_allure.py --alluredir C:\Users\dmefr\OneDrive\Escritorio\Proyecto_Python_Selenium\src\report\reportsAllure\allure-results

echo ## Fin de la ejecucion del archivo ##
pause
allure generate C:\Users\dmefr\OneDrive\Escritorio\Proyecto_Python_Selenium\src\report\reportsAllure\allure-results --output C:\Users\dmefr\OneDrive\Escritorio\Proyecto_Python_Selenium\src\report\reportsAllure\allure-report --clean

pause

