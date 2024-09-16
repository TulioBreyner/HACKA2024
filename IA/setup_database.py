"""
Code samples for vector database quickstart pages:
    https://redis.io/docs/latest/develop/get-started/vector-database/
"""

import json
import time

import numpy as np
import pandas as pd
import requests
import redis
from redis.commands.search.field import (
    NumericField,
    TagField,
    TextField,
    VectorField,
)
from redis.commands.search.indexDefinition import IndexDefinition, IndexType
from redis.commands.search.query import Query
from sentence_transformers import SentenceTransformer

data_json = [
{
    'id': 0,
    'authors': 'JOANA PEREIRA REPINALDO',
    'year': 2015,
    'title': 'CONTROLE DE VELOCIDADE DE UM SERVOMOTOR UTILIZANDO SOFTWARE LABVIEW REAL-TIME',
    'keywords': 'Instrumentação; Sistema de Controle; LabVIEW; Controle em Tempo Real',
    'link': 'https://youtube.com',
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
    'year': 2016,
    'title': 'SDN no Contexto de IoT: Refatoração de Middleware para Monitoramento de Pacientes Crônicos Baseada em Software-Defined Networking',
    'keywords': 'Software-defined networking; internet of things; gerência de redes; middleware; redes domésticas',
    'link': 'https://google.com',
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
},
{
    'id': 2,
    'authors': 'Jetro Turan Salvador, Tereza Cristina Carvalho, Luiz Antonio Corrêa Lucchesi',
    'year': 2011,
    'title': 'Relações cálcio e magnésio presentes no solo e teores foliares de macronutrientes',
    'keywords': 'Glycine max (L.) Merrill; Nutrients; Leave',
    'link': 'https://periodicos.pucpr.br/cienciaanimal/article/view/11060/10445',
    'abstract': '''A disponibilidade de nutrientes no solo é dependente de uma série de fatores.
Por causa das diferentes inte-rações que ocorrem, o uso e monitoramento das relações entre nutrientes no solo pode ser uma das formas adequadas
para proporcionar um equilíbrio nutricional para as plantas.
O objetivo deste trabalho foi avaliar se a aplicação de diferentes relações cálcio e magnésio no solo alteram
os teores de cálcio, magnésio, fósforo e potássio em plantas de soja.
O trabalho foi conduzido em delineamento inteiramente casualizado, em casa de vegetação, utilizando terra oriunda de um latossolo
submetido a sete diferentes relações de cálcio e magnésio (1:0, 10:1, 3:1, 1:1, 1:3, 1:10 e 0:1) e o
tratamento testemunha, sendo utilizadas três repetições por tratamento.
Realizou-se o cultivo de duas plantas de soja por vaso, sendo estas, aos 75 dias após a se-meadura,
submetidas a análises foliares quanto aos teores de cálcio, magnésio, fósforo e potássio.
Ocorreram alterações significativas nos teores trocáveis de cálcio e magnésio do solo e nos teores foliares de cálcio,
magnésio e potássio, quando se usaram diferentes relações de cálcio e magnésio no solo'''
},
{
    'id': 3,
    'authors': 'Jacob Biamonte, Peter Wittek, Nicola Pancotti, Patrick Rebentrost, Nathan Wiebe & Seth Lloyd',
    'year': 2017,
    'title': 'Quantum machine learning',
    'keywords': '',
    'link': 'https://www.nature.com/articles/nature23474',
    'abstract': '''Fuelled by increasing computer power and algorithmic advances, machine learning techniques have become powerful
tools for finding patterns in data. Quantum systems produce atypical patterns that classical systems are thought not
to produce efficiently, so it is reasonable to postulate that quantum computers may outperform classical computers on
machine learning tasks. The field of quantum machine learning explores how to devise and implement quantum software
that could enable machine learning that is faster than that of classical computers. Recent work has produced quantum
algorithms that could act as the building blocks of machine learning programs, but the hardware and software challenges
are still considerable.'''
}
]

with open('data.json', 'w') as file:
    file.write(json.dumps(data_json))

client = redis.Redis(host="localhost", port=6379, decode_responses=True)

[client.json().delete(key) for key in client.keys()]

pipeline = client.pipeline()
for i, data in enumerate(data_json, start=1):
    redis_key = f"articles:{i:03}"
    pipeline.json().set(redis_key, "$", data)
res = pipeline.execute()

res = client.json().get("articles:001", "$.title")

keys = sorted(client.keys("articles:*"))

abstracts = client.json().mget(keys, "$.abstract")
abstracts = [item for sublist in abstracts for item in sublist]
embedder = SentenceTransformer("msmarco-distilbert-base-v4")
embeddings = embedder.encode(abstracts).astype(np.float32).tolist()
VECTOR_DIMENSION = len(embeddings[0])

pipeline = client.pipeline()
for key, embedding in zip(keys, embeddings):
    pipeline.json().set(key, "$.abstract_embeddings", embedding)
pipeline.execute()

schema = (
    NumericField("$.id", as_name="id"),
    NumericField("$.year", as_name="year"),
    TextField("$.title", no_stem=True, as_name="title"),
    TextField("$.abstract", no_stem=True, as_name="abstract"),
    TextField("$.authors", no_stem=True, as_name="authors"),
    TextField("$.link", no_stem=True, as_name="link"),
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
definition = IndexDefinition(prefix=["articles:"], index_type=IndexType.JSON)

try:
    res = client.ft("idx:articles_vss").create_index(fields=schema, definition=definition)
except Exception as e:
    print(f'Got an erro: {e}\nGonna drop it!')
    client.ft("idx:articles_vss").dropindex()
    res = client.ft("idx:articles_vss").create_index(fields=schema, definition=definition)
print('>>', res)

info = client.ft("idx:articles_vss").info()
num_docs = info["num_docs"]
indexing_failures = info["hash_indexing_failures"]
print(f"{num_docs} documents indexed with {indexing_failures} failures")

