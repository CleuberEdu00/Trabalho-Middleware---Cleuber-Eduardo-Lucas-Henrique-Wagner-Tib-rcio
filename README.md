# Trabalho-Middleware---Cleuber-Eduardo-Lucas-Henrique-Wagner-Tiburcio

# Atividade de Middleware — Redis Streams

Atividade prática da disciplina de Sistemas Distribuídos, explorando o Redis Streams como plataforma de middleware de streaming de eventos.

**Integrantes:** Cleuber Eduardo Lopes Santana, Lucas Henrique Gonçalves Ferreira, Wagner Tibúrcio Ezequiel

## Como funciona

A aplicação é formada por dois processos independentes que nunca se comunicam diretamente entre si — toda a troca de dados passa pelo Redis, que atua como middleware.

- **Produtor** (`produtor.py`): publica mensagens em uma stream Redis (`canal:hello`) usando o comando `XADD`.
- **Consumidor** (`consumidor.py`, `consumidor2.py`): lê a stream por meio de um Consumer Group (`grupo-hello`), usando `XREADGROUP`, e confirma cada mensagem processada com `XACK`.

O Redis roda em um container Docker no **Computador A**, que também executa os consumidores. O **Computador B** roda apenas o produtor, conectando-se ao Redis do Computador A pela rede privada criada pelo **Tailscale** (VPN mesh), mesmo estando em redes Wi-Fi diferentes.

O Consumer Group garante que cada mensagem seja entregue a apenas um consumidor ativo (balanceamento tipo fila de trabalho), e a stream mantém as mensagens persistidas até serem confirmadas — permitindo recuperação mesmo se um consumidor cair.

## Pré-requisitos

- Docker instalado no Computador A
- Tailscale instalado e autenticado na mesma conta em ambos os computadores
- Python 3.x e a biblioteca `redis-py` em ambos: `pip install redis`

## Como rodar

**1. No Computador A — suba o Redis:**
```bash
docker run -d --name redis-streams -p 6379:6379 redis:7.2
```

**2. Em ambos os computadores — confira a rede Tailscale:**
```bash
tailscale status
```
Anote o IP do Computador A (ex.: `100.75.109.69`) e ajuste a variável `host` no `produtor.py`.

**3. No Computador A — inicie o consumidor:**
```bash
python consumidor.py
```

**4. No Computador B — execute o produtor:**
```bash
python produtor.py
```

As mensagens enviadas pelo produtor devem aparecer no terminal do consumidor em tempo real.

**Testando concorrência:** rode `python consumidor2.py` em um terceiro terminal no Computador A para ver o Redis distribuir as mensagens entre os dois consumidores.

**Testando falha:** derrube um consumidor (Ctrl+C) e envie mensagens com o produtor — elas continuam acumuladas na stream (`docker exec -it redis-streams redis-cli XLEN canal:hello`). Derrube o próprio Redis (`docker stop redis-streams`) para observar o erro de conexão no produtor.

## Estrutura

```
produtor.py      # roda no Computador B
consumidor.py    # roda no Computador A (consumidor-1)
consumidor2.py   # roda no Computador A (consumidor-2, para teste de concorrência)
```
