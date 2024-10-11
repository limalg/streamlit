import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_stock_data():
    """
    Extrai dados das ações com os maiores Dividend Yield do site Investidor10.
    """
    url = 'https://investidor10.com.br/acoes/rankings/maiores-dividend-yield/'
    response = requests.get(url)
    if response.status_code != 200:
        st.error('Falha ao acessar o site.')
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Encontrar todas as tabelas na página
    tables = soup.find_all('table')
    if not tables:
        st.error('Nenhuma tabela encontrada na página.')
        return None

    # Supondo que a primeira tabela seja a desejada
    table = tables[0]
    
    # Ler a tabela usando pandas
    df = pd.read_html(str(table), decimal=',', thousands='.')[0]
    
    return df

def main():
    st.title('Rankings - Maiores Dividend Yield')
    
    if st.button('Atualizar'):
        with st.spinner('Atualizando dados...'):
            data = fetch_stock_data()
            if data is not None:
                st.success('Dados atualizados com sucesso!')
                st.dataframe(data)
    else:
        data = fetch_stock_data()
        if data is not None:
            st.dataframe(data)

if __name__ == '__main__':
    main()
