# Generated by Django 2.0.1 on 2018-01-04 14:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphqlendpoint', '0022_auto_20180104_1543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='call',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='event', to='graphqlendpoint.Call'),
        ),
    ]