# Generated by Django 2.1.1 on 2018-10-05 07:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('is_deleted', models.BooleanField(default=False)),
                ('deleted_time', models.DateTimeField(blank=True, null=True)),
                ('title', models.CharField(max_length=255)),
                ('task_type', models.IntegerField(choices=[(0, 'TASK'), (1, 'SUB TASK'), (2, 'BUG')], default=0)),
                ('label', models.CharField(blank=True, max_length=255, null=True)),
                ('priority', models.IntegerField(choices=[(0, 'LOWEST'), (1, 'LOW'), (2, 'MEDIUM'), (3, 'HIGH'), (4, 'HIGHEST')])),
                ('branch', models.CharField(max_length=20, unique=True)),
                ('progress', models.IntegerField(choices=[(0, 'TODO'), (1, 'IN PROGRESS'), (2, 'IN REPO'), (3, 'TEST'), (4, 'DONE')], default=0)),
                ('descriptions', models.TextField()),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignee', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='task.Task')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
