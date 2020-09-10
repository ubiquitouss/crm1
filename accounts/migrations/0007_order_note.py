# Generated by Django 3.1.1 on 2020-09-10 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_product_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='note',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Out For Delivery', 'Out for delivery'), ('Delivered', 'Delivered')], max_length=1000, null=True),
        ),
    ]
