# Generated by Django 2.0 on 2018-04-08 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Census',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('voting_id', models.PositiveIntegerField()),
                ('voter_id', models.PositiveIntegerField()),
                ('adscripcion', models.CharField(max_length=128)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='census',
            unique_together={('voting_id', 'voter_id')},
        ),
    ]
