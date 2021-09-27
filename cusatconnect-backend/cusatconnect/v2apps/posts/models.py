from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation

from v2apps.accounts.models import User


class Activity(models.Model):
    LOVE = 'L'
    ANGRY = 'A'
    UP_VOTE = 'U'
    DOWN_VOTE = 'D'
    ACTIVITY_TYPES = (
        (LOVE, 'Love'),
        (ANGRY, 'Angry'),
        (UP_VOTE, 'Up Vote'),
        (DOWN_VOTE, 'Down Vote'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)

    # Below the mandatory fields for generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()


class Post(models.Model):

    post_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='user')
    post_description = models.TextField(_('Post Description'), max_length=500, blank=True)
    post_image = models.ImageField(_('Post Image'), blank=True, upload_to='Post_Images/')
    date = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation(Activity)

    # def __str__(self):
    #     return self.post_owner.first_name


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    comment = models.TextField(_('Comment'), max_length=500, blank=True)
    comment_owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)
    activities = GenericRelation(Activity)

    # def __str__(self):
    #     return self.p
