# Aplicación Web Segura de Agenda (web.py + Supabase)

## 1. Instalación de las librerías

````bash
pip install -r requirements.txt
````

## 2. Archivo .env

````
SUPABASE_URL=https://TU_PROYECTO.supabase.co
SUPABASE_KEY=TU_LLAVE_ANON
````

## 3. Base de datos

Ejecutar `sql/agenda.sql` en el SQL Editor de Supabase.
Crear un usuario en Authentication → Users → Add user (marcar *Auto Confirm User*).

## 4. Ejecutar

````bash
python app.py
````

Abrir `/login`.
