from django.views.generic import ListView, DetailView, View
from django.shortcuts import render
from django.core.paginator import Paginator
from . import models, forms

# from django.urls import reverse
# from django.http import Http404
# from django.core.paginator import Paginator, EmptyPage
# from django.http import HttpResponse

# def all_rooms(request): # function based view
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


class HomeView(ListView):  # class based view

    """ HomeView Definition """

    model = models.Room
    paginate_by = 12
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


# def room_detail(request, pk):  # function-based view <- not that confusing.
#     try:
#         room = models.Room.objects.get(pk=pk)
#         return render(request, "rooms/detail.html", {"room": room})
#     except models.Room.DoesNotExist:
#         # return redirect(reverse("core:home"))
#         # This will give core:home url. looks more professional insted of just doing "/".
#         raise Http404()


class RoomDetail(DetailView):  # class based view.

    """ RoomDetail Definition """

    model = models.Room
    # pk_url_kwarg = "pk" #pk is default


class SearchView(View):
    def get(self, request):

        country = request.GET.get("country")

        if country:

            # bound forms: some data will be given to this form. we dont' know whether it's clean or not.
            form = forms.SearchForm(request.GET)

            if form.is_valid():  # validate it to see if it's clean
                # print(form.cleaned_data)  # then, print
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True
                    # using Foreign key, in host(user) get superhost.

                for amenity in amenities:
                    filter_args["amenities"] = amenity

                for facility in facilities:
                    filter_args["facilities"] = facility

                print(filter_args)

                qs = models.Room.objects.filter(**filter_args).order_by("-created")

                paginator = Paginator(qs, 10, orphans=5)

                page = request.GET.get("page", 1)

                rooms = paginator.get_page(page)

                return render(
                    request, "rooms/search.html", {"form": form, "rooms": rooms}
                )
        else:  # when first time, the page is loaded
            form = forms.SearchForm()  # unbound form

        return render(request, "rooms/search.html", {"form": form})

    # city = request.GET.get("city", "Anywhere")  # Anywhere is default
    # city = str.capitalize(city)
    # country = request.GET.get("country", "KR")
    # room_type = int(request.GET.get("room_type", 0))  # because 'pk' is integer.

    # price = int(request.GET.get("price ", 0))
    # guests = int(request.GET.get("guests", 0))
    # bedrooms = int(request.GET.get("bedrooms", 0))
    # beds = int(request.GET.get("beds", 0))
    # baths = int(request.GET.get("baths", 0))

    # instant = bool(request.GET.get("instant", False))
    # # as it was string, not boolean true or false, so make it boolean.
    # superhost = bool(request.GET.get("superhost", False))

    # selected_amenities = request.GET.getlist("amenities")
    # selected_facilities = request.GET.getlist("facilities")

    # form = {  # from request
    #     "city": city,
    #     "selected_room_type": room_type,
    #     "selected_country": country,
    #     "price": price,
    #     "guests": guests,
    #     "bedrooms": bedrooms,
    #     "beds": beds,
    #     "baths": baths,
    #     "selected_amenities": selected_amenities,
    #     "selected_facilities": selected_facilities,
    #     "instant": instant,
    #     "superhost": superhost,
    # }

    # room_types = models.RoomType.objects.all()
    # amenities = models.Amenity.objects.all()
    # facilities = models.Facility.objects.all()

    # choices = {  # from database
    #     "countries": countries,
    #     "room_types": room_types,
    #     "amenities": amenities,
    #     "facilities": facilities,
    # }

    # filter_args = {}

    # if city != "Anywhere":
    #     filter_args["city__startswith"] = city

    # filter_args["country"] = country
    # print(filter_args)

    # if room_type != 0:
    #     filter_args["room_type__pk"] = room_type

    # if price != 0:
    #     filter_args["price__lte"] = price

    # if guests != 0:
    #     filter_args["guests__gte"] = guests

    # if bedrooms != 0:
    #     filter_args["bedrooms__gte"] = bedrooms

    # if beds != 0:
    #     filter_args["beds__gte"] = beds

    # if baths != 0:
    #     filter_args["baths__gte"] = baths

    # if instant is True:
    #     filter_args["instant_book"] = True

    # if superhost is True:
    #     filter_args["host__superhost"] = True
    #     # using Foreign key, in host(user) get superhost.

    # if len(selected_amenities) > 0:
    #     for s_amenity in selected_amenities:
    #         filter_args["amenities__pk"] = int(s_amenity)

    # # print(filter_args)

    # if len(selected_facilities) > 0:
    #     for s_facility in selected_facilities:
    #         filter_args["facilities__pk"] = int(s_facility)

    # # print(filter_args)

    # rooms = models.Room.objects.filter(**filter_args)

    # **: get element from list like '...' in JS.

