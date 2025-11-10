import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
from crewai import LLM
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import schedule
import time
import json
from crewai import Crew
from trip_agents import TripAgents
from trip_tasks import TripTasks

#load_dotenv()

class Quejas:

    def __init__(self, datos):
        self.datos = datos
    def run(self):
            agents = TripAgents()
            tasks = TripTasks()
            
            escritor = agents.escritor()
            escritor_task = tasks.resumen_task(
                escritor, self.datos
            )
            crew = Crew(
            agents = [escritor],
            tasks = [escritor_task],
            verbose = True
            )
            return crew.kickoff()
        

def enviar_email(destinatario, asunto, mensaje):
    remitente = "mercadonaimpostor@gmail.com"
    contraseña = "mmoh mken xocv disp" 

    msg = MIMEMultipart()
    msg["From"] = remitente
    msg["To"] = destinatario
    msg["Subject"] = asunto

    msg.attach(MIMEText(mensaje, "plain"))
    #Conectamos con Gmail y enviamos mensaje
    with smtplib.SMTP("smtp.gmail.com", 587) as servidor:
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.send_message(msg)


def tarea_mensual(resp):

    enviar_email("estrellaherrejon.in@gmail.com", "Reporte mensual", resp)


with open("tools/bbdd/quejas.json", "r", encoding="utf-8") as bbdd:
    quejas = json.load(bbdd)

total_quejas = []
for clave, valor in quejas.items():
    total_quejas.append(valor)

quejas_r = Quejas(total_quejas)
respuesta = quejas_r.run()
tarea_mensual(respuesta.raw)
with open("tools/bbdd/quejas.json", "w", encoding="utf-8") as bbdd:
    json.dump({}, bbdd, indent=4, ensure_ascii=False)
#schedule.every().month.at("09:00").do(tarea_mensual)

#while True:
    #schedule.run_pending()
    #time.sleep(60)
