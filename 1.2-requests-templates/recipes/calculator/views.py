from django.shortcuts import render

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
    'hotdog': {
        'булочка для хот-дога, шт': 1,
        'сосиска, штука': 1,
        'кетчуп, г': 20,
        'горчица, г': 10,
    },

    # можете добавить свои рецепты ;)
}

# Напишите ваш обработчик. Используйте DATA как источник данных
# Результат - render(request, 'calculator/index.html', context)
# В качестве контекста должен быть передан словарь с рецептом:
# context = {
#   'recipe': {
#     'ингредиент1': количество1,
#     'ингредиент2': количество2,
#   }
# }


def context_fill(recipe, servings, context1 = {'recipe':{}}):
    for ingredient in DATA[recipe]:
#        print(ingredient,DATA[recipe][ingredient]*servings)
        context1['recipe'][ingredient] = DATA[recipe][ingredient]*servings
    return context1

def home_view(request):
    template_name = 'calculator/home.html'
    recipes_list = {}
    for item in DATA:
        recipes_list[item] = item
    context = {
        'recipes_list': recipes_list
    }
    return render(request, template_name, context)


def omlet_view(request):
    template_name = 'calculator/index.html'
    servings = int(request.GET.get("servings",1))
    context = {'recipe':{}}
    for ingredient in DATA['omlet']:
#        print(ingredient,DATA['omlet'][ingredient]*servings)
        context['recipe'][ingredient] = DATA['omlet'][ingredient]*servings

    return render(request, template_name, context)

def context_fill(recipe, servings):
    context1 = {}
    context1.clear()
    context1 = {'recipe':{}}
    for ingredient in DATA[recipe]:
#        print(ingredient,DATA[recipe][ingredient]*servings)
        context1['recipe'][ingredient] = DATA[recipe][ingredient]*servings
    return context1


def pasta_view(request):
    template_name = 'calculator/index.html'
    servings = int(request.GET.get("servings",1))
    context = context_fill('pasta',servings)
    return render(request, template_name, context)

def buter_view(request):
    template_name = 'calculator/index.html'
    servings = int(request.GET.get("servings",1))
    context = context_fill('buter',servings)
    return render(request, template_name, context)

def hotdog_view(request):
    template_name = 'calculator/index.html'
    servings = int(request.GET.get("servings",1))
    context = context_fill('hotdog',servings)
    return render(request, template_name, context)
