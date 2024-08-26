import pandas as pd

# Carregar o CSV
df = pd.read_csv('consumo.csv', sep=';', decimal=',')

# Verificar se a coluna "Selecionado" existe e removê-la
if 'Selecionado' in df.columns:
    df = df.drop(columns=['Selecionado'])

# Salvar o DataFrame atualizado de volta no arquivo CSV
df.to_csv('consumo.csv', index=False, sep=';', decimal=',')
