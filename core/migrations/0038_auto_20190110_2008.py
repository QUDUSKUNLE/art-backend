# Generated by Django 2.1.2 on 2019-01-10 20:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0037_remove_andelacentre_country_old'),
    ]

    operations = [
        migrations.RenameField(
            model_name='andelacentre',
            old_name='centre_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='assetcategory',
            old_name='category_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='assetmake',
            old_name='make_label',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='assetmodelnumber',
            old_name='make_label',
            new_name='asset_make',
        ),
        migrations.RenameField(
            model_name='assetmodelnumber',
            old_name='model_number',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='assetsubcategory',
            old_name='sub_category_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='assettype',
            old_name='asset_type',
            new_name='name',
        ),
    ]
