# 📌 Session 5.2: Non-Root Container Security Hardening

**Date:** July 25, 2026

This session hardens container runtime security by configuring execution under an unprivileged user (`appuser` UID 1000) rather than `root`.

---

### 1. 🎓 Concepts Introduced

*   **Principle of Least Privilege:** Security standard dictating that applications must execute with minimal required system access rights.
*   **Non-root Execution (`USER appuser`):** Explicitly switching container execution context to a non-privileged user account.
*   **Container Escape Mitigation:** Preventing potential application exploits from gaining host-level `root` privileges.

---

### 2. 🧠 Architecture Decision Records (ADRs)

#### Dilemma: Container Execution Privilege Level
*   **Option 1: Default `root` User Execution**
    *   *Pros/Cons:* Convenient, but presents severe security risk if an RCE vulnerability allows container breakout to host system as root.
*   **Option 2: Unprivileged `appuser` (UID 1000) Execution (Selected)**
    *   *Why this choice?* Running as non-root mitigates container escape risks and complies with enterprise DevSecOps standards.

---

### 3. 🛠️ Implementation & Auto-Documentation

#### Dockerfile Security Snippet:
```dockerfile
RUN groupadd -g 1000 appgroup && \
    useradd -u 1000 -g appgroup -s /bin/sh -m appuser && \
    chown -R appuser:appgroup /app

USER appuser
```

#### Validation Command:
```bash
docker run --rm aipe-framework:latest whoami
```
*Expected Output:* Prints `appuser`.

---

### 4. 📌 Session Summary

1.  **Security Hardening:** Enforced non-root execution (`appuser` UID 1000).
2.  **Least Privilege Compliance:** Mitigated host breakout vulnerabilities.
