import folium
from django.shortcuts import render, get_object_or_404
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils import timezone

MOSCOW_CENTER = [55.751244, 37.618423]

DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)

def find_image(id):
    pokemon = Pokemon.objects.get(id=id)
    if pokemon.image:
        return pokemon.image.url
    else:
        return DEFAULT_IMAGE_URL

def show_all_pokemons(request):
    time = timezone.localtime()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lt=time,
                                                       disappeared_at__gt=time):
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )
    pokemons_on_page = []

    for pokemon in Pokemon.objects.all():
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': find_image(pokemon.id),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    time = timezone.localtime()
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    pokemons = {
        "pokemon_id": pokemon.id,
        "title_ru": pokemon.title,
        "img_url": request.build_absolute_uri(pokemon.image.url),
        "title_en": pokemon.title_eng,
        "title_jp": pokemon.title_jp,
        "description": pokemon.description
    }
    if pokemon.previous_evolution:
        pokemons["previous_evolution"] = {
            "title_ru": pokemon.previous_evolution.title,
            "pokemon_id": pokemon.previous_evolution.id,
            "img_url": pokemon.previous_evolution.image.url
        }

        pokemons["next_evolution"] = {
            "title_ru": pokemon.title,
            "pokemon_id": pokemon.id,
            "img_url": pokemon.image.url
        }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in PokemonEntity.objects.filter(pokemon__title=pokemon.title,
                                                       appeared_at__lt=time,
                                                       disappeared_at__gt=time):
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            request.build_absolute_uri(pokemon_entity.pokemon.image.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemons
    })
