# Generated by Django 5.0.4 on 2024-05-03 13:48

import api.validator
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_product_options_remove_product_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.ImageField(upload_to='uploads/product/', validators=[api.validator.validate_file_size]),
        ),
    ]
