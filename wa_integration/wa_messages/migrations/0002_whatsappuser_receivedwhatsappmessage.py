# Generated by Django 4.2.17 on 2024-12-23 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wa_messages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhatsappUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wa_id', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReceivedWhatsappMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_type', models.CharField(blank=True, default='text', max_length=32)),
                ('content', models.TextField(blank=True, max_length=4096)),
                ('sent_time', models.DateTimeField()),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wa_messages.whatsappuser')),
            ],
        ),
    ]
