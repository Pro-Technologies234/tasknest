from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenRefreshView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import logging
logger = logging.getLogger('django')

from .serializers import (
    UserRegistrationSerializer,
    CustomUserSerializer,
    UserUpdateSerializer,
)

CustomUser = get_user_model()

# ---------------------------------------------------------------------
# Register View
# ---------------------------------------------------------------------
@swagger_auto_schema(method='post', request_body=UserRegistrationSerializer, responses={201: UserRegistrationSerializer})
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'details': f'User {user.email} was Registered Successfully',
                'user': CustomUserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.exception("Registration failed with exception")
            return Response({'detail': 'Server error occurred.'}, status=500)

    logger.debug(f"Registration errors: {serializer.errors}")
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



login_schema = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'email': openapi.Schema(type=openapi.TYPE_STRING),
        'password': openapi.Schema(type=openapi.TYPE_STRING),
    },
    required=['email', 'password']
)

@swagger_auto_schema(method='post', request_body=login_schema, responses={200: CustomUserSerializer})
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(request, email=email, password=password)

    if not user:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    return Response({
        'user': CustomUserSerializer(user).data,
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    })


# --

# ---------------------------------------------------------------------
# Logout View
# ---------------------------------------------------------------------

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        required=['refresh'],
        properties={'refresh': openapi.Schema(type=openapi.TYPE_STRING)}
    ),
    responses={200: 'Logged out successfully'}
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
    except KeyError:
        return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
    except TokenError:
        return Response({"detail": "Invalid or expired token."}, status=status.HTTP_400_BAD_REQUEST)

# ---------------------------------------------------------------------
# Update User Profile View
# ---------------------------------------------------------------------
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
    Updates the authenticated user's profile.
    """
    user = request.user
    serializer = UserUpdateSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(CustomUserSerializer(user).data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------------------
# Get Current User Profile
# ---------------------------------------------------------------------
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_user_profile(request):
#     """
#     Retrieves the authenticated user's profile.
#     """
#     user = request.user
#     serializer = CustomUserSerializer(user)
#     return Response(serializer.data, status=status.HTTP_200_OK)


@swagger_auto_schema(method='get', responses={200: CustomUserSerializer})
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    print("[DEBUG] Demo Project trying to get User.")
    try:
        user = request.user
        if user is None:
            print("User not found.")
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"detail": f"An error occurred: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )