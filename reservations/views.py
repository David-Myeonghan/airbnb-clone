import datetime
from django.http import Http404
from django.views.generic import View
from django.contrib import messages
from django.shortcuts import render, redirect, reverse
from rooms import models as room_models
from reviews import forms as review_forms
from . import models


class CreateError(Exception):
    pass


# From template argument -> url -> view parameter.
def create(request, room, year, month, day):
    try:
        # Check if the url date exists. (user could change url address)
        date_obj = datetime.datetime(year, month, day)
        room = room_models.Room.objects.get(pk=room)
        models.BookedDay.objects.get(day=date_obj, reservation__room=room)
        # if the BookedDay is found, it means user cannot reserve the room. so raise CreateError.
        raise CreateError()
    except (room_models.Room.DoesNotExist, CreateError):
        messages.error(request, "Can't Reserve That Room")
        return redirect(reverse("core:home"))
    except models.BookedDay.DoesNotExist:
        reservation = models.Reservation.objects.create(
            guest=request.user,
            room=room,
            # Cannot reserve more than 1 day, as we use HTML and Django, not JS.
            check_in=date_obj,
            check_out=date_obj + datetime.timedelta(days=1),
        )
        return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))


# Can inherit from DetailView.
# but wanna check whether the user is host, or not and use a form to make an review.
class ReservationDetailView(View):
    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        # Instead of doing models.reservation.DoesNotExist:, made model manager!
        reservation = models.Reservation.objects.get_or_none(pk=pk)
        if not reservation or (
            # the user has to be guest or host
            reservation.guest != self.request.user
            and reservation.room.host != self.request.user
        ):
            raise Http404()
        form = review_forms.CreateReviewForm()
        return render(
            self.request,
            "reservations/detail.html",
            {"reservation": reservation, "form": form},
        )


def edit_reservation(request, pk, verb):
    reservation = models.Reservation.objects.get_or_none(pk=pk)
    if not reservation or (
        # the user has to be guest or host
        reservation.guest != request.user
        and reservation.room.host != request.user
    ):
        raise Http404()
    if verb == "confirm":
        reservation.status = models.Reservation.STATUS_CONFIRMED
    elif verb == "cancel":
        reservation.status = models.Reservation.STATUS_CANCELLED
        models.BookedDay.objects.filter(reservation=reservation).delete()
    reservation.save()
    messages.success(request, "Reservation Updated")
    return redirect(reverse("reservations:detail", kwargs={"pk": reservation.pk}))
