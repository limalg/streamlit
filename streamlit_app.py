import streamlit as st
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import hashlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta


# Inicializar o aplicativo Firebase somente se ainda não estiver inicializado
if len(firebase_admin._apps) == 0:
    cred = credentials.Certificate('client.json')
    firebase_admin.initialize_app(cred , {
        'databaseURL': 'https://casa-9085b-default-rtdb.firebaseio.com/'
    })

categorias = [
    ' ',
    'Alimentação',
    'Itens Comuns',
    'Viagem',
    'Compras Parceladas',
    'Fim de Semana',
    'Luz',
    'Condominio',
    'Gas',
    'Aluguel',
    'Investimento Foz',
    'Mercado',
    'Internet',
    'Transporte',
    'Seguro contra incêndio',
    'Pet',
    'Facily',
    'Faxina'
]

# Função para gerar o hash da senha
def generate_password_hash(password):
    password = str(password)
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    hashed_password = hash_object.hexdigest()
    return hashed_password

# Função para verificar o hash da senha
def verify_password(password, hashed_password):
    password = str(password)
    hash_object = hashlib.sha256()
    hash_object.update(password.encode())
    new_hashed_password = hash_object.hexdigest()
    return hashed_password == new_hashed_password

# Função para autenticar o usuário
@st.cache_resource
def authenticate_user(email, password):
    ref = db.reference('/users')
    users = ref.get()
    if not users:
        return None
    email = email.strip().lower()
    email = email.split("@")[0]
    for user_id, user_data in users.items():
        email_input = user_data['email'].strip().lower()
        email_input = email_input.split("@")[0]
        if email_input == email:
            hashed_password = user_data.get('password')
            if verify_password(password, hashed_password):
                return {
                    'id': user_id,
                    'email': email,
                    'admin': user_data.get('admin')
                }
            else:
                st.error('Credenciais inválidas.')

    return None



def pagina_login():
    if 'email' not in st.session_state:
        st.header('Faça login')
        email = st.text_input('E-mail', key='login_email')
        password = st.text_input('Senha', type='password', key='login_password')
        if st.button('Entrar'):
            # Verificar se as credenciais são válidas
            user = authenticate_user(email, password)
            st.session_state['login_successful'] = False
            if user:
                st.session_state.update(user)
                st.session_state['login_successful'] = True
                st.experimental_rerun()
            else:
                st.error('Credenciais inválidas.')
                return None


# Função da tela de lançamento de registro
def create():
    with st.form(key='create_form'):
        #categorias = []  # Defina as categorias aqui
        usuario = st.text_input('Usuário')
        pagamento = st.text_input('Pagamento')
        data = st.date_input('Data')
        descricao = st.text_input('Descrição')
        categoria = st.selectbox('Categoria',options=categorias )
        valor = st.number_input('Valor')
        parcela = st.number_input('Parcela', min_value=1, value=1)
        tipo_despesa = st.text_input('Tipo de Despesa')

        submitted = st.form_submit_button('Criar Registro')

        if submitted:
            if int(parcela) > 1:
                data = datetime.strptime(str(data), '%Y-%m-%d')
                parcelas = int(parcela) + 1
                for num in range(1, parcelas):
                    nova_data = data + relativedelta(months=num)
                    nova_data = nova_data.strftime('%Y-%m-%d')
                    despesa = {
                        'data': nova_data,
                        'descricao': descricao,
                        'categoria': categoria,
                        'valor': valor,
                        'parcela': num,
                        'usuario': usuario,
                        'pagamento': pagamento,
                        'id': True,
                        'tipo_despesa': tipo_despesa
                    }
                    #response = db.child("despesa").push(despesa)
                    db.child("despesa").push(despesa)
            else:
                despesa = {
                    'data': str(data),
                    'descricao': descricao,
                    'categoria': categoria,
                    'valor': valor,
                    'parcela': parcela,
                    'usuario': usuario,
                    'pagamento': pagamento,
                    'id': True,
                    'tipo_despesa': tipo_despesa
                }
                #response = db.child("despesa").push(despesa)
                #st.write(despesa)
                print(despesa)
                db.child("despesa").push(despesa)

            st.success('Registro criado com sucesso.')

# Função para exibir a tela do dashboard com gráficos
@st.cache_data
def exibir_dashboard():
    st.header('Dashboard')
    
    # Exibir gráficos fictícios para o exemplo
    # Gráfico 1 - Pizza
    data = {'Categoria': ['Alimentação', 'Transporte', 'Moradia'],
            'Valor': [500, 300, 700]}
    df = pd.DataFrame(data)
    fig1, ax1 = plt.subplots()
    ax1.pie(df['Valor'], labels=df['Categoria'], autopct='%1.1f%%')
    ax1.axis('equal')
    st.subheader('Gráfico de Pizza')
    st.pyplot(fig1)

    # Gráfico 2 - Barras
    data = {'Mês': ['Jan', 'Fev', 'Mar', 'Abr', 'Mai'],
            'Gastos': [4000, 4500, 5500, 3000, 5000]}
    df = pd.DataFrame(data)
    fig2, ax2 = plt.subplots()
    ax2.bar(df['Mês'], df['Gastos'])
    ax2.set_xlabel('Mês')
    ax2.set_ylabel('Gastos')
    ax2.set_title('Gráfico de Barras')
    st.subheader('Gráfico de Barras')
    st.pyplot(fig2)

    # Gráfico 3 - Linha
    data = {'Dia': ['01', '02', '03', '04', '05'],
            'Valor': [100, 200, 300, 400, 500]}
    df = pd.DataFrame(data)
    fig3, ax3 = plt.subplots()
    ax3.plot(df['Dia'], df['Valor'])
    ax3.set_xlabel('Dia')
    ax3.set_ylabel('Valor')
    ax3.set_title('Gráfico de Linha')
    st.subheader('Gráfico de Linha')
    st.pyplot(fig3)

    # Gráfico 4 - Scatter
    data = {'X': np.random.randn(100),
            'Y': np.random.randn(100)}
    df = pd.DataFrame(data)
    fig4, ax4 = plt.subplots()
    ax4.scatter(df['X'], df['Y'])
    ax4.set_xlabel('X')
    ax4.set_ylabel('Y')
    ax4.set_title('Gráfico de Scatter')
    st.subheader('Gráfico de Scatter')
    st.pyplot(fig4)


def sidebar():
    if 'login_successful' in st.session_state and st.session_state['login_successful']:
        st.header('Despesa Familiar')
        if st.sidebar.button('Home'):
            st.write('Home')
        if st.sidebar.button('Lançar Registro'):
            create()
        if st.sidebar.button('Listar Registros'):
            st.write('Listar Registros')
        if st.sidebar.button('Dashboard'):
            exibir_dashboard()
        if st.sidebar.button('Sair'):
            st.session_state.clear()  # Limpar a sessão
            st.experimental_rerun()

def main():
    st.set_page_config(page_title="D_F", page_icon="🧊", layout="centered", initial_sidebar_state='expanded') #collapsed wide centered
    with open ('styles.css') as f:
        st.markdown(f"<style> {f.read()} </style>",unsafe_allow_html=True)

    if 'login_successful' in st.session_state and st.session_state['login_successful']:
        sidebar()
    else:
        pagina_login()    

if __name__ == '__main__':
    main()
