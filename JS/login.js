// login.js

document.getElementById('login-form').addEventListener('submit', function(event) {
    event.preventDefault();
  
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
  
    if (username === 'user' && password === 'user') {
      sessionStorage.setItem('loggedIn', 'true');
      window.location.href = 'buscaArtigos.html';
    } else {
      alert('Usuário ou senha inválidos.');
    }
  });
  