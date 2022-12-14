# Generated by Django 3.0.1 on 2022-08-26 15:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_clothing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Centre_Type',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Clothing_Disp_Centre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Council',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gov_area', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='Suburb',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('district', models.CharField(max_length=128)),
            ],
        ),
        migrations.RemoveField(
            model_name='ewastesite',
            name='site_id',
        ),
        migrations.AlterField(
            model_name='clothing',
            name='address',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='clothing',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ewastesite',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='ewastesite',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='clothing',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Suburb'),
        ),
        migrations.AlterField(
            model_name='clothing',
            name='name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Clothing_Disp_Centre'),
        ),
        migrations.AlterField(
            model_name='ewastesite',
            name='ownership',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Centre_Type'),
        ),
        migrations.AlterField(
            model_name='ewastesite',
            name='site',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.Council'),
        ),
    ]
