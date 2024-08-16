import logging
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from recipes.models import Users
from django.db import IntegrityError

import bcrypt

logger = logging.getLogger(__name__)

class SignupView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        try:
            username = request.data.get('username')
            fullname = request.data.get('fullname')
            password = request.data.get('password')
            retypePassword = request.data.get('retypePassword')
            email = request.data.get('email')

            # Validasi input
            if not username or not password or not email:
                response_data = {
                    'message': 'Username, password, dan email harus diisi.'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Cek apakah user dengan username yang sama sudah ada
            if User.objects.filter(username=username).exists():
                response_data = {
                    'message': 'Username sudah digunakan.'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            if password != retypePassword:
                response_data = {
                    'message': 'Password berbeda.'
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

            # Buat user baru
            user = User.objects.create_user(username=username, password=password, email=email) #auth_user
            user.save()

            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            users = Users.objects.create(username=username, fullname=fullname, password=password, role='User', is_deleted='f', created_by='admin') #user
            users.save()
            
            response_data = {
                'message': f"User {username} registered successfully!",
                "statusCode": status.HTTP_200_OK,
                "status": "TRUE"
            }

            logger.info(f"User {username} berhasil dibuat")
            return Response(response_data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            logger.error(f"IntegrityError during signup: {str(e)}")
            response_data = {
                'message': 'Terjadi kesalahan pada pembuatan user.'
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except Exception as e:
            logger.error(f"An error occurred during signup: {str(e)}")
            return Response([], status=status.HTTP_500_INTERNAL_SERVER_ERROR)