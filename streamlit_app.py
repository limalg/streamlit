import requests
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# URL desejada
url = 'https://www.fundamentus.com.br/resultado.php'

# Definindo cabeçalhos
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}

# Fazendo a solicitação GET com cabeçalhos
response = requests.get(url, headers=headers)

# Verificando se a solicitação foi bem-sucedida
if response.status_code == 200:
    # Ler diretamente o HTML usando o Pandas
    df = pd.read_html(response.text)[0]

    # Criar o título
    st.title('Detalhes sobre ações')

    # Vamos criar uma lista com todos os papeis disponíveis
    papeis_disponiveis = sorted(df['Papel'].unique())

    # Criar um multiselect no Streamlit
    papeis_selecionados = st.multiselect('Selecione os papeis:', papeis_disponiveis)

    # Filtrar o DataFrame com base nos papeis selecionados
    df_filtrado = df[df['Papel'].isin(papeis_selecionados)]

    # Exibir o DataFrame filtrado
    st.write('DataFrame filtrado:', df_filtrado)

    # Criar um gráfico com os dados do DataFrame filtrado
    plt.figure(figsize=(10, 6))
    for papel in papeis_selecionados:
        dados_papel = df_filtrado[df_filtrado['Papel'] == papel]
        plt.plot(dados_papel['Papel'], dados_papel['Div.Yield'], marker='o', label=papel)

    plt.xlabel('Papel')
    plt.ylabel('Div. Yield')
    plt.title('Dividend Yield por Papel')
    plt.xticks(rotation=45)
    plt.legend()
    st.pyplot(plt)

else:
    st.error(f'Erro ao fazer a solicitação. Código de status: {response.status_code}')

if __name__ == '__main__':
    main()
