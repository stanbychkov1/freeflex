from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()

router.register('courses', views.CourseViewSet)
router.register('files', views.FileViewSet)
router.register('links', views.LinkViewSet)

extrapatterns = [
    path('', include(router.urls)),
    path(r'courses/<int:id>/subscribe/',
         views.SubscribeView.as_view()),
    path(r'courses/<int:id>/rating/',
         views.RatingView.as_view()),
    path('subscribed_courses/',
         views.SubscribedCoursesView.as_view()),
]

urlpatterns = [
    path('v1/', include(extrapatterns) ),
]
