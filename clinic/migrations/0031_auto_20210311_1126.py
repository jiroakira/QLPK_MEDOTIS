# Generated by Django 3.1.6 on 2021-03-11 04:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0030_auto_20210305_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phankhoakham',
            name='bac_si_lam_sang',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bac_si', to=settings.AUTH_USER_MODEL),
        ),
    ]
