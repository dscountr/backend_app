# Generated by Django 2.2.3 on 2019-07-22 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20190717_1802'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(default='!1xKZFUMiyDaS7Exy0CurdiaQ1Pp88xxHpN0kw3pb', max_length=255),
        ),
    ]
