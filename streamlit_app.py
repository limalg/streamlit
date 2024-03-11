import requests
import pandas as pd
import streamlit as st
import plotly.express as px

def retorno_pagina(url):
    # URL desejada
    #url = 'https://www.fundamentus.com.br/resultado.php'
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
        return df
    else:
        st.error(f'Erro ao fazer a solicitação. Código de status: {response.status_code}')

def retorno_setor(papel):
    # URL desejada
    url = f'https://www.fundamentus.com.br/detalhes.php?papel={papel}'
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
        valor = df.iloc[4, 1]
        return valor
    else:
        return 'S/Setor'


def trata_df(colunas,url):
    df = retorno_pagina(url)
    for coluna in colunas:
        df[coluna] = df[coluna].str.replace('.', '').str.replace(',', '').str.replace('%', '')  # Convertendo para float 
        lis_valor_correto = []
        for atributo in df[coluna]:
            aplicar_virgula = str(atributo)
            if len(aplicar_virgula) == 5:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 4:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 3:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 6:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 7:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 8:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}")   
            elif len(aplicar_virgula) == 9:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}")   
            elif len(aplicar_virgula) == 10:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}")                                      
            elif len(aplicar_virgula) == 11:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}")
            elif len(aplicar_virgula) == 12:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 13:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 14:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}")  
            elif len(aplicar_virgula) == 15:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 16:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 17:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 18:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 19:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}")
            elif len(aplicar_virgula) == 20:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}")
            elif len(aplicar_virgula) == 21:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) == 22:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}")
            elif len(aplicar_virgula) == 23:
                lis_valor_correto.append(f"{aplicar_virgula[:len(aplicar_virgula)-2]}.{aplicar_virgula[-2:]}") 
            elif len(aplicar_virgula) <= 2:
                lis_valor_correto.append(f"{0}.{aplicar_virgula[-2:]}")                                                                                                                                                                                     
        df[coluna] = lis_valor_correto
        df[coluna] = df[coluna].astype('float')
    return df

def aplica_filtros_dividendos_acoes():
    df = trata_df(['Cotação','P/L','P/VP', 'Div.Yield','P/Cap.Giro', 'P/EBIT', 'P/Ativ Circ.Liq', 'EV/EBIT', 'EV/EBITDA',
                   'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Liq.2meses','Patrim. Líq', 'Dív.Brut/ Patrim.', 'Cresc. Rec.5a'],
                   'https://www.fundamentus.com.br/resultado.php')
    df = df[(df['P/L'] >= 1) & (df['P/L'] <= 9)]
    df = df[(df['P/VP'] >= -1) & (df['P/VP'] <= 2)]
    df = df[(df['Div.Yield'] >= 8) & (df['Div.Yield'] <= 23)]
    df = df[(df['Mrg. Líq.'] >= 0)]
    df = df[(df['Liq.2meses'] >= 1000000)] 
    df = df[(df['Dív.Brut/ Patrim.'] <= 0.5)]
    lis_setor = []
    for atributo in df['Papel']:
        lis_setor.append(retorno_setor(atributo))
    #print(lis_setor)
    df['Setor'] = lis_setor  
    df = df[['Papel', 'Cotação', 'Div.Yield','Setor']].sort_values(by='Div.Yield', ascending=False)
    df = df.reset_index(drop=True)
    return df

def aplica_filtros_dividendos_fiis(ffo_yield,p_vp1,p_vp2,div_yield1,div_yield2,liquidez):
    df = trata_df([ 'Cotação', 'FFO Yield', 'Dividend Yield', 
                   'Valor de Mercado', 'Preço do m2','Aluguel por m2', 'Cap Rate', 'Vacância Média'],
                   'https://www.fundamentus.com.br/fii_resultado.php')
    df = df.rename(columns={"Dividend Yield": "Div.Yield", "Segmento": "Setor"})
    df['Liquidez'] = df['Liquidez'].str.replace('.', '')
    df['Liquidez'] = pd.to_numeric( df['Liquidez'] )
    df['P/VP'] = df['P/VP']/100
    df = df[(df['FFO Yield'] >= ffo_yield)]
    df = df[(df['P/VP'] >= p_vp1) & (df['P/VP'] <= p_vp2)]
    df = df[(df['Div.Yield'] >= div_yield1) & (df['Div.Yield'] <= div_yield2)]
    df = df[(df['Liquidez'] >= liquidez)] # A função de tratamento está comendo 2 casa decimais apenas para Fiis

    df = df[['Papel', 'Cotação', 'Div.Yield','Setor']].sort_values(by='Div.Yield', ascending=False)
    df = df.reset_index(drop=True)
    return df

def main():
    info_acoes = """
                <strong>P/L (Preço/Lucro):</strong> Deve ser maior ou igual a 1 e menor ou igual a 9.
    <strong>P/VP (Preço/Valor Patrimonial):</strong> Deve ser maior ou igual a -1 e menor ou igual a 2.
    <strong>Dividend Yield:</strong> Deve ser maior ou igual a 8 e menor ou igual a 23.
    <strong>Margem Líquida:</strong> Deve ser maior ou igual a 0.
    <strong>Liquidez Média dos Últimos 2 Meses:</strong> Deve ser maior ou igual a 1.000.000.
    <strong>Dívida Bruta sobre Patrimônio Líquido:</strong> Deve ser menor ou igual a 0,5.
                """
    info_fiis = """
                <strong>FFO Yield:</strong> Deve ser maior ou igual a 10.
                <strong>P/VP (Preço/Valor Patrimonial):</strong> Deve ser maior ou igual a 0 e menor ou igual a 110.
                <strong>Dividend Yield:</strong> Deve ser maior ou igual a 12 e menor ou igual a 23.
                <strong>Liquidez:</strong> Deve ser maior ou igual a 1.000.000.
                """
    
    st.header('Detalhes sobre Ações e Fiis com Analise em Dividendos:', divider='rainbow')
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        # Criar o título
        st.subheader('Ranking Ações')
        with st.expander("Regras para aplicar:"):
            st.write(info_acoes, unsafe_allow_html=True)
        df = aplica_filtros_dividendos_acoes()
        st.write(df)
    with col2:
        # Criar o título
        st.subheader('Ranking FIIS')
        with st.expander("Regras para aplicar:"):
            ffo_yield = st.slider('FFO Yield %', 0.0, 80.0, 10.0)
            p_vp1 = st.slider('P/VP', 0.0, 3.0,(0.0,1.10))
            div_yield = st.slider('Div.Yield %', 0.0, 40.0,(12.0,23.0))
            liquidez = st.slider('Liquidez', 500000, 2000000, 1000000)
            #st.write(info_fiis, unsafe_allow_html=True)
        df = aplica_filtros_dividendos_fiis(ffo_yield,p_vp1[0],p_vp1[1],div_yield[0],div_yield[1],liquidez)
        st.write(df)
    df_acao = aplica_filtros_dividendos_acoes()
    df_fiis = aplica_filtros_dividendos_fiis(ffo_yield,p_vp1[0],p_vp1[1],div_yield[0],div_yield[1],liquidez)
    df_acao_fiss = pd.concat([df_acao, df_fiis], ignore_index=True).sort_values(by='Div.Yield', ascending=False)
    df_acao_fiss = df_acao_fiss.reset_index(drop=True)
    fig = px.bar(df_acao_fiss,y='Papel', x='Div.Yield',color='Setor',title='Papel por Div. Yield')
    col3.plotly_chart(fig,use_container_width=True,)
    #st.write(fig )
  
    
if __name__ == "__main__":
    main()
