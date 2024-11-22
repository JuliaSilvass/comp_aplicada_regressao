import pandas as pd
import os

# Carregar o CSV
data = pd.read_csv('Dados/primeiro.csv')

# Pasta de destino
pasta_destino = 'Dados_atualizado/'

# Verifique se a pasta existe. Se não, crie-a.
if not os.path.exists(pasta_destino):
    os.makedirs(pasta_destino)

# Colunas que devem ser numéricas
numerical_columns = ['idade', 'escore_CF', 'pontuacao_cf', 'arit_percentil', 'arit_resposta']

# Garantir que todas as colunas numéricas estejam no formato correto
data[numerical_columns] = data[numerical_columns].apply(pd.to_numeric, errors='coerce')

# Checar se os tipos estão corretos
print(data.dtypes)

# Funções de transformação
def stringToNumeric(data, column):
    """Converte strings em números sequenciais."""
    # Verifica se a coluna é do tipo 'object' (strings)
    if data[column].dtype == 'object':
        data[column] = data[column].astype('category').cat.codes
    return data


def stringToIndex(data, column, mapping):
    """Converte strings em índices com base em um mapeamento fornecido."""
    # Verifica se a coluna é do tipo 'object' (strings)
    if data[column].dtype == 'object':
        data[f'{column}_index'] = data[column].map(mapping)
    return data

def stringToBinary(data, column):
    """Converte uma coluna para valores binários."""
    # Verifica se a coluna é do tipo 'object' (strings)
    if data[column].dtype == 'object':
        data[f'{column}_binary'] = data[column].apply(lambda x: 1 if x == 'M' else 0)
    return data

# Dicionário de pré-processamento
preprocessing_steps = {
    'sexo': {'type': 'binary'},  # Transforma 'M' para 1 e outros para 0
    'resultado_teste_cf': {
        'type': 'index',
        'mapping': {
            'média': 2,
            'baixa': 1,
            'alta': 3,
            'muito alta':4,
            'muito baixa':5
        }
    },
    'psicogenese': {
        'type': 'index',
        'mapping': {
            'Silábico': 1,
            'Alfabético': 2,
            'Pré-silábico': 3,
            'Silábico-alfabético': 4
        }
    },
    'arit_interpretacao': {
        'type': 'index',
        'mapping': {
            'Médio': 1,
            'Alerta para déficit': 2,
            'Acima do esperado': 3,
            'Déficit grave': 4,
            'Médio-inferior': 5,
            'Médio-superior': 6,
            'Muito acima do esperado': 7
        }
    }
}

# Aplicar as transformações
for column, config in preprocessing_steps.items():
    if config['type'] == 'numeric':
        data = stringToNumeric(data, column)
    elif config['type'] == 'index':
        data = stringToIndex(data, column, config['mapping'])
    elif config['type'] == 'binary':
        data = stringToBinary(data, column)

# Defina o caminho completo do arquivo de destino
caminho_arquivo = os.path.join(pasta_destino, 'novo_primeiro.csv')

# Salve o DataFrame em um novo arquivo CSV dentro da pasta
data.to_csv(caminho_arquivo, index=False, quoting=0)  # quoting=0 remove aspas

# Mensagem de sucesso
print("Arquivo atualizado com sucesso!")
