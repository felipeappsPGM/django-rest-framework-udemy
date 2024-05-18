from django.contrib.auth.models import User
from rest_framework import serializers

from recipes.models import Category
from tag.models import Tag


class TagSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    slug = serializers.SlugField()

class RecipeSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published')
    preparation = serializers.SerializerMethodField(method_name="any_method_name")
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )
    category_name = serializers.StringRelatedField(source = 'category',)
    
    author = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all()
    )
    author_name = serializers.StringRelatedField(source = 'author')
    
    tags = serializers.PrimaryKeyRelatedField(
        queryset = Tag.objects.all(),
        many=True,
    )
    tags_objects = TagSerializer(
        many=True,
        source='tags',
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        queryset=Tag.objects.all(),
        view_name='recipes:recipes_api_v2_tag'
    )
    
    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'