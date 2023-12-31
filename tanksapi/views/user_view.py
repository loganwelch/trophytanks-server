"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth.models import User
from tanksapi.models import Profile


class UserView(ViewSet):
    """Level up game types view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single user
        Returns:
            Response -- JSON serialized user
        """
        user = User.objects.get(pk=pk)
        profile = Profile.objects.get(user=user)
        serializer = UserSerializer(user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all users

        Returns:
            Response -- JSON serialized list of users
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, pk):
        user = User.objects.get(pk=pk)
        user.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class ProfileSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""

    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'full_name')


class UserSerializer(serializers.ModelSerializer):
    """JSON serializer for customers"""

    class Meta:
        model = User
        fields = ('id', 'username', 'last_name', 'first_name',
                'email', 'date_joined', 'is_staff')
