@demo_qa
Feature: Prueba en Sitio DemoQA para mover un elemento

@demo_qa_scenario
Scenario: Mover elemento en la pantalla
    Given el usuario abre el navegador
    When ingresa a la pagina de DemoQA
    When usuario arrastra el elemento "Draggable" a la nueva posición
    Then verifica que el elemento se ha movido a la nueva posición

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

#Generacion Reporte HTML
#behave -f behave_html_formatter:HTMLFormatter -o reports_html/html_report.html