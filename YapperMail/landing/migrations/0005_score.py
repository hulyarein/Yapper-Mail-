# Generated by Django 5.1.1 on 2024-11-01 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0004_alter_profile_gender'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.PositiveIntegerField()),
            ],
        ),
    ]
