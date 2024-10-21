# Construcción de Diagrama ER.
Se crea el diagrama Entidad-relación para el modelo de datos de la propuesta de inventario saas.

Esta propuesta de diagrama ER incluye:

## Autenticación y autorización.

* Módulo de autenticación de usuario, basado en el estándar RBAC: (Role Based Access Control), en donde se gestionan entidades globales para Usuario y Permisos

```
- auth.user
- auth.permission
```

Y entidades relacionales para separar la lógica de Roles y asignación de Permisos a roles por compañía.

```
- company_user
- company_role
- company_user_role
- company_permission_role
```

Cada una de estas entidades cuenta con un atributo company_id para establecer la separación lógica de datos de autenticación y autorización por compañia y así lograr flexibilidad en la estructura de datos para soportar el modelo multi-company.

## Gestión de inventario.

* También se definen las entidades que formarán parte de la gestión de organización, Inventario de productos, proveedores y transacciones (Órdenes de compra y Órdenes de venta)

Para esta demo se contemplaron las siguientes entidades:

### Compañia:

```
- company
```

### Inventario:

```
- category
- brand
- storehouse
- product
```

### Órdenes de compra:

```
- supplier
- purchase_order
- purchase_order_detail
- status
- purchase_order_status
```

### Órdenes de venta:

```
- customer
- sales_order
- sales_order_detail
- y también podría ampliarse el flujo de estados, seguimientos de ventas,  y gestión de facturación.
```

Para conocer más detalles del diagrama ER puedes:

### [Descargar Diagrama ER en formato .jpg ](docs/inventory_saas-drawio.jpg) 

### [Abrir Diagrama ER en draw.io](https://drive.google.com/file/d/1jSxp8p7y6OfkytfZGJGoFGCq1-H3XUBi/view?usp=sharing)


# Estructura del esquema en formato SQL
Para esta demo se decide construir el esquema de base de datos usando las siguientes entidades del diagrama ER propuesto:

```
- auth.user
- public.company
- public.company_user
- public.category
- public.product
- public.supplier
- public.purchase_order
- public.purchase_order_detail
- public.customer
- public.sales_order
- public.sales_order_detail

```

Para conocer el contenido de la estructura SQL de las tablas propuestas, revisar el siguiente enlace:

### [Ver estructura SQL del modelo propuesto](docs/sql-inventory_saas.sql)

### Explicación de cómo asegurarte de que los datos de las diferentes empresas no se mezclen.

En el análisis realizado a este requerimiento, se pudo determinar que es necesario aplicar una estrategia de aislamiento y separación lógica de los datos utilizando el atributo company_id en todas las tablas y trazar una relación directa hacia la tabla public.company.  

En este caso, las tablas que tendrán el atributo company_id son:

```
- public.company_user
- public.category
- public.product
- public.supplier
- public.purchase_order
- public.purchase_order_detail
- public.customer
- public.sales_order
- public.sales_order_detail

```
A nivel de consultas, también es necesario que personalizar las queries en las tablas indicadas para que la consulta tenga siempre dentro del WHERE el parámetro company_id, y así evitar la devolución de datos de una empresa que no corresponde

Por ejemplo:

```
SELECT * FROM public.product WHERE company_id = 10;
```

Otro de los elementos importantes en cuanto a la consultas y la separación lógica de los datos, es implementar el filtrado haciendo join public.company_user para determinar si el usuario que realiza la consulta tiene ese company_id relacionado. Con esto se comenzaría a crear una capa de seguridad para el acceso a los datos multicompany, evitando que un usuario no autorizado pueda visualizar datos de otras compañías que no le corresponden.

También hay un enfoque más avanzado llamado Row-Level Security (RLS), que permite crear políticas de acceso sobre las tablas para poder acceder a los registros en la base de datos, (Documentación con PostgreSQL), esto con el fin de que postgres  valide si el user_id que intenta hacer la consulta está presente en la tabla company_user y tiene asignado el company_id de la tabla destino.

Estas reglas, pueden definirse directamente en el backend de la app.

### Justificación de las claves primarias, foráneas e índices elegidos, incluyendo cómo manejar los datos multi-company.

* En cuanto a las claves primarias, se le ha asignado el atributo id como PK a todas las tablas para poder identificar cada registro de manera única, y luego usar este campo en las relaciones como claves foraneas en otras tablas y garantizar que funcionen de manera correcta.

* Con relación a las claves foraneas (FK), cada tabla hija ha sido relacionada con su entidad padre a través de una FK para garantizar integridad referencial. Por ejemplo: Las tablas public.company_user, public.category, public.product se les asignó la FK en el atributo company_id, de manera que evite crear un registro si el id de la compañia no existe en la tabla public.company

* En cuanto a los índices, se han añadido en cada clave foránea de las tablas para optimizar las consultas y mejorar el rendimiento de la base de datos, también se añadieros índices a algunos campos como email en la tabla auth.user, order_code en public.purchase_order que pueden ser campos de consulta frecuente.

Y para el manejo de datos multi-company se han añadido índices en tolas la tablas para el campo company_id.

* Finalmente se ha creado la base de datos utilizando el gestor de migraciones Alembic, integrado en el framework FastAPI de Dejango, esto con el fin de mantener un historial de las modificaciones DDL que afectan directamente la estructura de la BD, y poder realizar rollback a una versión específica si es necesario.
