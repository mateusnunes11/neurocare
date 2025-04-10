from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    gender = models.CharField(max_length=10, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Questionnaire(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questionnaires')
    response_date = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField(null=True, blank=True)
    suffering_level = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return f"Questionário {self.id} - {self.user.username}"


class Answer(models.Model):
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name='answers')
    question_number = models.IntegerField()
    question_text = models.TextField(null=True, blank=True) 
    answer = models.BooleanField()

    def __str__(self):
        return f"Q{self.question_number} - {'Sim' if self.answer else 'Não'}"
