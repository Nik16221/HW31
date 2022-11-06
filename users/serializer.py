from rest_framework import serializers
from users.models import Location, User


class UserCreateSerializer(serializers.ModelSerializer):
    location = serializers.SlugRelatedField(required=False,
                                            queryset=Location.objects.all(),
                                            many=True,
                                            slug_field='name')

    def is_valid(self, *, raise_exception=False):
        self.locations = self.initial_data.pop('location', [])
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_date):
        user = User.objects.create(**validated_date)
        for loc_name in self.locations:
            location, _ = Location.objects.get_or_create(name=loc_name)
            user.location.add(location)
        return user

    class Meta:
        model = User
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"
