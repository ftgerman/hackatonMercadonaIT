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
        agenterecetas = agents.buscador()
        ingredientes_task = tasks.buscadorecetas(
            agenterecetas,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )
        agenteIngredientes = agents.cocinero()
        listaIngredientes= tasks.sacaingredientes(
            agenterecetas,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )
        crew = Crew(
            agents=[agenterecetas,agenteIngredientes],
            tasks=[ingredientes_task,listaIngredientes],
            verbose=True
        )

        return crew.kickoff()

    def run3(self):
        agents = TripAgents()
        tasks = TripTasks()
        recommender_agent = agents.agenteRecomendador()
        recommend_task = tasks.recommend_task(
            recommender_agent,
            self.origin,
            self.cities,
            self.interests,
            self.date_range
        )
        crew = Crew(
            agents=[recommender_agent],
            tasks=[recommend_task],
            verbose=True
        )

        return crew.kickoff()

    def run2(self):
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
st.set_page_config(page_title="MercaBot", layout="centered")
st.title("MercaBot")
st.markdown("Introduzca categoría y consulta.")

with st.form("mb_form"):
    
    categorias = ["Seleccione categoría...","Recordatorio", "Productos para recetas", "Queja"]
    categoria = st.selectbox(
        "Categoría",
        categorias,
        index=0
    )
    consulta = st.text_input("Consulta")
    btn_enviar = st.form_submit_button("Generar respuesta")

if btn_enviar and categoria!="Seleccione categoría..." and consulta!="":
    #with st.spinner("🧠 Generando respuesta..."):
        #trip_crew = TripCrew(location, cities, date_range, interests)
        #result = trip_crew.run()

    st.success("✅ ¡Respuesta dada!")
    st.markdown("Respuesta:")
    #st.write(result.raw)
