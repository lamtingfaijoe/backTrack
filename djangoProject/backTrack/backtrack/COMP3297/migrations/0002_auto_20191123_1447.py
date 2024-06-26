# Generated by Django 2.2.7 on 2019-11-23 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('COMP3297', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='managerordeveloper',
            options={'ordering': ['post', 'name']},
        ),
        migrations.AlterModelOptions(
            name='pbi',
            options={'ordering': ['project', 'priority']},
        ),
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='sprint_backlog',
            options={'ordering': ['project', 'sprint_number']},
        ),
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['project', 'pbi', 'task_status']},
        ),
        migrations.AlterField(
            model_name='managerordeveloper',
            name='name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='pbi',
            name='priority',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='pbi',
            unique_together={('project', 'priority')},
        ),
        migrations.AlterUniqueTogether(
            name='sprint_backlog',
            unique_together={('project', 'sprint_number')},
        ),
        migrations.AlterUniqueTogether(
            name='task',
            unique_together={('pbi', 'description')},
        ),
    ]
