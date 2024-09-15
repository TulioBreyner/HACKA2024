document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById('search-form');
    const queryInput = document.getElementById('query');
    const chatWindow = document.getElementById('chat-window');

    form.addEventListener('submit', async function (e) {
        e.preventDefault();

        const query = queryInput.value.trim();

        if (!query) {
            alert("Por favor, insira uma consulta.");
            return;
        }

        // Exibe a mensagem do usuário no chat (à direita)
        addMessageToChat('user', query);

        // Limpa o campo de entrada após o envio da mensagem
        queryInput.value = '';

        try {
            const response = await fetch('http://localhost:5000/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query })
            });

            const articles = await response.json();

            if (Array.isArray(articles)) {
                articles.forEach((article) => {
                    const resultMessage = `
                        <h3>${article.title || 'Título não encontrado'}</h3>
                        <p>Autor: ${article.author || 'Autor não encontrado'}</p>
                        <p>Ano de Publicação: ${article.year || 'Data não encontrada'}</p>
                        <a href="${article.link || '#'}" target="_blank">Ver Artigo</a>
                    `;
                    // Exibe a resposta do programa no chat (à esquerda)
                    addMessageToChat('response', resultMessage);
                });
            } else {
                addMessageToChat('response', 'Erro ao processar os dados. Por favor, tente novamente.');
            }

        } catch (error) {
            console.error('Erro ao buscar os artigos:', error);
            addMessageToChat('response', 'Erro ao buscar os artigos. Por favor, tente novamente.');
        }
    });

    function addMessageToChat(type, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', type === 'user' ? 'user-message' : 'response-message');

        const messageBubble = document.createElement('div');
        messageBubble.classList.add('message-bubble');
        messageBubble.innerHTML = content;

        messageDiv.appendChild(messageBubble);
        chatWindow.appendChild(messageDiv);

        // Faz scroll automático para a última mensagem
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }
});
