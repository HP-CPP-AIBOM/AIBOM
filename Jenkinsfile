pipeline {
    agent { label 'worker'}

    stages {
        stage('clone the AImodel repo') {
            steps {
                cleanWs()
                git url: 'https://github.com/HP-CPP-AIBOM/AIBOM.git', branch: 'main'
                sh 'mkdir reports'
            }
        }
        stage('clone the AIBOM repo') {
            steps {
                dir('AImodel'){
                    git url: 'https://github.com/HPE-CPP-AIBOM/xgen.git', branch: 'main'
                }
                
            }
        }
        stage('generate AIBOM') {
            steps {
                    sh 'python3 generate_aibom.py --model-path /home/ubuntu/workspace/AIBOM/AImodel'
            }
        }
        stage("Trivy scan "){
            steps{
                sh 'trivy fs AImodel --format json --output /home/ubuntu/workspace/AIBOM/reports/Trivy_vuln.json'
            }
        }
        stage("Syft scan"){
            steps{
                sh 'syft dir:AImodel -o json --file /home/ubuntu/workspace/AIBOM/reports/Syft_vuln.json'
            }
        }
        stage('Pull docker image from docker hub'){
            steps{
                sh 'docker pull kubehabs/cvss_dashboard:amd64'
            }
        }
        stage('run docker image'){
            steps{
                sh 'docker run --rm -p 8501:8501 kubehabs/cvss_dashboard:amd64'
                
                
            }
        }
        
    }
}

