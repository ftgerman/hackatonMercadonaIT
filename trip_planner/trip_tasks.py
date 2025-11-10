import os
from crewai import Task
from textwrap import dedent
from datetime import date

class TripTasks:

    def recommend_task(self, agent):
        ticket = ""
        for f in os.listdir("../tickets/"):
            if f.endswith(".txt"):
                with open(os.path.join("../tickets/", f), "r") as file:
                    ticket += file.read() + "\n"
        
        return Task(   
            
            description=dedent(f"""
                You are an expert personal shopper and data analyst for Mercadona. Your goal is to analyze the client's past purchase history (provided as 'Client Tickets') to identify their shopping patterns, preferences, and potential needs.

                Based on your analysis, you must recommend **three specific products** from Mercadona that the client has *not* purchased before but would likely enjoy.

                **Your instructions are:**
                1.  **Analyze Purchase History:** Carefully scan all the 'Client Tickets'. Look for:
                    * **Frequently Bought Items:** What do they buy every time? (e.g., 'Leche semidesnatada', 'Huevos').
                    * **Product Categories:** Are they buying a lot from a specific category? (e.g., 'Fruta y Verdura', 'Sin Gluten', 'Cuidado Personal', 'Limpieza').
                    * **Dietary Preferences:** Can you infer any dietary needs? (e.g., 'Bebida de Soja' or 'Tofu' might suggest vegetarian/vegan preferences).
                    * **Missing Complements:** Do they buy items that have a common partner? (e.g., they buy 'Spaghetti' but never 'Tomate Frito'; they buy 'Shampoo' but never 'Conditioner').

                2.  **Generate Recommendations:** Select **exactly three** new products. These should be logical recommendations based on the patterns you found. For example:
                    * If they always buy 'Yogur Natural', recommend 'Yogur Griego'.
                    * If they buy 'Sin Gluten', recommend a new 'Pasta Sin Gluten' or 'Pan de molde Sin Gluten'.
                    * If they buy 'Guacamole', recommend 'Hummus'.

                3.  **Provide Justification:** For each of the three recommendations, you MUST provide a one-sentence justification that links it to their purchase history.

                It is imperative that your recommendations are **specific products available at Mercadona**. Avoid generic suggestions like 'buy more fruits' or 'try new snacks'. Instead, name actual products they can find in the store.                                
                **The final result must be entirely in Spanish.**
                               
                {self.__tip_section()}

                
                Client Tickets: {ticket}


            """),
            agent=agent,
            expected_output="A list of 3 recommended products from Mercadona based on the client's tickets and preferences"
        )

    def buscadorecetas(self, agent, comida):
        return Task(
            description=dedent(f"""
                From a recipe input: {comida}
                You are a Culinary Ingredient Specialist.

                Your primary role is to find the necessary components for a specific dish. You will receive a food name as input (e.g., "Paella Valenciana" or "Chocolate Chip Cookies").

                Your goal is to use your search tools to browse the internet, locate a popular and reliable recipe for that dish, and then extract only the list of required ingredients.

                You must not return the full recipe, cooking instructions, preparation steps, or cooking times. Your final output must strictly be the itemized list of ingredients.
                
                In spanish !!!!!
            """),
            agent=agent,
            expected_output="The recipe given by the input: {comida}",
            output_file="receta.txt"
        )
    
    def sacaingredientes(self, agent):
        #receta = open("receta.txt","r").read()
        return Task(
            
            description=dedent(f"""
                From the recipe store in the file "receta.txt":
                You will have to extract the ingredients from the recipe.
            """),
            agent=agent,
            expected_output="The list of ingredients that are used in the recipe and the amounts"
        
        )

    def plan_task(self, agent, origin, interests, range):
        return Task(
            description=dedent(f"""
                Expand this guide into a full 7-day travel 
                itinerary with detailed per-day plans, including 
                weather forecasts, places to eat, packing suggestions, 
                and a budget breakdown.
                
                You MUST suggest actual places to visit, actual hotels 
                to stay and actual restaurants to go to.
                
                This itinerary should cover all aspects of the trip, 
                from arrival to departure, integrating the city guide
                information with practical travel logistics.
                
                Your final answer MUST be a complete expanded travel plan,
                formatted as markdown, encompassing a daily schedule,
                anticipated weather conditions, recommended clothing and
                items to pack, and a detailed budget, ensuring THE BEST
                TRIP EVER. Be specific and give it a reason why you picked
                each place, what makes them special! {self.__tip_section()}

                Trip Date: {range}
                Traveling from: {origin}
                Traveler Interests: {interests}
            """),
            agent=agent,
            expected_output="Complete expanded travel plan with daily schedule, weather conditions, packing suggestions, and budget breakdown"
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"
