# Generated by Django 4.0.5 on 2022-07-03 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0015_student_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issuedbook',
            name='id',
        ),
        migrations.AlterField(
            model_name='issuedbook',
            name='student_id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]