# Generated by Django 4.0.5 on 2022-06-29 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_item_description_alter_item_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
