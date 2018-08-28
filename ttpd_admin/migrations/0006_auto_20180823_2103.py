# Generated by Django 2.0.6 on 2018-08-23 13:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ttpd_admin', '0005_auto_20180823_2102'),
    ]

    operations = [
        migrations.CreateModel(
            name='TechnologyGenerators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Generators')),
                ('technology', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ttpd_admin.Technologies')),
            ],
            options={
                'verbose_name': 'technology generators',
                'verbose_name_plural': 'technology generators',
            },
        ),
        migrations.AddField(
            model_name='technologies',
            name='generators',
            field=models.ManyToManyField(blank=True, through='ttpd_admin.TechnologyGenerators', to='ttpd_admin.Generators'),
        ),
    ]