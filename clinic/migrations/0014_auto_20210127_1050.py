# Generated by Django 3.1.5 on 2021-01-27 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0013_mauphieu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mauphieu',
            name='dich_vu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='mau_phieu', to='clinic.dichvukham'),
        ),
    ]
