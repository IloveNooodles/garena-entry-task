# Generated by Django 3.2.4 on 2022-09-06 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_pasword_user_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='created_at',
            field=models.TimeField(auto_created=True, auto_now=True),
        ),
    ]
