from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Avg
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Course(models.Model):
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=1500)
    score = models.PositiveIntegerField(default=0)
    file = models.ManyToManyField(to='File', related_name='course')
    link = models.ManyToManyField(to='Link', related_name='course')

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='follower')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='followed_course')

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='rating')
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='rating')
    rating = models.PositiveIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, message='Минимальная оценка - 1'),
            MaxValueValidator(10, message='Максимальная оценка - 10')])

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'


class File(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='uploads/')

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'

    def __str__(self):
        return self.title


class Link(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField()

    class Meta:
        ordering = ('-pk',)
        verbose_name = 'Ссылка'
        verbose_name_plural = 'Ссылки'

    def __str__(self):
        return self.title


@receiver(post_save, sender=Rating, dispatch_uid="update_rating")
def update_rating(sender, instance, **kwargs):
    score = round(Rating.objects.filter(
        course=instance.course.id
    ).aggregate(Avg('rating')).get('rating__avg'))
    instance.course.score = score
    instance.course.save()
