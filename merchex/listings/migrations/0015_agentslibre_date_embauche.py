# Generated by Django 5.0.7 on 2024-08-21 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('listings', '0014_agentslibre'),
    ]

    operations = [
        migrations.AddField(
            model_name='agentslibre',
            name='date_embauche',
            field=models.DateField(blank=True, null=True),
        ),
    ]
