# Generated by Django 5.0.4 on 2024-04-27 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_merge_20240427_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='id',
            field=models.CharField(default='b6df30a5-587f-4a7b-b997-b6e38ea9ff63', editable=False, max_length=36, primary_key=True, serialize=False),
        ),
    ]
