# Libertas mitentwickeln

Jeder darf sich an der Entwicklung der App beteiligen! Im Folgenden findest du einige Informationen, die du bei der Mitentwicklung beachten solltest.

Informationen, wie du eine lokale Instanz von Libertas erstellst, findest du in der [README.md](https://github.com/the-haps/libertas/blob/development/README.md).

## Wenn du kein Mitglied des Repositories bist

* Bitte erstelle dir mit dem Knopf oben rechts einen eigenen Fork ([Anleitung](https://guides.github.com/activities/forking/)).
* Du hast anschließend in deinem Profil eine vollständige Kopie vom Libertas-Repositories, in dem du alles ausprobieren und verändern kannst und darfst!
* Baue Änderungen am besten immer basierend auf dem `development`-Branch. Mehr Informationen zu den unterschiedlichen Branches findest du weiter unten.
* Sobald du fertig mit einer bestimmten Funktion bist, kannst du eine Pull Request in den `development`-Branch erstellen ([Anleitung](https://guides.github.com/activities/forking/#making-changes)), die Änderungen können dann in das Haupt-Repository gemerged werden!

## Wenn du Mitglied des Repositories bist

* Arbeite niemals im `main` oder `development`-Branch!
* Erstelle dir entweder einen eigenen Branch basierend auf dem `development`-Branch, oder forke das komplette Repository.
* Sobald du fertig mit einer bestimmten Funktion bist, kannst du eine Pull Request in den `development`-Branch erstellen ([Anleitung](https://guides.github.com/activities/forking/#making-changes)), die Änderungen können dann in das Haupt-Repository gemerged werden!

## Änderungen Dokumentieren

* Füge deinem Code aussagekräftige Kommentare hinzu, die dessen Funktion erklären.
* Erkläre in einem Commit **immer** was für Änderungen du vorgenommen hast.
* Nenne in der Pull Request, was für Änderungen du vorgenommen hast, und warum diese von Bedeutung sind. Sollte deine Änderungen mit einer Issue zusammenhängen, makiere es bitte.

## Bedeutung der verschiedenen Branches/Tags

* Main
  * Der Main-Branch entspricht der öffentlichen Betaversion von Libertas auf https://beta.thehaps.de/
  * Nach jeder Änderung lädt der Server automatisch das neuste Paket herunter, sodass unter dem Link jederzeit die Version des Beta-Branches zu finden ist.
  * Der Branch ist schreibgeschützt, alle Änderungen müssen zuerst durch Development-Branch laufen
  * Mit Tags werden Releases gekennzeichnet
* Development
  * Hier werden alle Änderungen zusammengeführt, bevor sie in den `main`-Branch gemerged werden
  * Er ist der Default-Branch
