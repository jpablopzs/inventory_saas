#!/bin/sh

until nc -z -v -w30 db 5432; do
  echo "Esperando a que la base de datos esté disponible..."
  sleep 1
done

echo "Base de datos lista. Ejecutando migraciones..."
# crear las migraciones:
# alembic revision --autogenerate -m "revision"

#ejecutar y actualizar las migraciones en bd:
alembic upgrade head

echo "Iniciando el servidor..."
uvicorn app.main:app --reload --port=8000 --host=0.0.0.0
