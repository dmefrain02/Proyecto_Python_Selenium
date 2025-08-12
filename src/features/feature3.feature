@mercado_libre
Feature: Buscar producto en Mercado Libre

@mercado_libre_scenario_outline
Scenario Outline: Ingresar a Mercado Libre y buscar un producto con diferentes artículos
    Given el usuario abre el navegador de pruebas
    When ingresa a la pagina de Mercado Libre
    When usuario busca el producto <Articulo>
    When usuario presiona la tecla Enter
    Then verifica que se muestran los resultados de la búsqueda con el elemento buscado "<ElementoBusqueda>" y el texto esperado "<TextoEsperado>"

    Examples:
    |Articulo|ElementoBusqueda|TextoEsperado|
    |PlayStation 5|//a[contains(text(),'Playstation 5 Slim Digital Avenida Tecnologica')]|Playstation 5 Slim Digital Avenida Tecnologica|
    |Xbox Series X|//a[contains(text(),'Xbox Series X Blanco')]|Xbox Series X Blanco|
    |Nintendo Switch|//a[contains(text(),'Nintendo Switch Oled Avenida Tecnologica')]|Nintendo Switch Oled Avenida Tecnologica|

@mercado_libre_scenario
Scenario: Ingresar a Mercado Libre y buscar un producto (específico)
    Given el usuario abre el navegador de pruebas
    When ingresa a la pagina de Mercado Libre
    When usuario busca el producto Roku Streaming Stick
    When usuario presiona la tecla Enter
    Then verifica que se muestran los resultados de la búsqueda con el elemento buscado "//a[contains(text(),'Roku Express Hd Streaming Media Player *itech')]" y el texto esperado "Roku Express Hd Streaming Media Player *itech"

## Ejecutar pruebas en behave en consola: behave

## Ejecutar un solo feature o escenario de pruebas en behave
## behave -t @demo_qa (ejecutar solo el feature de DemoQA con el tag @demo_qa)
## behave -t @demo_qa_scenario (ejecutar solo un escenario del feature de DemoQA con el tag @demo_qa_scenario)
## behave feature.feature (ejecutar el feature completo sin tags)

## Ejecutar pruebas en behave con generacion de reportes allure y html en consola con/sin tags 
#behave -f allure_behave.formatter:AllureFormatter -o ../reports/allure-results -t @mercado_libre
#behave -f allure_behave.formatter:AllureFormatter -o ../reports/allure-results
#behave -f allure_behave.formatter:AllureFormatter -o allure-results -t @mercado_libre
#behave -f allure_behave.formatter:AllureFormatter -o allure-results

#Generacion de reporte Allure en carpeta temporal a partir de los resultados generados
#allure serve ../reports/allure-results
#allure serve allure-results

#Abrir el reporte Allure a partir de la carpeta allure report generada con los resultados
#allure generate ../reports/allure-results -o ../reports/allure-report --clean
#allure generate allure-results -o allure-report --clean
#allure open ../reports/allure-report

#Generacion Reporte HTML con/sin tags
#behave -f behave_html_formatter:HTMLFormatter -o reports_html/html_report.html -t @mercado_libre
#behave -f behave_html_formatter:HTMLFormatter -o reports_html/html_report.html @demo_qa_scenario
#behave -f behave_html_formatter:HTMLFormatter -o reports_html/html_report.html

#behave -f html -o report/report.html -f allure_behave.formatter:AllureFormatter -o allure-results

#Por Validar
#behave feature3.feature -f behave_html_formatter:HTMLFormatter -o ../reports/report.html -f allure_behave.formatter:AllureFormatter -o ../reports/allure-results -t @mercado_libre_scenario