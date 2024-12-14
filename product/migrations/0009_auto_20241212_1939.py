# Generated by Django 3.2.18 on 2023-12-19 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_auto_20230510_1347'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='age_maximal',
            field=models.IntegerField(blank=True, db_column='Max Age', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='age_minimal',
            field=models.IntegerField(blank=True, db_column='Min Age', null=True),
        ),
    ]
