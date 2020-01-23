# from django.utils import timezone
from django.views.generic import ListView

# from django.shortcuts import render, redirect
# from django.core.paginator import Paginator, EmptyPage
from . import models

# from django.http import HttpResponse


class HomeView(ListView):

    """ HomeView Definition """

    model = models.Room
    paginate_by = 10
    paginate_orphans = 5
    ordering = "created"
    page_kwarg = "page"
    context_object_name = "rooms"

    # def get_context_data(
    #     self, **kwargs
    # ):  # 'rooms' and 'page_obj' is included in context.
    #     # Call the base implementation first to get a context
    #     context = super().get_context_data(**kwargs)
    #     now = timezone.now()
    #     # Add in a QuerySet of all the books
    #     context["now"] = now
    #     return context


# function based view

# def all_rooms(request):
#     # print(dir(request)

#     # from GET request, get the value of "page". if page = none, default=1.
#     page = request.GET.get("page", 1)
#     room_list = models.Room.objects.all()  # not evaluated yet.
#     paginator = Paginator(room_list, 10, orphans=5)  # Make Paginator

#     try:
#         rooms = paginator.page(int(page))  # where the contents(rooms) are from
#         return render(request, "rooms/home.html", {"page": rooms})
#     except EmptyPage:
#         return redirect("/")

#     # one way to paginate...
#     # page = int(page or 1)  # page is the page above or default=1.
#     # page_size = 10
#     # limit = page_size * page
#     # offset = limit - page_size
#     # all_rooms = models.Room.objects.all()[offset:limit]
#     # page_count = ceil(models.Room.objects.count() / page_size)

#     # return render(
#     #     request,
#     #     "rooms/all_rooms.html",
#     #     {
#     #         "page": rooms
#     #         # "rooms": all_rooms,
#     #         # "page": page,
#     #         # "page_count": page_count,
#     #         # "page_range": range(1, page_count),
#     #     },
#     # )
