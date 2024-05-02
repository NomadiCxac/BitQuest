# rpg/views.py
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from .models import Shop, ItemTemplate, Player, StatSheet
from .forms import ItemForm  # Make sure to import the form
import json
from django.core.exceptions import ValidationError

# Create your views here.


def index(request):
    # Renders the index.html template that includes links to other views
    return render(request, 'rpg/index.html')

def shop_list(request):
    shops = Shop.objects.all().values('name', 'currency', 'vendor__name')  # Simple data selection
    return JsonResponse(list(shops), safe=False)

def item_list(request):
    stats_config = [
        {'name': 'physical_damage', 'label': 'Physical Damage (0-1000)', 'min': 0, 'max': 1000, 'step': '0.01'},
        {'name': 'magic_damage', 'label': 'Magic Damage (0-1000)', 'min': 0, 'max': 1000, 'step': '0.01'},
        {'name': 'critical_damage', 'label': 'Critical Damage % (100-1000)', 'min': 100, 'max': 1000, 'step': '0.01'},
        {'name': 'critical_chance', 'label': 'Critical Chance % (0-10)', 'min': 0, 'max': 10, 'step': '0.01'},
        {'name': 'strength', 'label': 'Strength (0-1000)', 'min': 0, 'max': 1000, 'step': '0.01'},
        {'name': 'intelligence', 'label': 'Intelligence (0-1000)', 'min': 0, 'max': 1000, 'step': '0.01'},
        {'name': 'dexterity', 'label': 'Dexterity (0-1000)', 'min': 0, 'max': 1000, 'step': '0.01'},
        {'name': 'focus', 'label': 'Focus (0-1000)', 'min': 0, 'max': 1000, 'step': '0.01'},
        {'name': 'strength_modifier', 'label': 'Strength Modifier % (100-1000)', 'min': 100, 'max': 1000, 'step': '0.01'},
        {'name': 'intelligence_modifier', 'label': 'Intelligence Modifier % (100-1000)', 'min': 100, 'max': 1000, 'step': '0.01'},
        {'name': 'dexterity_modifier', 'label': 'Dexterity Modifier % (100-1000)', 'min': 100, 'max': 1000, 'step': '0.01'},
        {'name': 'focus_modifier', 'label': 'Focus Modifier % (100-1000)', 'min': 100, 'max': 1000, 'step': '0.01'}
    ]

    # Fetch items only if "fetch" parameter is present
    items = ItemTemplate.objects.select_related('stats').all() if 'fetch' in request.GET else []
    items_with_stats = []
    for item in items:
        stat_fields = {field.name: getattr(item.stats, field.name) for field in StatSheet._meta.fields if field.name != 'id'}
        items_with_stats.append({'item': item, 'stats': stat_fields})

    if request.method == 'POST':
        data = request.POST
        stats_data = {stat['name']: float(data.get('stats[' + stat['name'] + ']', 0)) for stat in stats_config}
        new_stat_sheet = StatSheet.objects.create(**stats_data)
        item = ItemTemplate(name=data['name'], itemType=data['itemType'], stats=new_stat_sheet)

        try:
            item.full_clean()  # Validates the item
            item.save()
            return JsonResponse({'success': True, 'id': item.id}, safe=False)
        except ValidationError as e:
            new_stat_sheet.delete()  # Clean up if item creation fails
            return JsonResponse({'success': False, 'error': ", ".join(e.messages)}, status=400)

    # GET request handling: Fetch and return all items
    if 'fetch' in request.GET:
        items = ItemTemplate.objects.select_related('stats').all()
        items_data = [{
            'id': item.id,
            'name': item.name,
            'itemType': item.itemType,
            'stats': {field.name: getattr(item.stats, field.name) for field in StatSheet._meta.fields if field.name != 'id'}
        } for item in items]
        return JsonResponse(items_data, safe=False)

    # If not a POST and 'fetch' parameter not in GET, return an empty list or appropriate message
    return JsonResponse({'message': 'No items fetched'}, status=200)

def player_list(request):
    players = Player.objects.all().values('name', 'currency', 'stats')  # Simple data selection
    return JsonResponse(list(players), safe=False)

