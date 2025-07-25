Feature: Prueba en Sitio DemoQA para mover un elemento

Scenario: Mover elemento en la pantalla
    Given el usuario abre el navegador
    When ingresa a la pagina de DemoQA
    When usuario arrastra el elemento "Draggable" a la nueva posición
    Then verifica que el elemento se ha movido a la nueva posición