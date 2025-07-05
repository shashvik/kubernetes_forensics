# 🕵️ Kubernetes Pod Forensics Lab

A simple project to simulate a Kubernetes pod compromise and demonstrate container forensics using tools like `crictl`, volume extraction, and runtime analysis.

---

## 📁 Project Structure

```
.
├── Dockerfile              # Container image for the vulnerable app
├── app.py                  # Vulnerable Flask app allowing command execution
├── vulnerable-pod.yaml     # Kubernetes Deployment & Service YAML
└── Readme.md               # This file
```

---

## 🚀 Overview

This project simulates a **Remote Command Execution (RCE)** vulnerability in a Kubernetes pod, where an attacker can deploy malware (e.g., **XMRig** cryptominer) inside a container.

The project also demonstrates how to:

- Deploy a deliberately vulnerable pod.
- Simulate a compromise.
- Perform basic forensic investigation on the pod.

---

## 🔖 Getting Started

### 1. Build and Push the Docker Image

```bash
# Build for amd64 (for EKS/EC2 compatibility)
docker buildx build --platform linux/amd64 -t <your-dockerhub-or-ecr-username>/vuln-shell-app:latest .

# Push to Docker Hub or ECR
docker push <your-dockerhub-or-ecr-username>/vuln-shell-app:latest
```

### 2. Deploy to Kubernetes

```bash
kubectl apply -f vulnerable-pod.yaml
```

Access the application:
```
http://<node-public-ip>:30007
```

---

## 🔫 Simulating the Attack

1. Open the web app in the browser.
2. Type shell commands in the search bar (e.g., `ls`, `uname -a`).
3. Simulate malware by downloading any sample script or tool (e.g., **XMRig**).

---

## 🔍 Forensic Investigation Steps

1. **Get the Pod's Container ID:**
```bash
kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[0].containerID}'
```

2. **Extract and Copy Filesystem:**
```bash
CONTAINER_ID=$(kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[0].containerID}' | sed 's/^containerd:\/\///')
sudo cp -r /run/containerd/io.containerd.runtime.v2.task/k8s.io/$CONTAINER_ID/rootfs /home/forensics/<pod-name>-rootfs-$(date +%Y%m%d%H%M%S)
```

3. **Inspect Container Runtime:**
```bash
VERSION="v1.33.0"
wget https://github.com/kubernetes-sigs/cri-tools/releases/download/$VERSION/crictl-$VERSION-linux-amd64.tar.gz
sudo tar zxvf crictl-$VERSION-linux-amd64.tar.gz -C /usr/local/bin
rm -f crictl-$VERSION-linux-amd64.tar.gz

sudo crictl inspect $CONTAINER_ID
```

---

## 💡 Key Takeaways

- Kubernetes containers are **ephemeral**—malware and evidence can disappear if not preserved immediately.
- Always **copy the container's filesystem** to a **persistent storage** before pod termination.
- Tools like `crictl`, `kubectl`, and direct filesystem access are crucial for **incident response and forensic analysis** in Kubernetes.

---

## 🌐 License

This project is intended for **educational and defensive security purposes only**. Use responsibly.

