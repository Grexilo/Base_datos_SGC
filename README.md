# Conjunto de datos provenientes del Catalogo Sísmico Colombiano.

Este repositorio consistes principalmente de los archivos usados para la creación del conjunto de datos provenientes del Catalogo Sísmico Colombiano y que se encuentran almacenados en el cluster del grupo de investigación en Conectividad y Procesamiento de Señales (CPS) de la Universidad Industrial de Santander.

## **Tener en cuenta**
- La función **consultaSGC** es la función modificada de la herramienta por parte del profesor Jheyston Serrano, esta función toma un archivo de excel con los eventos que pueden ser descargados desde el [Catalogo Sísmico Colombiano](http://bdrsnc.sgc.gov.co/paginas1/catalogo/Consulta_Experta_Seiscomp/consultaexperta.php), y los demas prametros permiten delimitar las zona de interes para la cual se requiere hacer una consulta y retorna los datos descargados como un pandas dataframe
- La función **joint_data** recibe como argumentos el pandas dataframe proveniente de la función anterior y otro dataframe cargados del archivo provenientes del Servicio Geologico Colombiano (SGC)  que contiene la información de los picados de la onda P o S dependiendo del canal que se observe, esta función se encarga de añadir esa información a los datos y los guarda como un archivo comprimido pickle.
- La función **make_trace**  recibe como entrada una fila con toda la información previamente unida y genera un objeta **trace** del modulos Obspy
- La función **graph_trace**  recibe el objeto **trace** y grafica la traza sismica con un a linea vertical que muestra el picado realizaso por el SGC

**Nota:** En el archivo SGC.py en la linea 113 se debe modificar el path con el archivo de excel **estaciones.xlsx** 
