# Generated by Django 3.2.4 on 2021-07-12 19:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0008_auto_20210705_0915'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['-created'], 'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
    ]
