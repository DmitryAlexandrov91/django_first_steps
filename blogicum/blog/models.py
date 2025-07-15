from datetime import datetime

from django.db import models
from django.contrib.auth import get_user_model

from core.models import PublishedModel

User = get_user_model()


class Category(PublishedModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы латиницы,'
                  ' цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'


class Location(PublishedModel):
    name = models.CharField(
        max_length=256,
        verbose_name='Название места')

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class PostQuerySet(models.QuerySet):
    def related_data(self):
        return self.select_related(
            'category', 'location', 'author')

    def base_filters(self):
        return self.filter(
            is_published=True,
            category__is_published=True,
            pub_date__date__lte=datetime.now()
        )


class PostManager(models.Manager):
    def get_posts_qs(self):
        return (
            PostQuerySet(self.model)
            .related_data()
            .base_filters()
        )


class Post(PublishedModel):
    title = models.CharField(
        max_length=256,
        verbose_name='Заголовок')
    text = models.TextField(
        verbose_name='Текст'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем'
                  ' — можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name='Категория'
    )
    objects = PostQuerySet.as_manager()
    published = PostManager()

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
