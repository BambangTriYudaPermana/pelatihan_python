from django.urls import path, include
from .views import RecipeListCreate, DaftarResepMakananView, LoginAPIView, RecipeCreateView, CategoryList, LevelList
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from recipes.view.login import LoginView
from recipes.view.signup import SignupView
from recipes.view.recipe import RecipeListView,RecipeDetailView



urlpatterns = [
    path('login/', LoginView.as_view()),
    path('sign-up/', SignupView.as_view()),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('recipes/', RecipeListCreate.as_view(), name='recipe-list-create'),
    path('book-recipe/book-recipes/', DaftarResepMakananView.as_view(), name='daftar-resep-makanan'),
    path('create-recipe/', RecipeCreateView.as_view(), name='create-recipe'),

    path('recipes-list/', RecipeListView.as_view(), name='recipe-list'),
    path('recipes-detail/<int:recipe_id>/', RecipeDetailView.as_view(), name='recipe-detail'),

    path('category/', CategoryList.as_view()),
    path('level/', LevelList.as_view()),

]