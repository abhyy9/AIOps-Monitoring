# AIOps - Intelligent Infrastructure Monitoring & Auto-Remediation System

An AI-powered infrastructure monitoring system that automatically detects anomalies and fixes them without human intervention.

## 🎯 What it does

- Monitors server metrics (CPU, Memory, Disk) every 15 seconds
- AI model detects anomalies before they cause crashes
- Automatically fixes issues without human intervention
- Beautiful Grafana dashboard for visualization

## 🔄 How it works
Node Exporter → collects server metrics

↓

Prometheus → stores metrics every 15s

↓

AI Model → detects anomalies

↓

Auto Remediation → fixes issues automatically

↓

Grafana → shows everything visually

## 🛠️ Tools Used

| Tool | Purpose |
|------|---------|
| Terraform | Infrastructure as Code - creates EC2 automatically |
| Prometheus | Collects and stores server metrics |
| Grafana | Visualizes metrics in beautiful dashboards |
| Node Exporter | Exposes server stats to Prometheus |
| Python + Scikit-learn | AI anomaly detection model |
| FastAPI | REST API to serve model predictions |
| Docker + Docker Compose | Containerizes all services |
| GitHub Actions | CI/CD - auto deploys on code push |
| AWS EC2 | Cloud server |

## 🚀 Services

| Service | Port |
|---------|------|
| Grafana Dashboard | 3000 |
| Prometheus | 9090 |
| Node Exporter | 9100 |
| AI Model API | 8000 |

## 📊 AI Model

- Algorithm: Isolation Forest
- Detects anomalies in CPU, Memory, Disk usage
- Auto-remediates:
  - High CPU → clears system cache
  - High Memory → restarts services
  - High Disk → cleans Docker files

## 🏗️ Setup

### 1. Infrastructure
```bash
cd terraform
terraform init
terraform apply
```

### 2. Deploy Monitoring Stack
```bash
cd monitoring
sudo docker-compose up -d
```

### 3. Train AI Model
```bash
python3 ai-model/train.py
```

### 4. Run API
```bash
sudo docker build -t aiops-api -f api/Dockerfile .
sudo docker run -d --name aiops-api -p 8000:8000 aiops-api
```

### 5. Start Auto Remediation
```bash
nohup python3 remediation/remediate.py > remediation.log 2>&1 &
```

## 📝 Resume Description

**AIOps - Intelligent Infrastructure Monitoring & Auto-Remediation System**
- Built AI-powered infrastructure monitoring using Prometheus, Grafana and Python
- Trained ML anomaly detection model (Isolation Forest) to detect server failures
- Implemented auto-remediation to fix issues without human intervention
- Provisioned AWS infrastructure using Terraform (IaC)
- Containerized all services using Docker and Docker Compose
- Automated deployment using GitHub Actions CI/CD pipeline

**Tools:** Python, Scikit-learn, FastAPI, Prometheus, Grafana, Terraform, Docker, GitHub Actions, AWS EC2
