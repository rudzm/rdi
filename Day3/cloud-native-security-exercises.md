# Cloud-Native Security Exercises

## Exercise 1 — Kubernetes RBAC & ServiceAccount

### Goal
Create a Pod running with a **ServiceAccount** that can **list Pods only in one namespace**, then **prove it from inside the Pod** by calling the Kubernetes API using `curl`.

---

### Step 1 — Create Namespace
```bash
kubectl create ns demo
```

---

### Step 2 — Create ServiceAccount
```yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: pod-lister
  namespace: demo
```

---

### Step 3 — Create Role (list/get/watch Pods)
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: pod-reader
  namespace: demo
rules:
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["get", "list", "watch"]
```

---

### Step 4 — Create RoleBinding
```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: pod-reader-binding
  namespace: demo
subjects:
  - kind: ServiceAccount
    name: pod-lister
    namespace: demo
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: pod-reader
```

---

### Step 5 — Create Pod Using the ServiceAccount
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: rbac-test
  namespace: demo
spec:
  serviceAccountName: pod-lister
  containers:
    - name: curl
      image: curlimages/curl:8.6.0
      command: ["sh", "-c", "sleep 36000"]
```

---

### Step 6 — Test Access from Inside the Pod
```bash
kubectl exec -n demo -it rbac-test -- sh
```

Inside the Pod:
```sh
APISERVER="https://kubernetes.default.svc"
TOKEN="$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
CACERT="/var/run/secrets/kubernetes.io/serviceaccount/ca.crt"

curl --cacert "$CACERT" \
  -H "Authorization: Bearer $TOKEN" \
  "$APISERVER/api/v1/namespaces/demo/pods"
```

Test forbidden access:
```sh
curl -o /dev/null -w "%{http_code}\n" --cacert "$CACERT" \
  -H "Authorization: Bearer $TOKEN" \
  "$APISERVER/api/v1/namespaces/default/pods"
```

Expected result: `403 Forbidden`

---

## Exercise 2 — SBOM Generation and Vulnerability Analysis (Syft & Grype)

### Goal
Generate an **SBOM** for a container image and analyze vulnerabilities using **Grype**.

---

### Step 1 — Build Image
```bash
docker build -t hello-app:demo .
```

---

### Step 2 — Generate SBOM (CycloneDX)
```bash
syft hello-app:demo -o cyclonedx-json > sbom.cdx.json
```

---

### Step 3 — Inspect SBOM
```bash
syft hello-app:demo
```

---

### Step 4 — Scan Image with Grype
```bash
grype hello-app:demo
```

Export results:
```bash
grype hello-app:demo -o json > grype-findings.json
```

---

### Deliverables
- `sbom.cdx.json`
- `grype-findings.json`
- Short summary of top risks and mitigation options
