# Generated by Django 4.0 on 2023-01-21 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_remove_grade_activities_remove_grade_final_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_number',
            field=models.CharField(default='000', max_length=20),
        ),
        migrations.AddField(
            model_name='student',
            name='student_number',
            field=models.CharField(default='0000', max_length=20),
        ),
    ]
