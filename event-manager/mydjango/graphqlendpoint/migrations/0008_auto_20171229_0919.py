# Generated by Django 2.0 on 2017-12-29 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphqlendpoint', '0007_transfer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='origin',
            field=models.CharField(max_length=200, null=True),
        ),
    ]