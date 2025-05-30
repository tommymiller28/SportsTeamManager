# Generated by Django 4.2.7 on 2025-04-08 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitchingstat',
            name='earned_runs',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pitchingstat',
            name='hits_allowed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pitchingstat',
            name='home_runs_allowed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pitchingstat',
            name='innings_pitched',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pitchingstat',
            name='pitches_thrown',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pitchingstat',
            name='runs_allowed',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pitchingstat',
            name='strikeouts',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='pitchingstat',
            name='walks',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
