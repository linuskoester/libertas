# Libertas
![Build Beta Package](https://github.com/the-haps/libertas/workflows/Build%20Beta%20Package/badge.svg)
![Python Syntax Check](https://github.com/the-haps/libertas/workflows/Python%20Syntax%20Check/badge.svg)

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

## Bedeutung der verschiedenen Branches

- Release
  - Der Release-Branch entspricht der Liveversion von Libertas auf https://thehaps.de.
  - Der Branch ist schreibgeschützt, alle Änderungen müssen zuvor durch den Beta-Branch gelaufen sein.
- Beta
  - Der Beta-Branch entspricht der öffentlichen Betaversion von Libertas auf https://beta.thehaps.de/
  - Nach jeder Änderung lädt der Server automatisch das neuste Paket herunter, sodass unter dem Link jederzeit die Version des Beta-Branches zu finden ist.
  - Der Branch ist ebenfalls schreibgeschützt, alle Änderungen müssen zuerst in dem Development-Branch zusammengeführt werden.
- Development
  - Hier werden alle Änderungen zusammengeführt, bevor sie in die anderen Branches gemerged werden.
  - Es ist der Default-Branch.

**Wenn du Mitglied des Repositories bist**, musst du Änderungen immer in einem eigenen Branch machen. Sobald du mit deinen Änderungen fertig bist, kannst du eine Pull-Request aufmachen, um deinen Branch in den Development-Branch zu mergen.

**Wenn du kein Mitglied des Repositories bist**, erstelle dir einfach ein eigenen Fork von diesem Repository (Knopf oben Rechts), du hast dann eine vollständige Kopie in deinem Profil, mit der du alles machen kannst! Sobald du etwas fertig entwickelt hast, kannst du eine Pull-Request von deinem Fork auf den Development Branch in diesem Repository erstellen.
