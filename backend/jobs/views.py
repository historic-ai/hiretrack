from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import JobApplication
from .serializers import JobApplicationSerializer

# GET all applications of logged in user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_applications(request):
    applications = JobApplication.objects.filter(user=request.user)
    serializer = JobApplicationSerializer(applications, many=True)
    return Response(serializer.data)

# POST create new application
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_application(request):
    serializer = JobApplicationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# GET single application by id
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_single_application(request, pk):
    try:
        application = JobApplication.objects.get(pk=pk, user=request.user)
    except JobApplication.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = JobApplicationSerializer(application)
    return Response(serializer.data)

# PUT update application
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_application(request, pk):
    try:
        application = JobApplication.objects.get(pk=pk, user=request.user)
    except JobApplication.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = JobApplicationSerializer(application, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# DELETE application
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_application(request, pk):
    try:
        application = JobApplication.objects.get(pk=pk, user=request.user)
    except JobApplication.DoesNotExist:
        return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
    application.delete()
    return Response({'message': 'Deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# REGISTER
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    # Check if all fields are given
    if not username or not email or not password:
        return Response(
            {'error': 'Please provide username, email and password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check if username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already taken'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Create the user
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )

    # Create token for this user
    token = Token.objects.create(user=user)

    return Response({
        'message': 'Account created successfully',
        'token': token.key,
        'username': user.username
    }, status=status.HTTP_201_CREATED)


# LOGIN
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {'error': 'Please provide username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check username and password
    user = authenticate(username=username, password=password)

    if not user:
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Get or create token
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        'message': 'Login successful',
        'token': token.key,
        'username': user.username
    })


# LOGOUT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    # Delete the token — user must login again to get new token
    request.user.auth_token.delete()
    return Response({'message': 'Logged out successfully'})