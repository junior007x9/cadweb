# Generated by Django 4.2.16 on 2024-12-14 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_categoria_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('cpf', models.CharField(max_length=15, verbose_name='C.P.F')),
                ('datanasc', models.DateField(verbose_name='Data de Nascimento')),
            ],
        ),
        migrations.AlterModelOptions(
            name='categoria',
            options={},
        ),
        migrations.RemoveField(
            model_name='categoria',
            name='created_at',
        ),
        migrations.AlterField(
            model_name='categoria',
            name='ordem',
            field=models.IntegerField(),
        ),
    ]
