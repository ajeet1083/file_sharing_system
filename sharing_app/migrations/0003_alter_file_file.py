# Generated by Django 5.0.7 on 2024-07-21 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sharing_app', '0002_alter_user_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='media/'),
        ),
    ]
