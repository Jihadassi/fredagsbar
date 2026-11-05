
import os
from urllib.parse import quote

import httpx
import streamlit as st

API_URL = os.getenv("API_URL", "http://localhost:5000")

st.set_page_config(
    page_title="Fredagsbar",
    page_icon="🍻",
    layout="centered"
)


def api_request(method, path, **kwargs):
    """Send en forespørgsel til Flask API'et."""
    try:
        response = httpx.request(
            method,
            f"{API_URL}{path}",
            timeout=2,
            **kwargs
        )
        response.raise_for_status()

        if response.status_code == 204:
            return None

        return response.json()

    except httpx.ConnectError:
        st.error("Kan ikke forbinde til API'et. Er Flask-serveren startet?")

    except httpx.TimeoutException:
        st.error("API'et svarer for langsomt. Prøv igen.")

    except httpx.HTTPStatusError as error:
        try:
            message = error.response.json().get(
                "error", "Der opstod en fejl"
            )
        except ValueError:
            message = "API'et returnerede et ugyldigt svar"

        st.error(message)

    except httpx.HTTPError:
        st.error("Der opstod en netværksfejl.")

    except ValueError:
        st.error("API'et returnerede ugyldig JSON.")

    return None


st.title("🍻 Fredagsbar")
st.write("Se vores events, tilmeld dig, eller opret et nyt arrangement.")

# Brugerens navn gemmes i session_state
if "name" not in st.session_state:
    st.session_state.name = ""

with st.sidebar:
    st.header("Din profil")
    st.text_input("Dit navn", key="name")

name = st.session_state.name.strip()

# Hent alle events ved hver genkørsel
events = api_request("GET", "/events")

if events is None:
    st.stop()

# Oversigt over alle events
st.subheader("📋 Oversigt over events")

rows = []

for event in events:
    participants_count = len(event["participants"])
    available = event["capacity"] - participants_count

    rows.append({
        "Titel": event["title"],
        "Dato": event["date"],
        "Tilmeldte": participants_count,
        "Ledige pladser": available
    })

st.dataframe(rows, use_container_width=True, hide_index=True)

# Vælg et event og tilmeld/afmeld
st.subheader("🎟️ Tilmeld eller afmeld")

if events:
    selected_id = st.selectbox(
        "Vælg et event",
        options=[event["id"] for event in events],
        format_func=lambda event_id: next(
            event["title"]
            for event in events
            if event["id"] == event_id
        )
    )

    selected_event = next(
        event for event in events
        if event["id"] == selected_id
    )

    participants = selected_event["participants"]
    available = selected_event["capacity"] - len(participants)

    st.write(f"**Dato:** {selected_event['date']}")
    st.write(f"**Ledige pladser:** {available}")

    st.write("**Deltagere:**")
    if participants:
        st.write(", ".join(participants))
    else:
        st.write("Ingen tilmeldte endnu.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "✅ Tilmeld",
            disabled=(available == 0 or not name),
            use_container_width=True
        ):
            result = api_request(
                "POST",
                f"/events/{selected_id}/signups",
                json={"name": name}
            )

            if result is not None:
                st.session_state["notice"] = "Du er nu tilmeldt!"
                st.rerun()

    with col2:
        if st.button(
            "❌ Afmeld",
            disabled=not name,
            use_container_width=True
        ):
            encoded_name = quote(name, safe="")

            result = api_request(
                "DELETE",
                f"/events/{selected_id}/signups/{encoded_name}"
            )

            # DELETE returnerer 204 uden JSON
            # Kontrollér opdateringen ved at hente events igen
            updated_events = api_request("GET", "/events")

            if updated_events is not None:
                updated_event = next(
                    (event for event in updated_events
                     if event["id"] == selected_id),
                    None
                )

                if updated_event and name not in updated_event["participants"]:
                    st.session_state["notice"] = "Du er nu afmeldt!"
                    st.rerun()

else:
    st.info("Der er endnu ingen events.")

if "notice" in st.session_state:
    st.success(st.session_state.pop("notice"))


# Formular til oprettelse af events
st.divider()
st.subheader("➕ Opret et nyt event")

with st.form("create_event_form", clear_on_submit=True):
    title = st.text_input("Eventets titel")
    date = st.date_input("Dato")
    capacity = st.number_input(
        "Antal pladser",
        min_value=1,
        value=10,
        step=1
    )

    submitted = st.form_submit_button("Opret event")

if submitted:
    if not title.strip():
        st.error("Du skal indtaste en titel.")
    else:
        result = api_request(
            "POST",
            "/events",
            json={
                "title": title.strip(),
                "date": date.isoformat(),
                "capacity": int(capacity)
            }
        )

        if result is not None:
            st.session_state["notice"] = "Eventet blev oprettet!"
            st.rerun()
