# Generated by Django 5.1.1 on 2025-01-10 01:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_remove_product_images_productimage_product'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
