# Generated by Django 2.2 on 2019-04-25 22:13

from django.db import migrations

def capitalize(apps,schema_editor):
    Product=apps.get_model("main","Product")
    for product in Product.objects.all():
        product.name=product.name.capitalize() 
        product.save()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_merge_20190425_2211'),
    ]

    operations = [
        migrations.RunPython(
            capitalize,
            migrations.RunPython.noop
        )
    ]

