# Generated by Django 4.0.4 on 2022-12-10 16:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0003_rename_text_contactadmin_content'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactadmin',
            options={'ordering': ['id'], 'verbose_name': 'User comment', 'verbose_name_plural': 'Users comments'},
        ),
    ]