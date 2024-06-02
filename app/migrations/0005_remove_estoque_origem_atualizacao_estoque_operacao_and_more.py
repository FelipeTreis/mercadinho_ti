# Generated by Django 5.0.6 on 2024-06-02 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_estoque_origem_atualizacao_alter_estoque_produto_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='estoque',
            name='origem_atualizacao',
        ),
        migrations.AddField(
            model_name='estoque',
            name='operacao',
            field=models.CharField(default='entrada', max_length=10),
        ),
        migrations.AddField(
            model_name='estoque',
            name='origem',
            field=models.CharField(default='compra', max_length=20),
        ),
    ]
