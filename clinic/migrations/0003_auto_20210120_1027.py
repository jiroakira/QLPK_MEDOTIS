# Generated by Django 3.1.5 on 2021-01-20 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_dichvukham_chi_so'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='muc_bao_hiem',
            new_name='muc_huong',
        ),
        migrations.AddField(
            model_name='user',
            name='can_nang',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='gt_the_den',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='gt_the_tu',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ma_dkbd',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ma_khuvuc',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='mien_cung_ct',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gioi_tinh',
            field=models.CharField(blank=True, choices=[('1', 'Nam'), ('2', 'Nữ'), ('3', 'Không xác định')], max_length=10, null=True),
        ),
    ]
