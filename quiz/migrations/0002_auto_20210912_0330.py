# Generated by Django 3.2.7 on 2021-09-12 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='token',
            name='id',
        ),
        migrations.AlterField(
            model_name='token',
            name='username',
            field=models.TextField(primary_key=True, serialize=False),
        ),
    ]
