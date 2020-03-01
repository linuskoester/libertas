from django.http.response import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from libertas.models import Ausgabe


def viewer(request, number, view_type):
    document = get_object_or_404(Ausgabe, number=number)

    pdf_data = "%s/%s" % (document.file_identifier, view_type)

    return render(request, 'viewer/viewer.html', {'pdf_data': pdf_data})


def protected_file(request, identifier, view_type):
    ausgabe = get_object_or_404(Ausgabe, file_identifier=identifier)
    if view_type == "read":
        if request.user.is_authenticated:
            return FileResponse(ausgabe.file)
    if view_type == "probe":
        return FileResponse(ausgabe.leseprobe)
    else:
        return redirect('index')
