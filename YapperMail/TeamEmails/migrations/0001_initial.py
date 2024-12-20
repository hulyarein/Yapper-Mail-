# Generated by Django 5.1.3 on 2024-12-04 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryTeamEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isDelegate', models.BooleanField(default=False)),
                ('isScheduled', models.BooleanField(default=False)),
                ('isDo', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TeamEmail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=500)),
                ('content', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('isDeleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TeamEmailFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
            ],
        ),
        migrations.CreateModel(
            name='TeamReply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='TeamReplyFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='uploads/')),
            ],
        ),
    ]
