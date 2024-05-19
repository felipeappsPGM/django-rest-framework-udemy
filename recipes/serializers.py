
from rest_framework import serializers

from authors.validators import AuthorRecipeValidator
from recipes.models import Recipe
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
            'id', 'title', 'description', 'author',
            'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_links',
            'preparation_time', 'preparation_time_unit', 'servings',
            'servings_unit',
            'preparation_steps', 'cover', "author_name"
            ]
        
    
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(method_name="any_method_name", read_only=True)
    
    category= serializers.StringRelatedField(read_only=True)
   
    author_name = serializers.StringRelatedField(read_only=True)
    
    
    tag_objects = TagSerializer(
        many=True,
        source='tags', read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        #queryset=Tag.objects.all(), tirei pq coloquei como somente leitura add o read_only
        view_name='recipes:recipes_api_v2_tag',
        read_only=True
    )
    
    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} {recipe.preparation_time_unit}'
    
    
    def validate(self, attrs):
        super_validate = super().validate(attrs)
        AuthorRecipeValidator(data=attrs, ErrorClass=serializers.ValidationError)

        
        return super_validate
