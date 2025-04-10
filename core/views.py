from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import User, Questionnaire, Answer

questions = [
    "Você tem se sentido nervoso(a), tenso(a) ou preocupado(a)?",
    "Você tem tido dificuldade para dormir?",
    "Você tem se sentido facilmente assustado(a)?",
    "Você tem sofrido com dores de cabeça com frequência?",
    "Você tem perdido o apetite?",
    "Você tem se sentido triste ultimamente?",
    "Você tem chorado com frequência?",
    "Você tem achado difícil aproveitar suas atividades diárias?",
    "Você tem tido dificuldade para tomar decisões?",
    "Você tem tido dificuldades no trabalho por se sentir mal?",
    "Você sente que sua vida está parada?",
    "Você tem se sentido inútil?",
    "Você tem pensado em acabar com tudo?",
    "Você tem se sentido cansado(a) o tempo todo?",
    "Você tem sentido desconforto no estômago?",
    "Você tem tido dificuldade para pensar com clareza?",
    "Você tem perdido o interesse pelas coisas?",
    "Você tem se sentido inútil como pessoa?",
    "Você tem tido a impressão de que está fazendo tudo devagar?",
    "Você tem ouvido vozes sem saber de onde vêm ou visto coisas que outras pessoas não vêem?"
]


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('questionario')
        else:
            return render(request, 'login.html', {'erro': 'Credenciais inválidas'})
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        age = request.POST.get('age')
        gender = request.POST.get('gender')

        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {'erro': 'Usuário já existe'})

        user = User.objects.create_user(username=username, password=password, age=age, gender=gender)
        login(request, user)
        return redirect('questionario')
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')


@login_required
def questionnaire_view(request):
    if request.method == 'POST':
        user = request.user
        questionnaire = Questionnaire.objects.create(user=user)
        total_score = 0

        for i in range(1, 21):
            resposta = request.POST.get(f'q{i}')
            if resposta:
                boolean = True if resposta == "sim" else False
                Answer.objects.create(
                    questionnaire=questionnaire,
                    question_number=i,
                    question_text=questions[i - 1],
                    answer=boolean
                )
                if boolean:
                    total_score += 1

        # Avaliação
        if total_score == 0:
            nivel = "Não foi identificado sofrimento mental"
        elif 1 <= total_score <= 7:
            nivel = "Sofrimento mental leve"
        elif 8 <= total_score <= 14:
            nivel = "Sofrimento mental moderado"
        else:
            nivel = "Sofrimento mental grave"

        questionnaire.total_score = total_score
        questionnaire.suffering_level = nivel
        questionnaire.save()

        return render(request, 'resultado.html', {'score': total_score, 'nivel': nivel})

    return render(request, 'questionnaire.html', {'questions': questions})
