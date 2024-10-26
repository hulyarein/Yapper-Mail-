# Generated by Django 5.1.1 on 2024-10-14 20:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('EmailCompositionAndManagement', '0005_alter_email_fromuser_alter_email_touser_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('emailId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emialReply', to='EmailCompositionAndManagement.email')),
                ('fromUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reply_to_email', to='EmailCompositionAndManagement.temporaryuser')),
            ],
        ),
    ]