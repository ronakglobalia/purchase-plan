# Generated by Django 4.2.9 on 2024-01-17 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_alter_package_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
