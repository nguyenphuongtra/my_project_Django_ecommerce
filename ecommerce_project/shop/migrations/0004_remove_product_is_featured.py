# Generated by Django 5.2 on 2025-04-14 09:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_product_is_featured'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_featured',
        ),
    ]
