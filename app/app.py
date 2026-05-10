pipeline {
    agent any

    environment {
        TELEGRAM_TOKEN = credentials('TELEGRAM_TOKEN')
        TELEGRAM_CHAT_ID = '1221106616'
    }

    stages {

        stage('Clonar codigo') {
            steps {
                echo 'Clonando el repositorio...'
                checkout scm
            }
        }

        stage('Escanear vulnerabilidades') {
            steps {
                echo 'Escaneando con Trivy...'
                sh '''
                    docker run --rm \
                    -v $(pwd):/proyecto \
                    aquasec/trivy:latest fs /proyecto/app \
                    --exit-code 1 \
                    --severity HIGH,CRITICAL \
                    --format table \
                    > reporte.txt 2>&1 || true
                '''
            }
        }

        stage('Evaluar reporte') {
            steps {
                script {
                    def reporte = readFile('reporte.txt')
                    echo reporte
                    if (reporte.contains('HIGH') || reporte.contains('CRITICAL')) {
                        error('Vulnerabilidades encontradas. Despliegue bloqueado.')
                    } else {
                        echo 'Codigo limpio. Continuando...'
                    }
                }
            }
        }

        stage('Desplegar app') {
            steps {
                echo 'Desplegando la app...'
                sh 'docker-compose up -d --build'
            }
        }

    }

    post {
        failure {
            sh """
                curl -s -X POST https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage \
                -d chat_id=${TELEGRAM_CHAT_ID} \
                -d text='🚨 Despliegue BLOQUEADO por vulnerabilidades en el codigo'
            """
        }
        success {
            sh """
                curl -s -X POST https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage \
                -d chat_id=${TELEGRAM_CHAT_ID} \
                -d text='✅ App desplegada exitosamente. Sin vulnerabilidades detectadas'
            """
        }
    }
}
