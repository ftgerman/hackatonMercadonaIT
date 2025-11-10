import streamlit as st
from crewai import Crew
from trip_agents import TripAgents
from trip_tasks import TripTasks
from dotenv import load_dotenv

load_dotenv()

class TripCrew:

    def __init__(self, consulta, categoria):
        self.consulta = consulta
        self.categoria = categoria

    def run(self):
        agents = TripAgents()
        tasks = TripTasks()
        match categoria:
            case "Recomendador":
                recommender_agent = agents.agenteRecomendador()
                recomment_task = tasks.recommend_task(
                    recommender_agent,
                )
                crew = Crew(
                agents = [recommender_agent],
                tasks = [recomment_task],
                verbose = True
                )
                return crew.kickoff()
            case "Recetas":
                cocinero = agents.cocinero()
                buscador = agents.buscador()
                buscadorecetas = tasks.buscadorecetas(
                    cocinero, consulta
                )
                sacaingredientes = tasks.sacaingredientes(buscador,buscadorecetas)
                crew = Crew(
                agents = [cocinero, buscador],
                tasks = [buscadorecetas, sacaingredientes],
                verbose = True
                )
                return crew.kickoff()

    def run3(self):
        pass

    def run2(self):
        pass


# Interfaz Streamlit
st.set_page_config(page_title="MercaBot", layout="centered")
st.title("MercaBot")
st.markdown("Introduzca categoría y consulta.")

with st.form("mb_form"):
    
    categorias = ["Seleccione categoría...","Recomendador","Recordatorio", "Recetas", "Queja"]
    categoria = st.selectbox(
        "Categoría",
        categorias,
        index=0
    )
    consulta = st.text_input("Consulta")
    btn_enviar = st.form_submit_button("Generar respuesta")

if btn_enviar and categoria!="Seleccione categoría..." and consulta!="":
    with st.spinner("🧠 Generando respuesta..."):
        trip_crew = TripCrew(consulta, categoria)
        result = trip_crew.run()
    if categoria == "Queja":
        pass
    st.success("✅ ¡Respuesta dada!")
    st.markdown("Respuesta:")
    #st.write(result.raw)
