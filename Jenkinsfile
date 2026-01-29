pipeline {
    agent {
        docker {
            image 'python:3.11-slim'
            args '-v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    environment {
        IMAGE_NAME = "library-management:latest"
    }

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies & Test') {
            steps {
                bat '''
                python -m venv venv
                . venv/bin/activate
                pip install --upgrade pip
                pip install -r requirements.txt
                pytest
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                bat '''
                docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Trivy Security Scan') {
            steps {
                bat '''
                apt-get update
                apt-get install -y wget gnupg lsb-release

                wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor -o /usr/share/keyrings/trivy.gpg
                echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" \
                    > /etc/apt/sources.list.d/trivy.list

                apt-get update
                apt-get install -y trivy

                trivy image --severity HIGH,CRITICAL --exit-code 1 $IMAGE_NAME
                '''
            }
        }
    }

    post {
        success {
            echo 'CI Pipeline completed successfully ✅'
        }
        failure {
            echo 'CI Pipeline failed 🚨 Check logs for details'
        }
    }
}
