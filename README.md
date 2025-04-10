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
2. Crie um ambiente virtual: `python -m venv venv`
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Instale as dependências: `pip install -r requirements.txt`
5. Configure as variáveis de ambiente no arquivo `.env`

## Execução

1. Inicie o Langflow (necessário para o processamento de dados):
   ```
   uv run langflow run
   ```

2. Em outro terminal, inicie a aplicação Flask:
   ```
   python main.py
   ```

3. Acesse a aplicação em seu navegador:
   ```
   http://localhost:5000
   ```

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
