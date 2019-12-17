# Generated by Django 2.2 on 2019-12-16 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('img', models.ImageField(upload_to='img/')),
                ('image_id', models.IntegerField()),
                ('width', models.IntegerField(default=None)),
                ('height', models.IntegerField(default=None)),
                ('detect_result', models.NullBooleanField(default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='new task')),
                ('info', models.TextField(default=0)),
                ('user', models.TextField(default='root')),
                ('date', models.DateTimeField(auto_now=True)),
                ('parent_mission_id', models.IntegerField(default=None)),
                ('image_path', models.TextField(default='/home/freeverc/Workspace/AerialImage/Django/AerialPatrolMissions/detection/media')),
                ('image_num', models.IntegerField(default=0)),
                ('image_list', models.FilePathField(match='JPG^', path=models.TextField(default='/home/freeverc/Workspace/AerialImage/Django/AerialPatrolMissions/detection/media'))),
                ('detect_path', models.TextField(default='/home/freeverc/Workspace/AerialImage/houduan/b')),
                ('seg_path', models.TextField(default='/home/freeverc/Workspace/AerialImage/houduan/c')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=True, related_name='children', to='detection.Mission')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]