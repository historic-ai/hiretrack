from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
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