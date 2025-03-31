import pickle

import pandas as pd
import streamlit as st
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


def base_dados():
    """Carrega a base de dados de alugueis."""
    dados = pd.read_csv('./dados/base_alugueis.csv')
    return dados


def modelo_regressao():
    """Carrega o modelo de regressão linear."""
    modelo = pickle.load(open('./modelo/modelo_regressao.sav', 'rb'))
    return modelo


def pre_processamento(
    cidade,
    area,
    quartos,
    banheiros,
    vagas,
    andar,
    animais,
    mobilia,
    codominio,
    iptu,
    seguro,
):
    """Pré processamento dos dados para aplicação do regressor."""

    # Nova linha
    nova_linha = {
        'cidade': cidade,
        'area': area,
        'quartos': quartos,
        'banheiros': banheiros,
        'vagas': vagas,
        'andar': andar,
        'animais': animais,
        'mobilia': mobilia,
        'condominio': codominio,
        'iptu': iptu,
        'seguro': seguro,
    }
    nova_linha = pd.DataFrame(nova_linha, index=[0])
    dados = base_dados()
    dados = dados.drop(['aluguel', 'total'], axis=True)
    dados = pd.concat([dados, nova_linha], ignore_index=True)

    # Definindo variáveis com features numéricas e categóricas
    variavel_num = [
        'area',
        'quartos',
        'banheiros',
        'vagas',
        'andar',
        'animais',
        'mobilia',
        'condominio',
        'iptu',
        'seguro',
    ]
    variavel_cat = ['cidade']

    # Definido transformações com estimador final
    num_transformer = Pipeline(steps=[('scaler', StandardScaler())])
    cat_transformer = Pipeline(steps=[('onehot', OneHotEncoder())])

    # Criando o pré-processador
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', num_transformer, variavel_num),
            ('cat', cat_transformer, variavel_cat),
        ]
    )

    # Aplicando o pré-processamento
    processed = preprocessor.fit_transform(dados)
    return processed


def regressor(dados):
    """Aplicando o modelo de regressao linear."""
    modelo = modelo_regressao()
    return modelo.predict(dados)[len(dados) - 1]


def main():
    st.set_page_config(page_title='Preço de Aluguel', page_icon='🏘')
    st.markdown(
        "<h3 style='text-align:center; font-family:Verdana'>Consulta de Preço de Aluguel</h3>",
        unsafe_allow_html=True,
    )
    st.sidebar.title("Seleção de Características do Imóvel:")


    # Filtros
    cidade = st.sidebar.selectbox(
        'Selecione a Cidade:',
        [
            'Belo Horizonte',
            'Campinas',
            'Porto Alegre',
            'Rio de Janeiro',
            'São Paulo',
        ],
    )
    area = st.sidebar.slider('Área do Imóvel m²:', 11, 500, 11)
    quartos = st.sidebar.slider('Quantidade de Quartos:', 1, 5, 2)
    banheiros = st.sidebar.slider('Quantidade de Banheiros:', 1, 6, 2)
    vagas = st.sidebar.slider('Vagas de Estacionamento:', 0, 4, 1)
    andar = st.sidebar.slider('Andar:', 0, 20, 1)
    coluna1, colona2 = st.sidebar.columns(2)
    animais_filtro = coluna1.radio('Aceita animais?', ['Sim', 'Não'], index=1)
    mobilia_filtro = colona2.radio('é Mobiliado?', ['Sim', 'Não'], index=1)
    condominio = st.sidebar.slider('Valor do Condomínio:', 0, 2800, 530)
    iptu = st.sidebar.slider('Valor do IPTU:', 0, 876, 94)
    seguro = st.sidebar.slider('Valor do Seguro Contra Incendio:', 3, 136, 30)

    animais = 0
    if animais_filtro == 'Sim':
        animais = 1

    mobilia = 0
    if mobilia_filtro == 'Sim':
        mobilia = 1

    if st.sidebar.button('CONSULTAR'):
        processed = pre_processamento(
            cidade,
            area,
            quartos,
            banheiros,
            vagas,
            andar,
            animais,
            mobilia,
            condominio,
            iptu,
            seguro,
        )
        previsao = round(regressor(processed), 2)
        aluguel = f'R$ {previsao:.2f}'
        texto = f'Com base nas informações selecionadas, o valor do aluguel previsto para cidade de {cidade}:'
        st.markdown(texto)
        cl1, cl2, cl3 = st.columns(3)
        cl2.header(aluguel)

        fixa = {
            'Parâmetros': [
                'Cidade', 'Área m²', 'Quantidade de Quartos', 'Quantidade de Banheiros',
                'Quantidade de Vagas', 'Andar', 'Aceita Animais', 'Mobilia',
                'Valor do Condomínio', 'Valor do IPTU', 'Valor do Seguro Incendio'
            ],
            'Valores': [
                cidade, f'{float(area):.2f}', quartos, banheiros, vagas, andar,
                animais_filtro, mobilia_filtro, f'{float(condominio):.2f}', 
                f'{(iptu):.2f}', f'{(seguro):.2f}'
            ]
        }
        df = pd.DataFrame(fixa)
        c1, c2, c3 = st.columns([0.1, 2.3, 0.1])
        c2.write('Configuração do Imóvel:')
        c2.dataframe(df, width=600, height=422)
        st.header('', divider='red')


if __name__ == '__main__':
    main()
