Feature: Buscar producto en Mercado Libre

Scenario Outline: Ingresar a Mercado Libre y buscar un producto con diferentes artículos
    Given el usuario abre el navegador de pruebas
    When ingresa a la pagina de Mercado Libre
    When usuario busca el producto <Articulo>
    When usuario presiona la tecla Enter
    Then verifica que se muestran los resultados de la búsqueda

    Examples:
    |Articulo|
    |PlayStation 5|
    |Xbox Series X|
    |Nintendo Switch|

Scenario: Ingresar a Mercado Libre y buscar un producto (específico)
    Given el usuario abre el navegador de pruebas
    When ingresa a la pagina de Mercado Libre
    When usuario busca el producto Roku Streaming Stick
    When usuario presiona la tecla Enter
    Then verifica que se muestran los resultados de la búsqueda

## Ejecutar pruebas en behave en consola: behave

## Ejecutar pruebas en behave con generacion de reportes allure y html en consola 
#behave -f allure_behave.formatter:AllureFormatter -o reports/allure-results
#behave -f allure_behave.formatter:AllureFormatter -o allure-results

#Generacion de reporte Allure
#allure serve reports/allure-results
#allure serve allure-results

#Generar reporte Allure limpiar resultados anteriores
#allure generate reports/allure-results -o reports/allure-report --clean
#allure generate allure-results -o allure-report --clean

#Generacion Reporte HTML
#behave -f behave_html_formatter:HTMLFormatter -o reports_html/html_report.html