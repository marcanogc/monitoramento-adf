# monitoramento_adf.py
"""
Monitoramento de Custos no Azure Data Factory

Script para monitoramento de custos em tempo real do Azure Data Factory
Projeto: adf-monitoramento-custos
"""

from azure.identity import DefaultAzureCredential
from azure.mgmt.datafactory import DataFactoryManagementClient
from azure.mgmt.costmanagement import CostManagementClient
import pandas as pd
import matplotlib.pyplot as plt
import warnings

# Configurações iniciais
warnings.filterwarnings('ignore')
ADF_NAME = "adf-monitoramento-custos"
RESOURCE_GROUP = "rg-monitoramento-custos"
SUBSCRIPTION_ID = "SUA_SUBSCRIPTION_AQUI"

def configurar_cliente_azure():
    """Configura os clientes do Azure SDK"""
    credential = DefaultAzureCredential()
    
    adf_client = DataFactoryManagementClient(credential, SUBSCRIPTION_ID)
    cost_client = CostManagementClient(credential)
    
    return adf_client, cost_client

def pipeline_copia_exemplo(adf_client):
    """Cria pipeline de cópia dados Blob -> SQL"""
    pipeline_params = {
        "properties": {
            "activities": [
                {
                    "name": "CopiaDadosBlobParaSQL",
                    "type": "Copy",
                    "inputs": [{"referenceName": "dataset_entrada_blob", "type": "DatasetReference"}],
                    "outputs": [{"referenceName": "dataset_saida_sql", "type": "DatasetReference"}],
                    "typeProperties": {
                        "source": {"type": "BlobSource"},
                        "sink": {"type": "SqlSink"}
                    }
                }
            ]
        }
    }
    
    try:
        adf_client.pipelines.create_or_update(
            RESOURCE_GROUP,
            ADF_NAME,
            "PipelineCustos",
            pipeline_params
        )
        print("Pipeline criado com sucesso")
    except Exception as e:
        print(f"Erro na criação do pipeline: {str(e)}")

def analisar_custos(cost_client):
    """Coleta e analisa dados de custos"""
    query_params = {
        "type": "ActualCost",
        "timeframe": "MonthToDate",
        "dataset": {
            "granularity": "Daily",
            "aggregation": {"totalCost": {"name": "CustoTotal", "function": "Sum"}},
            "grouping": [{"type": "Dimension", "name": "ServiceName"}]
        }
    }
    
    try:
        resultado = cost_client.query.usage(
            f"/subscriptions/{SUBSCRIPTION_ID}/resourceGroups/{RESOURCE_GROUP}",
            query_params
        )
        
        dados = [{
            "data": row[0],
            "servico": row[2],
            "custo": row[1]
        } for row in resultado.rows]
        
        return pd.DataFrame(dados)
    except Exception as e:
        print(f"Erro na análise de custos: {str(e)}")
        return None

def gerar_relatorio(df):
    """Gera relatório gráfico dos custos"""
    plt.style.use('seaborn')
    df.plot(
        x='data',
        y='custo',
        kind='line',
        title='Custo Diário do ADF',
        figsize=(12, 7),
        marker='o',
        color='#0072B5'
    )
    
    plt.xlabel("Data")
    plt.ylabel("Custo (USD)")
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('relatorio_custos_adf.png')
    print("Relatório gerado: relatorio_custos_adf.png")

def configurar_alertas(cost_client):
    """Configura sistema de alertas de custo"""
    parametros_orcamento = {
        "category": "Cost",
        "amount": 500.0,
        "timeGrain": "Monthly",
        "timePeriod": {"startDate": "2024-01-01"},
        "notifications": {
            "alerta80": {
                "threshold": 80,
                "contactEmails": ["ti@empresa.com.br"],
                "operator": "GreaterThanOrEqualTo"
            }
        }
    }
    
    try:
        cost_client.budgets.create_or_update(
            RESOURCE_GROUP,
            "OrcamentoADF",
            parametros_orcamento
        )
        print("Alertas configurados com sucesso")
    except Exception as e:
        print(f"Erro na configuração de alertas: {str(e)}")

def main():
    """Fluxo principal de execução"""
    adf_client, cost_client = configurar_cliente_azure()
    
    # Criar pipeline (executar apenas uma vez)
    # pipeline_copia_exemplo(adf_client)
    
    # Análise de custos
    dados_custos = analisar_custos(cost_client)
    
    if dados_custos is not None:
        print("\nResumo Estatístico:")
        print(dados_custos.describe())
        gerar_relatorio(dados_custos)
        
        # Configurar alertas
        configurar_alertas(cost_client)

if __name__ == "__main__":
    main()
