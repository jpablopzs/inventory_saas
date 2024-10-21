# FastAPI Inventory Service

Este es un servicio de inventario construido con FastAPI. La aplicación usa Docker para facilitar la configuración y la ejecución, y utiliza Alembic para las migraciones de base de datos.

### Estructura del Proyecto

```text
.
├── Dockerfile               # Archivo de configuración de Docker
├── README.md                # Documentación del proyecto
├── alembic                  # Carpeta con scripts de migración de Alembic
├── alembic.ini              # Archivo de configuración de Alembic
├── app
│   ├── auth                 # Módulo de autenticación
│   │   ├── controllers      # Lógica de controladores para autenticación
│   │   ├── models           # Modelos de datos para autenticación
│   │   ├── routes           # Rutas y endpoints para autenticación
│   │   └── schemas          # Esquemas de validación para autenticación
│   ├── core                 # Lógica central de la aplicación
│   │   ├── database.py      # Conexión y gestión de base de datos
│   │   └── exception_notification.py # Manejo de notificaciones de excepciones
│   ├── inventory            # Módulo de inventario
│   │   ├── controllers      # Lógica de controladores para el inventario
│   │   ├── models           # Modelos de datos para el inventario
│   │   ├── routes           # Rutas y endpoints para el inventario
│   │   └── schemas          # Esquemas de validación para el inventario
│   └── main.py              # Archivo principal de la aplicación FastAPI
├── docker-compose.yml       # Configuración de Docker Compose
└── requirements.txt         # Dependencias de Python
```
### Requisitos
* Docker
* Docker Compose
* Python 3.12
* PostgreSQL
* Variables de Entorno

El archivo .env debe contener las siguientes variables de 
entorno para configurar correctamente la aplicación:

```text 
POSTGRES_USER=postgres
POSTGRES_PASSWORD=123123
POSTGRES_DB=inventory_service
POSTGRES_URL=postgresql+asyncpg://postgres:123123@db:5432/inventory_service
JWT_SECRET=guiyfgc837tgf3iw87-012389764
JWT_ALGORITHM=HS256
JWT_EXPIRATION=3600
CSRF_FRONT=None
ENVIRONMENT=development
```
## Docker
### Dockerfile

El Dockerfile está configurado para crear un contenedor que ejecute la aplicación inventory_saas. Usa la imagen base python:3.12-slim y configura el entorno de desarrollo.

### docker-compose.yml

El archivo docker-compose.yml configura los servicios necesarios para la aplicación. Incluye  2 servicios, una para la base de datos PostgreSQL y otro para el contenedor de la aplicación.

## Instalación
1. Clona el repositorio:
```
    git clone https://github.com/jpablopzs/inventory_saas.git
```

2. Configura las variables de entorno:
Configura tu archivo .env y asegúrate de que las variables de entorno estén correctamente configuradas.

3. Construye y ejecuta los contenedores con Docker Compose:

```
    docker-compose up --build
```
Esto iniciará los contenedores de la base de datos y la aplicación FastAPI. La API estará disponible en
 ```   
http://localhost:8000/docs

```
## Migraciones de Base de Datos

1. Inicializa las migraciones de Alembic:
Para aplicar las migraciones, primero asegúrate de que los contenedores están en funcionamiento.

```
docker exec -it app_inventory_service sh
```
 y luego:

```
alembic upgrade head
```

## Endpoints
La API de FastAPI expone varios endpoints. Los detalles de los endpoints y su documentación pueden encontrarse en:

 ```   
http://localhost:8000/docs

```
De igual forma, será compartida la colección de Postman  para la ejecución de pruebas de los endpoints 

## Seguridad
La API usa autenticación basada en JWT. Asegúrate de que el JWT_SECRET en el archivo .env sea fuerte y único para tu aplicación.

## Documentación de partes de la prueba:
Para conocer los detalles  de las partes de la prueba técnica seguir los siguientes enlaces:

## [Prueba Etapa 1: Diseño de Base de Datos](docs/README-Etapa1.md)
## [Prueba Etapa 2: Creación del Backend](docs/README-Etapa2.md)
## [Prueba Etapa 3: Evaluación de Código](docs/README-Etapa3.md)
## [Prueba Etapa 4: Dockerización de un Servicio REST](docs/README-Etapa4.md)
## [Prueba Etapa 5: Despliegue en la Nube](docs/README-Etapa5.md)
