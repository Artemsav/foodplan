
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='название')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=25, verbose_name='Имя пользователя')),
                ('coocking_for', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='На скольких готовим')),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Название рецепта')),
                ('calories', models.DecimalField(decimal_places=2, max_digits=7)),
                ('proteins', models.DecimalField(decimal_places=2, max_digits=5)),
                ('fats', models.DecimalField(decimal_places=2, max_digits=5)),
                ('carbs', models.DecimalField(decimal_places=2, max_digits=5)),
                ('image', models.ImageField(upload_to='', verbose_name='картинка')),
                ('description', models.TextField(blank=True, max_length=200, verbose_name='описание')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recipes', to='foodservice.recipecategory', verbose_name='категория')),
            ],
            options={
                'verbose_name': 'рецепт',
                'verbose_name_plural': 'рецепты',
            },
        ),
        migrations.CreateModel(
            name='Allergie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Название алергии')),
                ('allergic_users', models.ManyToManyField(blank=True, null=True, related_name='allergies', to='foodservice.User', verbose_name='Аллергии')),
                
            ],
        ),
    ]
