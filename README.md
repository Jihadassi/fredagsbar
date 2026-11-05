
# Fredagsbar – Event-system

Obligatorisk Python-opgave: Fredagsbarens event-system.

Systemet er bygget med Flask, Streamlit, httpx og Docker.

## Funktioner

- Se alle events og ledige pladser
- Hent et bestemt event
- Opret nye events
- Tilmeld personer til events
- Afmeld personer fra events
- Slet events via API
- Forhindre tilmeldinger, når et event er fuldt
- Forhindre dobbelt tilmelding
- Vise fejlbeskeder, hvis noget går galt

## Teknologier

- Python
- Flask – backend/API
- Streamlit – frontend
- httpx – kommunikation med API
- uv – Python-pakkehåndtering
- Docker og Docker Compose

## Start med Docker

Kræver Docker og Docker Compose.

Kør fra projektets rodmappe:

    docker compose up --build

Åbn derefter:

Frontend: http://localhost:8501

API: http://localhost:5000/events

API'et er tilgængeligt på port 5000 og kan testes med Postman.

Stop systemet med Ctrl+C og eventuelt:

    docker compose down

## Start lokalt uden Docker

Kræver Python og uv.

Installer afhængigheder:

    uv sync

Start API'et i terminal 1:

    uv run api.py

Start Streamlit i terminal 2:

    uv run streamlit run app.py

Åbn http://localhost:8501.

## API-endpoints

| Metode | URL | Beskrivelse | Succes |
|--------|-----|-------------|--------|
| GET | /events | Hent alle events | 200 |
| GET | /events/{id} | Hent et event | 200 |
| POST | /events | Opret et event | 201 |
| POST | /events/{id}/signups | Tilmeld person | 201 |
| DELETE | /events/{id}/signups/{name} | Afmeld person | 204 |
| DELETE | /events/{id} | Slet event | 204 |

## Eksempel: Opret et event

POST /events

JSON-body:

    {
      "title": "Julefrokost",
      "date": "2026-12-18",
      "capacity": 20
    }

## Eksempel: Tilmelding

POST /events/1/signups

JSON-body:

    {
      "name": "Jihad"
    }

## Fejlhåndtering

API'et returnerer følgende statuskoder:

- 400 – Manglende eller ugyldige oplysninger
- 404 – Event eller tilmelding findes ikke
- 409 – Event er fuldt, eller personen er allerede tilmeldt

Fejl returneres som JSON med feltet "error".

## Arkitektur

Projektet består af to Docker-services:

- api: Flask-server på port 5000
- frontend: Streamlit på port 8501

Frontend sender HTTP-forespørgsler til API'et med httpx.

Ved lokal kørsel bruges http://localhost:5000.

I Docker bruges http://api:5000.

API-adressen styres med miljøvariablen API_URL.

## Datalagring

Events opbevares i en Python-liste i hukommelsen.

Der bruges ingen database.

Alle ændringer nulstilles, når API-processen genstartes.

## API-dokumentation

swagger.json indeholder API-dokumentationen
og kan åbnes i https://editor.swagger.io/.
