import streamlit as st
from requests_html import AsyncHTMLSession
import pandas as pd
import asyncio

async def buscar_informacoes_ativo_acao(ticker):
    session = AsyncHTMLSession()
    url = f'https://www.fundamentus.com.br/detalhes.php?papel={ticker}'
    response = await session.get(url)
    await response.html.arender()  # Renderiza a página para garantir que todo o conteúdo seja carregado
    
    informacoes = {}
    html_text = response.html.text
    
    informacoes['Papel'] = ticker
    informacoes['Cotação'] = html_text[html_text.find('?Cotação') + len('?Cotação'):].split()[0]
    informacoes['P/VP'] = html_text[html_text.find('?P/VP') + len('?P/VP'):].split()[0]
    informacoes['LPA'] = html_text[html_text.find('?LPA') + len('?LPA'):].split()[0]
    informacoes['ROE'] = html_text[html_text.find('?ROE') + len('?ROE'):].split()[0]
    informacoes['Dividend Yield'] = html_text[html_text.find('?Div. Yield') + len('?Div. Yield'):].split()[0]
    informacoes['Setor'] = html_text[html_text.find('?Subsetor') + len('?Subsetor'):].split()[0]
    
    return informacoes

async def buscar_informacoes_ativo_fii(ticker):
    session = AsyncHTMLSession()
    url = f'https://www.fundamentus.com.br/detalhes.php?papel={ticker}'
    response = await session.get(url)
    await response.html.arender()  # Renderiza a página para garantir que todo o conteúdo seja carregado
    
    informacoes = {}
    html_text = response.html.text
    
    informacoes['Papel'] = ticker
    informacoes['Cotação'] = html_text[html_text.find('?Cotação') + len('?Cotação'):].split()[0]
    informacoes['P/VP'] = html_text[html_text.find('?P/VP') + len('?P/VP'):].split()[0]
    informacoes['LPA'] = html_text[html_text.find('?LPA') + len('?LPA'):].split()[0]
    informacoes['ROE'] = html_text[html_text.find('?ROE') + len('?ROE'):].split()[0]
    informacoes['Dividend Yield'] = html_text[html_text.find('?Div. Yield') + len('?Div. Yield'):].split()[0]
    informacoes['Setor'] = html_text[html_text.find('?Segmento') + len('?Segmento'):].split()[0]
    
    return informacoes    

# Função principal do Streamlit
def main():
    st.title('Informações de Ações e FIIs Brasileiros')

    # Lista de ações brasileiras
    acoes_brasileiras = ['GOAU4', 'ITUB4', 'KLBN3', 'VAMO3', 'TAEE11']

    # Lista de FIIs brasileiros
    fiis_brasileiros = ['XPML11', 'RBRF11', 'MXRF11', 'VGHF11', 'JPPA11']

    # Lista para armazenar as informações de cada ação
    lista_informacoes = []

    # Buscar informações para ações brasileiras
    for ticker_acao in acoes_brasileiras:
        informacoes_acao = asyncio.run(buscar_informacoes_ativo_acao(ticker_acao))
        if informacoes_acao:
            lista_informacoes.append(informacoes_acao)

    # Buscar informações para FIIs brasileiros
    for ticker_fii in fiis_brasileiros:
        informacoes_fii = asyncio.run(buscar_informacoes_ativo_fii(ticker_fii))
        if informacoes_fii:
            lista_informacoes.append(informacoes_fii)        

    # Criar DataFrame a partir da lista
    df_resultado = pd.DataFrame(lista_informacoes)

    # Exibir DataFrame resultante
    st.write(df_resultado)

if __name__ == '__main__':
    main()
