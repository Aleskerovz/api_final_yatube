from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models

User = get_user_model()

NUM_CHARACTERS = 15


class Group(models.Model):
    title = models.CharField('Заголовок', max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField('Описание')

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'

    def __str__(self):
        return self.title


class Post(models.Model):
    text = models.TextField('Текст')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        'Картинка',
        upload_to='posts/', blank=True)
    group = models.ForeignKey(
        Group, on_delete=models.SET_NULL,
        related_name='posts', blank=True, null=True
    )

    class Meta:
        verbose_name = 'Публикацию'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.text[:NUM_CHARACTERS]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Автор',)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name='comments',
        verbose_name='Публикация',)
    text = models.TextField('Текст комментария')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:NUM_CHARACTERS]


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик')
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор')

    class Meta:
        verbose_name = 'Подписчика'
        verbose_name_plural = 'Подписчики'

    def clean(self):
        if self.user == self.following:
            raise ValidationError('Нельзя подписаться на самого себя')
        if Follow.objects.filter(
                user=self.user, following=self.following).exists():
            raise ValidationError(
                'Вы уже подписаны на данного пользователя')

    def __str__(self):
        return f'{self.user.username} подписан на {self.following.username}'
