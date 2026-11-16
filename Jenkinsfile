
pipeline {
    agent any

    options {
        disableConcurrentBuilds()
    }

    environment {
        DB_NAME = 'tareas_db'
        DB_PORT = '5432'
    }

    stages {
        stage('Checkout') {
            steps {
                error 'Fallo controlado para evidenciar una ejecucion fallida'
                
                echo 'Descargando codigo desde GitHub...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Construyendo las imagenes de los servicios...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'postgres-api-tareas',
                        usernameVariable: 'DB_USER',
                        passwordVariable: 'DB_PASSWORD'
                    )
                ]) {
                    sh '''
                        set +x
                        docker compose build app
                        docker compose pull db
                    '''
                }
            }
        }

        stage('Test') {
            steps {
                echo 'Iniciando servicios y ejecutando pruebas...'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'postgres-api-tareas',
                        usernameVariable: 'DB_USER',
                        passwordVariable: 'DB_PASSWORD'
                    )
                ]) {
                    sh '''
                        set +x

                        docker compose up -d

                        echo "Esperando a que la API este disponible..."

                        for i in $(seq 1 30); do
                            if docker compose exec -T app python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" >/dev/null 2>&1; then
                                echo "API disponible"
                                break
                            fi

                            if [ "$i" -eq 30 ]; then
                                echo "La API no inicio correctamente"
                                exit 1
                            fi

                            sleep 2
                        done

                        echo "Comprobando conexion con PostgreSQL..."

                        docker compose exec -T db pg_isready -U "$DB_USER" -d "$DB_NAME"

                        echo "Probando registro y consulta de tareas..."

                        docker compose exec -T app python - <<'PY'
import json
import urllib.request

url = "http://localhost:5000"

payload = json.dumps({
    "title": "Prueba automatizada Jenkins",
    "description": "Verificacion de comunicacion con PostgreSQL"
}).encode()

request = urllib.request.Request(
    url + "/tasks",
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(request) as response:
    created = json.loads(response.read())
    assert response.status == 201
    print("Tarea creada correctamente:", created["id"])

with urllib.request.urlopen(url + "/tasks") as response:
    tasks = json.loads(response.read())

assert any(task["id"] == created["id"] for task in tasks)

print("Tarea recuperada correctamente desde PostgreSQL")
print("Pruebas superadas")
PY
                    '''
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline ejecutado correctamente.'
        }

        failure {
            echo 'El pipeline fallo. Revisar los registros.'
        }

        always {
            sh 'docker compose down -v --remove-orphans || true'
        }
    }
}
