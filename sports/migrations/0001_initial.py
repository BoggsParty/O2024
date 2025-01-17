# Generated by Django 4.1 on 2024-07-18 20:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('athlete', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numeric_code', models.IntegerField()),
                ('full_name', models.CharField(default='', max_length=200)),
                ('abbreviation', models.CharField(default='', help_text='Alpha-3', max_length=3)),
            ],
            options={
                'verbose_name': 'County',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.CreateModel(
            name='Sport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport_name', models.CharField(default='', max_length=200)),
                ('slug', models.SlugField(default='')),
                ('order', models.IntegerField(default=100)),
                ('active', models.BooleanField(default=False)),
                ('ass_link', models.URLField(blank=True, help_text='The official website of sports international governing body.')),
                ('team', models.BooleanField(default=True)),
                ('locked', models.BooleanField(default=False)),
                ('awarded', models.BooleanField(default=False)),
                ('lock_date', models.DateField(blank=True)),
                ('awarded_date', models.DateField(blank=True)),
                ('athletes', models.ManyToManyField(blank=True, to='sports.athlete')),
                ('bronze_athlete', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ba', to='sports.athlete')),
                ('bronze_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='bc', to='sports.country')),
                ('country_teams', models.ManyToManyField(blank=True, to='sports.country')),
                ('gold_athlete', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ga', to='sports.athlete')),
                ('gold_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='gc', to='sports.country')),
                ('silver_athlete', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sa', to='sports.athlete')),
                ('silver_country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sc', to='sports.country')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('icon', models.ImageField(blank=True, upload_to='')),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('sport', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sports.sport')),
            ],
            options={
                'verbose_name': 'Images',
                'verbose_name_plural': 'Images',
            },
        ),
    ]
