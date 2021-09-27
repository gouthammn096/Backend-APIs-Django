from rest_framework import serializers

from .models import Post, Comment, Activity


class PostSerializer(serializers.ModelSerializer):

    post_owner_first_name = serializers.ReadOnlyField(source='post_owner.first_name')
    post_owner_last_name = serializers.ReadOnlyField(source='post_owner.last_name')

    class Meta:
        fields = ('id', 'post_description', 'post_image', 'post_owner',
                  'post_owner_first_name', 'post_owner_last_name',)
        model = Post


class CommentSerializer(serializers.ModelSerializer):

    comment_owner_first_name = serializers.ReadOnlyField(source='comment_owner.first_name')
    comment_owner_last_name = serializers.ReadOnlyField(source='comment_owner.last_name')

    class Meta:
        fields = ('id', 'post', 'comment', 'comment_owner_first_name',
                  'comment_owner_last_name', 'up_vote', 'down_vote')
        model = Comment


class LikeGetSerializer(serializers.ModelSerializer):
    activity_count = serializers.SerializerMethodField()
    love_count = serializers.SerializerMethodField()
    angry_count = serializers.SerializerMethodField()
    up_vote_count = serializers.SerializerMethodField()
    down_vote_count = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'activity_count', 'love_count', 'angry_count', 'up_vote_count', 'down_vote_count', )
        model = Post

    def get_activity_count(self, obj):
        post = Post.objects.get(id=obj.id)
        return post.activities.count()

    def get_love_count(self, obj):
        post = Post.objects.get(id=obj.id)
        return post.activities.filter(activity_type=Activity.LOVE).count()

    def get_angry_count(self, obj):
        post = Post.objects.get(id=obj.id)
        return post.activities.filter(activity_type=Activity.ANGRY).count()

    def get_up_vote_count(self, obj):
        post = Post.objects.get(id=obj.id)
        return post.activities.filter(activity_type=Activity.UP_VOTE).count()

    def get_down_vote_count(self, obj):
        post = Post.objects.get(id=obj.id)
        return post.activities.filter(activity_type=Activity.DOWN_VOTE).count()


class LikeSerializer(serializers.ModelSerializer):

    like_owner_first_name = serializers.ReadOnlyField(source='user.first_name')
    like_owner_last_name = serializers.ReadOnlyField(source='user.last_name')

    class Meta:
        fields = ('id', 'user', 'activity_type', 'like_owner_first_name',
                  'like_owner_last_name', 'content_type', 'object_id',)
        model = Activity
