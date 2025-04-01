# Monitoramento de Custos no Azure Data Factory

[![Azure](https://img.shields.io/badge/Azure-Functions-blue)](https://azure.microsoft.com)
[![Data Factory](https://img.shields.io/badge/Data-Factory-orange)](https://learn.microsoft.com/en-us/azure/data-factory/)

Este notebook documenta el proceso de monitoreo de costos en Azure Data Factory (ADF) utilizando herramientas nativas de Azure.

## Requisitos Previos
- Suscripción de Azure
- Azure Data Factory creado
- Azure Storage Account
- Python 3.8+
- Bibliotecas de Azure SDK

## Configuración Inicial

```python
# Instalación de dependencias
!pip install azure-identity azure-mgmt-datafactory azure-mgmt-costmanagement pandas matplotlib

# Importación de bibliotecas
from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.costmanagement import CostManagementClient
import pandas as pd
import matplotlib.pyplot as plt

# Autenticación con Azure
credential = DefaultAzureCredential()
subscription_id = "<your-subscription-id>"
resource_group_name = "<your-resource-group>"
adf_name = "adf-monitoramento-custos"

# Clientes de administración
adf_client = DataFactoryManagementClient(credential, subscription_id)
cost_client = CostManagementClient(credential)
