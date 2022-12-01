# misw4204 - Desarrollo de software en la nube - 202215

# Proyecto: Blazing Fast Audio Converter
## Integrantes del equipo
* Andres Ramirez - a.ramirezr2@uniandes.edu.co
* Carlos Andrés García Aljure - ca.garciaa1@uniandes.edu.co
* Iván Darío Chacón - id.chacon123@uniandes.edu.co
* Sebastian Aya - s.ayat@uniandes.edu.co

# Entrega 5

[Video sustentación entrega 5]()

[Arquitectura, conclusiones y consideraciones.pdf](https://github.com/saya6/misw4204-desarrollo-software-en-la-nube-202215/files/10128673/Arquitectura.conclusiones.y.consideraciones.pdf)

[Escenario y Pruebas de Estrés API REST y Batch.pdf](https://github.com/saya6/misw4204-desarrollo-software-en-la-nube-202215/files/10128677/Escenario.y.Pruebas.de.Estres.API.REST.y.Batch.pdf)


# Descripción
Blazing Fast Audio Converted (BFAC) es un servicio web construido sobre un stack de Python + Flask para facilitar la conversión de archivos MP3, WAV y OGG.

# Documentación de API - Postman

[URL de la documentación de API](https://documenter.getpostman.com/view/807412/2s84DrQhAZ#3b9434a5-eb93-440b-8dd1-b913acdb6986)

Ejecuta la colección en Postman y crea un Enviroment agregando la varibale `baseUrl`, la cual debe tener el valor: `http://estudiantesmiso.space`

# Escenarios de prueba

Los escenarios se encuentran en esta [ubicación](https://github.com/saya6/misw4204-desarrollo-software-en-la-nube-202215/tree/master/scenarios_jmeter), para ejecutarlo debe actualizar el parámetro `file`, es decir, adjuntar el archivo a convertir

# Requisitos para poner en marcha del proyecto

Hacer uso del servicio App Engine para el worker y el web-api haciendo uso de la consola de GCP, una instancia GCP Cloud SQL de PostgreSQL 14, un bucket de Cloud Storage y un tópico de Pub/Sub.

Clonar el repositorio en una máquina, que tenga instalado el SDK de GCP:

Para desplegar el Api-Rest, ingresar a la carpeta conversion-service/ del proyecto y ejecutar
```gcloud app deploy app-web.yaml```

Para desplegar el worker, ingresar a la carpeta conversion-service/ del proyecto y ejecutar
```gcloud app deploy app-worker.yaml```


Importante: el sistema se despliega en la nube, por ende, se debe configurar los servicios que intervienen en la ejecución de Blazing Fast Audio Converted (BFAC), los cuales son:

- Cloud Load Balancing
- Cloud SQL
- Cloud Storage
- Cloud Pub/Sub
- SendGrid

Nota: si es la primera vez que ejecuta el proyecto, este comando puede tardar varios minutos mientras descarga y compila dependencias.

Para parar todo el stack, presiona `ctrl + c` esto frenara todos los contenedores docker y parara la ejecución del proyecto.


