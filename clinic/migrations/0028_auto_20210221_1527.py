# Generated by Django 3.1.6 on 2021-02-21 08:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0027_auto_20210221_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='huyen',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.district'),
        ),
        migrations.AddField(
            model_name='user',
            name='tinh',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.province'),
        ),
        migrations.AddField(
            model_name='user',
            name='xa',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='clinic.ward'),
        ),
    ]
