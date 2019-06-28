from rest_framework import serializers
from conduit.apps.profiles.serializers import ProfileSerializer
from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):

    author = ProfileSerializer(read_only=True)
    description = serializers.CharField(required=False)
    slug = serializers.SlugField(required=False)

    favorited = serializers.SerializerMethodField()
    favoritesCount = serializers.SerializerMethodField(
        method_name='get_favorites_count'
    )

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Article
        fields = ('author', 'body', 'createdAt', 'description', 'favorited', 'favoritesCount',
                  'slug', 'title', 'updatedAt', )

    def create(self, validated_data):
        author = self.context.get('author', None)
        print(author)
        return Article.objects.create(author=author, **validated_data)

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_favorited(self, instance):
        request = self.context.get('request', None)

        if request is None:
            return False

        if not request.user.is_authenticated:
            return False

        return request.user.profile.has_favorited(instance)

    def get_favorites_count(self, instance):
        return instance.favorited_by.count()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()


class CommentSerializer(serializers.ModelSerializer):

    author = ProfileSerializer(required=False)

    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')

    class Meta:
        model = Comment
        fields = (
            'id',
            'author',
            'body',
            'createdAt',
            'updatedAt',
        )

    def create(self, validated_data):
        article = self.context['article']
        author = self.context['author']

        return Comment.objects.create(
            author=author, article=article, **validated_data
        )

    def get_created_at(self, instance):
        return instance.created_at.isoformat()

    def get_updated_at(self, instance):
        return instance.updated_at.isoformat()
