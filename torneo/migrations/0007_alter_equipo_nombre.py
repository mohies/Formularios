# Generated by Django 5.1.2 on 2024-12-02 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torneo', '0006_alter_torneo_participantes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipo',
            name='nombre',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
