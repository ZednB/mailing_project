# Generated by Django 4.2 on 2024-04-17 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0003_newsletter_end_mail_newsletter_start_mail'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsletter',
            options={'permissions': [('block user', 'Can block user'), ('deactivate', 'Can deactivate newsletter')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
