# Generated by Django 5.1.1 on 2025-01-25 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0035_esewatransaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='esewatransaction',
            old_name='date',
            new_name='created_at',
        ),
        migrations.AddField(
            model_name='esewatransaction',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='esewatransaction',
            name='amount',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='esewatransaction',
            name='status',
            field=models.CharField(choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], max_length=10),
        ),
    ]
