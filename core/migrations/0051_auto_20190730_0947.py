# Generated by Django 2.1.10 on 2019-07-30 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0050_history'),
    ]

    operations = [
        migrations.CreateModel(
            name='DepartmentalTeam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Department')),
            ],
        ),
        migrations.AddField(
            model_name='asset',
            name='team_name',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.DepartmentalTeam'),
        ),
        migrations.AddField(
            model_name='assetassignee',
            name='team',
            field=models.ForeignKey(blank=True, default=None, help_text='refers to the specific team within a department to which an asset is assigned', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.DepartmentalTeam'),
        ),
        migrations.AddField(
            model_name='assetowner',
            name='team',
            field=models.ForeignKey(blank=True, default=None, help_text='refers to the specific team within a department to which an asset is assigned', null=True, on_delete=django.db.models.deletion.CASCADE, to='core.DepartmentalTeam'),
        ),
        migrations.AddField(
            model_name='user',
            name='team',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='core.DepartmentalTeam'),
        ),
    ]
