# Generated by Django 3.0.8 on 2020-09-14 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0003_auto_20200914_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='loans',
            field=models.ManyToManyField(related_name='user_loans', to='network.Loan'),
        ),
        migrations.AlterField(
            model_name='loan',
            name='member',
            field=models.CharField(max_length=60),
        ),
        migrations.DeleteModel(
            name='Member',
        ),
    ]
