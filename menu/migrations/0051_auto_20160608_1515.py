# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-08 15:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import menu.models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0050_auto_20160608_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='plato_en_menu',
            name='menu',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menu.MENU'),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='email',
            field=models.EmailField(error_messages={'invalid': 'Email inválido.', 'required': 'Email inválido', 'unique': 'Ese email ya está en uso.'}, max_length=200, primary_key=True, serialize=False, validators=[menu.models.validate_correo]),
        ),
    ]