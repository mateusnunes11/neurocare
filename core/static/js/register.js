document.getElementById('registerForm').addEventListener('submit', function (event) {
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const age = document.getElementById('age');
    const gender = document.getElementById('gender');

    if (username.value.trim() === '' || password.value.trim() === '' || age.value.trim() === '' || gender.value === '') {
        alert('Por favor, preencha todos os campos.');
        event.preventDefault();
        return;
    }

    if (password.value.length < 6) {
        alert('A senha deve ter no mínimo 6 caracteres.');
        event.preventDefault();
        return;
    }

    if (parseInt(age.value) <= 0) {
        alert('Por favor, insira uma idade válida.');
        event.preventDefault();
        return;
    }
});
