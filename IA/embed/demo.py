import redis.client
from sentence_transformers import SentenceTransformer
import numpy as np
import json
import redis
from redis.commands.json.path import Path
from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField,
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query

client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def clear():
    for key in client.keys():
        client.delete(key)
    print('keys:', client.keys())

data_json = [
{
    'id': 0,
    'authors': 'JOANA PEREIRA REPINALDO',
    'title': 'CONTROLE DE VELOCIDADE DE UM SERVOMOTOR UTILIZANDO SOFTWARE LABVIEW REAL-TIME',
    'keywords': 'Instrumentação; Sistema de Controle; LabVIEW; Controle em Tempo Real',
    'abstract': '''Este trabalho apresenta uma ferramenta didática para sistemas de controle que
possibilita a associação entre os conceitos teóricos e práticos. Facilita o aprendizado
ao proporcionar o desenvolvimento de experiências de laboratório. É possível aplicar
técnicas de controle clássico como de controladores PID (Proporcional, Integral e
Derivativo) permitindo ao usuário controlar a velocidade do servomotor. A entrada do
sistema pode ser definida como uma forma de onda: quadrada, triangular ou senoidal.
O controle do servomotor é realizado através de uma placa de aquisição de dados e
do software LabVIEW, o qual possui uma interface gráfica amigável facilitando o
manuseio do aluno. O sistema utiliza a técnica hardware-in-the-loop em tempo real e
é capaz de armazenar os dados para análises qualitativas e quantitativas off-line.'''
},
{
    'id': 1,
    'authors': 'LUCAS MENDES RIBEIRO ARBIZA',
    'title': 'SDN no Contexto de IoT: Refatoração de Middleware para Monitoramento de Pacientes Crônicos Baseada em Software-Defined Networking',
    'keywords': 'Software-defined networking; internet of things; gerência de redes; middleware; redes domésticas',
    'abstract': '''Algumas palavras e definições comumente utilizadas quando se está falando de Software-Defined
Networking, como programabilidade, flexibilidade, ou gerenciamento centralizado, parecem
muito apropriadas ao contexto de um outro paradigma de rede: Internet of Things. Em redes
domésticas já não é incomum a existência de dispositivos projetados para segurança, climatização, iluminação, monitoramento de saúde e algumas formas de automação que diferem entre
si em diversos aspectos, como no modo de operar e de se comunicar. Lidar com este tipo de
cenário, que pode diferir bastante daquilo que estamos acostumados na gerência de redes e serviços, fazendo uso dos recursos tradicionais como ferramentas e protocolos bem estabelecidos,
pode ser difícil e, em alguns casos, inviável. Com o objetivo de possibilitar o monitoramento
remoto de pacientes com doenças crônicas através de dispositivos de healthcare disponíveis
no mercado, uma proposta de middleware foi desenvolvida em um projeto de pesquisa para
contornar as limitações relacionadas à interoperabilidade, coleta de dados, gerência, segurança
e privacidade encontradas nos dispositivos utilizados. O middleware foi projetado com o intuito de executar em access points instalados na casa dos pacientes. Contudo, as limitações de
hardware e software do access point utilizado refletem no desenvolvimento, pois restringem
o uso de linguagens de programação e recursos que poderiam agilizar e facilitar a implementação dos módulos e dos mecanismos necessários. Os contratempos encontrados no desenvolvimento motivaram a busca por alternativas, o que resultou na refatoração do middleware
através de Software-Defined Networking, baseando-se em trabalhos que exploram o uso desse
paradigma em redes domésticas. O objetivo deste trabalho é verificar a viabilidade da utilização de Software-Defined Networking no contexto de Internet of Things, mais especificamente,
aplicado ao serviço de monitoramento de pacientes da proposta anterior e explorar os possíveis benefícios resultantes. Com a refatoração, a maior parte da carga de serviços da rede e do
monitoramento foi distribuída entre servidores remotos dedicados, com isso os desenvolvedores
podem ir além das restrições do access point e fazer uso de recursos antes não disponíveis, o que
potencializa um processo de desenvolvimento mais ágil e com funcionalidades mais complexas, ampliando as possibilidades do serviço. Adicionalmente, a utilização de Software-Defined
Networking proporcionou a entrega de mais de um serviço através de um único access point,
escalabilidade e autonomia no gerenciamento das redes e dos dispositivos e na implantação de
serviços, fazendo uso de recursos do protocolo OpenFlow, e a cooperação entre dispositivos e
serviços a fim de se criar uma representação digital mais ampla do ambiente monitorado.'''

}
]
# open('data.json', 'w').write(json.dumps(data_json))

clear()

def insert(client: redis.Redis, prefix, data):
    pipeline = client.pipeline()
    for i, entry in enumerate(data):
        pipeline.json().set(f'{prefix}:{i:03}', Path.root_path(), entry)
    pipeline.execute()

def insert_in(client: redis.Redis, keys, prefix, data):
    pipeline = client.pipeline()
    for key, value in zip(keys, data):
        pipeline.json().set(key, f"$.{prefix}_embeddings", value)
    pipeline.execute()

def create_embed(data):
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    embeddings = model.encode(data).astype(np.float32).tolist()
    return embeddings

def create_index(index, schema, prefix):
    try:
        definition = IndexDefinition(prefix=[f"{prefix}:"], index_type=IndexType.JSON)
        return client.ft(index).create_index(fields=schema, definition=definition)
    except Exception as e:
        print(f'Got an erro: {e}\nGonna drop it!')
        client.ft(index).dropindex()
        return create_index(index, schema, definition)

def create_query(embedder: SentenceTransformer, queries):
    encoded_query = embedder.encode(queries)

    return {
        'query_vector': np.array(encoded_query, dtype=np.float32).tobytes()
    }

def search(client: redis.Redis, index, query):
    return client.ft(index).search(
        Query('(*)=>[KNN 3 @vector $query_vector AS vector_score]')
            .sort_by('vector_score')
            .return_fields('vector_score', 'id', 'authors', 'keywords', 'abstract')
            .dialect(2),
        query
    ).docs

insert(client, 'articles', data_json)

keys = sorted(client.keys("articles:*"))
abstracts = [
    item for v in client.json().mget(keys, "$.abstract")
    for item in v
]

embeddings = create_embed(abstracts)
VECTOR_DIMENSION = len(embeddings[0])

insert_in(client, keys, 'abstract', embeddings)

# print(client.keys())
# print(client.json().get('articles:001', "$.abstract_embeddings"))

schema = (
    NumericField("$.id", as_name="id"),
    TextField("$.title", no_stem=True, as_name="title"),
    TextField("$.abstract", no_stem=True, as_name="abstract"),
    TextField("$.authors", no_stem=True, as_name="authors"),
    TextField("$.keywords", no_stem=True, as_name="keywords"),
    VectorField(
        "$.abstract_embeddings",
        "FLAT",
        {
            "TYPE": "FLOAT32",
            "DIM": VECTOR_DIMENSION,
            "DISTANCE_METRIC": "COSINE",
        },
        as_name="vector",
    ),
)

res = create_index('idx:articles_vss', schema, 'articles')
info = client.ft("idx:article_vss").info()
num_docs = info["num_docs"]
print('NUM_DOCS:', num_docs, res)

exit()

model = SentenceTransformer("msmarco-distilbert-base-v4")
# query_vector = create_query(model, ['servomotor'])

print(client.json().mget(client.keys('articles:*'), '$.abstract_embeddings'))
# print(search(client, 'idx:article_vss', query_vector))

#num_docs = info["num_docs"]
#indexing_failures = info["hash_indexing_failures"]

# print(info)
