# from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from .models import Recipes, Categories, Levels
from .serializers import RecipeSerializer, CategorySerializer, LevelSerializer
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth import login
from .serializers import LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta,datetime
# Create your views here.

class RecipeListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Recipes.objects.all()
    serializer_class = RecipeSerializer

class CategoryList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer

    def list(self, request, *args, **kwargs):
        # Call the original list method to get the data
        response = super().list(request, *args, **kwargs)
        
        # Customize the response format
        data = response.data
        custom_response = {
            "data": data,
            "message": "Sukses",
            "statusCode": status.HTTP_200_OK,
            "status": "OK"
        }
        
        return Response(custom_response, status=status.HTTP_200_OK)
    

class LevelList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Levels.objects.all()
    serializer_class = LevelSerializer

    def list(self, request, *args, **kwargs):
        # Call the original list method to get the data
        response = super().list(request, *args, **kwargs)
        
        # Customize the response format
        data = response.data
        custom_response = {
            "data": data,
            "message": "Sukses",
            "statusCode": status.HTTP_200_OK,
            "status": "OK"
        }
        
        return Response(custom_response, status=status.HTTP_200_OK)
    
class DaftarResepMakananView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # recipe_name = request.data.get('recipe_name')
        # Filter recipes for the specified user
        recipe_name = request.query_params.get('recipe_name', '')
        if recipe_name:
            recipes = Recipes.objects.filter(recipe_name__icontains=recipe_name).order_by('recipe_name')
        else:
            recipes = Recipes.objects.all().order_by('recipe_name')
            
        # recipes = Recipes.objects.filter(recipe_name=recipe_name)
        serializer = RecipeSerializer(recipes, many=True)

        formatted_data = []
        for recipe in serializer.data:
            formatted_data.append({
                "recipeId": recipe['recipe_id'],
                "categories": {
                    "categoryId": recipe['category']['category_id'], 
                    "categoryName": recipe['category']['category_name'] 
                },
                "levels": {
                    "levelId": recipe['level']['level_id'],
                    "levelName": recipe['level']['level_name']  
                },
                "recipeName": recipe['recipe_name'],
                "imageUrl": recipe['image_url'],  
                "time": recipe['time'],  
                "isFavorite": recipe['is_favorite']  
            })

        response_data = {
            "total": recipes.count(),
            "data": formatted_data,
            "message": "Berhasil memuat Resep Masakan",
            "statusCode": status.HTTP_200_OK,
            "status": "OK"
        }


        return Response(response_data, status=status.HTTP_200_OK)

class RecipeCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "This is a protected view"})

class LoginAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            token = generate_jwt_token(user)
            return Response(
                {
                    "token": token,
                    "message": "Login berhasil!"
                }, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)
    refresh['user_id'] = user.id

    expired_time = datetime.now() + timedelta(days=1)
    expired_formatted = expired_time.strftime("%d/%m/%Y %H:%M:%S")

    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
        'expired' : expired_formatted
    }