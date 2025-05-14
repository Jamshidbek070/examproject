from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Category, Product, ProductImage, UserProfile, Comment, Like, Rating
from .serializers import (
    CategorySerializer, ProductSerializer, ProductImageSerializer,
    UserProfileSerializer, CommentSerializer, LikeSerializer, RatingSerializer
)
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from .serializers import RegisterSerializer, LoginSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token


# 1️⃣ Kategoriya API (List va Detail)
class CategoryListView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# 2️⃣ Mahsulot API (List, Detail)
class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# 3️⃣ Izoh API (Create va List)
class CommentCreateView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        serializer.save(user=self.request.user, product=product)


# 4️⃣ Layk API (Create va List)
class LikeCreateView(generics.CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        serializer.save(user=self.request.user, product=product)


# 5️⃣ Reyting API (Create va List)
class RatingCreateView(generics.CreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        product = Product.objects.get(id=self.request.data['product'])
        serializer.save(user=self.request.user, product=product)


# 6️⃣ Foydalanuvchi profili (GET va Update)
class UserProfileView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile


# 7️⃣ Wishlist API (Add va Remove mahsulotlar)
class WishlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile
        serializer = ProductSerializer(profile.wishlist.all(), many=True)
        return Response(serializer.data)

    def post(self, request):
        product = Product.objects.get(id=request.data['product_id'])
        request.user.profile.wishlist.add(product)
        return Response({'status': 'added to wishlist'}, status=201)

    def delete(self, request):
        product = Product.objects.get(id=request.data['product_id'])
        request.user.profile.wishlist.remove(product)
        return Response({'status': 'removed from wishlist'}, status=204)


# 8️⃣ Admin mahsulot qo‘shish uchun faqat admin
class AdminProductCreateView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            return Response({
                'user': RegisterSerializer(user).data,
                'token': token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# 2️⃣ Foydalanuvchi tizimga kirish (Login)
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.filter(username=serializer.validated_data['username']).first()
            if user and user.check_password(serializer.validated_data['password']):
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'user': RegisterSerializer(user).data,
                    'token': token.key
                }, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)