# Generated by Django 4.2 on 2024-11-28 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produit', '0001_initial'),
        ('commande', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='commande',
            name='produit_commande',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produit.produit'),
        ),
    ]
