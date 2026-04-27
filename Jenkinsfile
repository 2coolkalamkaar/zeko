pipeline {
    agent any
    
    environment {
        // TODO: Update these environment variables according to your setup
        DOCKER_IMAGE = 'your-dockerhub-username/python-k8s-starter'
        DOCKER_CREDENTIALS_ID = 'dockerhub-credentials'
        SONARQUBE_SERVER_NAME = 'SonarQube' // Name configured in Jenkins > Manage Jenkins > System
        SONAR_PROJECT_KEY = 'python-k8s-starter'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('SonarQube Analysis') {
            environment {
                // Ensure you have a SonarQube Scanner tool configured in Jenkins with this name
                // Go to Manage Jenkins > Tools > SonarQube Scanner installations
                SCANNER_HOME = tool 'SonarQubeScanner'
            }
            steps {
                withSonarQubeEnv("${SONARQUBE_SERVER_NAME}") {
                    sh "${SCANNER_HOME}/bin/sonar-scanner \
                        -Dsonar.projectKey=${SONAR_PROJECT_KEY} \
                        -Dsonar.projectName=${SONAR_PROJECT_KEY} \
                        -Dsonar.sources=."
                }
            }
        }
        
        stage('Docker Image Build') {
            steps {
                script {
                    // Builds the image and tags it with both the build number and 'latest'
                    sh "docker build -t ${DOCKER_IMAGE}:${env.BUILD_NUMBER} -t ${DOCKER_IMAGE}:latest ."
                }
            }
        }
        
        stage('Docker Image Push') {
            steps {
                script {
                    // Logs into Docker Hub and pushes the images
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
            // Clean up to prevent storage issues and log out of Docker
            sh "docker logout || true"
            cleanWs()
        }
    }
}
