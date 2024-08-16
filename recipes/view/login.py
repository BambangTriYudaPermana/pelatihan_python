import logging

import bcrypt
from django.http import HttpResponseServerError
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import timedelta,datetime
from django.contrib.auth import authenticate



from ..models import Users

logger = logging.getLogger(__name__)


class LoginView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []
    
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            
            user = authenticate(username=username, password=password)
            
            if user is not None:
                profile = Users.objects.filter(username=user.username).first()
                token = generate_jwt_token(user)
                response_data = {
                    'data' : {
                        'id' : user.id,
                        'token' : token,
                        'type' : 'django',
                        'username' : user.username,
                        'role' : profile.role
                    },
                    'message' : 'Success',
                    "statusCode": status.HTTP_200_OK,
                    "status": "TRUE"
                }
                return Response(response_data, status=status.HTTP_200_OK)       
            else:
                response_data = {
                    'token' : '',
                    'message' : "Username dan Password Tidak Sesuai",
                    "statusCode": status.HTTP_200_OK,
                    "status": "FALSE"
                }
                logger.info(f"User tidak ditemukan euy")
                return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"An error occurred during login: {str(e)}")
            return Response([], status=status.HTTP_400_BAD_REQUEST)
        
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