# Generated by Django 3.0.4 on 2020-03-22 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20200321_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(default=0, max_length=200),
            preserve_default=False,
        ),
    ]