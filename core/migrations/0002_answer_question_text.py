# Generated by Django 5.2 on 2025-04-10 00:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='question_text',
            field=models.TextField(default='Pergunta não disponível'),
            preserve_default=False,
        ),
    ]
