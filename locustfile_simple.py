from locust import HttpUser, task, between

class LinkExtractorUser(HttpUser):
    wait_time = between(1, 2)

    test_urls = [
        "http://google.com",
        "http://github.com", 
        "http://wikipedia.org",
        "http://microsoft.com",
        "http://amazon.com"
    ]

    @task
    def extract_links(self):
        for url in self.test_urls:
            # API Ruby do step6 espera GET /api/URL
            response = self.client.get(f"/api/{url}", name="/api/[url]")