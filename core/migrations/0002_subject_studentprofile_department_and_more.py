# Generated by Django 5.0.7 on 2024-10-03 17:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.department'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student')], max_length=10),
        ),
        migrations.RemoveField(
            model_name='studentprofile',
            name='subjects',
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('course_type', models.CharField(choices=[('DSC', 'Discipline-Specific Core'), ('DSE', 'Discipline-Specific Elective'), ('AEC', 'Ability Enhancement Compulsory Course'), ('SEC', 'Skill Enhancement Course'), ('MDC', 'Multi-Disciplinary Course')], max_length=3)),
                ('credit', models.IntegerField(default=2)),
                ('semester', models.IntegerField(default=1)),
                ('availability', models.IntegerField(default=40)),
                ('programme', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.programme')),
                ('excluded_subjects', models.ManyToManyField(blank=True, to='core.subject')),
            ],
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='subjects',
            field=models.ManyToManyField(to='core.subject'),
        ),
    ]
