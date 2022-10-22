# misw4204 - Desarrollo de software en la nube - 202215

# Proyecto: Blazing Fast Audio Converter
## Integrantes del equipo
* Andres Ramirez - a.ramirezr2@uniandes.edu.co
* Carlos Andrés García Aljure - ca.garciaa1@uniandes.edu.co
* Iván Darío Chacón - id.chacon123@uniandes.edu.co
* Sebastian Aya - s.ayat@uniandes.edu.co

# Descripción
Blazing Fast Audio Converted (BFAC) es un servicio web construido sobre un stack de Python + Flask para facilitar la conversión de archivos MP3, WAV y OGG.

# Requisitos de software para arrancar el proyecto
- docker
- docker compose
- make
- bash o zsh

# Requisitos de hardware para arrancar el proyecto
- Contar con al menos 1 vCPU o mejor
- 1GB RAM
- 10Gib de Disco, preferiblemente SSD

# Puesta en marcha del proyecto
Para todas las tareas de administración, disponemos de diferentes targets de `make` para `compilar`, `levantar` y `limpiar` todo el proyecto con sus respectivas dependencias en dos ambientes principalmente: `dev` y `prod`.

# Ambiente de producción
## Ejecución
Ejecutar dentro de la carpeta del proyecto el siguiente comando
```
make up
```
Nota: si es la primera vez que ejecuta el proyecto, este comando puede tardar varios minutos mientras descarga y compila dependencias.

Para parar todo el stack, presiona `ctrl + c` esto frenara todos los contenedores docker y parara la ejecución del proyecto.

## Limpieza
Para borrar el sistema de archivos con datos almacenados en base de datos, se debe ejecutar el siguiente comando:
```
make delete
```

# Ambiente de desarrollo
## Ejecución
Ejecutar dentro de la carpeta del proyecto el siguiente comando
```
make dev-up
```
Nota: si es la primera vez que ejecuta el proyecto, este comando puede tardar varios minutos mientras descarga y compila dependencias.

Revisar el documento XXX para consultar los diferentes endpoints soportados por el API.

Para parar todo el stack, presiona `ctrl + c` esto frenara todos los contenedores docker y parara la ejecución del proyecto.

## Limpieza
Para borrar el sistema de archivos con datos almacenados en base de datos, se debe ejecutar el siguiente comando:
```
make dev-prune
```

# Herramientas de monitoreo de recursos de infraestructura
Este proyecto también provee, mediante targets de make, ciertas herramientas para monitorear los recursos del servidor en donde este se ejecuta.

Para ponerlas en marcha se debe ejecutar el siguiente comando
```
make start-metrics-services
```

Para acceder al dashboard principal de métricas se hace por medio del navegador:

http://ip-servidor:3000

```
usuario: admin
password: admin
```

Dar clic en: `Dashboard -> Browse -> General -> Node Exported Full`
Deberá aparecer un dashboard parecido al siguiente:

![image](https://user-images.githubusercontent.com/98656909/197349300-bad352ce-4872-42ee-bd10-7461895a19f8.png)

