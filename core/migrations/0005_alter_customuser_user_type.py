# Generated by Django 5.0.7 on 2024-10-13 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_studentprofile_edit_approved_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student')], default='student', max_length=10),
        ),
    ]
