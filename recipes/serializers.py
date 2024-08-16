# from rest_framework import serializers
# from .models import Recipes, Categories, Levels


# class RecipeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Recipes
        # fields = '__all__'

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Categories
#         fields = ['category_id', 'category_name']

# class LevelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Levels
#         fields = ['level_id', 'level_name']

# class RecipeSerializer(serializers.ModelSerializer):
#     Categories = CategorySerializer(source='category',read_only=True)
#     Levels = LevelSerializer(source='level',read_only=True, )

#     class Meta:
#         model = Recipes
#         fields = [
#             'recipe_id', 'recipe_name', 'image_url', 'time', 'is_favorite', 'category', 'level'
#         ]

# serializers.py
from rest_framework import serializers
from .models import Recipes, Categories, Levels, Users

from rest_framework import serializers
from django.contrib.auth import authenticate

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['category_id', 'category_name']  # Use field names as defined in the Categories model

class LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Levels
        fields = ['level_id', 'level_name']  # Use field names as defined in the Levels model

class RecipeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Match the model field name
    level = LevelSerializer(read_only=True)  # Match the model field name

    class Meta:
        model = Recipes
        fields = [
            'recipe_id', 'recipe_name', 'image_url', 'time', 'is_favorite', 'category', 'level'
        ]
    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError("Login gagal. Username atau password salah.")
        else:
            raise serializers.ValidationError("Username dan password harus diisi.")

        data['user'] = user
        return data