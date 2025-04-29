from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Questionnaire, Answer
import uuid

User = get_user_model()


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
            return redirect('questionnaire')
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

        user = User.objects.create_user(
            username=username,
            password=password,
            age=age,
            gender=gender,
            token=uuid.uuid4()
        )

        return redirect('login')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def questionnaire_view(request):
    user = request.user

    if not hasattr(user, 'token') or not user.token:
        return redirect('login')

    if request.method == 'POST':
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

        return render(request, 'resultado.html', {
            'score': total_score,
            'nivel': nivel,
            'token': user.token,
        })

    return render(request, 'questionnaire.html', {
        'questions': questions,
        'token': user.token,  
    })

from django.db.models import Q

@login_required
@login_required
def dashboard_view(request):
    user = request.user
    questionarios_user = Questionnaire.objects.filter(user=user)

    respostas_sim_user = Answer.objects.filter(
        questionnaire__in=questionarios_user,
        answer=True
    ).count()

    total_questionarios_user = questionarios_user.count()
    media_individual = (respostas_sim_user / (total_questionarios_user * 20) * 100) if total_questionarios_user > 0 else 0

    total_questionarios_geral = Questionnaire.objects.count()
    respostas_sim_geral = Answer.objects.filter(answer=True).count()
    media_geral = (respostas_sim_geral / (total_questionarios_geral * 20) * 100) if total_questionarios_geral > 0 else 0

    leves = Questionnaire.objects.filter(total_score__gte=1, total_score__lte=7).count()
    moderados = Questionnaire.objects.filter(total_score__gte=8, total_score__lte=14).count()
    graves = Questionnaire.objects.filter(total_score__gte=15).count()

    usuarios_transtorno = Questionnaire.objects.filter(total_score__gte=7).values('user').distinct().count()
    total_usuarios = Questionnaire.objects.values('user').distinct().count()
    sem_transtorno = total_usuarios - usuarios_transtorno

    percentual_transtorno = (usuarios_transtorno / total_usuarios * 100) if total_usuarios > 0 else 0

    context = {
    'respostas_sim_user': respostas_sim_user,
    'media_individual': round(media_individual, 2),
    'media_geral': round(media_geral, 2),
    'percentual_transtorno': round(percentual_transtorno, 2),
    'total_questionarios_user': total_questionarios_user,
    'total_questionarios_geral': total_questionarios_geral,
    'usuarios_transtorno': usuarios_transtorno,
    'sem_transtorno': sem_transtorno,
    'leves': leves or 0,
    'moderados': moderados or 0,
    'graves': graves or 0,
}


    return render(request, 'dashboard.html', context)

