import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

STREAM = 'canal:hello'
GRUPO = 'grupo-hello'
CONSUMIDOR = 'consumidor-2'

try:
    r.xgroup_create(STREAM, GRUPO, id='0', mkstream=True)
except redis.exceptions.ResponseError:
    pass

print(f'[CONSUMIDOR] Aguardando mensagens...')

while True:
    resposta = r.xreadgroup(GRUPO, CONSUMIDOR, {STREAM: '>'}, count=1, block=5000)
    if resposta:
        for stream_nome, mensagens in resposta:
            for msg_id, dados in mensagens:
                print(f'[CONSUMIDOR] Recebido {msg_id}: {dados}')
                r.xack(STREAM, GRUPO, msg_id)