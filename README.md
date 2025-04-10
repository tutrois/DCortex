# DCortexAugment

Um dashboard para análise de produtos da Amazon, utilizando web scraping e processamento de dados para extrair informações sobre produtos eletrônicos em promoção.

## Estrutura do Projeto

O projeto foi reorganizado seguindo os princípios de Clean Code e SOLID, com suporte para múltiplos agentes:

```
DCortexAugment/
├── src/                    # Código fonte principal
│   ├── api/                # Rotas e endpoints da API
│   ├── config/             # Configurações da aplicação
│   ├── models/             # Modelos de dados
│   ├── services/           # Serviços e lógica de negócios
│   │   └── agents/         # Agentes para processamento de dados
│   │       ├── langflow/    # Implementação de agentes Langflow
│   │       ├── base.py      # Classes base para agentes
│   │       ├── interfaces.py # Interfaces para agentes
│   │       └── registry.py   # Registro e fábrica de agentes
│   ├── static/             # Arquivos estáticos (CSS, JS, imagens)
│   ├── templates/          # Templates HTML
│   └── utils/              # Utilitários e funções auxiliares
├── tests/                  # Testes automatizados
├── .env                    # Variáveis de ambiente
├── main.py                 # Ponto de entrada da aplicação
└── requirements.txt        # Dependências do projeto
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

1. Inicie o Langflow: `uv run langflow run`
2. Em outro terminal, execute a aplicação: `python main.py`
3. Acesse o dashboard em: http://127.0.0.1:5000

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
