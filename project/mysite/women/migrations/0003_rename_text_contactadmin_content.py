# Generated by Django 4.0.4 on 2022-11-30 13:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0002_contactadmin_alter_women_options_alter_category_slug_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contactadmin',
            old_name='text',
            new_name='content',
        ),
    ]