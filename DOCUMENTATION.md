# Security Pipeline Lab — English Documentation

## What is this project?
A CI/CD pipeline with automated security scanning built with Jenkins and Docker. It analyzes code before deployment and blocks it if vulnerabilities are found, notifying the team via Telegram.

## Security Mechanism Selected
**Automated Security Pipeline (DevSecOps)** — Every time code is pushed to GitHub, Jenkins automatically runs two security scanners before allowing deployment.

## How it works
1. Developer pushes code to GitHub
2. Jenkins detects the change and starts the pipeline
3. **Trivy** scans dependencies for known CVEs
4. **Semgrep** scans source code for dangerous patterns
5. If vulnerabilities are found → deployment is **blocked** + Telegram alert 🚨
6. If code is clean → app is deployed + Telegram confirmation ✅

## Tools Used
| Tool | Purpose |
|------|---------|
| Jenkins | CI/CD automation |
| Docker | Container management |
| Trivy | Dependency vulnerability scanner |
| Semgrep | Source code static analysis (SAST) |
| Telegram Bot | Real-time notifications |

## Risk Mitigated & Security Principles
| Vulnerability | Principle Violated | Detected By |
|---|---|---|
| Hardcoded secrets | Confidentiality | Semgrep |
| SQL Injection | Integrity | Semgrep |
| Command Injection | Availability | Semgrep |
| Outdated dependencies | Availability | Trivy |

## Repository Structure

security-pipeline-lab/
├── app/                  # Vulnerable Flask app (demo target)
│   ├── app.py
│   ├── requirements.txt
│   └── Dockerfile
├── jenkins/
│   └── Jenkinsfile       # Full CI/CD pipeline definition
├── semgrep-rules.yaml    # Custom security rules
└── docker-compose.yml    # Container orchestration

## Results
- **Vulnerable code** → Pipeline FAILS → Telegram: "Deployment BLOCKED"
- **Clean code** → Pipeline SUCCEEDS → App deployed → Telegram: "App deployed successfully"
