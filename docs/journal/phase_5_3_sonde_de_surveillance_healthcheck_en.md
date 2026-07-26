# 📌 Session 5.3: Container System Health Probe (`HEALTHCHECK`)

**Date:** July 25, 2026

This session adds native container monitoring probes using the `HEALTHCHECK` directive in the Dockerfile to check `/health` status every 15 seconds.

---

### 1. 🎓 Concepts Introduced

*   **Docker HEALTHCHECK Instruction:** Configures container daemon to periodically run health commands inside running containers.
*   **Orchestrator Liveness Probes:** Signals used by Kubernetes or Docker Swarm to automatically restart unresponsive container instances.
*   **Minimal Curl Health Polling:** Executing lightweight `curl` requests against `http://localhost:8000/health`.

---

### 2. 🧠 Architecture Decision Records (ADRs)

#### Dilemma: Container Monitoring Mechanism
*   **Option 1: Relying solely on Process ID (PID 1) monitoring**
    *   *Pros/Cons:* Checks if Uvicorn process is running, but fails to detect deadlocks or frozen event loops.
*   **Option 2: Docker `HEALTHCHECK` Probe against GET `/health` (Selected)**
    *   *Why this choice?* Actively tests HTTP endpoint response, ensuring real operational readiness.

---

### 3. 🛠️ Implementation & Auto-Documentation

#### Dockerfile Instruction:
```dockerfile
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1
```

#### Validation Command:
```bash
docker ps
```
*Expected Output:* Container status displays `(healthy)`.

---

### 4. 📌 Session Summary

1.  **Native Container Probe:** Integrated `HEALTHCHECK` command into Dockerfile.
2.  **Orchestrator Readiness:** Provided active status polling for production deployment.
