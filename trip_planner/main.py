import streamlit as st
from crewai import Crew
from trip_agents import TripAgents
from trip_tasks import TripTasks
from dotenv import load_dotenv

load_dotenv()

class TripCrew:

    def __init__(self, origin, cities, date_range, interests):
        self.origin = origin
        self.cities = cities
        self.date_range = date_range
        self.interests = interests

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()

        city_selector_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_expert()
        travel_concierge_agent = agents.travel_concierge()

        identify_task = tasks.identify_task(
            city_selector_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )
        gather_task = tasks.gather_task(
            local_expert_agent,
            self.origin,
            self.interests,
            self.date_range
        )
        plan_task = tasks.plan_task(
            travel_concierge_agent,
            self.origin,
            self.interests,
            self.date_range
        )

        crew = Crew(
            agents=[city_selector_agent, local_expert_agent, travel_concierge_agent],
            tasks=[identify_task, gather_task, plan_task],
            verbose=True
        )

        return crew.kickoff()


# Interfaz Streamlit
st.set_page_config(page_title="Planificador de viajes", layout="centered")
st.title("🌍 Planificador de viajes")
st.markdown("Introduce los datos para generar tu plan de viaje personalizado con agentes inteligentes.")

with st.form("trip_form"):
    location = st.text_input("¿Desde dónde viajas?")
    cities = st.text_input("¿Qué pais quieres visitar?")
    date_range = st.text_input("¿Cuál es tu rango de fechas para el viaje?")
    interests = st.text_area("¿Cuáles son tus intereses o aficiones?")
    submitted = st.form_submit_button("Generar plan de viaje")

if submitted:
    with st.spinner("🧠 Planeando tu viaje con ayuda de agentes inteligentes..."):
        trip_crew = TripCrew(location, cities, date_range, interests)
        result = trip_crew.run()

    st.success("✅ ¡Plan de viaje generado!")
    st.markdown("### ✈️ Tu Plan de Viaje")
    st.write(result.raw)
