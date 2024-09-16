// login.js

window.addEventListener('load', function() {
  const splashScreen = document.getElementById('splash-screen');
  const logo = document.querySelector('.splash-screen .logo img');
  const loginContainer = document.querySelector('.login-container');
  const logoContainer = document.querySelector('.logo-container .logo img');

  setTimeout(() => {
    // Move logo and fade out background
    logo.classList.add('move-logo');
    splashScreen.classList.add('fade-out');
  }, 1000);

  // After animation, hide splash screen and show login form and logo in its final position
  setTimeout(() => {
    splashScreen.classList.add('hidden');
    loginContainer.classList.remove('hidden');
    // Move the logo to the final position above the login container
    logoContainer.src = logo.src; // Reuse the logo in the final position
  }, 2000);
});

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
