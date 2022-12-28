import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity, PokemonElement
from django.utils.timezone import localtime
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, html, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    iframe = folium.IFrame(html=html, width=500, height=300)
    popup = folium.Popup(iframe, max_width=2650)
    folium.Marker(
        [lat, lon],
        icon=icon,
        popup=popup
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemon_locations = PokemonEntity.objects.filter(
        appeared_at__lte=localtime(), disappeared_at__gte=localtime())
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_location in pokemon_locations:
        html = (f"""
            <table>
<thead>
<tr>
<th>Что за покемон</th>
<th>{pokemon_location.pokemon.title_ru}</th>
</tr>
</thead>
<tfoot>
<tr>
<td></td>
<td></td>
</tr>
</tfoot>
<tbody>
<tr>
<td>Начало спауна</td><td>{pokemon_location.appeared_at}</td></tr>
<tr>
<td>Конец спауна</td><td>{pokemon_location.disappeared_at}</td></tr>
<tr>
<td>Уровень</td><td>{pokemon_location.level}</td></tr>
<tr>
<td>Здоровье</td><td>{pokemon_location.health}</td></tr>
<tr>
<td>Сила</td><td>{pokemon_location.strenght}</td></tr>
<tr>
<td>Защита</td><td>{pokemon_location.defence}</td></tr>
<tr>
<td>Выносливость</td><td>{pokemon_location.stamina}</td></tr>
</tbody>
</tr>
</table>
""")
        add_pokemon(
            folium_map, pokemon_location.lat,
            pokemon_location.lon,
            html,
            request.build_absolute_uri(pokemon_location.pokemon.photo.url)
        )

    pokemons_on_page = []
    pokemons = Pokemon.objects.all()
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.photo.url),
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.all()
    element_types = []
    requested_pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    pokemon_info = {
        "pokemon_id": requested_pokemon.id,
        "title_ru": requested_pokemon.title_ru,
        "title_en": requested_pokemon.title_en,
        "title_jp": requested_pokemon.title_jp,
        "img_url": request.build_absolute_uri(requested_pokemon.photo.url),
        "description": requested_pokemon.description,
        "previous_evolution": requested_pokemon.previous_evolution,
        "element_type": element_types
    }

    if requested_pokemon.previous_evolution:
        pokemon_info["previous_evolution"] = {
            "title_ru": requested_pokemon.previous_evolution.title_ru,
            "pokemon_id": requested_pokemon.previous_evolution.id,
            "img_url": request.build_absolute_uri(requested_pokemon.previous_evolution.photo.url)
        }
    if requested_pokemon.elements.all():
        for element_type in requested_pokemon.elements.all():
            strong_types = []
            for strong in element_type.strong_against_type.all():
                strong_types.append(strong)

            element_types.append({
                'title': element_type.title,
                'img': element_type.icon.url,
                'strong_against': strong_types
            })

    next_evolution = requested_pokemon.next_evolutions.first()
    if next_evolution:
        pokemon_info["next_evolution"] = {
            "title_ru": next_evolution.title_ru,
            "pokemon_id": next_evolution.id,
            "img_url": request.build_absolute_uri(next_evolution.photo.url)
        }
    html = (f"""            
    <p>{requested_pokemon.title_ru}</p>
    """)

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in requested_pokemon.entities.all():
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            html,
            request.build_absolute_uri(pokemon_entity.pokemon.photo.url)
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_info
    })
