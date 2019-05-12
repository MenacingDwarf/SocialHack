# Generated by Django 2.2.1 on 2019-05-12 03:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0007_lesson_current_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='current_activity',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='currant_lesson', to='database.Activity'),
        ),
    ]
