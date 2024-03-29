# Generated by Django 4.1.1 on 2022-09-07 19:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colour', models.CharField(max_length=100, verbose_name='Spalva')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=30, unique=True)),
                ('name', models.CharField(max_length=200, verbose_name='Pavadinimas')),
                ('summary', models.TextField(blank=True, help_text='Trumpas spintos aprašymas', max_length=1000, verbose_name='Aprašymas')),
                ('colour', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='colours', to='woodwork.colour')),
            ],
        ),
        migrations.CreateModel(
            name='Type',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Įveskite spintos tipą (pvz. miegamojo drabužinė)', max_length=200, verbose_name='Tipas')),
            ],
        ),
        migrations.CreateModel(
            name='ProductInstance',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, help_text='Unikalus ID spintos kopijai', primary_key=True, serialize=False)),
                ('due_back', models.DateField(blank=True, null=True, verbose_name='Bus galima užsakyti')),
                ('status', models.CharField(blank=True, choices=[('a', 'Užsakoma'), ('p', 'Užsakyta'), ('g', 'Galima užsakyti'), ('r', 'Rezervuota')], default='a', help_text='Statusas', max_length=1)),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='woodwork.product')),
            ],
            options={
                'ordering': ['due_back'],
            },
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.ManyToManyField(help_text='Išrinkite tipą(us) šiai spintai', to='woodwork.type'),
        ),
    ]
