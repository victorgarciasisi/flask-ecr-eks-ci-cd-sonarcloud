# Flask → ECR → EKS + SonarCloud (CI/CD)

Repo de ejemplo mínimo:
- Flask + Gunicorn
- Dockerfile + docker-compose
- GitHub Actions: SonarCloud → ECR → EKS
- K8s manifests (Deployment + Service)

## Requisitos previos
- AWS CLI configurado y permisos para ECR + EKS
- Un clúster EKS existente (p.ej., `CLUSTER_NAME=my-eks`)
- Un repositorio ECR creado (p.ej., `flask-eks-demo`)
- SonarCloud: organización y proyecto creados

## Secrets necesarios en GitHub (Settings → Secrets and variables → Actions → *New repository secret*)

**AWS / ECR / EKS**
- `AWS_REGION` → p.ej. `eu-west-1`
- `AWS_ACCOUNT_ID` → tu ID de cuenta AWS
- `ECR_REPOSITORY` → p.ej. `flask-eks-demo`
- `CLUSTER_NAME` → nombre de tu EKS
- `K8S_NAMESPACE` → p.ej. `default`
- **OIDC recomendado**: `AWS_ROLE_TO_ASSUME` → ARN del role que permita ECR (push) y EKS (Describe/Update kubeconfig)
  - Políticas mínimas: `AmazonEC2ContainerRegistryPowerUser`, `AmazonEKSClusterPolicy`, `AmazonEKSDescribePolicy` (o equivalentes por permisos finos)

**SonarCloud**
- `SONAR_TOKEN` → token del proyecto u organización en SonarCloud

> Alternativa (no OIDC): añade también `AWS_ACCESS_KEY_ID` y `AWS_SECRET_ACCESS_KEY` y ajusta el workflow.

## Deploy inicial
1. **Local opcional**:
   ```bash
   docker compose up --build
   # abre http://localhost:8000
   ```
2. **Primer push** a `main` desencadena el pipeline:
   - SonarCloud analiza
   - Se construye imagen y se empuja a ECR con tag `latest` y `GITHUB_SHA`
   - Se aplican manifiestos y se actualiza la imagen del Deployment
3. Obtén la **URL pública** del Service (ALB/NLB/ELB) en EKS:
   ```bash
   kubectl get svc my-app-service -n <tu-namespace>
   ```

## Notas
- El deployment apunta inicialmente a `REPLACE_ME_ECR_URI/...`. El workflow lo sobreescribe con `kubectl set image` usando el SHA del commit.
- Para producción, considera separar `apply` inicial y usar Helm/Kustomize para versionar imágenes.
- Agrega tests si quieres calidad extra y SonarCloud podrá medir cobertura.
```

---

**Listo.** Sustituye los placeholders (`YOUR_SONARCLOUD_ORG`, `YOUR_SONARCLOUD_PROJECT_KEY`, `REPLACE_ME_ECR_URI`) y crea los **secrets** indicados. Luego haz push a `main`.

