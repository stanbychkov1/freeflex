from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from . import models


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.File
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Link
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):

    score = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Course
        fields = ('id', 'title', 'description', 'score',)


class CourseFullSerializer(serializers.ModelSerializer):
    file = FileSerializer(many=True, read_only=True, required=False)
    link = LinkSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = models.Course
        fields = ('id', 'title', 'description', 'score', 'file', 'link',)


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Subscription
        fields = '__all__'

    def validate(self, attrs):
        course = self.context.get('view').kwargs.get('id')
        user = self.context.get('request').user
        message = 'Вы уже подписаны на этот курс.'

        if models.Subscription.objects.filter(
                user=user, course=course).exists():
            raise serializers.ValidationError(message)
        return attrs


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Rating
        fields = ('rating',)

    def validate(self, attrs):
        course = self.context.get('view').kwargs.get('id')
        user = self.context.get('request').user
        message = 'Вы уже оставляли оценку этому курсу.'

        if models.Rating.objects.filter(
                user=user, course=course).exists():
            raise serializers.ValidationError(message)
        return attrs


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ('username', 'password',)

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(UserRegistrationSerializer, self).create(validated_data)


