"""View module for handling requests about game types"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tanksapi.models import Tank, Profile, Tag


class TankView(ViewSet):
    """Trophy Tanks tank view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single tank
        Returns:
            Response -- JSON serialized tank
        """
        tank = Tank.objects.get(pk=pk)
        serializer = TankSerializer(tank)
        return Response(serializer.data)

    def list(self, request):
        """Handle GET requests to get all tanks

        Returns:
            Response -- JSON serialized list of tanks
        """
        tanks = Tank.objects.order_by('-gallons')
        if "user" in request.query_params:
            profile = Profile.objects.get(user=request.auth.user)
            tanks = tanks.filter(profile=profile)

        serializer = TankSerializer(tanks, many=True)
        return Response(serializer.data)


    def create(self, request):
        print(request.data)
        profile = Profile.objects.get(user=request.auth.user)
        tags = Tag.objects.filter(pk__in=request.data["tags"])

        tank = Tank.objects.create(
            profile=profile,
            name=request.data["name"],
            gallons=request.data["gallons"],
            flora=request.data["flora"],
            fauna=request.data["fauna"],
            started_date=request.data["started_date"],
            noteworthy_comments=request.data["noteworthy_comments"],
            photo_url=request.data["photo_url"]
        )

        tank.tags.set(tags)
        serializer = TankSerializer(tank)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        try:
            tank = Tank.objects.get(pk=pk)
        except Tank.DoesNotExist:
            return Response({"error": "Tank not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update basic fields
        tank.name = request.data.get("name", tank.name)
        tank.gallons = request.data.get("gallons", tank.gallons)
        tank.flora = request.data.get("flora", tank.flora)
        tank.fauna = request.data.get("fauna", tank.fauna)
        tank.started_date = request.data.get("started_date", tank.started_date)
        tank.noteworthy_comments = request.data.get(
            "noteworthy_comments", tank.noteworthy_comments)
        tank.photo_url = request.data.get("photo_url", tank.photo_url)

        # Update the user (profile) associated with the tank if provided
        if "profile" in request.data:
            new_profile_id = request.data["profile"]
            try:
                new_profile = Profile.objects.get(pk=new_profile_id)
                tank.profile = new_profile
            except Profile.DoesNotExist:
                return Response({"error": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update tank tags if provided
        if "tags" in request.data:
            tags = Tag.objects.filter(pk__in=request.data["tags"])
            tank.tags.set(tags)

        tank.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)
        # tank = Tank.objects.get(pk=pk)
        # tank.name = request.data["name"]
        # tank.gallons = request.data["gallons"]
        # tank.flora = request.data["flora"]
        # tank.fauna = request.data["fauna"]
        # tank.started_date = request.data["started_date"]
        # tank.noteworthy_comments = request.data["noteworthy_comments"]
        # tank.photo_url = request.data["photo_url"]

        # # Update the user (profile) associated with the tank
        # new_profile_id = request.data["id"]
        # new_profile = Profile.objects.get(pk=new_profile_id)
        # tank.profile = new_profile

        # # Update tank tags using a list of tag objects
        # tag_ids = request.data["tags"]
        # tags = Tag.objects.filter(pk__in=tag_ids)
        # tank.tags.set(tags)

        # tank.save()

        # return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        tank = Tank.objects.get(pk=pk)
        tank.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class TankTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'label')


class ProfileTankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'full_name')


class TankSerializer(serializers.ModelSerializer):
    profile = ProfileTankSerializer(many=False)
    tags = TankTagSerializer(many=True)

    class Meta:
        model = Tank
        fields = ('id', 'profile', 'name', 'gallons',
                'flora', 'fauna', 'started_date', 'noteworthy_comments',
                'photo_url', 'tags')

