# Script de apoyo para desplegar SubSonic Festival en Azure Container Apps.
# Ejecutar desde la raiz del repositorio.
# Revisar los nombres antes de lanzar los comandos.

$RG = "subsonic-rg"
$LOC = "westeurope"
$ACR = "subsonicacr12345"
$ENV = "subsonic-env"
$APP = "subsonic-app"
$IMAGE = "subsonic-festival"
$TAG = "practica04"

az login

az group create --name $RG --location $LOC

az acr create `
  --resource-group $RG `
  --name $ACR `
  --sku Basic `
  --admin-enabled true

az acr login --name $ACR

docker build -f Docker/Dockerfile -t "${IMAGE}:${TAG}" .
docker tag "${IMAGE}:${TAG}" "$ACR.azurecr.io/${IMAGE}:${TAG}"
docker push "$ACR.azurecr.io/${IMAGE}:${TAG}"

az extension add --name containerapp --upgrade
az provider register --namespace Microsoft.App
az provider register --namespace Microsoft.OperationalInsights

az containerapp env create `
  --name $ENV `
  --resource-group $RG `
  --location $LOC

$ACR_USER = az acr credential show --name $ACR --query username -o tsv
$ACR_PASS = az acr credential show --name $ACR --query "passwords[0].value" -o tsv

az containerapp create `
  --name $APP `
  --resource-group $RG `
  --environment $ENV `
  --image "$ACR.azurecr.io/${IMAGE}:${TAG}" `
  --target-port 8000 `
  --ingress external `
  --registry-server "$ACR.azurecr.io" `
  --registry-username $ACR_USER `
  --registry-password $ACR_PASS

az containerapp show `
  --name $APP `
  --resource-group $RG `
  --query properties.configuration.ingress.fqdn `
  -o tsv
