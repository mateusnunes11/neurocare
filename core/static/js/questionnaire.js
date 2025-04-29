document.getElementById('questionnaireForm').addEventListener('submit', function (event) {
    const totalQuestions = 20;
    for (let i = 1; i <= totalQuestions; i++) {
        const radios = document.getElementsByName('q' + i);
        if (![...radios].some(radio => radio.checked)) {
            alert(`Por favor, responda a pergunta ${i} antes de enviar.`);
            event.preventDefault();
            return;
        }
    }
});
