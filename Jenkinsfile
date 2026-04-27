pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = 'kalamkaar/python-k8s-starter'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        SONARQUBE_SERVER_NAME = 'SonarQube' 
        SONAR_PROJECT_KEY = 'python-app'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/2coolkalamkaar/zeko.git'
            }
        }
        
        stage('SonarQube Analysis') {
            steps {
                sh '''
                    sonar-scanner \\
                      -Dsonar.projectKey=python-app \\
                      -Dsonar.sources=. \\
                      -Dsonar.host.url=http://20.193.146.119:9000 \\
                      -Dsonar.login=sqp_f4fa5d6444449d4304169aa8d4c084c2c609d2ee
                '''
            }
        }
        
        stage('Docker Image Build') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }
        
        stage('Docker Image Push') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: env.DOCKER_CREDENTIALS_ID, passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh "echo \$DOCKER_PASSWORD | docker login -u \$DOCKER_USERNAME --password-stdin"
                        sh "docker push ${DOCKER_IMAGE}:${env.BUILD_NUMBER}"
                        sh "docker push ${DOCKER_IMAGE}:latest"
                    }
                }
            }
        }
    }
    
    post {
        always {
            sh "docker logout || true"
            cleanWs()
        }
    }
}
