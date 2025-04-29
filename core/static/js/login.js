document.getElementById('loginForm').addEventListener('submit', function (event) {
    const username = document.getElementById('username');
    const password = document.getElementById('password');

    if (username.value.trim() === '' || password.value.trim() === '') {
        alert('Por favor, preencha todos os campos.');
        event.preventDefault();
    }
});
