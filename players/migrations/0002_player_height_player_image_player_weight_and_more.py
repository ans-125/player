# Generated by Django 5.2.4 on 2025-07-10 12:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='height',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(250)], verbose_name='الطول (سم)'),
        ),
        migrations.AddField(
            model_name='player',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='player_images/', verbose_name='صورة اللاعب'),
        ),
        migrations.AddField(
            model_name='player',
            name='weight',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(30), django.core.validators.MaxValueValidator(150)], verbose_name='الوزن (كجم)'),
        ),
        migrations.AlterField(
            model_name='player',
            name='birth_year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1995), django.core.validators.MaxValueValidator(2014)], verbose_name='سنة الميلاد'),
        ),
        migrations.AlterField(
            model_name='player',
            name='description',
            field=models.TextField(blank=True, verbose_name='المهارات'),
        ),
        migrations.AlterField(
            model_name='player',
            name='previous_clubs',
            field=models.TextField(blank=True, help_text='اكتب تفاصيل المسيرة الاحترافية للاعب', verbose_name='المسيرة الاحترافية'),
        ),
    ]
