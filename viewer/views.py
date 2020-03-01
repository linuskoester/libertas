from django.http.response import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from libertas.models import Ausgabe
from django.contrib import messages
from django.http import Http404


def viewer(request, number, view_type):
    document = get_object_or_404(Ausgabe, number=number)

    if view_type == "read":
        if request.user.is_authenticated:
            pdf_data = "%s/0" % document.file_identifier
        else:
            messages.error(request, 'Du bist nicht im Besitz dieser Ausgabe!')
            return redirect('index')

    elif view_type == "leseprobe":
        if document.leseprobe:
            pdf_data = "%s/1" % document.file_identifier
        else:
            raise Http404()

    else:
        raise Http404()

    return render(request, 'viewer/viewer.html', {'pdf_data': pdf_data})


def protected_file(request, identifier, view_type):
    ausgabe = get_object_or_404(Ausgabe, file_identifier=identifier)
    if view_type == "0":
        if request.user.is_authenticated:
            return FileResponse(ausgabe.file)
    if view_type == "1":
        return FileResponse(ausgabe.leseprobe)
    else:
        raise Http404()
