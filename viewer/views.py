from datetime import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.http.response import FileResponse
from django.shortcuts import get_object_or_404, redirect, render

from libertas.models import Ausgabe
from libertas.views import wartung


def ual(request, type, name, number):
    user = User.objects.get(username=request.user)
    if type == "v":
        user.profile.ual += "V [" + str(datetime.now()) + "] Zugriff auf Viewer: " + \
            name + " (#" + number + ") - " + \
            request.META['HTTP_USER_AGENT'] + "\n"
    if type == "d":
        user.profile.ual += "D [" + str(datetime.now()) + "] Zugriff auf Datei:    " + \
            name + " (#" + str(number) + ") - " + \
            request.META['HTTP_USER_AGENT'] + "\n"
    user.save()


def viewer(request, number, view_type):
    # Wartung
    w = wartung(request, "viewer")
    if w:
        return w

    leseprobe = False
    ausgabe = get_object_or_404(Ausgabe, number=number)
    if view_type == "read" and ausgabe.access_read(request.user):
        ual(request, "v", ausgabe.name, number)
        pdf_data = "%s/0" % ausgabe.file_identifier
    elif view_type == "leseprobe" and ausgabe.access_leseprobe(request.user):
        pdf_data = "%s/1" % ausgabe.file_identifier
        leseprobe = True
    elif view_type == "thumbnail" and ausgabe.visible():
        return FileResponse(ausgabe.thumbnail)
    elif request.user.is_authenticated:
        messages.error(request, """<strong>Du bist nicht im Besitz dieser Ausgabe.</strong>
                                     Wenn du im Besitz eines Codes bist, löse ihn ein,
                                     um Zugriff auf die Ausgabe zu bekommen.""")
        return redirect('redeem')
    else:
        messages.error(
            request, 'Du musst dich zuerst anmelden um eine Ausgabe zu lesen.')
        return redirect('signin')

    return render(request, 'viewer/viewer.html', {'pdf_data': pdf_data, 'ausgabe': ausgabe, 'leseprobe': leseprobe})


def protected_file(request, identifier, view_type):
    # Wartung
    w = wartung(request, "viewer")
    if w:
        return w

    ausgabe = get_object_or_404(Ausgabe, file_identifier=identifier)
    if view_type == "0" and ausgabe.access_read(request.user):
        ual(request, "d", ausgabe.name, ausgabe.number)
        return FileResponse(ausgabe.file)
    elif view_type == "1" and ausgabe.access_leseprobe(request.user):
        return FileResponse(ausgabe.leseprobe)
    else:
        raise Http404()
