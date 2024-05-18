from django.contrib.auth.models import User
from rest_framework import serializers

from recipes.models import Category, Recipe
from tag.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
    # id = serializers.IntegerField()
    # name = serializers.CharField()
    # slug = serializers.SlugField()

class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        #fields = all()
        fields = [
            'author', 'tags', 'description', 'public', 'id', 'category', 'tag_links', 'author_name',
            'preparation',
            'title', 'category_name', 'tags_objects', 'tag_links',
            ]
        
    id = serializers.IntegerField()
    title = serializers.CharField(max_length=65)
    description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(method_name="any_method_name", read_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), 
    )
    category_name = serializers.StringRelatedField(source = 'category', read_only=True)
    
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
        source='tags', read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        queryset=Tag.objects.all(),
        view_name='recipes:recipes_api_v2_tag'
    )
    
    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'