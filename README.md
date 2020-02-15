# Libertas
[![Development](https://img.shields.io/github/workflow/status/the-haps/libertas/Python%20Syntax%20Check/development?label=development&logo=github&style=flat-square)](https://github.com/the-haps/libertas/tree/development)
[![Beta](https://img.shields.io/github/workflow/status/the-haps/libertas/Build%20Beta%20Package/beta?label=beta&logo=github&style=flat-square)](https://github.com/the-haps/libertas/tree/beta)
<!-- [![Release](https://img.shields.io/github/workflow/status/the-haps/libertas/Build%20Release%20Package/release?label=release&logo=github&style=flat-square)](https://github.com/the-haps/libertas/tree/release) -->


## Was ist Libertas?
Libertas ist der Projektname für die Web-App der Schülerzeitung "TheHaps" von der Halepaghen-Schule. Die App ermöglicht den digitalen Erwerb und das Lesen der Zeitung, direkt aus dem Browser.

Jede*r darf sich an der Entwicklung der App beteiligen! Libertas wurde mit Django 3.0 entwickelt, außerdem ermöglicht eine vorkonfigurierter Docker Container Stack das einfache Aufsetzen einer lokalen Instanz.

## Aufsetzen einer lokalen Instanz

### Vorraussetzungen
- Git
- [Docker](https://docs.docker.com/install/)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Wie setze ich den Container Stack auf?

Clone als erstes das Git-Repository:
```
git clone https://github.com/the-haps/libertas.git
cd libertas
```
Starte anschließend den Container Stack mit `docker-compose`:
```
docker-compose up
```

Um den Container Stack zu stoppen:
```
docker-compose down
```

Um den Container Stack zu stoppen **und die Datenbank zu löschen**:
```
docker-compose down -v
```

Alle Informationen zu Docker Compose findest du in der [Dokumentation](https://docs.docker.com/compose/).

### Was beinhaltet der Container Stack?
Der Container Stack (siehe `docker-compose.yml`) besteht aus folgenden Docker-Containern:

- Django (Libertas)
  - Sobald der Container Stack gestartet wurde, ist Libertas unter `localhost:8000` im Browser erreichbar.
  - Beim ersten Start wird es einige Minuten brauchen, bis der Container startet, da er zuerst auf die vollständige Initialisierung von MariaDB wartet.
  - Sobald der Container das erste mal gestartet wird, wird automatisch ein Admin-Account angelegt. Der Benutzername lautet `admin`, das Passwort `adminpassword`.
- MariaDB
  - Die Datenbank, welche von Django benutzt wird.
- MailHog
  - Alle von Django versendete E-Mails werden zum Testen abgefangen. Du kannst sie anschließend im Browser unter `localhost:8025` einsehen.

Die Konfiguration lässt sich in der `config.env` und in der `docker-compose.yml` anpassen. Anschließend muss der Container Stack neugestartet werden. Im Normalfall solltest du aber nichts ändern müssen.

## Libertas mitentwickeln

Libertas ist bewusst open source und kann von jedem mitentwickelt werden! Du findest alle Informationen dazu in der [CONTRIBUTING.md](https://github.com/the-haps/libertas/blob/development/CONTRIBUTING.md).
