# Automated Framework for generation and maintainnence of AIBill of meterials 
This project automates the security and AI bill of materials (AIBOM) reporting for AI models using Jenkins pipelines. It leverages tools like Trivy and Syft to scan for vulnerabilities and generate metadata reports. The entire setup runs on AWS EC2 instances.
# Tools Used 
- GitHub – Version control and webhook trigger source
- Jenkins – CI/CD orchestration
- Docker – Containerization
- Trivy – Vulnerability scanner
- Syft – SBOM generator
- Streamlit – Visualization of reports
- AWS EC2 – Infrastructure

# 1. Jenkins Master Setup(EC2)
### Prerequisites:
- A fresh Ubuntu EC2 instance (e.g. t2.medium)
- Port 8080 opened in the security group
### Install Java & Jenkins
``` Bash
sudo apt update
sudo apt install fontconfig openjdk-21-jre -y
java -version
```
``` bash
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc] https://pkg.jenkins.io/debian-stable binary/" | sudo tee /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt update
sudo apt install jenkins -y
```
### Post-Installation
- Enable port 8080 in your EC2 security group
- Get the Jenkins admin password:
  ```
  sudo cat /var/lib/jenkins/secrets/initialAdminPassword
  ```
- Set up Jenkins in the browser at http://<EC2-PUBLIC-IP>:8080
### Install Plugins:
- Go to Manage Jenkins → Plugins
- Install:
  - GitHub
  - Docker Pipeline
  - Pipeline
  - Pipeline View

> this project is done on AWS EC2. we have taken 2 EC2 instances one for master and another as worker
- Master Node - Jenkin setup
- Woker Node - Jenkins agent

# 2. Worker Node Setup (EC2 Agent)
### Requirements:
- Java 17+
- Docker (with permissions)
- Trivy
- Syft
🔸 Install Java
```
sudo apt update
sudo apt install fontconfig openjdk-21-jre -y
java -version
```
🔸 Install Docker
- Add Docker's GPG key and repo
```
sudo apt-get install ca-certificates curl -y
sudo install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo tee /etc/apt/keyrings/docker.asc > /dev/null
sudo chmod a+r /etc/apt/keyrings/docker.asc

echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | \
sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

sudo apt update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin -y

# Verify Docker
sudo docker run hello-world
```
✅ Add user to Docker group:
```
sudo usermod -aG docker ubuntu
newgrp docker
```
🔸 Install Trivy
```
sudo apt install wget apt-transport-https gnupg lsb-release -y
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo "deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -cs) main" | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt update
sudo apt install trivy -y
```
🔸 Install Syft
```
sudo snap install syft --classic
```

# 3. SSH Setup Between Master & Worker

- On Jenkins Master:
```
ssh-keygen  # press Enter to all prompts
cat ~/.ssh/id_rsa.pub
```
- On Worker Node:
```
Paste the public key into:
~/.ssh/authorized_keys
```
- Verify connection:
```
ssh ubuntu@<WORKER_PUBLIC_IP>
```

# 4. Add Agent Node in Jenkins
- From Jenkins Master:
  1. Go to Manage Jenkins → Nodes → New Node
  2. Set:
```
    Node name: agent-ec2
    Launch method: Launch agent via SSH
    Host: <Worker IP>
    Credentials: SSH key created earlier
    Remote root directory: /home/ubuntu
```

# 5. Create Jenkins Pipeline

> Project Settings:
- Type: Pipeline
- Enable:
  - GitHub Project
  - GitHub hook trigger for GITScm polling
  - Set the GitHub repo URL
- paste provided jenkins script in Jenkins templete

# 6. Set Up GitHub Webhook Trigger

### On GitHub:
- Go to Settings → Webhooks → Add webhook
- Payload URL: http://<JENKINS_MASTER_PUBLIC_IP>:8080/github-webhook/
- Content type: application/json
- Trigger: Push events

# 7. Result

###  On every push to your GitHub repo:
- Jenkins pipeline is triggered
- AIBOM, SBOM, and vulnerability reports are generated
- Streamlit dashboard is available at http://<worker-ip>:8501
- Open the dashboard in your browser to view live scan results and model metadata



