from django import template
from lists import models as list_models

register = template.Library()

# Get user from the context, and then check the room is in the user's list.
@register.simple_tag(takes_context=True)
def on_favs(context, room):
    user = context.request.user
    the_list, _ = list_models.List.objects.get_or_create(
        user=user, name="My Favourites Houses"
    )
    return room in the_list.rooms.all()
