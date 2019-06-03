# Generated by Django 2.2.1 on 2019-05-24 11:07

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
            name='Course',
            fields=[
                ('course_id', models.AutoField(primary_key=True, serialize=False, verbose_name='课程id')),
                ('name', models.CharField(max_length=30, verbose_name='课程')),
                ('student_amount', models.IntegerField(default=0, verbose_name='总人数')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_updated_time', models.DateTimeField(auto_now=True, verbose_name='最后更新时间')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='老师')),
            ],
            options={
                'verbose_name_plural': '课程',
                'db_table': 'Course',
                'ordering': ['last_updated_time'],
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.CharField(max_length=30, verbose_name='学号')),
                ('name', models.CharField(max_length=30, verbose_name='姓名')),
                ('class_name', models.CharField(max_length=30, verbose_name='班级')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_updated_time', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
            ],
            options={
                'verbose_name_plural': '学生信息',
                'db_table': 'Student',
                'ordering': ['class_name', 'last_updated_time'],
            },
        ),
        migrations.CreateModel(
            name='StudentPicture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('face_picture_path', models.CharField(max_length=100, verbose_name='学生人脸图片路径')),
                ('encoding_face', models.BinaryField(verbose_name='人脸编码信息')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rc_app.Student', unique=True, verbose_name='学生')),
            ],
        ),
        migrations.CreateModel(
            name='StudentCourse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rc_app.Course', verbose_name='课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rc_app.Student', verbose_name='学生')),
            ],
            options={
                'verbose_name_plural': '学生课程对应关系',
                'db_table': 'StudentCourse',
                'ordering': ['course'],
            },
        ),
        migrations.CreateModel(
            name='StudentAbsentSituation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absent_or_late', models.BooleanField(choices=[(True, '缺席'), (False, '迟到')], default=True, verbose_name='缺席还是迟到')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('last_updated_time', models.DateTimeField(auto_now=True, verbose_name='最后修改时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rc_app.Course', verbose_name='课程')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rc_app.Student', verbose_name='学生')),
            ],
            options={
                'verbose_name_plural': '学生缺席情况',
                'db_table': 'StudentAbsentSituation',
                'ordering': ['create_time'],
            },
        ),
    ]