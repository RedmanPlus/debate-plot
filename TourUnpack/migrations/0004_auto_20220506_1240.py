# Generated by Django 3.2.13 on 2022-05-06 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TourUnpack', '0003_unsignedcastratedrelation'),
    ]

    operations = [
        migrations.AddField(
            model_name='unsignedcastratedrelation',
            name='r1pos',
            field=models.CharField(default='No', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unsignedcastratedrelation',
            name='r2pos',
            field=models.CharField(default='No', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unsignedcastratedrelation',
            name='r3pos',
            field=models.CharField(default='No', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unsignedcastratedrelation',
            name='r4pos',
            field=models.CharField(default='No', max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='unsignedcastratedrelation',
            name='r5pos',
            field=models.CharField(default='No', max_length=2),
            preserve_default=False,
        ),
    ]
