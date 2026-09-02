from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, get_user_model

from .serializers import UserRegisterSerializer, UserSerializer, LoginSerializer ,LogoutSerializer

User = get_user_model()


# API ចុះឈ្មោះ (Register)
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate Token for newly registered user
        token, _ = Token.objects.get_or_create(user=user)

        data = serializer.data
        data['token'] = token.key

        return Response(data, status=status.HTTP_201_CREATED)


# API ចូលប្រើប្រាស់ (Login)
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer  # Tells DRF what fields to render in HTML

    def get(self, request):
        """Displays the HTML form in DRF's browsable API"""
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        }, status=status.HTTP_200_OK)

class LogoutView(APIView):
    # SessionAuthentication allows the browser's current login session to work here
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    def get(self, request):
        """Renders the HTML form inside the DRF browsable UI"""
        serializer = self.serializer_class()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """Handles the logout action submitted via the form"""
        # Delete token if using TokenAuthentication
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()

        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)




# API មើលព័ត៌មានផ្ទាល់ខ្លួន (Profile)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)