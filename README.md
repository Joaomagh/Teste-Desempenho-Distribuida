# Teste de Desempenho - Aplicação Link Extractor

Este repositório contém os scripts e resultados dos testes de desempenho realizados na aplicação "Link Extractor", como parte do Trabalho 4.

O objetivo é comparar o desempenho de duas implementações de API (Python e Ruby), com e sem o uso de cache (Redis), sob diferentes níveis de carga.

## Status Atual do Projeto

Até o momento, as seguintes etapas foram concluídas:

1.  **Ambiente Configurado**: A aplicação `linkextractor` foi configurada e está rodando em contêineres Docker, orquestrados com `docker-compose`. O ambiente inclui:
    *   Servidor Web (PHP)
    *   Servidor de API (inicialmente com a versão Ruby)
    *   Servidor de Cache (Redis)

2.  **Script de Teste Criado**: Um script `locustfile.py` foi desenvolvido para simular o comportamento do usuário. Cada usuário virtual executa uma sequência de 10 requisições `POST` para a API, extraindo links de 10 URLs diferentes.

3.  **Primeira Bateria de Testes Executada**: Os testes para a **API em Ruby com cache ativado** foram concluídos. Os seguintes cenários de carga foram executados:
    *   1 Usuário Virtual
    *   10 Usuários Virtuais
    *   50 Usuários Virtuais
    *   100 Usuários Virtuais

4.  **Resultados Coletados**: Os resultados brutos para cada um dos testes acima foram salvos em formato `.csv` no diretório `/results`.

5.  **Controle de Versão**: O projeto foi versionado com Git e enviado para este repositório no GitHub.

## Como Executar o Projeto

Siga os passos abaixo para replicar o ambiente e executar os testes.

### Pré-requisitos

*   Git
*   Docker e Docker Compose
*   Python 3.x e Pip

### 1. Clonar o Repositório

```bash
git clone https://github.com/Joaomagh/Teste-de-Desempenho-Distribuida.git
cd Teste-de-Desempenho-Distribuida
```

### 2. Instalar Dependências

Instale o Locust, que é a ferramenta de teste utilizada.

```bash
pip install locust
```

### 3. Iniciar o Ambiente da Aplicação

Os serviços da aplicação rodam em contêineres Docker.

```bash
# Navegue até o diretório que contém o docker-compose
cd linkextractor/step6

# Construa e inicie os contêineres em segundo plano
docker-compose up -d --build
```

Para verificar se os três serviços (`api`, `web`, `redis`) estão rodando, use o comando `docker-compose ps`.

### 4. Executar os Testes de Desempenho

Volte para o diretório raiz do projeto e execute o Locust.

```bash
# Voltar para a raiz
cd ../..

# Exemplo de comando para executar o teste
locust -f locustfile.py --host http://localhost:4567 --users 1 --spawn-rate 1 --run-time 1m --headless --csv results/exemplo_teste
```

**Parâmetros do comando:**

*   `--host`: A URL da API que será testada.
*   `--users`: O número de usuários virtuais a serem simulados.
*   `--spawn-rate`: A taxa de novos usuários iniciados por segundo.
*   `--run-time`: A duração total do teste (ex: `1m` para 1 minuto).
*   `--headless`: Executa o teste sem a interface web do Locust.
*   `--csv`: Salva os resultados em arquivos CSV com o prefixo especificado.

## Próximos Passos (O Que Falta Fazer)

A lista abaixo detalha as etapas restantes para a conclusão do trabalho.

1.  **Executar Testes com API Ruby (Cache Desativado)**
    *   Parar o contêiner do Redis: `docker-compose -f linkextractor/step6/docker-compose.yml stop redis`.
    *   Executar os testes com 1, 10, 50 e 100 usuários.
    *   Reiniciar o Redis ao final: `docker-compose -f linkextractor/step6/docker-compose.yml start redis`.

2.  **Executar Testes com API Python (com e sem cache)**
    *   Alterar o arquivo `linkextractor/step6/docker-compose.yml` para usar a imagem da API Python (ex: `image: linkextractor-api:step6-python`).
    *   Reconstruir o ambiente com `docker-compose up -d --build`.
    *   Repetir a execução dos testes com 1, 10, 50 e 100 usuários, primeiro com o Redis ligado e depois com ele desligado.

3.  **Consolidar e Analisar os Resultados**
    *   Reunir os dados de todos os 16 arquivos `.csv`.
    *   Organizar os dados em uma única planilha (Excel, Google Sheets, etc.).
    *   Calcular métricas importantes como tempo de resposta médio, mediana, p95, e taxa de falhas.

4.  **Elaborar o Relatório Final**
    *   Criar gráficos comparativos para visualizar o impacto da linguagem (Ruby vs. Python) e do cache.
    *   Escrever as conclusões com base nos dados coletados, explicando os resultados observados.
