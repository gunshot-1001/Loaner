pipeline {
    agent any

    environment {
        BACKEND_IMAGE = "loaner-backend"
        FRONTEND_IMAGE = "loaner-frontend"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/gunshot-1001/Loaner.git'
            }
        }

        stage('Build Backend Docker Image') {
            steps {
                dir('backend') {
                    echo "Building backend Docker image..."
                    bat 'docker build -t %BACKEND_IMAGE% .'
                }
            }
        }

        stage('Build Frontend Docker Image') {
            steps {
                dir('frontend') {
                    echo "Building frontend Docker image..."
                    bat 'docker build -t %FRONTEND_IMAGE% .'
                }
            }
        }

        stage('Stop Old Containers') {
            steps {
                echo "Stopping old containers if they exist..."
                bat 'docker stop loaner-backend || exit 0'
                bat 'docker stop loaner-frontend || exit 0'
                bat 'docker rm loaner-backend || exit 0'
                bat 'docker rm loaner-frontend || exit 0'
            }
        }

        stage('Run Containers') {
            steps {
                echo "Running new containers..."
                bat 'docker run -d --name loaner-backend -p 5000:5000 %BACKEND_IMAGE%'
                bat 'docker run -d --name loaner-frontend -p 3000:80 %FRONTEND_IMAGE%'
            }
        }

    }

    post {
        always {
            echo "Cleaning up unused Docker resources..."
            bat 'docker system prune -f'
        }
    }
}
