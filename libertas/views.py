from datetime import datetime

from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth import logout
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RedeemForm
from .models import Artikel, Code, Configuration, User, ausgaben_user, ausgaben_visible, news_list, artikel_list
from django.template.loader import render_to_string
from django.http.response import HttpResponseNotFound, HttpResponseServerError


def log_user(user, flag, message):
    LogEntry.objects.log_action(
        user_id=user.id,
        content_type_id=ContentType.objects.get_for_model(
            user).pk,
        object_id=user.id,
        object_repr=user.username,
        action_flag=flag,
        change_message=message)


def wartung(request, pagetype=""):
    wartung = Configuration.objects.get(name="Einstellungen")
    if request.user.is_superuser:
        if wartung.voll():
            messages.warning(request, 'Wartungsmodus (Voll) aktiviert!')
        if wartung.auth():
            messages.warning(request, 'Wartungsmodus (Auth.) aktiviert!')
        if wartung.signup():
            messages.warning(request, 'Wartungsmodus (Regist.) aktiviert!')
        if wartung.viewer():
            messages.warning(request, 'Wartungsmodus (Viewer) aktiviert!')
    else:
        if wartung.voll():
            return render(request, 'libertas/wartung.html')
        if wartung.auth():
            if request.user.is_authenticated:
                messages.warning(
                    request, 'Du wurdest aufgrund von Wartungsarbeiten abgemeldet.')
                logout(request)
            elif pagetype == "auth" or pagetype == "signup":
                messages.error(
                    request, """Zurzeit ist die Anmeldung und Registrierung aufgrund von Wartungsarbeiten nicht möglich.
                                <a href="https://status.thehaps.de/">Hier</a> findest du mehr Informationen.""")
                return redirect('index')
        if wartung.signup() and pagetype == "signup":
            messages.error(
                request, """Zurzeit ist die Registrierung aufgrund von Wartungsarbeiten nicht möglich.
                            <a href="https://status.thehaps.de/">Hier</a> findest du mehr Informationen.""")
            return redirect('index')
        if wartung.viewer() and pagetype == "viewer":
            messages.error(
                request, """Aufgrund von Wartungsarbeiten lassen sich zurzeit keine digitalen Ausgaben und Leseproben lesen.
                            <a href="https://status.thehaps.de/">Hier</a> findest du mehr Informationen.""")
            return redirect('index')
    return False


def startseite(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    try:
        ausgabe = ausgaben_visible()[0]
    except IndexError:
        ausgabe = False
    inventory = ausgaben_user(request.user)

    try:
        news = news_list()[:2]
    except IndexError:
        news = False

    return render(request, 'libertas/startseite.html', {'ausgabe': ausgabe,
                                                        'inventory': inventory,
                                                        'news_list': news,
                                                        'artikel_list': artikel_list()})


def ausgaben(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    ausgaben = ausgaben_visible()
    inventory = ausgaben_user(request.user)

    return render(request, 'libertas/pages/ausgaben.html', {'menu': 'ausgaben',
                                                            'ausgaben': ausgaben,
                                                            'inventory': inventory})


def artikel(request, pk):
    # Wartung
    w = wartung(request)
    if w:
        return w

    artikel = get_object_or_404(Artikel, pk=pk)

    return render(request, 'libertas/pages/artikel.html', {'artikel': artikel})


def news(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/pages/news.html', {'menu': 'news', 'news_list': news_list()})


def podcast(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/pages/podcast.html', {'menu': 'podcast'})


def team(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/pages/team.html', {'menu': 'team'})


def faq(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/pages/faq.html', {'menu': 'faq'})


def redeem(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    if not request.user.is_authenticated:
        return redirect('signin')
    if request.method == 'POST':
        form = RedeemForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code'].upper()
            code = Code.objects.get(code=code)
            code.user = User.objects.get(username=request.user)
            log_user(request.user, CHANGE, 'Benutzer hat Code %s (%s) eingelöst.' %
                     (code.code, code.ausgabe.name))
            code.redeemed = datetime.now()
            code.save()
            messages.success(
                request, 'Du hast jetzt Zugriff auf die Ausgabe <code>%s</code>.' % code.ausgabe.name)
            return redirect('ausgaben')
    else:
        form = RedeemForm()

    return render(request, 'libertas/pages/redeem.html', {'menu': 'user-redeem', 'form': form})


def buy(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/pages/buy.html', {'menu': 'buy'})


def datenschutz(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/pages/legal/datenschutz.html')


def agb(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/pages/legal/agb.html')


def impressum(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return render(request, 'libertas/pages/legal/impressum.html')


def error404(request, exception):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return HttpResponseNotFound(render_to_string('libertas/error/404.html'))


def error500(request):
    # Wartung
    w = wartung(request)
    if w:
        return w

    return HttpResponseServerError(render_to_string('libertas/error/500.html'))
