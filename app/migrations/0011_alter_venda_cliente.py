# Generated by Django 5.0.6 on 2024-06-15 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_remove_venda_matricula_colaborador_venda_cliente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venda',
            name='cliente',
            field=models.CharField(max_length=60),
        ),
    ]
