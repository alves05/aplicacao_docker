# Previsão de Aluguel - Dockerizado

- **Equipe**:
   - Danilo Pontes;
   - Saulo Bernardo;
   - Wiliams Alves.

## Sobre o projeto

Este projeto tem como objetivo prever o valor do aluguel de um imóvel com base em suas características, utilizando um modelo de regressão. A aplicação é desenvolvida em Python e utiliza o framework Streamlit para criação de uma interface interativa. O foco principal é a conteinerização da aplicação utilizando Docker.

## Tecnologias Utilizadas

- Python
- Streamlit
- Pandas
- Scikit-Learn
- Pickle
- Docker

## Estrutura do Projeto

```

|-- dados/
|   |-- base_alugueis.csv 
|
|-- modelo/
|   |-- modelo_regressao.sav 
|
|-- app.py  
|-- Dockerfile  
|-- compose.yml  
|-- requirements.txt  
|-- README.md
|-- LICENSE  

```

## Instalação e Execução com Docker Compose

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/seu-usuario/previsao-aluguel.git
   cd previsao-aluguel
   ```

2. **Construa e inicie os contêineres:**
   ```bash
   docker compose up --build
   ```

3. **Copie e cole o endereço no navegador ou clique no link IP no Docker Desktop:**
   ```
   http://localhost:8501
   ```

![docker](/imagens/tela-docker-desktop.png)


4. **Para excluir os contêineres:**
   ```bash
   docker compose down
   ```

## Como Usar

1. Utilize os filtros laterais para inserir as características do imóvel desejado.

![filtros](/imagens/filtros-aplicacao.png)

2. Clique no botão **CONSULTAR** para obter a previsão do aluguel.

![resultado](/imagens/resultado-consulta.png)


## Licença

Este projeto está licenciado sob a Licença GNU.

