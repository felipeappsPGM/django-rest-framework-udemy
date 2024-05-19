
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Recipe
from recipes.serializers import RecipeSerializer, TagSerializer
from tag.models import Tag


@api_view(http_method_names=['GET', 'POST', 'OPTIONS'])
def recipe_api_list(request):
    if request.method == 'GET':
        recipes = Recipe.objects.get_published()[:10]
        serializer = RecipeSerializer(
            instance=recipes,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print(request.data)
        serializer = RecipeSerializer(
             data=request.data, 
            context={'request': request},
           
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        
            


@api_view(http_method_names=['GET', 'PATCH', 'OPTIONS', 'DELETE'])
def recipe_api_detail(request, pk):
    recipe = get_object_or_404(
         Recipe.objects.get_published(), pk=pk
     )
    if request.method == 'GET':
        serializer = RecipeSerializer(
            instance=recipe,
            many=False,
            context={'request': request}
        )
        return Response(serializer.data)
    
    elif request.method == 'PATCH':
        ...
        serializer = RecipeSerializer(
            instance=recipe, #enviar dados
            data=request.data,  #receber dados
            many=False,
            context={'request': request},
            partial= True, # indicar que quer editar apenas um campo ou mais
        )
        
        serializer.is_valid(raise_exception=True)
        serializer.save(
            
        )
        return Response(
            serializer.data,
            )
        
        
    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    #recipe = Recipe.objects.get_published().filter(pk=pk).first()
    
    # if recipe:
    #     serializer = RecipeSerializer(instance=recipe, many=False)
    #     return Response(serializer.data)
    
    # else:
    #     return Response(
    #         {
    #             'detail': 'Eita, receita não encontrada'
    #         },
    #         status=status.HTTP_404_NOT_FOUND
    #     )
    
@api_view(http_method_names=['GET', 'POST', 'OPTIONS'])
def tag_api_detail(request, pk):
    tag = get_object_or_404(
        Tag.objects.all(),
        pk=pk
    )
    serializer = TagSerializer(instance=tag, many=False, context = {'request': request})
    
    return Response(serializer.data)