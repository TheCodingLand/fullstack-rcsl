# Generated by Django 2.0 on 2017-12-27 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('graphqlendpoint', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='call',
            name='name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]