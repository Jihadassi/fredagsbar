
import httpx

API_URL = "http://localhost:5000"


def test(name, expected, response):
    actual = response.status_code

    if actual == expected:
        print(f"BESTÅET: {name} ({actual})")
    else:
        print(f"FEJLET: {name} (forventet {expected}, fik {actual})")


# Test 1: Hent alle events
response = httpx.get(f"{API_URL}/events")
test("Hent alle events", 200, response)


# Test 2: Hent et event, der ikke findes
response = httpx.get(f"{API_URL}/events/99999")
test("Event findes ikke", 404, response)


# Test 3: Opret event uden titel
response = httpx.post(
    f"{API_URL}/events",
    json={"date": "2026-12-10", "capacity": 5}
)
test("Manglende titel", 400, response)


# Test 4: Opret event med ugyldig kapacitet
response = httpx.post(
    f"{API_URL}/events",
    json={"title": "Test", "date": "2026-12-10", "capacity": 0}
)
test("Ugyldig kapacitet", 400, response)


# Test 5: Opret et gyldigt testevent
response = httpx.post(
    f"{API_URL}/events",
    json={"title": "Automatisk test", "date": "2026-12-10", "capacity": 1}
)
test("Opret event", 201, response)

event_id = response.json()["id"]


# Test 6: Tilmeld første deltager
response = httpx.post(
    f"{API_URL}/events/{event_id}/signups",
    json={"name": "Anna"}
)
test("Tilmelding", 201, response)


# Test 7: Forsøg dobbelt tilmelding
response = httpx.post(
    f"{API_URL}/events/{event_id}/signups",
    json={"name": "Anna"}
)
test("Dobbelt tilmelding", 409, response)


# Test 8: Forsøg tilmelding til fuldt event
response = httpx.post(
    f"{API_URL}/events/{event_id}/signups",
    json={"name": "Peter"}
)
test("Fuldt event", 409, response)


# Test 9: Afmeld deltager
response = httpx.delete(
    f"{API_URL}/events/{event_id}/signups/Anna"
)
test("Afmelding", 204, response)


# Test 10: Slet testevent
response = httpx.delete(f"{API_URL}/events/{event_id}")
test("Slet event", 204, response)


print("\nAlle tests er gennemført!")
