# Migration to fix phone_numberr from IntegerField to CharField
# This is needed because IntegerField cannot store Nepali phone numbers (10 digits)

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_numberr',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
