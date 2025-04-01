# Monitoramento de Custos no Azure Data Factory

[![Azure](https://img.shields.io/badge/Azure-Functions-blue)](https://azure.microsoft.com)
[![Data Factory](https://img.shields.io/badge/Data-Factory-orange)](https://learn.microsoft.com/en-us/azure/data-factory/)

Este notebook documenta o processo de monitoramento de custos no Azure Data Factory (ADF) utilizando ferramentas nativas do Azure.

## Pré-requisitos
- Assinatura do Azure
- Azure Data Factory criado
- Conta de Armazenamento do Azure
- Python 3.8+
- Bibliotecas do Azure SDK

## Configuração Inicial

```python
# Instalação de dependências
!pip install azure-identity azure-mgmt-datafactory azure-mgmt-costmanagement pandas matplotlib

# Importação de bibliotecas
from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.costmanagement import CostManagementClient
import pandas as pd
import matplotlib.pyplot as plt

# Autenticação com Azure
credential = DefaultAzureCredential()
subscription_id = "<sua-subscription-id>"
resource_group_name = "<seu-resource-group>"
adf_name = "adf-monitoramento-custos"

# Clientes de gerenciamento
adf_client = DataFactoryManagementClient(credential, subscription_id)
cost_client = CostManagementClient(credential)
```

Este projeto demonstra como monitorar custos associados ao Azure Data Factory (ADF) utilizando ferramentas nativas do Azure como Azure Cost Management e Alertas de Orçamento. Abaixo estão os passos de implementação, insights e melhorias potenciais.

---

## Guia Passo a Passo

### 1. Criar um Data Factory
1. No **Portal do Azure**, clique em **Criar um recurso**.
2. Pesquise por **Data Factory** e siga o assistente de criação:
   - **Nome**: `adf-monitoramento-custos`.
   - **Versão**: V2.
   - **Região**: Selecione a mais próxima.
   - Habilite integração com Git (opcional para versionamento).
3. Revise e crie o recurso.

### 2. Criar um Pipeline de Exemplo
1. Acesse o **ADF Studio**.
2. Crie um novo pipeline:  
   **Author > Pipelines > New pipeline**.
3. Adicione uma atividade **Copy Data**:
   - **Origem**: Blob Storage (ex: arquivo CSV).
   - **Destino**: Azure SQL Database (tabela de destino).
4. Publique o pipeline.

### 3. Executar o Pipeline para Gerar Custos
1. Execute manualmente:  
   **Trigger > Trigger Now**.
2. Repita a execução para simular uso contínuo.

### 4. Analisar Custos no Azure Cost Management
1. Navegue até **Cost Management + Billing** no Portal do Azure.
2. Selecione o escopo (ex: grupo de recursos do ADF).
3. Filtre os custos por:
   - **Serviço**: Selecione "Data Factory".
   - **Recurso**: Veja custos específicos do ADF.

### 5. Configurar Orçamentos e Alertas
1. Em **Cost Management**, vá para **Budgets**.
2. Crie um novo orçamento:
   - **Valor**: Defina um limite mensal (ex: R$ 500).
   - **Alertas**: Configure notificações em 50%, 90% e 100% do limite.
3. Salve o orçamento.

---

## Insights e Aprendizados
- **Custos por Atividade**: Atividades como `Copy Data` têm custo variável conforme volume de dados.
- **Otimização**:
  - Execute pipelines em horários com preços reduzidos.
  - Use **Auto-pause** para workloads não críticos.
- **Tags**: Utilize tags (ex: `projeto=marketing`) para agrupar custos.
- **Monitoramento**: Acompanhe regularmente os dashboards do Cost Management.

---

## Conclusão
Este projeto mostra como monitorar custos do Azure Data Factory de forma eficiente usando ferramentas nativas do Azure. Com orçamentos e métricas, equipes podem controlar gastos e evitar surpresas.

[![Azure](https://img.shields.io/badge/Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white)](https://azure.microsoft.com)
