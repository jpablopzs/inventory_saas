# FastAPI Inventory Service

Este es un servicio de inventario construido con FastAPI. La aplicación usa Docker para facilitar la configuración y la ejecución, y utiliza Alembic para las migraciones de base de datos.

### Estructura del Proyecto

```text
├── Dockerfile             # Archivo para la construcción de la imagen Docker de la aplicación.
├── README.md              # Documento con información general del proyecto.
├── alembic                # Directorio de configuración para las migraciones de base de datos con Alembic.
│   ├── README.md          # Instrucciones y detalles de uso de Alembic.
│   └── versions           # Subdirectorio que contiene las migraciones generadas.
├── alembic.ini            # Archivo de configuración principal de Alembic.
├── app                    # Directorio principal de la aplicación FastAPI.
│   ├── auth               # Módulo de autenticación.
│   │   ├── controllers    # Lógica para controladores y manejo de autenticación.
│   │   ├── models         # Modelos de la base de datos relacionados con la autenticación.
│   │   ├── routes         # Rutas relacionadas con el sistema de autenticación.
│   │   └── schemas        # Esquemas Pydantic para validación de datos en el módulo de autenticación.
│   ├── core               # Módulo central de la app (Driver de conexión a base de datos y excepciones).
│   ├── inventory          # Módulo de inventario.
│   │   ├── controllers    # Lógica para controladores relacionados con inventario.
│   │   ├── models         # Modelos de la base de datos para inventario.
│   │   ├── routes         # Rutas relacionadas con el manejo de inventario.
│   │   └── schemas        # Esquemas Pydantic para validación de datos en inventario.
│   └── main.py            # Punto de entrada principal para iniciar la aplicación FastAPI.
├── docker-compose.yml      # Configuración para orquestación de contenedores Docker.
├── docs                   # Documentación adicional del proyecto.
├── refactor_php            # Directorio con código PHP refactorizado (Etapa 3 prueba).
│   ├── database.php       # Archivo PHP relacionado con la gestión de la base de datos.
│   └── employee.php       # Archivo PHP para el manejo de empleados.
├── requirements.txt        # Lista de dependencias y librerías Python necesarias para el proyecto.
└── start.sh                # Script para iniciar la aplicación.

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
