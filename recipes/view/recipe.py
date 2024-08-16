from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from recipes.models import Recipes, Categories, Levels, FavoriteFoods
from recipes.serializers import RecipeSerializer
from rest_framework.exceptions import NotFound, ValidationError
from django.core.exceptions import FieldError
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta,datetime
from rest_framework.views import APIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction,connection
import os

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

from django.utils import timezone



class RecipeListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    
    def get_queryset(self):
        queryset = Recipes.objects.all()
        queryset = queryset.filter(is_deleted=False)
        
        sort_by = self.request.query_params.get('sortBy', None)
        if sort_by:
            sort_field, sort_order = sort_by.split(',')
            if sort_order == 'desc':
                sort_field = f'-{sort_field}'
            queryset = queryset.order_by(sort_field)
        else:
            queryset = queryset.order_by('recipe_name') 

        return queryset

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.get_queryset()
            page_size = int(request.query_params.get('pageSize', 10))
            page_number = int(request.query_params.get('pageNumber', 1))
            
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            page = paginator.paginate_queryset(queryset, request)

            if page is None:
                raise NotFound(detail="Page not found")

            serializer = self.get_serializer(page, many=True)
            
            response_data = {
                'total': queryset.count(),
                'next': paginator.get_next_link(),
                'previous': paginator.get_previous_link(),
                'results': serializer.data,
                'message': 'Success',
                'statusCode': 200,
                'status': 'Success'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        
        except FieldError as fe:
            return Response({
                'message': f'Invalid field: {str(fe)}',
                'statusCode': 400,
                'status': 'Error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except ValidationError as ve:
            return Response({
                'message': f'Validation error: {str(ve)}',
                'statusCode': 400,
                'status': 'Error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except NotFound as nf:
            return Response({
                'message': f'{str(nf)}',
                'statusCode': 404,
                'status': 'Error'
            }, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return Response({
                'message': f'An unexpected error occurred: {str(e)}',
                'statusCode': 500,
                'status': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                document = request.FILES
                if not document: 
                    document is None
                else:
                    document = request.FILES['files']
                    upload_files(document,request.data.get('image_filename'))
                response_data = {
                    'data': serializer.data,
                    'message': 'Recipe created successfully',
                    'statusCode': 201,
                    'status': 'Success'
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
        
        except ValidationError as ve:
            return Response({
                'message': f'Validation error: {str(ve)}',
                'statusCode': 400,
                'status': 'Error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'message': f'An unexpected error occurred: {str(e)}',
                'statusCode': 500,
                'status': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RecipeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RecipeSerializer
    queryset = Recipes.objects.filter(is_deleted=False)
    lookup_field = 'recipe_id'
    
    def put(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=False)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                # Handle file upload
                document = request.FILES.get('files', None)
                if document:
                    file_name = request.data.get('image_filename')
                    upload_files(document, file_name)
                    instance.save()
                    
                response_data = {
                    'data': serializer.data,
                    'message': 'Recipe updated successfully',
                    'statusCode': 200,
                    'status': 'Success'
                }
                return Response(response_data, status=status.HTTP_200_OK)
                
        except ValidationError as ve:
            return Response({
                'message': f'Validation error: {str(ve)}',
                'statusCode': 400,
                'status': 'Error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'message': f'An unexpected error occurred: {str(e)}',
                'statusCode': 500,
                'status': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                instance = self.get_object()
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                self.perform_update(serializer)

                param_is_favorite = request.data.get('is_favorite')
                if param_is_favorite:
                    check = FavoriteFoods.objects.exists(recipe_id=kwargs.get('recipe_id'))
                    if check:
                        FFood = FavoriteFoods.objects.create(
                            user_id=request.user.id,
                            recipe_id=kwargs.get('recipe_id'),
                            is_favorite= True,
                            created_by= request.user.id,
                            created_time=timezone.now(),
                            )
                # Handle file upload
                document = request.FILES.get('files', None)
                if document:
                    file_name = request.data.get('image_filename')
                    upload_files(document, file_name)
                    instance.save()
                    
                response_data = {
                    'data': serializer.data,
                    'message': 'Recipe berhasil diupdate',
                    'statusCode': 200,
                    'status': 'Success'
                }
                return Response(response_data, status=status.HTTP_200_OK)
                
        except ValidationError as ve:
            return Response({
                'message': f'Validation error: {str(ve)}',
                'statusCode': 400,
                'status': 'Error'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return Response({
                'message': f'An unexpected error occurred: {str(e)}',
                'statusCode': 500,
                'status': 'Error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            
def upload_files(file, file_name):
    if file:
        base_name, ext = os.path.splitext(file_name)
        if not ext:
           
            ext = '.jpg' 

        file_name = f"{base_name}{ext}"
        file_path = os.path.join('uploads', file_name)
        file_url = default_storage.save(file_path, ContentFile(file.read()))
        return file_url
    return None