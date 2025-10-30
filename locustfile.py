from locust import HttpUser, task, between

class LinkExtractorUser(HttpUser):
    """
    Classe de usuário que simula o comportamento de um cliente
    fazendo requisições para a API Link Extractor.
    """
    # Define um tempo de espera aleatório entre 1 e 2 segundos
    # após a conclusão de cada sequência de tarefas.
    wait_time = between(1, 2)

    # Lista de 10 URLs que serão usadas para os testes de extração.
    # Conforme solicitado no plano do projeto.
    test_urls = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.wikipedia.org",
        "https://www.microsoft.com",
        "https://www.amazon.com",
        "https://www.apple.com",
        "https://www.docker.com",
        "https://www.python.org",
        "https://www.ruby-lang.org",
        "https://locust.io"
    ]

    @task
    def extract_links_sequence(self):
        """
        Esta é a tarefa principal do usuário virtual.
        Ela simula um usuário fazendo uma sequência de 10 chamadas para a API,
        uma para cada URL na lista `test_urls`.
        Isso corresponde ao cenário de teste principal.
        """
        for url_to_test in self.test_urls:
            # O endpoint da API é GET /api/<url> (tanto Python quanto Ruby)
            self.client.get(f"/api/{url_to_test}", name="/api/[url]")

    def on_start(self):
        """
        Método executado quando um usuário virtual é iniciado.
        Pode ser usado para login ou outras tarefas de setup.
        Neste caso, não é necessário, mas é um bom lugar para futuras inicializações.
        """
        pass

# Para executar este teste, use o comando no terminal:
# Para API Python (step5): locust -f locustfile.py --host http://localhost:5000
# Para API Ruby (step6): locust -f locustfile.py --host http://localhost:4567
#
# Onde:
# -f locustfile.py: Especifica o arquivo de teste.
# --host: Define o alvo do teste (porta varia conforme o step)
