# %%
import pandas as pd
import streamlit as st
import joblib

# Define o título da página
st.set_page_config(page_title="Previsão de Preço de Imóveis")
st.title("Previsão de Preço de Imóveis Airbnb")
st.markdown(
    "Utilize este formulário para estimar o preço de um imóvel com base em suas características.")


@st.cache_resource  # Cache o modelo para que seja carregado apenas uma vez
def load_model():
    return joblib.load('modelo.joblib')


@st.cache_data  # Cache o dataframe para que seja carregado apenas uma vez
def load_data():
    return pd.read_csv('dados.csv')


modelo = load_model()
dados = load_data()

# Dicionário com nomes mais amigáveis para exibição
labels = {
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'accommodates': 'Capacidade de hóspedes',
    'bathrooms': 'Número de banheiros',
    'bedrooms': 'Número de quartos',
    'beds': 'Número de camas',
    'extra_people': 'Pessoa extras adicional',
    'minimum_nights': 'Noites mínimas',
    'ano': 'Ano do anúncio',
    'mes': 'Mês do anúncio',
    'n_amenities': 'Quantidade de comodidades',
    'host_listings_count': 'Total de anúncios do anfitrião',
    'host_is_superhost': 'Anfitrião é Superhost?',
    'instant_bookable': 'Reserva instantânea?',
    'property_type': 'Tipo de propriedade',
    'room_type': 'Tipo de quarto',
    'cancellation_policy': 'Política de cancelamento'
}

# Dicionários originais
x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']
            }


dicionario = {}

for item in x_listas:  # para cada chave do dicionario ele cria uma nova chave com _ e o valor
    for valor in x_listas[item]:
        dicionario[f'{item}_{valor}'] = 0


# Seção de entradas numéricas
st.header("Características numéricas do imóvel")
for item in x_numericos:
    # Usa .get() para segurança, caso a chave não esteja em labels
    display_label = labels.get(item, item.replace('_', ' ').title())
    if item == 'latitude' or item == 'longitude':
        valor = st.number_input(
            display_label, step=0.00001, value=0.0, format="%.5f")
    elif item == 'extra_people':
        valor = st.number_input(display_label, step=0.01, value=0.0)
    else:
        valor = st.number_input(display_label, step=1, value=0)
    x_numericos[item] = valor

# Seção de campos booleanos
st.header("Informações sobre reserva")
for item in x_tf:
    # Use labels.get(item, item) aqui
    display_label = labels.get(item, item)
    # Use display_label aqui
    valor = st.selectbox(display_label, ('Sim', 'Não'))
    if valor == 'Sim':
        x_tf[item] = 1
    else:
        x_tf[item] = 0

# Seção de categorias
st.header("Informações categóricas do anúncio")
for item in x_listas:
    # Use labels.get(item, item) aqui
    display_label = labels.get(item, item)
    # Use display_label aqui
    valor = st.selectbox(display_label, x_listas[item])
    dicionario[f'{item}_{valor}'] = 1

botao = st.button('Prever Valor do Imovél')

if botao:
    dicionario.update(x_numericos)
    dicionario.update(x_tf)
    valores_x = pd.DataFrame(dicionario, index=[0])
    dados = pd.read_csv('dados.csv')
    colunas = list(dados.columns)[1:-1]
    # valor x vai ser o antigo valores de X mas na ordem colunas que foi obitido do dados.csv
    valores_x = valores_x[colunas]
    preco = modelo.predict(valores_x)
    st.success(f'O valor estimado do imóvel é: R$ {preco[0]:,.2f}')
