# Despliegue de Inventory SaaS
Este documento describe los pasos realizados para desplegar la aplicación Inventory SaaS utilizando Docker y Nginx en una instancia de Amazon EC2 con Ubuntu.

## Pasos para el despliegue
### 1. Configurar la instancia EC2

Se creó una cuenta en AWS para esta demo.
Ya dentro de AWS, 
se lanzó una instancia de EC2 con Ubuntu.

Se descargó el archivo juan.perez.pem con las credenciales de acceso.

### 2. Conectarse a la instancia vía SSH

Luego se realizó la conexión a la instancia  vía ssh con:

```
ssh -i "juan.perez.pem" ubuntu@ec2-13-59-196-202.us-east-2.compute.amazonaws.com
```

### 3. Se actualizaron los paquetes de la instancia
Una vez dentro de la instancia, se actualizaron los paquetes con:

```
sudo apt update
sudo apt full-upgrade -y
```

### 4. Instalar dependencias
Se instalaron las dependencias de Git, Docker y Docker Compose con el siguiente comando:

```
sudo apt install git docker-compose docker.io
```

### 5. Clonar el repositorio del proyecto

Se clonó el repositorio público de inventory_saas con el comando:

```
git clone -b staging https://github.com/jpablopzs/inventory_saas.git
```

### 6. Instalar Nginx

Se instaló Nginx para configurar un servidor proxy inverso:

```
sudo apt install nginx
```

### 7. Configurar Nginx

Se creó un archivo para la configuración de Nginx : 

Ruta del directorio:
``` 
cd /etc/nginx/sites-available/ 
```

Nombre del archivo:
```
sudo nano inventory-saas.conf
```

Contenido del archivo:

```
server {
#    server_name example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location ~ /\.git {
        return 403;
    }

}
```

Una vez guardado el archivo, se creó un enlace simbólico en el directorio sites-enabled:

```
sudo ln -s /etc/nginx/sites-available/inventory-saas.conf /etc/nginx/sites-enabled/
```

Y finalmente se reinició el nginx:

```
sudo systemctl restart nginx
```

### 8. Desplegar la aplicación con Docker.

Finalmente, dentro de la raíz del proyecto: ``` cd inventory_saas/ ```
se ejecutó el comando para construir y desplegar la aplicación con Docker Compose:

```
sudo docker-compose up -d --build
```

Finalizada la ejecución se verificó el servicio con la IP pública de la instancia.

```
http://13.59.196.202/docs
```