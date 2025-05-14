from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ProductListView, ProductDetailView,
    CategoryListView, CategoryDetailView,
    CommentCreateView, LikeCreateView, RatingCreateView,
    UserProfileView, WishlistView, AdminProductCreateView,
    RegisterView, LoginView
)

# Swagger schema va view'ni import qilish
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger schema yaratish
schema_view = get_schema_view(
   openapi.Info(
      title="OILAM UCHUN E-Commerce API",
      default_version='v1',
      description="API hujjati",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@oilamuchun.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
)

# URL'lar ro'yxati
urlpatterns = [
    # Kategoriya URL'lari
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    
    # Mahsulot URL'lari
    path('products/', ProductListView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    
    # Izoh URL'lari
    path('comments/', CommentCreateView.as_view(), name='comment-create'),
    
    # Layk URL'lari
    path('likes/', LikeCreateView.as_view(), name='like-create'),
    
    # Reyting URL'lari
    path('ratings/', RatingCreateView.as_view(), name='rating-create'),
    
    # Foydalanuvchi profili URL'lari
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    
    # Wishlist URL'lari
    path('wishlist/', WishlistView.as_view(), name='wishlist'),
    
    # Admin mahsulot qo'shish URL'i
    path('admin/products/', AdminProductCreateView.as_view(), name='admin-product-create'),
    
    # Ro‘yxatdan o‘tish va Login URL'lari
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    
    # Swagger API hujjatlari uchun URL
    path('swagger/', schema_view.as_view(), name='swagger'),  # Swagger URL qo'shish
]
