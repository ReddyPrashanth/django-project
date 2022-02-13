# Generated by Django 3.2.11 on 2022-01-25 03:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('active', models.BooleanField(default=True)),
                ('sort_order', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='InventorySize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ProductInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_url', models.CharField(max_length=100, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('slug', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('sort_order', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddConstraint(
            model_name='size',
            constraint=models.UniqueConstraint(fields=('slug',), name='uq_slug_size'),
        ),
        migrations.AddField(
            model_name='productinventory',
            name='color',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.color'),
        ),
        migrations.AddField(
            model_name='productinventory',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='inventorysize',
            name='product_inventory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.productinventory'),
        ),
        migrations.AddField(
            model_name='inventorysize',
            name='size',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.size'),
        ),
        migrations.AddConstraint(
            model_name='color',
            constraint=models.UniqueConstraint(fields=('name',), name='uq_name_color'),
        ),
        migrations.AddIndex(
            model_name='productinventory',
            index=models.Index(fields=['product_id'], name='idx_product_id_inventory'),
        ),
        migrations.AddIndex(
            model_name='productinventory',
            index=models.Index(fields=['color_id'], name='idx_color_id_inventory'),
        ),
        migrations.AddIndex(
            model_name='inventorysize',
            index=models.Index(fields=['size_id'], name='idx_size_id_inventory_size'),
        ),
        migrations.AddIndex(
            model_name='inventorysize',
            index=models.Index(fields=['product_inventory_id'], name='idx_inventory_id_size'),
        ),
    ]
