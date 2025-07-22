# PreSetUP
### Tools Used :
- Github
- Jenkins
- AWS EC2
- Trivy
- Syft
- Docker
- Streamlit


> this project is done on AWS EC2. we have taken 2 EC2 instances one for master and another as worker
- Master Node - Jenkin setup
- Woker Node - Jenkins agent

# 1. Jenkins Master setUP
in EC2 master instance 
- Install java
```BASH
sudo apt update
sudo apt install fontconfig openjdk-21-jre
java -version
openjdk version "21.0.3" 2024-04-16
OpenJDK Runtime Environment (build 21.0.3+11-Debian-2)
OpenJDK 64-Bit Server VM (build 21.0.3+11-Debian-2, mixed mode, sharing)
```
- Install Jenkins
```
sudo wget -O /etc/apt/keyrings/jenkins-keyring.asc \
  https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key
echo "deb [signed-by=/etc/apt/keyrings/jenkins-keyring.asc]" \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null
sudo apt-get update
sudo apt-get install jenkins
```
- After jenkins installation
  - enable port 8080 in your instance by editing inbound rule
  - unlock jenkins - enter the command ``` sudo cat /var/lib/jenkins/secrets/initialAdminPassword ``` to get administration password
- Setup Jenkins
  - go to Manage Jenkins
  - go to plugin --> Available plugins
  - install Docker , github, pipeline view
 ### 2. EC2 worker server setup(jenkins agent)
 - install java 17+
```
sudo apt update
sudo apt install fontconfig openjdk-21-jre
java -version
openjdk version "21.0.3" 2024-04-16
OpenJDK Runtime Environment (build 21.0.3+11-Debian-2)
OpenJDK 64-Bit Server VM (build 21.0.3+11-Debian-2, mixed mode, sharing)
```
 - install docker
```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update

# intall docker
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# verify the installation
sudo docker run hello-world
```
 - install trivy
```
sudo apt-get install wget apt-transport-https gnupg lsb-release
wget -qO - https://aquasecurity.github.io/trivy-repo/deb/public.key | sudo apt-key add -
echo deb https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main | sudo tee -a /etc/apt/sources.list.d/trivy.list
sudo apt-get update
sudo apt-get install trivy
```
 - install syft
```
sudo snap install syft --classic
```
# 3. SSH setUP
- generate ssh key in jenkins master
  ```
      ssh-keygen
  ```
- get the public key and paste it in authorized-key file of worker node
- confirm the ssh setup using the following command
  ```
   ssh ubuntu@44.210.131.85   
   ```
# 4. setup the node in jenkins


# 5. 
  

# CI/CD Pipeline for AI BOM Generator

This Jenkins pipeline automates the process of fetching, building, testing, and promoting an AI-based Bill of Materials (AIBOM) model. The pipeline ensures that the model is properly validated, tested, and checked for security vulnerabilities before deployment.

## 📌 Pipeline Stages

### 1️⃣ **Build**

- Cleans the existing model directory.
- Fetches the model from either a GitHub repository or a local path.
- Ensures essential files (`dataset.json` and `model_info.json`) exist.

### 2️⃣ **Deploy**

- Fetches the AIBOM script from the predefined repository.
- Copies the necessary script (`generate_aibom.py`) into the model directory.

### 3️⃣ **Test**

- Installs security tools (**Syft** and **Trivy**) for Software Bill of Materials (SBOM) and vulnerability scanning.
- Runs the AIBOM script to generate reports.
- Ensures that the reports directory is created.

### 4️⃣ **Promote**

- Validates the generated reports (`aibom.json`, `sbom.json`, `vulnerability.json`).
- Checks for security vulnerabilities in the `vulnerability.json` file.
- Displays the generated reports.

## 🔧 **Setup & Configuration**

### **Pipeline Parameters**

| Parameter          | Default Value | Description                                   |
| ------------------ | ------------- | --------------------------------------------- |
| `MODEL_GIT_URL`    | `""` (empty)  | GitHub repository URL for fetching the model. |
| `MODEL_LOCAL_PATH` | `""` (empty)  | Local path to fetch the model.                |

### **Environment Variables**

| Variable             | Value                                                  |
| -------------------- | ------------------------------------------------------ |
| `GIT_CREDENTIALS_ID` | `github-credentials`                                   |
| `MODEL_DIR`          | `F:/HPE_Project/Model`                                 |
| `SCRIPT_REPO`        | `https://github.com/HPE-CPP-AIBOM/AIBOM_Generator.git` |
| `REPORT_DIR`         | `${MODEL_DIR}/reports`                                 |
| `TOOLS_DIR`          | `${MODEL_DIR}/tools`                                   |

## 🚀 **Running the Pipeline**

To execute the pipeline:

1. Configure the `MODEL_GIT_URL` or `MODEL_LOCAL_PATH` as parameters.
2. Run the pipeline from Jenkins.
3. Monitor the console output for errors or warnings.

## ✅ **Success Criteria**

- Model is successfully fetched.
- Required files exist in the model directory.
- Security tools are installed and executed without errors.
- Vulnerability scan shows no critical issues.
- Reports are successfully generated in the `reports/` directory.

## ⚠️ **Failure Scenarios**

- Missing model files (`dataset.json` or `model_info.json`).
- Pipeline fails due to security vulnerabilities in the model.
- Reports not generated properly.

## 📝 **Post-Pipeline Execution**

- If the pipeline fails, check the logs for errors.
- If the pipeline succeeds, review the generated reports.
- Take necessary actions based on security scan results before promoting the model.

---

🚀 **This CI/CD pipeline ensures secure and validated AI model deployment with automated vulnerability scanning.** Happy coding! 🎯

