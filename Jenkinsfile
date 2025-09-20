pipeline {
    agent any

    stages {
        stage('Get Code') {
            steps {
                git 'https://github.com/gunshot-1001/Loaner.git'
            }
        }

        stage('Build Backend') {
            steps {
                dir('backend') {
                    sh 'docker build -t loaner-backend .'
                }
            }
        }

        stage('Build Frontend') {
            steps {
                dir('frontend') {
                    sh 'docker build -t loaner-frontend .'
                }
            }
        }

        stage('Run Containers') {
            steps {
                sh 'docker stop loaner-backend || true'
                sh 'docker stop loaner-frontend || true'
                sh 'docker rm loaner-backend || true'
                sh 'docker rm loaner-frontend || true'

                sh 'docker run -d --name loaner-backend -p 5000:5000 loaner-backend'
                sh 'docker run -d --name loaner-frontend -p 3000:3000 loaner-frontend'
            }
        }
    }
}
