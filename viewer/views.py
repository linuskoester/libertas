from django.http.response import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from libertas.models import Ausgabe
from django.contrib import messages
from django.http import Http404
from libertas.models import Token, User


def viewer(request, number, view_type):
    ausgabe = get_object_or_404(Ausgabe, number=number)

    if view_type == "read" and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        if Token.objects.filter(user=user, ausgabe=ausgabe).exists():
            pdf_data = "%s/0" % ausgabe.file_identifier
            pdf_name = ausgabe.name
        else:
            messages.error(request, """<strong>Du bist nicht im Besitz dieser Ausgabe.</strong>
                                    Wenn du im Besitz eines Tokens bist, löse ihn ein,
                                    um Zugriff auf die Ausgabe zu bekommen.""")
            return redirect('redeem')
    elif view_type == "leseprobe":
        if ausgabe.leseprobe:
            pdf_data = "%s/1" % ausgabe.file_identifier
            pdf_name = "%s (Leseprobe)" % ausgabe.name
        else:
            raise Http404()
    elif view_type == "thumbnail":
        if ausgabe.thumbnail:
            return FileResponse(ausgabe.thumbnail)
        else:
            raise Http404()
    else:
        raise Http404()

    return render(request, 'viewer/viewer.html', {'pdf_data': pdf_data, 'pdf_name': pdf_name})


def protected_file(request, identifier, view_type):
    ausgabe = get_object_or_404(Ausgabe, file_identifier=identifier)
    if view_type == "0" and request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        if Token.objects.filter(user=user, ausgabe=ausgabe).exists():
            return FileResponse(ausgabe.file)
        else:
            raise Http404()
    elif view_type == "1":
        return FileResponse(ausgabe.leseprobe)
    else:
        raise Http404()
