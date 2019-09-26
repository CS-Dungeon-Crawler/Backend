# Generated by Django 2.2.5 on 2019-09-26 01:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('adv', '0013_auto_20190925_2040'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='armor',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AlterModelOptions(
            name='weapon',
            options={'base_manager_name': 'objects'},
        ),
        migrations.AddField(
            model_name='item',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_adv.item_set+', to='contenttypes.ContentType'),
        ),
    ]