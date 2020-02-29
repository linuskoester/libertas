from django.shortcuts import render

# Create your views here.


def viewer(request, pdf):
    pdf_name = "/static/viewer/pdf/" + pdf + ".pdf"
    return render(request, 'viewer/viewer.html', {'pdf_name': pdf_name})
