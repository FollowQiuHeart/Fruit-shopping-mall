# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-03-17 10:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_auto_20200317_1801'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'verbose_name': '商品', 'verbose_name_plural': '复数名称'},
        ),
        migrations.AlterModelOptions(
            name='goodstype',
            options={'verbose_name': '商品类别', 'verbose_name_plural': '商品类别'},
        ),
        migrations.AlterModelTable(
            name='goods',
            table='goods',
        ),
    ]
