# misw4204 - Desarrollo de software en la nube - 202215

# Proyecto: Blazing Fast Audio Converter
## Integrantes del equipo
* Andres Ramirez - a.ramirezr2@uniandes.edu.co
* Carlos Andrés García Aljure - ca.garciaa1@uniandes.edu.co
* Iván Darío Chacón - id.chacon123@uniandes.edu.co
* Sebastian Aya - s.ayat@uniandes.edu.co

# Entrega 2

El usuario debe estar logueado con la cuenta de la universidad para ver el video.

[Vídeo sustentación entrega 2](https://uniandes-my.sharepoint.com/:v:/g/personal/ca_garciaa1_uniandes_edu_co/EUnImg2dc_pIrxtCOVpSK1oBkfaxxWev7BhGXOihut98IA?e=CRNRMM)

[Arquitectura, conclusiones y consideraciones.pdf](https://github.com/saya6/misw4204-desarrollo-software-en-la-nube-202215/files/9894604/Arquitectura.conclusiones.y.consideraciones.pdf)

[Escenario y Pruebas de Estrés API REST y Batch.pdf](https://github.com/saya6/misw4204-desarrollo-software-en-la-nube-202215/files/9894602/Escenario.y.Pruebas.de.Estres.API.REST.y.Batch.pdf)


# Descripción
Blazing Fast Audio Converted (BFAC) es un servicio web construido sobre un stack de Python + Flask para facilitar la conversión de archivos MP3, WAV y OGG.

# Documentación de API - Postman

[URL de la documentación de API](https://documenter.getpostman.com/view/807412/2s84DrQhAZ#3b9434a5-eb93-440b-8dd1-b913acdb6986)

Ejecuta la colección en Postman y crea un Enviroment agregando la varibale `baseUrl`, la cual debe tener el valor: `http://estudiantesmiso.space`


# Puesta en marcha del proyecto

Contar con 3 instancias de GCP compute engine serie N1, tipo  F1-micro con 1 vCPU, 614 MiB RAM, 10 GiB en almacenamiento y una instancia GCP Cloud SQL de PostgreSQL 14.

Clonar el repositorio en dos de las máquinas y realizar los siguiente:

En una máquina se debe ejecutar el web-api, con el siguiente comando : 
```make cloud-web-run```

En otra máquina se debe ejecutar el worker, con el siguiente comando: 
```make cloud-daemon-run```

La otra máquina debe ser configurada como un servidor NFS

Nota: si es la primera vez que ejecuta el proyecto, este comando puede tardar varios minutos mientras descarga y compila dependencias.

Para parar todo el stack, presiona `ctrl + c` esto frenara todos los contenedores docker y parara la ejecución del proyecto.


