import streamlit as st
from crewai import Crew
from trip_agents import TripAgents
from trip_tasks import TripTasks
from dotenv import load_dotenv

import json 

load_dotenv()

class TripCrew:

    def __init__(self, consulta, categoria):
        self.consulta = consulta
        self.categoria = categoria
        self.receta = ""

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
                buscador = agents.buscador()
                buscadorecetas = tasks.buscadorecetas(
                    buscador, consulta
                )
                crew = Crew(
                agents = [buscador],
                tasks = [buscadorecetas],
                verbose = True
                )
                return crew.kickoff()


# Interfaz Streamlit
st.set_page_config(page_title="MercaBot", layout="centered")
st.title("MercaBot 🛒🤖")
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

if btn_enviar and ((categoria!="Seleccione categoría..." and consulta!="") or (categoria=="Recomendador")):
    if categoria == "Queja":
        telefono ="+34 637601888" 
        datos = {
            "telefono" : telefono,
            "queja" : consulta
        }
        with open("tools/bbdd/quejas.json", "r", encoding="utf-8") as bbdd:
            quejas = json.load(bbdd)
            try:
                quejas[telefono].append(consulta)
            except KeyError:
                quejas[telefono] = []
                quejas[telefono].append(consulta)
        with open("tools/bbdd/quejas.json", "w", encoding="utf-8") as bbdd:
            json.dump(quejas, bbdd, indent=4, ensure_ascii=False)
        st.success("Gracias por el comentario")

    else:
        with st.spinner("🧠 Generando respuesta..."):
            trip_crew = TripCrew(consulta, categoria)
            result = trip_crew.run()
        

        st.write(result.raw)
