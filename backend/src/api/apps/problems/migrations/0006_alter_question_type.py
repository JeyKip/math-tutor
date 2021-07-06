# Generated by Django 3.2.4 on 2021-07-02 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_auto_20210701_1824'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='type',
            field=models.CharField(choices=[('Integer', 'Integer'), ('Decimal', 'Decimal'), ('Text', 'Text'), ('Boolean', 'Boolean'), ('Single Choice', 'Single Choice'), ('Multiple Choice', 'Multiple Choice')], max_length=32, verbose_name='Type'),
        ),
    ]
