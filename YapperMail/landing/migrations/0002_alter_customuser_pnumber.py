# Generated by Django 5.1 on 2024-11-19 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pnumber',
            field=models.CharField(blank=True, max_length=13, null=True, unique=True),
        ),
    ]
