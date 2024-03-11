import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from io import StringIO

def retorno_pagina(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_string = response.text
        df = pd.read_html(StringIO(html_string), decimal=',')[0]
        return df
    else:
        st.error(f'Erro ao fazer a solicitação. Código de status: {response.status_code}')


def trata_df(colunas, url):
    df = retorno_pagina(url)
    for coluna in colunas:
        df[coluna] = df[coluna].str.replace(r'[.,%]', '', regex=True)
        df[coluna] = pd.to_numeric(df[coluna])
        df[coluna] = df[coluna] / 100 if coluna not in ['Liq.2meses', 'Patrim. Líq','Liquidez'] else df[coluna]

    return df

def aplica_filtros_dividendos_acoes(pl_range, pvp_range, div_yield_range, margem_liq_min, liq_min, div_brut_patrim_max):
    df = trata_df(['Cotação','P/L','P/VP', 'Div.Yield','P/Cap.Giro', 'P/EBIT', 'P/Ativ Circ.Liq', 'EV/EBIT', 'EV/EBITDA',
                   'Mrg Ebit', 'Mrg. Líq.', 'ROIC', 'ROE', 'Patrim. Líq', 'Dív.Brut/ Patrim.', 'Cresc. Rec.5a'],
                   'https://www.fundamentus.com.br/resultado.php')
    df['Liq.2meses'] = df['Liq.2meses'].str.replace(r'[.,%]', '', regex=True).astype('Int64')
    df['Liq.2meses'] = df['Liq.2meses']/100
    df = df[(df['P/L'].between(pl_range[0], pl_range[1])) & 
            (df['P/VP'].between(pvp_range[0], pvp_range[1])) & 
            (df['Div.Yield'].between(div_yield_range[0], div_yield_range[1])) & 
            (df['Mrg. Líq.'] >= margem_liq_min) & 
            (df['Liq.2meses'] >= liq_min) & 
            (df['Dív.Brut/ Patrim.'] <= div_brut_patrim_max)]
    df['Setor'] = df['Papel'].apply(retorno_setor)
    return df


def aplica_filtros_dividendos_fiis(ffo_yield, p_vp1, p_vp2, div_yield1, div_yield2, liquidez):
    df = trata_df(['Cotação', 'FFO Yield', 'Dividend Yield', 'Liquidez',
                   'Valor de Mercado', 'Preço do m2','Aluguel por m2', 'Cap Rate', 'Vacância Média'],
                   'https://www.fundamentus.com.br/fii_resultado.php')
    df = df.rename(columns={"Dividend Yield": "Div.Yield", "Segmento": "Setor"})
    df['P/VP'] = df['P/VP'] / 100
    df = df[(df['FFO Yield'] >= ffo_yield) & 
            (df['P/VP'].between(p_vp1, p_vp2)) & 
            (df['Div.Yield'].between(div_yield1, div_yield2)) & 
            (df['Liquidez'] >= liquidez)]
    return df

def retorno_setor(papel):
    url = f'https://www.fundamentus.com.br/detalhes.php?papel={papel}'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        df = pd.read_html(StringIO(response.text), decimal=',')[0]
        valor = df.iloc[4, 1]
        return valor
    else:
        return 'S/Setor'

def main():
    st.sidebar.header('Filtros para Ações e FIIs:', divider='rainbow')
    st.header('Oportunidades com foco em Dividendos:', divider='rainbow')
    # Sliders para ações
    with st.sidebar.expander("Regras para aplicar em Ações:"):
        pl_range = st.slider('Faixa de P/L', 0.0, 20.0, (1.0, 9.0))
        pvp_range = st.slider('Faixa de P/VP', -2.0, 4.0, (-1.0, 2.0))
        div_yield_range = st.slider('Faixa de Dividend Yield', 5.0, 35.0, (8.0, 23.0))
        margem_liq_min = st.slider('Margem Líquida Mínima', 0, 100, 0)
        liq_min = st.slider('Liquidez Mínima', 500000, 5000000, 1000000)
        div_brut_patrim_max = st.slider('Dívida Bruta/Patrimônio Máxima', 0.0, 1.5, 0.5)
    # Sliders para FIIs
    with st.sidebar.expander("Regras para aplicar em FIIs:"):
        ffo_yield = st.slider('Faixa de FFO Yield %', 0.0, 80.0, 10.0)
        p_vp1, p_vp2 = st.slider('Faixa de P/VP', 0.0, 3.0, (0.0, 1.10))
        div_yield1, div_yield2 = st.slider('Faixa de Dividend Yield', 0.0, 40.0, (12.0, 23.0))
        liquidez = st.slider('Liquidez Mínima', 500000, 2000000, 1000000)

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    with col1:
        st.subheader('Ranking Ações')
        df = aplica_filtros_dividendos_acoes(pl_range, pvp_range, div_yield_range, margem_liq_min, liq_min, div_brut_patrim_max)
        df = df[['Papel', 'Cotação', 'Div.Yield','Setor']].sort_values(by='Div.Yield', ascending=False).reset_index(drop=True)
        st.write(df)

    with col2:
        st.subheader('Ranking FIIs')
        df = aplica_filtros_dividendos_fiis(ffo_yield, p_vp1, p_vp2, div_yield1, div_yield2, liquidez)
        df = df[['Papel', 'Cotação', 'Div.Yield','Setor']].sort_values(by='Div.Yield', ascending=False).reset_index(drop=True)
        st.write(df)

    df_acao = aplica_filtros_dividendos_acoes(pl_range, pvp_range, div_yield_range, margem_liq_min, liq_min, div_brut_patrim_max)
    df_fiis = aplica_filtros_dividendos_fiis(ffo_yield, p_vp1, p_vp2, div_yield1, div_yield2, liquidez)
    df_acao_fiis = pd.concat([df_acao, df_fiis], ignore_index=True).sort_values(by='Div.Yield', ascending=False).reset_index(drop=True)

    with col3:
        fig_yield = px.bar(df_acao_fiis, y='Papel', x='Div.Yield', color='Setor', title='Papel por Div. Yield')
        col3.plotly_chart(fig_yield, use_container_width=True)

    with col4:
        fig_yield = px.pie(df_acao_fiis, values='Div.Yield', names='Setor', color='Setor', title='Setor por Div. Yield')
        col4.plotly_chart(fig_yield, use_container_width=True)  

    st.write('Detalhes gerais:')
    st.write(df_acao_fiis)
    
if __name__ == "__main__":
    main()
