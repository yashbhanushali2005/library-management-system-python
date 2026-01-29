pipeline {
    agent any

    stages {

        stage('Checkout Code') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies & Test') {
    steps {
        echo 'Skipping local pip install – handled inside Docker'
    }
}


        stage('Build Docker Image') {
            steps {
                bat 'docker build -t library-ms:1.0 .'
            }
        }

        stage('Trivy Security Scan') {
    steps {
        bat '''
        docker run --rm ^
          -v //var/run/docker.sock:/var/run/docker.sock ^
          aquasec/trivy:latest ^
          image --severity HIGH,CRITICAL --exit-code 1 library-ms:1.0
        '''
    }
}

    }

    post {
        success {
            echo 'Pipeline completed successfully 🎉'
        }
        failure {
            echo 'Pipeline failed due to security or test issues 🚨'
        }
    }
}
