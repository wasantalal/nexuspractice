pipeline {
    agent any

    environment {
        
        GIT_REPO       = "https://github.com/wasantalal/nexuspractice.git"
        GIT_BRANCH     = "main"

        IMAGE_NAME     = "docker_env"               
        NEXUS_REGISTRY = "192.168.20.218:8082"

        
        IMAGE_TAG  = "v${BUILD_NUMBER}"
        FULL_IMAGE = "${NEXUS_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
    }

    stages {

        stage('Get Code From GitHub') {
            steps {
                echo "Cloning repository..."
                git branch: "${GIT_BRANCH}", url: "${GIT_REPO}"
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image..."
                bat """
                docker build -t %IMAGE_NAME%:%IMAGE_TAG% .
                """
            }
        }

        stage('Tag Image for Nexus') {
            steps {
                echo "Tagging image for Nexus..."
                bat """
                docker tag %IMAGE_NAME%:%IMAGE_TAG% %FULL_IMAGE%
                """
            }
        }

        stage('Login to Nexus') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: '216f8201-75a8-4533-9b9e-34ee08f79dae',
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {

                    bat """
                    echo %PASS% | docker login %NEXUS_REGISTRY% -u %USER% --password-stdin
                    """
                }
            }
        }

        stage('Push to Nexus') {
            steps {
                echo "Pushing image to Nexus..."
                bat """
                docker push %FULL_IMAGE%
                """
            }
        }

        stage('Run Container') {
            steps {
                echo "Stopping old container (if exists)..."
                bat """
                docker stop %IMAGE_NAME% || exit 0
                docker rm %IMAGE_NAME% || exit 0
                """

                echo "Running new container..."
                bat """
                docker run -d --name %IMAGE_NAME% -p 8000:8000 %FULL_IMAGE%
                """
            }
        }
    }

    post {
        success {
            echo "Pipeline completed successfully!"
        }
        failure {
            echo "Pipeline failed."
        }
    }
}
