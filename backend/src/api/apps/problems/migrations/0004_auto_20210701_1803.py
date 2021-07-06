# Generated by Django 3.2.4 on 2021-07-01 18:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20210630_1049'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='Changed')),
                ('text', models.CharField(max_length=2048, verbose_name='Question')),
                ('type', models.CharField(choices=[('Integer', 'Integer'), ('Decimal', 'Decimal'), ('Text', 'Text'), ('Single Choice', 'Single Choice'), ('Multiple Choice', 'Multiple Choice')], max_length=32, verbose_name='Type')),
                ('complexity', models.CharField(choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard'), ('Extremely Hard', 'Extremely Hard')], max_length=32, verbose_name='Complexity')),
                ('number_of_points', models.IntegerField(verbose_name='Number of Points')),
                ('max_attempts_to_solve', models.IntegerField(null=True, verbose_name='Max Attempts To Solve')),
                ('correct_answer', models.CharField(max_length=255, verbose_name='Correct Answer')),
                ('solution', models.TextField(blank=True, null=True, verbose_name='Solution')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='questions', to='problems.category', verbose_name='Category')),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'db_table': 'problems_questions',
            },
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('changed', models.DateTimeField(auto_now=True, verbose_name='Changed')),
                ('value', models.CharField(max_length=2048, unique=True, verbose_name='Value')),
                ('is_correct', models.BooleanField(verbose_name='Is Correct')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='problems.question', verbose_name='Question')),
            ],
            options={
                'verbose_name': 'Option',
                'verbose_name_plural': 'Options',
                'db_table': 'problems_questions_options',
            },
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['type'], name='problems_qu_type_091c3b_idx'),
        ),
        migrations.AddIndex(
            model_name='question',
            index=models.Index(fields=['complexity'], name='problems_qu_complex_836e87_idx'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.CheckConstraint(check=models.Q(('number_of_points__gte', 1), ('number_of_points__lte', 10)), name='Number of Points is an integer value between 1 and 10'),
        ),
        migrations.AddConstraint(
            model_name='question',
            constraint=models.CheckConstraint(check=models.Q(('max_attempts_to_solve__gte', 1)), name='Max Attempts To Solve is a positive integer value'),
        ),
    ]
