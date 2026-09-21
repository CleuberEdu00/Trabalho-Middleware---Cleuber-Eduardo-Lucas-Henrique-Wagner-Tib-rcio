import redis

r = redis.Redis(host='100.75.109.69', port=6379, decode_responses=True)

for i in range(10):
    mensagem = {'id_requisicao': str(i), 'conteudo': f'Hello World {i}', 'origem': 'Computador B'}
    msg_id = r.xadd('canal:hello', mensagem)
    print(f'[PRODUTOR] Mensagem enviada. ID da stream: {msg_id}')
    