# Generated by Django 2.2.16 on 2022-05-02 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20220502_2035'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='review',
            name='unique_review',
        ),
        migrations.AddConstraint(
            model_name='review',
            constraint=models.UniqueConstraint(fields=('title', 'author'), name='unique_review'),
        ),
    ]
