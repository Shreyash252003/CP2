# Generated by Django 4.0.5 on 2022-06-29 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_orderitem_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
