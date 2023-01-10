# Tema 3 - Platforma IoT Microservicii

## Rulare

Pentru a crea imaginea adaptorului (singura componenta a aplicatiei care nu este
o imagine de pe [hub.docker.com](hub.docker.com)) si a porni toate imaginile, se
poate folosi scriptul `run.sh`.

Inainte de rulare, trebuie definita variabila de mediu `SPRC_DVP`, ce va
reprezenta directorul in care se vor salva volumul bazei de date si volumul de
stocare pentru grafana.

## Structura

Aplicatia contine cele 4 componente specificate in enunt:

- Baza de date [InfluxDB](https://hub.docker.com/_/influxdb)
- Brokerul [eclipse-mosquitto](https://hub.docker.com/_/eclipse-mosquitto)
- Utilitarul de vizualizare a bazei de date,
[Grafana](https://hub.docker.com/r/grafana/grafana/)
- Adaptorul implementat in fisierul `adapter/adapter.py`

### Brokerul

Am folosit imaginea *eclipse-mosquitto* intrucat eram familiar cu ea de la
laboratorul de *MQTT*. Brokerul expune portul `1883`.

### Adaptorul

Este componenta care comunica cu baza de date si restul clientiilor. Adaptorul
se aboneaza la toate topicurile brokerului (`#`) si introduce datele trimise in
baza de date, folosind schema de mai jos.
Am folosit aceasta schema deoarece aveam nevoie sa accesez valorile trimise de
clientii brokerului intr-un format grupat dupa `statie` si `masuratoare` pentru
dashboard-ul `UPB IoT Data`, drept care am folosit aceasta combinatie pentru
`measurement` si am trimis fiecare masuratoare ca un mesaj ce respecta schema de
mai jos.

```json
{
        "measurement": "statie.masuratoare",
        "tags": {
                "type": "masuratoare",
                "statie": "statie"
        },
        "time": "timestamp",
        "fields": {
                "Value": "value"
        }
}
```

Am ales aceste taguri deoarece e nevoie de statie si tip pentru dashboardul
"Battery Dashboard" pentru a selecta si grupa datele ce trebuie afisate.

### Baza de date

Imaginea de `InfluxDB` se initializeaza cu ajutorul variabilelor de mediu care
se pot gasi in fisierul `stack.yml`. Aceste variabile sunt necesare pentru a
putea initializa baza de date cu bucket-ul `my-bucket`. Timpul de retentie al
datelor este infinit, deoarece variabila `DOCKER_INFLUXDB_INIT_RETENTION` nu
este setata. Volumul folosit de baza de date se afla in `${SPRC_DVP}/database`.

### Grafana

Dashboardurile sunt configurate in folderul `grafana-provisioning/dashboards`.
Credentialele de logare sunt cele din enuntul temei. De asemenea, acestea se
pot gasi si in fisierul `stack.yml`.
Eventualele modificari facute de utilizator sunt salvate in volumul
`${SPRC_DVP}/grafana-storage`.

## Testare

Pentru a putea vedea comportamentul aplicatiei, am folosit clientul din folderul
`client/`. Acesta adauga metricile `BAT`, `TEMP` si `HUMID` de la una din
urmatoarele locatii: `"UPB"`, `"Dorinel"`, `"Florinel"` cu valori aleatoare din
cate un interval pentru fiecare metrica. Statiile sunt tot valori aleatoare.

Pe langa scenariul principal de mai sus, clientul mai testeaza si urmatoarele
cazuri:

- trimiterea de mesaje cu metrici non numerice
- trimiterea de mesaje cu/fara timestamp
