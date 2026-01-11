# Generated manually to make weight field nullable

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_weightentry_diastolic_pressure_weightentry_pulse_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weightentry',
            name='weight',
            field=models.FloatField(blank=True, null=True),
        ),
    ]