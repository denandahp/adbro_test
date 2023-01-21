# Generated by Django 3.2 on 2023-01-21 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DenormalizedAdvertisement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('advertisement', models.UUIDField(editable=False)),
                ('group', models.UUIDField(editable=False)),
                ('campaign', models.UUIDField(editable=False)),
                ('site', models.UUIDField(editable=False)),
                ('slot', models.UUIDField(editable=False)),
                ('tags', models.CharField(blank=True, max_length=255, null=True)),
                ('data', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
