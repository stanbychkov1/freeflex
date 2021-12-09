from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from . import serializers, models, permissions, mixins


class CourseViewSet(mixins.PaginationMixin, ModelViewSet):
    queryset = models.Course.objects.all()
    serializer_class = serializers.CourseSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)


class SubscribeView(generics.CreateAPIView, generics.DestroyAPIView):
    serializer_class = serializers.SubscriptionSerializer

    def create(self, request, *args, **kwargs):
        course = get_object_or_404(models.Course,
                                   id=self.kwargs.get('id'))
        user = get_object_or_404(models.User,
                                 id=self.request.user.id)
        serializer = self.get_serializer(
            data={
                'user': user.id,
                'course': course.id
            })
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def get_object(self):
        course = get_object_or_404(models.Course,
                                   id=self.kwargs.get('id'))
        user = get_object_or_404(models.User,
                                 id=self.request.user.id)
        subscription = get_object_or_404(models.Subscription,
                                         user=user.id, course=course.id)
        return subscription


class RatingView(generics.CreateAPIView):
    serializer_class = serializers.RatingSerializer
    permission_classes = (permissions.IsSubscribedPerm,)

    def perform_create(self, serializer):
        course = get_object_or_404(models.Course,
                                   id=self.kwargs.get('id'))
        serializer.save(user=self.request.user, course=course)


class SubscribedCoursesView(mixins.PaginationMixin, generics.ListAPIView):
    serializer_class = serializers.CourseFullSerializer

    def get_queryset(self):
        user = get_object_or_404(models.User,
                                 id=self.request.user.id)
        return models.Course.objects.filter(followed_course__user=user)


class FileViewSet(mixins.PaginationMixin, ModelViewSet):
    queryset = models.File.objects.all()
    serializer_class = serializers.FileSerializer
    permission_classes = (permissions.IsAdminPerm,)


class LinkViewSet(mixins.PaginationMixin, ModelViewSet):
    queryset = models.Link.objects.all()
    serializer_class = serializers.LinkSerializer
    permission_classes = (permissions.IsAdminPerm,)


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = serializers.UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        message = f'Пользователь создан, получите токен для авторизации'
        return Response(message, status=status.HTTP_201_CREATED)
