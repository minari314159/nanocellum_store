# Generated by Django 5.0.4 on 2024-04-27 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_cart_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.BigIntegerField(default=1304130708571183466, editable=False, primary_key=True, serialize=False),
        ),
    ]
