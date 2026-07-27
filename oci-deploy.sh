#!/usr/bin/env bash
# ==============================================================================
# Script de Deploy em Nuvem Oracle Cloud Infrastructure (OCI)
# Desafio Alura Agentes — Nexus AI Agente Corporativo
# ==============================================================================

set -e

echo "🚀 [OCI DEPLOY] Iniciando automação de implantação na Nuvem Oracle (OCI)..."

# 1. Verificar instalação do Docker e OCI CLI
if ! command -v docker &> /dev/null; then
    echo "❌ Docker não foi encontrado. Instalando dependências..."
    sudo apt-get update
    sudo apt-get install -y docker.io docker-compose
fi

# 2. Configurar variáveis de ambiente OCI
export OCI_REGION=${OCI_REGION:-"sa-saopaulo-1"}
export OCI_BUCKET_NAME=${OCI_BUCKET_NAME:-"alura-agentes-knowledge-bucket"}
echo "📍 Região OCI Alvo: $OCI_REGION"
echo "🪣 Bucket OCI Object Storage: $OCI_BUCKET_NAME"

# 3. Build da imagem da aplicação
echo "📦 Construindo a imagem Docker da aplicação Nexus AI..."
docker build -t nexus-ai-agent:latest .

# 4. Parar contêiner antigo se existir e iniciar novo
echo "🔄 Inicializando serviço na Nuvem OCI (porta 8000)..."
docker stop nexus_ai_agent_oci 2>/dev/null || true
docker rm nexus_ai_agent_oci 2>/dev/null || true

docker run -d \
  --name nexus_ai_agent_oci \
  --restart always \
  -p 8000:8000 \
  -e OCI_REGION="$OCI_REGION" \
  -e OCI_BUCKET_NAME="$OCI_BUCKET_NAME" \
  nexus-ai-agent:latest

echo "✅ [OCI DEPLOY CONCLUÍDO] Agente de IA Corporativo ativo e acessível na porta 8000!"
echo "🔗 Healthcheck OCI: http://localhost:8000/api/health"
echo "🌐 Interface Web: http://localhost:8000/"
