document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('search-form');
    const queryInput = document.getElementById('query');
    const resultsDiv = document.getElementById('results');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const query = queryInput.value.trim();

        if (!query) {
            alert("Por favor, insira uma consulta.");
            return;
        }

        try {
            const response = await fetch('http://localhost:5000/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });

            const articles = await response.json();
            
            // Limpa os resultados anteriores
            resultsDiv.innerHTML = '';

            // Se a resposta da API for uma lista de artigos
            if (Array.isArray(articles)) {
                articles.forEach(article => {
                    // Cria o card usando template literals para maior clareza
                    const card = document.createElement('div');
                    card.classList.add('result-card');

                    card.innerHTML = `
                        <h3>${article.title || 'Título não encontrado'}</h3>
                        <p>Autor: ${article.author || 'Autor não encontrado'}</p>
                        <p>Ano de Publicação: ${article.year || 'Data não encontrada'}</p>
                        <a href="${article.link || '#'}" target="_blank">Ver Artigo</a>
                    `;

                    // Adiciona o card aos resultados
                    resultsDiv.appendChild(card);
                });
            } else {
                resultsDiv.innerHTML = `<p>Erro ao processar os dados. Por favor, tente novamente.</p>`;
            }

        } catch (error) {
            console.error('Erro ao buscar os artigos:', error);
            resultsDiv.innerHTML = `<p>Erro ao buscar os artigos. Por favor, tente novamente.</p>`;
        }
    });
});
