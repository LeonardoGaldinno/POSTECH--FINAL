## Descrição do Projeto

Este projeto tem como objetivo de explorar e analisar dados educacionais de crianças e jovens atendidos pela Passos Mágicos, gerando insights relevantes para apoiar suas ações estratégicas e ampliar o impacto social da organização. A aplicação permite acessar um relatório com insights e um dashboard interativo e proporciona aos usuários a oportunidade de utilizar um modelo de machine learning para prever as suas futuras pedras (classificações).

## Estrutura do Repositório

A estrutura do repositório é organizada da seguinte forma:

- **app.py**: Arquivo principal que inicia a aplicação Streamlit.
- **model.pkl**: Arquivo que contém o modelo treinado utilizado pela aplicação.
- **requirements.txt**: Lista de dependências necessárias para executar o projeto.
- **client/**: Diretório que contém a conexão com o banco de dados utilizado.
- **img/**: Diretório que armazena imagens utilizadas na aplicação ou no README.
- **pages/**: Diretório que contém páginas adicionais da aplicação.
- **.streamlit/**: Configurações específicas do Streamlit, como o arquivo `config.toml`.

## Instalação

Para configurar o ambiente e executar a aplicação localmente, siga os passos abaixo:

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/rborgesc/POSTECH--FINAL.git
   cd POSTECH--FINAL
   ```

2. **Crie um ambiente virtual** (recomendado):

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows, use venv\Scripts\activate
   ```

3. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Após a instalação das dependências, inicie a aplicação com o seguinte comando:

```bash
streamlit run app.py
```

A aplicação estará disponível no seu navegador padrão, geralmente acessível em `http://localhost:8501`.

Ou acesse via streamlit cloud em `https://datathon-phase5.streamlit.app/`.


