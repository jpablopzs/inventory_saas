# Proyecto de Servicio Inventory SaaS Dockerizado 

Este proyecto contiene un servicio REST construido con FastAPI de Python y una base de datos PostgreSQL. Los servicios están dockerizados y se pueden ejecutar fácilmente utilizando docker-compose.

en el archivo docker-compose.yml se encuentrasn 2 servicios configurados

* Servicio: ``` db ``` para crear una imagen y contenedor de PostgreSQL
* Servicio:  ``` inventory_service ```  para el contenedor de la aplicación API.

## Requisitos Previos

* Tener instalado Docker y Docker Compose.
* Variables de entorno configuradas para las credenciales de la base de datos y los JWT (puedes utilizar un archivo .env o definirlas en tu entorno local).
### Variables de Entorno Necesarias

```
POSTGRES_USER: Nombre de usuario para la base de datos.
POSTGRES_PASSWORD: Contraseña para el usuario de la base de datos.
POSTGRES_DB: Nombre de la base de datos (si no existe se creará automáticamente al construir la aplicación).
JWT_SECRET: Llave secreta para la firma de tokens JWT (ejemplo: guiyfgc837tgf3iw87-012389764).
JWT_ALGORITHM: Algoritmo utilizado para firmar los tokens (por ejemplo, HS256).
JWT_EXPIRATION: Tiempo de expiración de los tokens en segundos ejemplo: 3600 (equivale a una hora).
CSRF_FRONT: URL de frontend que interactúa con el servidor. Dejar en None si no se va asar
ENV: Entorno en el que está ejecutándose (por ejemplo, development o production).

```
Puedes definir estas variables en un archivo .env en la raíz del proyecto con el siguiente formato:

```
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_contraseña
POSTGRES_DB=nombre_base_datos
JWT_SECRET=tu_secreto
JWT_ALGORITHM=HS256
JWT_EXPIRATION=30
CSRF_FRONT=http://localhost:3000
ENV=development
```

## Instrucciones para la Construcción y Ejecución

### Clonar el repositorio

Clona el repositorio a tu máquina local.
```
git clone https://github.com/jpablopzs/inventory_saas.git
```

```
cd inventory_saas
```

```
Crear el archivo .env
```

### Crea el archivo .env en la raíz del proyecto, si no lo has hecho, y define las variables de entorno como se mencionó anteriormente.

### Construir los contenedores

Ejecuta el siguiente comando para construir los contenedores de la aplicación y la base de datos:

```
docker-compose up -d --build
```


Una vez que se hayan construido los contenedores, puedes verificar que los servicios estén corriendo:

```
docker ps
```


Tambien puedes verificar que el servicio ``` inventory_service ``` está corriendo si acceder a la siguiente url:


http://localhost:8000/docs

Te mostrará una interfaz de Swagger que te permitirá interactuar con las rutas disponibles en el servicio. De igual forma, esto también se podrá ver en una colección de Postman compartida en este proyecto.

### Ejecutar migraciones de tablas en BD

El script de inicio start.sh incluido en el contenedor de la aplicación se encargará de esperar a que la base de datos esté disponible y luego ejecutar las migraciones necesarias con Alembic usando el comando ``` alembic upgrade head ```.

Si deseas crear nuevas migraciones, puedes acceder al contenedor de la aplicación:

```
docker exec -it app_inventory_service /bin/bash
```

y luego ejecutar:

```
alembic revision --autogenerate -m "nueva revision"
```

Para aplicar los cambios:

```
alembic upgrade head
```

Y si requieres revertir un cambio enviado a la bd ejecutas:

``` alembic downgrade -1 ``` para revertir la ultima versión

O también,


``` alembic downgrade <revision_id> ``` para revertir a un número de revisión específica


De lo contrario: 

``` alembic downgrade base ``` para revertir todas las migraciones y dejar la BD sin estructura.



### Estructura del Proyecto

Dockerfile: Archivo para crear la imagen del servicio inventory_service.

docker-compose.yml: Archivo que define la infraestructura de contenedores, incluyendo el servicio inventory_service y la base de datos.

start.sh: Script de inicio que espera que la base de datos esté disponible, ejecuta las migraciones y luego inicia el servidor de la app inventory_service.

requirements.txt: Archivo que contiene las dependencias de Python.

alembic/versions/ : Directorio que contiene los archivos de migraciones  que se ejecutan automáticamente desde el archivo start.sh al iniciar el servicio.