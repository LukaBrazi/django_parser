# Generated by Django 3.0.6 on 2020-05-09 07:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('name', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='Brand name')),
                ('base_url', models.URLField(verbose_name='Base URL')),
            ],
            options={
                'verbose_name': 'Brand',
                'verbose_name_plural': 'Brands',
            },
        ),
        migrations.AlterModelOptions(
            name='car',
            options={'verbose_name': 'Car', 'verbose_name_plural': 'Cars'},
        ),
        migrations.AlterField(
            model_name='car',
            name='link',
            field=models.URLField(verbose_name='Link for Car'),
        ),
        migrations.AlterField(
            model_name='car',
            name='location',
            field=models.CharField(max_length=255, verbose_name='Location of car'),
        ),
        migrations.AlterField(
            model_name='car',
            name='price_in_uah',
            field=models.CharField(max_length=255, verbose_name='Price in UAH'),
        ),
        migrations.AlterField(
            model_name='car',
            name='price_in_usd',
            field=models.CharField(max_length=255, verbose_name='Price in USD'),
        ),
        migrations.AlterField(
            model_name='car',
            name='range',
            field=models.CharField(max_length=255, verbose_name='Car range'),
        ),
        migrations.AlterField(
            model_name='car',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Car title'),
        ),
        migrations.AddField(
            model_name='car',
            name='brand',
            field=models.ForeignKey(default='Other', on_delete=django.db.models.deletion.CASCADE, to='cars.Brand'),
        ),
    ]
