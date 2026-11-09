API de Gestión de Tareas con Docker

1. Descripción del proyecto

Este proyecto consiste en el desarrollo de una API REST para la gestión de tareas, construida con Python y Flask, utilizando PostgreSQL como sistema de gestión de bases de datos.

La aplicación está empaquetada mediante Docker y utiliza Docker Compose para administrar los servicios de la API y la base de datos de manera independiente.

El proyecto implementa una red personalizada de Docker que permite la comunicación entre los contenedores mediante nombres de servicio, además de un volumen persistente para conservar la información almacenada en PostgreSQL.

2. Tecnologías utilizadas

- Python 3.12: lenguaje de programación.
- Flask 3.1.2: framework para el desarrollo de la API REST.
- PostgreSQL 16: sistema de gestión de bases de datos.
- Docker: plataforma de contenerización.
- Docker Compose: herramienta para administrar múltiples contenedores.
- Git y GitHub: control de versiones y alojamiento del código.
- GitHub Actions: automatización de la construcción de imágenes Docker.

3. Estructura del proyecto

api-tareas-docker/
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── .github/
│   └── workflows/
│       └── docker-build.yml
│
├── .dockerignore
├── .gitignore
├── .env.example
├── docker-compose.yml
└── README.md

4. Requisitos previos

Para ejecutar el proyecto se necesita:

- Docker Desktop instalado y funcionando.
- Git instalado.
- PowerShell o una terminal compatible.
- Conexión a Internet para descargar las imágenes necesarias.

5. Instalación y ejecución

5.1. Clonar el repositorio

git clone https://github.com/Andres-D47/api-tareas-docker.git

Ingresar a la carpeta:

cd api-tareas-docker

5.2. Configurar las variables de entorno

Crear el archivo ".env" a partir del archivo de ejemplo.

En PowerShell:

Copy-Item .env.example .env

El archivo ".env" contiene la configuración de conexión a PostgreSQL:

DB_NAME=tareas_db
DB_USER=admin
DB_PASSWORD=CAMBIAR_ESTA_CLAVE
DB_PORT=5432

Se recomienda establecer una contraseña propia para el entorno local.

Importante: el archivo ".env" no debe subirse al repositorio de GitHub, ya que contiene credenciales.

5.3. Construir e iniciar los contenedores

Desde la carpeta raíz del proyecto, ejecutar:

docker compose up -d --build

Este comando construye la imagen de la API e inicia los servicios de Flask y PostgreSQL.

5.4. Verificar los contenedores

docker ps

Para consultar los registros de la aplicación:

docker compose logs app

6. Arquitectura y comunicación

El proyecto utiliza dos servicios principales:

- app: ejecuta la API REST desarrollada con Flask.
- db: ejecuta la base de datos PostgreSQL.

Ambos servicios se comunican mediante una red personalizada de Docker Compose llamada "tareas_network".

La API utiliza el nombre del servicio "db" como dirección del servidor de base de datos, evitando depender de direcciones IP internas.

Adicionalmente, PostgreSQL utiliza un volumen llamado "postgres_data" para conservar los datos incluso cuando los contenedores se detienen o se recrean.

7. Endpoints disponibles

La API se encuentra disponible en:

"http://localhost:5000"

Método| Endpoint| Descripción
GET| "/"| Información general de la API.
GET| "/health"| Verificación del estado de la API.
POST| "/tasks"| Registrar una nueva tarea.
GET| "/tasks"| Consultar todas las tareas registradas.

7.1. Registrar una tarea

Solicitud:

POST /tasks
Content-Type: application/json

Cuerpo JSON:

{
  "title": "Primera tarea",
  "description": "Descripción de ejemplo"
}

La API registra la tarea en PostgreSQL y devuelve el registro creado con su identificador.

7.2. Consultar tareas

GET /tasks

Devuelve una lista con las tareas almacenadas en la base de datos.

8. Comandos útiles de Docker

Iniciar los servicios:

docker compose up -d

Reconstruir las imágenes:

docker compose up -d --build

Consultar los contenedores:

docker ps

Consultar los registros:

docker compose logs

Consultar las redes:

docker network ls

Inspeccionar la red del proyecto:

docker network inspect api-tareas-docker_tareas_network

Detener los servicios:

docker compose down

Para eliminar también el volumen de PostgreSQL:

docker compose down -v

Advertencia: el último comando elimina el volumen y, por tanto, los datos almacenados en él.

9. Integración continua con GitHub Actions

El proyecto incluye un flujo de trabajo ubicado en:

".github/workflows/docker-build.yml"

Este flujo se ejecuta automáticamente cuando se realizan cambios mediante "push" o "pull request" hacia la rama "main".

Su función es:

1. Descargar el código del repositorio.
2. Configurar Docker Buildx.
3. Construir la imagen Docker de la API.
4. Informar si la construcción finaliza correctamente.

La imagen se construye como validación, sin publicarse en un registro externo.

10. Autor y repositorio

Repositorio GitHub:

https://github.com/Andres-D47/api-tareas-docker

Proyecto académico desarrollado para demostrar el uso de Docker, Docker Compose, redes, volúmenes, comunicación entre contenedores e integración continua.