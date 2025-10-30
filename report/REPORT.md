# Relatório de Performance - Link Extractor

Este relatório foi gerado automaticamente a partir dos resultados de execução do Locust (CSV).\n
## Resumo por cenário

|   total_reqs |   total_fails | avg_ms   | min_ms   | max_ms   | median_ms   | reqs_per_sec   | scenario            |   failure_rate |
|-------------:|--------------:|:---------|:---------|:---------|:------------|:---------------|:--------------------|---------------:|
|            0 |             0 |          |          |          |             |                | python_cache_10vu   |              0 |
|            0 |             0 |          |          |          |             |                | python_cache_1vu    |              0 |
|            0 |             0 |          |          |          |             |                | python_cache_50vu   |              0 |
|            0 |             0 |          |          |          |             |                | python_nocache_10vu |              0 |
|            0 |             0 |          |          |          |             |                | python_nocache_1vu  |              0 |
|            0 |             0 |          |          |          |             |                | python_nocache_50vu |              0 |
|            0 |             0 |          |          |          |             |                | ruby_cache_10vu     |              0 |
|            0 |             0 |          |          |          |             |                | ruby_cache_1vu      |              0 |
|            0 |             0 |          |          |          |             |                | ruby_cache_50vu     |              0 |
|            0 |             0 |          |          |          |             |                | ruby_nocache_10vu   |              0 |
|            0 |             0 |          |          |          |             |                | ruby_nocache_1vu    |              0 |
|            0 |             0 |          |          |          |             |                | ruby_nocache_50vu   |              0 |

## Gráficos

![](plots\avg_response_time.png)

![](plots\throughput.png)

![](plots\failure_rate.png)


## Interpretação rápida

- Compare tempos médios entre cenários para ver o impacto do cache e da linguagem.
- Observe throughput (req/s) para avaliar escalabilidade sob carga.
- Taxa de falha indica estabilidade/erro sob carga.
