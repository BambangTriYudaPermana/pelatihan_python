# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Categories(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)
    modified_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'categories'


class FavoriteFoods(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(blank=True, null=True)
    recipe_id = models.BigIntegerField(blank=True, null=True)
    is_favorite = models.BooleanField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)
    modified_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favorite_foods'


class HowToCooks(models.Model):
    how_to_cook_id = models.BigIntegerField(primary_key=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    position = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'how_to_cooks'


class Ingridients(models.Model):
    ingridient_id = models.BigIntegerField(primary_key=True)
    ingridient_measurement = models.CharField(max_length=255, blank=True, null=True)
    ingridient_name = models.CharField(max_length=255, blank=True, null=True)
    ingridient_quantity = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ingridients'


class Levels(models.Model):
    level_id = models.AutoField(primary_key=True)
    level_name = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)
    modified_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'levels'


class RecipeHowToCook(models.Model):
    how_to_cook = models.OneToOneField(HowToCooks, models.DO_NOTHING, primary_key=True)  # The composite primary key (how_to_cook_id, recipe_id) found, that is not supported. The first column is selected.
    recipe = models.ForeignKey('Recipes', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_how_to_cook'
        unique_together = (('how_to_cook', 'recipe'),)


class RecipeIngridient(models.Model):
    ingridient = models.OneToOneField(Ingridients, models.DO_NOTHING, primary_key=True)  # The composite primary key (ingridient_id, recipe_id) found, that is not supported. The first column is selected.
    recipe = models.ForeignKey('Recipes', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'recipe_ingridient'
        unique_together = (('ingridient', 'recipe'),)


class Recipes(models.Model):
    recipe_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Categories, models.DO_NOTHING, blank=True, null=True)
    level = models.ForeignKey(Levels, models.DO_NOTHING, blank=True, null=True)
    recipe_name = models.CharField(max_length=255, blank=True, null=True)
    image_filename = models.TextField(blank=True, null=True)
    time_cook = models.IntegerField(blank=True, null=True)
    ingredient = models.TextField(blank=True, null=True)
    how_to_cook = models.TextField(blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    is_favorite = models.BooleanField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)
    modified_time = models.DateTimeField(blank=True, null=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'recipes'


class Roles(models.Model):
    role_id = models.BigIntegerField(primary_key=True)
    role_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'roles'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    fullname = models.CharField(max_length=255, blank=True, null=True)
    password = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=100, blank=True, null=True)
    is_deleted = models.BooleanField(blank=True, null=True)
    created_by = models.CharField(max_length=255, blank=True, null=True)
    created_time = models.DateTimeField(blank=True, null=True)
    modified_by = models.CharField(max_length=255, blank=True, null=True)
    modified_time = models.DateTimeField(blank=True, null=True)
    role_0 = models.ForeignKey(Roles, models.DO_NOTHING, db_column='role_id', blank=True, null=True)  # Field renamed because of name conflict.

    class Meta:
        managed = False
        db_table = 'users'