# Generated by Django 4.2 on 2025-04-09 17:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0002_loan_due_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="loan",
            name="due_date",
            field=models.DateField(default=datetime.date(2025, 4, 9)),
        ),
    ]
