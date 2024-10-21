# Normalización y refactorización de código.

## Normanización de la tabla empoyees:

Luego de analizar la estructura de la tabla employees y encontrar la falta de normalización, problemas de redundancia, inconsistencia y facilitación de mantenimiento en la base de datos, se aplicó la siguiente lista de cambios para mejorar su eficiencia, mantenimiento y escalado del modelo de datos.

### Creación de Tablas Específicas:

* Se crearon varias tablas específicas  que solucionan la lista de problemas antes mencionados y ahora se cuenta con  entidades separadas en tablas específicas para una mejor organización, evitar la redundancia y facilita la gestión de datos. A continuación la lista de tablas resultante:

```
mysql> show tables;

+----------------------------+
| Tables_in_company          |
+----------------------------+
| company                    |
| department                 |
| employee                   |
| employee_dependent         |
| employee_education         |
| employee_emergency_contact |
| employee_position          |
| employee_salary            |
| employee_status            |
| manager                    |
| organization_chart         |
| performance_review         |
| relationship_type          |
| status_type                |
+----------------------------+
```

### [Ver estructura SQL del modelo propuesto](/docs/sql-refactor-estructure-parte3.sql)



### Normalización de Datos:

Eliminación de Datos Redundantes: 

Por ejemplo, la tabla employee_salary permite registrar múltiples salarios para un empleado sin tener que crear columnas adicionales en la tabla employee, de igual forma en los dependientes, evaluaciones de desempeño, educación, etc.

Problema Resuelto: Esto reduce la duplicación de datos y permite un manejo más eficiente de la información salarial, agregar nuevos dependientes, evaluciones y educaicón del empleado sin tener que modificar la estructura de las tablas. 

### Manejo de Relaciones:

Se establecieron relaciones claras mediante claves foráneas. Por ejemplo, employee_id en employee_salary y employee_dependent permite relacionar dependientes y salarios directamente con los empleados.

Problema Resuelto: Esto mejora la integridad referencial y asegura que no se puedan ingresar datos de dependientes o salarios que no correspondan a un empleado existente.

### Establecimiento nuevas tablas para almacenas los datos semillas de las relaciones principales:
Por ejemplo se crearon las tablas 

* department: (para guardar los departamento de la jerarquía organizacional)
* manager : para almacenar la jerarquia de las personas que supervisa a un empleado.
* relationship_type: para definir el tipo de relación que tiene un empleado con un dependiente:
* status_type: para almacenar el tipo de status que tiene un trabajador.
* organization_chart: para almacenar los cargos y asignar el position_id a un empleado.

### Separación de Información de Contacto de Emergencia:

La tabla employee_emergency_contact se creó para almacenar información de contacto de emergencia de los empleados, que antes estaba en la tabla employees.
Problema Resuelto: Almacenar los contactos de emergencia en su propia tabla permite tener múltiples contactos de emergencia por empleado sin aumentar el número de columnas en la tabla principal.

### Registro de Educación del empleado:

Se creó la tabla employee_education para registrar la información educativa de los empleados.
Problema Resuelto: Esto permite que un empleado tenga múltiples registros de educación sin crear múltiples columnas en la tabla employees, lo que facilita la adición y gestión de datos educativos.

### Registro de evaluación del Desempeño:

La tabla performance_review permite realizar un seguimiento de las evaluaciones de desempeño de los empleados.

Problema Resuelto: Esto elimina la necesidad de múltiples columnas en la tabla original y permite almacenar múltiples reseñas de desempeño por empleado, mejorando el seguimiento del rendimiento a lo largo del tiempo.

### otras mejoras:
Se agregaron indices a las tablas para mejorar el rendimiento en las consultas que tienen campos como claves foráneas.

También se agregó una capa de validación para asignar el company_id a cada tabla y así asegurar la separación lógica de datos por compañia en la base de datos.

## Refactorización del código:
En cuanto a la refactorización se aplicaron los siguientes campios:

### Uso de preparación de consultas

Cambio: Se ha implementado mysqli_prepare y mysqli_stmt_bind_param para la ejecución de consultas SQL. Este cambio es importante porque previene ataques de inyección SQL al separar el código SQL de los datos.

### Estructura de clases para modularidad
Se aplicó un enfoque Orientado a Objetos para mejorar la calidad y mantenimiento a futuro de la clase Employee y la conexión a la base de datos que se estaba manejando con una variable global $conn. 

### Validación de tablas permitidas
También se añadió una validación que verifica si la tabla solicitada en getEmployeeSubclass está en una lista de tablas permitidas, esto con el fin de prevenir el acceso no autorizado a tablas de otras entidades que no tiene relación con Employee , mejorando así la seguridad.

### Encapsulamiento de la lógica de consultas
Cambio: Las consultas a las tablas relacionadas con el empleado ahora se gestionan a través del método getEmployeeSubclass, que acepta el nombre de la tabla como un parámetro.
Justificación: Este enfoque no solo evita la duplicación de código, sino que también permite una fácil extensión. En el futuro, si se requieren más tablas relacionadas con empleados, se puede añadir fácilmente a la lista de tablas permitidas sin modificar la estructura principal.

### Manejo de Errores Mejorado
El método anterior también era carente de excepciones y no permitía verificar el estado de una consulta si era fallido y cual era el motivo.


### Respuesta JSON sstandarizada
Se ha implementado una función jsonResponse para estandarizar las respuestas JSON, para asegurar que todas las respuestas tengan un formato consistente.

### Mejoras en la seguridad
Cambio: Se han realizado validaciones adicionales en la entrada del usuario, como la conversión a enteros mediante intval, asegurando que los parámetros de entrada sean del tipo esperado.

### Consistencia de Datos
Cambio: Al utilizar company_id en las consultas, se asegura que solo se acceda a los datos de los empleados asociados a una empresa específica. Esto garantizará la integridad de los datos y evita la mezcla de información entre diferentes empresas.

El resultado final de la consulta devuelve un objeto JSON como este: 

```
{
  "status": "éxito",
  "message": "Empleado encontrado",
  "data": {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@techcorp.com",
    "phone": "555-987-6543",
    "address": "123 Main St",
    "city": "Tech City",
    "state": "Tech State",
    "country": "USA",
    "zip_code": "12345",
    "hire_date": "2022-01-15",
    "termination_date": null,
    "company_id": 1,
    "employee_positions": [
      {
        "id": 1,
        "company_id": 1,
        "employee_id": 1,
        "position_id": 1,
        "department_id": 1,
        "manager_id": 1,
        "is_current": 1
      }
    ],
    "previous_salaries": [
      {
        "id": 1,
        "employee_id": 1,
        "salary_amount": "75000.00",
        "is_current": 1,
        "start_date": "2024-10-21 00:20:18",
        "company_id": 1
      },
      {
        "id": 4,
        "employee_id": 1,
        "salary_amount": "65000.00",
        "is_current": 0,
        "start_date": "2023-01-01 00:00:00",
        "company_id": 1
      },
      {
        "id": 10,
        "employee_id": 1,
        "salary_amount": "55000.00",
        "is_current": 0,
        "start_date": "2022-01-01 00:00:00",
        "company_id": 1
      }
    ],
    "dependents": [
      {
        "id": 1,
        "name": "Anna Doe",
        "birthdate": "2010-05-15",
        "relationship_type_id": 1,
        "employee_id": 1,
        "company_id": 1
      },
      {
        "id": 4,
        "name": "James Doe",
        "birthdate": "2015-05-15",
        "relationship_type_id": 2,
        "employee_id": 1,
        "company_id": 1
      }
    ],
    "emergency_contact": [
      {
        "id": 1,
        "name": "Michael Doe",
        "employee_id": 1,
        "phone": "555-321-6540",
        "email": "michael.doe@techcorp.com",
        "address": "987 Pine St",
        "company_id": 1
      }
    ],
    "education": [
      {
        "id": 1,
        "employee_id": 1,
        "institution": "Tech University",
        "education_degree": "BSc Computer Science",
        "graduation_year": 2020,
        "company_id": 1
      }
    ],
    "performance_reviews": [
      {
        "id": 1,
        "date_review": "2023-01-15",
        "score": "4.50",
        "employee_id": 1,
        "company_id": 1
      }
    ],
    "employee_status": [
      {
        "id": 1,
        "status_date": "2024-10-21 00:20:18",
        "status_id": 1,
        "employee_id": 1,
        "company_id": 1
      }
    ]
  }
}
```

Para conocer los cambios aplicados script revisar estos enlaces:

### [Ver código PHP refactorizado](refactor_php/employee.php)
### [Ver código PHP conexión a Base de datos](refactor_php/database.php)
