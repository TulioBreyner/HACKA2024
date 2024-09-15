from flask import Flask, jsonify, request
from flask_cors import CORS
from scholarly import scholarly

app = Flask(__name__)
CORS(app)  # Habilitar CORS

# Função para buscar artigos
def search_articles(query):
    try:
        search_results = scholarly.search_pubs(query)
        articles = []
        for i, result in enumerate(search_results):
            if i >= 5:  # Limitar a 5 resultados
                break
            article = {
                'title': result.get('bib', {}).get('title', 'Título não encontrado'),
                'author': result.get('bib', {}).get('author', 'Autor não encontrado'),
                'year': result.get('bib', {}).get('pub_year', 'Data não encontrada'),
                'link': result.get('pub_url', 'Link não encontrado')
            }
            articles.append(article)
        if not articles:
            print("Nenhum artigo encontrado.")  # Log para depuração
        return articles
    except Exception as e:
        print(f"Erro ao buscar artigos: {e}")  # Log do erro
        return []

# Rota para lidar com a consulta do usuário
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    user_query = data.get('query', '')

    if not user_query:
        return jsonify({'response': 'Nenhuma consulta foi fornecida.'}), 400

    # Buscar artigos baseados na consulta do usuário
    articles = search_articles(user_query)

    # Retornar os artigos no formato desejado
    return jsonify(articles)

if __name__ == '__main__':
    app.run(debug=True)