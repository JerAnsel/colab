# Generated by Django 3.2.10 on 2022-04-27 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_codinglanguage_profile_spokenlanguage'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='images')),
            ],
        ),
    ]