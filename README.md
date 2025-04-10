# DCortex Amazon Dashboard

Dashboard para análise de produtos da Amazon, utilizando web scraping e processamento de dados com múltiplos agentes.

## Visão Geral

O DCortex Amazon Dashboard é uma aplicação web que coleta, processa e visualiza dados de produtos da Amazon. A aplicação utiliza uma arquitetura de múltiplos agentes para coletar e processar os dados, permitindo uma análise detalhada dos produtos.

## Funcionalidades

- **Coleta de Dados**: Coleta dados de produtos da Amazon usando web scraping
- **Processamento de Dados**: Processa e analisa os dados coletados
- **Visualização de Dados**: Apresenta os dados em um dashboard interativo
- **Tema Claro/Escuro**: Suporte para alternar entre temas claro e escuro
- **Design Responsivo**: Interface adaptável para diferentes tamanhos de tela

## Estrutura do Projeto

O projeto foi organizado seguindo os princípios de Clean Code e SOLID, com uma arquitetura modular e componentizada:

```
src/
├── api/                # Rotas da API Flask
├── config/             # Configurações da aplicação
├── models/             # Modelos de dados
├── services/           # Serviços e agentes
│   ├── agents/         # Implementação dos agentes
│   └── interfaces/     # Interfaces para os agentes
├── static/             # Arquivos estáticos
│   ├── css/            # Estilos CSS
│   ├── js/             # Scripts JavaScript
│   └── components/     # Componentes estáticos
├── templates/          # Templates HTML
│   └── components/     # Componentes HTML
└── utils/              # Utilitários
```

## Princípios SOLID Aplicados

1. **Single Responsibility Principle (SRP)**
   - Cada classe tem uma única responsabilidade
   - Separação clara entre busca de dados, processamento e apresentação
   - Agentes especializados para cada tipo de tarefa

2. **Open/Closed Principle (OCP)**
   - Classes extensíveis sem modificação
   - Arquitetura de agentes permite adicionar novos tipos sem alterar o código existente

3. **Liskov Substitution Principle (LSP)**
   - Implementações concretas podem substituir interfaces
   - Agentes seguem contratos bem definidos

4. **Interface Segregation Principle (ISP)**
   - Interfaces específicas para necessidades específicas
   - Interfaces separadas para agentes de busca e processamento

5. **Dependency Inversion Principle (DIP)**
   - Módulos de alto nível dependem de abstrações
   - Orquestrador de agentes trabalha com interfaces, não implementações concretas

## Arquitetura de Agentes

O projeto implementa uma arquitetura flexível de agentes que permite:

- **Registro de Agentes**: Agentes podem ser registrados dinamicamente
- **Fábrica de Agentes**: Criação de instâncias de agentes sob demanda
- **Orquestração**: Coordenação da execução de múltiplos agentes
- **Extensão**: Facilidade para adicionar novos tipos de agentes

### Agentes Disponíveis

- **ColetorDadosAmazon**: Agente especializado em coletar e processar dados de produtos da Amazon
  - **ColetorDadosAmazon - Busca**: Responsável por buscar dados brutos da Amazon
  - **ColetorDadosAmazon - Processamento**: Responsável por processar e estruturar os dados obtidos

## Instalação

1. Clone o repositório
   ```bash
   git clone https://github.com/seu-usuario/DCortexAugment.git
   cd DCortexAugment
   ```

2. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

5. Configure as variáveis de ambiente no arquivo `.env`:
   ```
   FLASK_ENV=development
   SECRET_KEY=sua-chave-secreta
   LANGFLOW_API_URL=http://localhost:7860/api/v1/run/
   OPENAI_API_KEY=sua-chave-api-openai
   DEFAULT_SCRAPE_URL=https://www.amazon.com.br/gp/bestsellers/?ref_=nav_cs_bestsellers
   ```

## Configuração do Langflow e do Bot

1. Inicie o Langflow:
   ```bash
   langflow run
   ```
   O Langflow estará disponível em `http://localhost:7860`

2. Importe o fluxo do bot ColetorDadosAmazon:
   - Acesse a interface do Langflow no navegador
   - Clique em "Import"
   - Selecione o arquivo `flows/coletor_dados_amazon.json` do repositório
   - Após importar, clique em "Edit" no fluxo
   - Verifique se todos os componentes estão configurados corretamente
   - Clique em "Build" para construir o fluxo
   - Clique em "Deploy" para implantar o fluxo

3. Copie a URL da API do fluxo implantado:
   - Após implantar, clique em "API Reference"
   - Copie a URL completa da API (algo como `http://localhost:7860/api/v1/run/98bc1dc9-3bb8-4941-ad26-3e26e775c31b`)
   - Atualize a variável `LANGFLOW_API_URL` no arquivo `.env` com esta URL

## Execução

1. Certifique-se de que o Langflow está em execução em um terminal:
   ```bash
   langflow run
   ```

2. Em outro terminal, inicie a aplicação Flask:
   ```bash
   python main.py
   ```

3. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

## Estrutura do Fluxo do Bot

O fluxo do bot ColetorDadosAmazon consiste em:

1. **TextInputComponent**: Recebe a URL da Amazon com o prefixo `https://r.jina.ai/`
2. **WebScraper**: Extrai dados da página da Amazon
3. **PromptTemplate**: Formata os dados para processamento
4. **LLMChain**: Processa os dados usando um modelo de linguagem
5. **OutputParser**: Estrutura a saída em formato JSON

O bot retorna um JSON com os seguintes campos para cada produto:
- `posição`: Posição do produto na lista
- `imagem`: URL da imagem do produto
- `titulo`: Nome do produto
- `preco`: Preço do produto
- `rating`: Avaliação do produto
- `url_produto`: URL do produto

### API Endpoints

- **GET /**: Página principal do dashboard
- **GET /fetch-data**: Busca dados de produtos usando os agentes configurados
  - Parâmetros opcionais:
    - `fetcher`: Tipo de agente de busca a ser usado (ex: `coletor_dados_amazon_fetcher`)
    - `processor`: Tipo de agente de processamento a ser usado (ex: `coletor_dados_amazon_processor`)
    - `source`: URL fonte para busca de dados
- **GET /agents**: Lista os agentes disponíveis no sistema

## Testes

Execute os testes com o comando:

```
pytest
```

## Tecnologias Utilizadas

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap, Chart.js
- **Processamento de dados**: Langflow
- **Padrões de Design**: Factory, Registry, Strategy
- **Testes**: Pytest
