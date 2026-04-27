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
                script {
                    // 1. Fetch the scanner executable from Jenkins Global Tools
                    def scannerHome = tool 'sonar-scanner'
                    
                    // 2. Wrap the execution in the SonarQube environment block
                    // This automatically injects the URL and secret token configured in Jenkins UI
                    withSonarQubeEnv(env.SONARQUBE_SERVER_NAME) {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=${env.SONAR_PROJECT_KEY} \
                              -Dsonar.sources=.
                        """
                    }
                }
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