# Generated by Django 3.2.19 on 2023-10-20 02:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('invite', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='employee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='invites', to='invite.employee', to_field='employee_id', verbose_name='邀请人'),
        ),
    ]
