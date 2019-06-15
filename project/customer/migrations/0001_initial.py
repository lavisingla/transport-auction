# Generated by Django 2.2 on 2019-06-15 15:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_auth', '0002_auto_20190615_1045'),
    ]

    operations = [
        migrations.CreateModel(
            name='item_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=100)),
                ('item_weight', models.DecimalField(decimal_places=2, max_digits=20)),
                ('item_length', models.DecimalField(decimal_places=2, max_digits=20)),
                ('item_width', models.DecimalField(decimal_places=2, max_digits=20)),
                ('item_height', models.DecimalField(decimal_places=2, max_digits=20)),
                ('handle_with_care', models.BooleanField(default=False)),
                ('item_material', models.CharField(max_length=100)),
                ('item_approximate_cost', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comfirmed', models.BooleanField(default=False)),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='user_auth.user_info')),
                ('item_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.item_info')),
                ('merchant', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='merchant', to='user_auth.user_info')),
            ],
        ),
        migrations.CreateModel(
            name='order_path_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_area', models.TextField()),
                ('source_city', models.CharField(max_length=30)),
                ('source_state', models.CharField(max_length=30)),
                ('source_pin', models.IntegerField()),
                ('destination_area', models.TextField()),
                ('destination_city', models.CharField(max_length=30)),
                ('destination_state', models.CharField(max_length=30)),
                ('destination_pin', models.IntegerField()),
                ('expecting_arrival', models.DateField(auto_now=True)),
                ('order_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer.order')),
            ],
        ),
        migrations.CreateModel(
            name='order_bets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('merchant_id', models.CharField(max_length=20)),
                ('bet_price', models.IntegerField()),
                ('extra_info', models.TextField()),
                ('pickup_days', models.IntegerField()),
                ('order_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customer.order')),
            ],
        ),
        migrations.CreateModel(
            name='images_by_customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='item_image')),
                ('item_information', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='customer.item_info')),
            ],
        ),
    ]
