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
