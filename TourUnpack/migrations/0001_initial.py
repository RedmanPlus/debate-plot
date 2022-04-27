# Generated by Django 3.2.13 on 2022-04-27 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UnsignedPlayer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('surname', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='UnsignedTournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('date_conducted', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='UnsignedWeirdTournament',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r1', models.IntegerField()),
                ('r2', models.IntegerField()),
                ('r3', models.IntegerField()),
                ('r4', models.IntegerField()),
                ('r5', models.IntegerField()),
                ('r6', models.IntegerField()),
                ('r1pos', models.CharField(max_length=2)),
                ('r2pos', models.CharField(max_length=2)),
                ('r3pos', models.CharField(max_length=2)),
                ('r4pos', models.CharField(max_length=2)),
                ('r5pos', models.CharField(max_length=2)),
                ('r6pos', models.CharField(max_length=2)),
                ('r1res', models.IntegerField()),
                ('r2res', models.IntegerField()),
                ('r3res', models.IntegerField()),
                ('r4res', models.IntegerField()),
                ('r5res', models.IntegerField()),
                ('r6res', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourUnpack.unsignedplayer')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourUnpack.unsignedtournament')),
            ],
        ),
        migrations.CreateModel(
            name='UnsignedRelation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r1', models.IntegerField()),
                ('r2', models.IntegerField()),
                ('r3', models.IntegerField()),
                ('r4', models.IntegerField()),
                ('r5', models.IntegerField()),
                ('r1pos', models.CharField(max_length=2)),
                ('r2pos', models.CharField(max_length=2)),
                ('r3pos', models.CharField(max_length=2)),
                ('r4pos', models.CharField(max_length=2)),
                ('r5pos', models.CharField(max_length=2)),
                ('r1res', models.IntegerField()),
                ('r2res', models.IntegerField()),
                ('r3res', models.IntegerField()),
                ('r4res', models.IntegerField()),
                ('r5res', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourUnpack.unsignedplayer')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourUnpack.unsignedtournament')),
            ],
        ),
        migrations.CreateModel(
            name='UnsignedOCMSLU',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('r1', models.IntegerField()),
                ('r2', models.IntegerField()),
                ('r3', models.IntegerField()),
                ('r4', models.IntegerField()),
                ('r5', models.IntegerField()),
                ('r6', models.IntegerField()),
                ('r7', models.IntegerField()),
                ('r8', models.IntegerField()),
                ('r9', models.IntegerField()),
                ('r1pos', models.CharField(max_length=2)),
                ('r2pos', models.CharField(max_length=2)),
                ('r3pos', models.CharField(max_length=2)),
                ('r4pos', models.CharField(max_length=2)),
                ('r5pos', models.CharField(max_length=2)),
                ('r6pos', models.CharField(max_length=2)),
                ('r7pos', models.CharField(max_length=2)),
                ('r8pos', models.CharField(max_length=2)),
                ('r9pos', models.CharField(max_length=2)),
                ('r1res', models.IntegerField()),
                ('r2res', models.IntegerField()),
                ('r3res', models.IntegerField()),
                ('r4res', models.IntegerField()),
                ('r5res', models.IntegerField()),
                ('r6res', models.IntegerField()),
                ('r7res', models.IntegerField()),
                ('r8res', models.IntegerField()),
                ('r9res', models.IntegerField()),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourUnpack.unsignedplayer')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='TourUnpack.unsignedtournament')),
            ],
        ),
    ]