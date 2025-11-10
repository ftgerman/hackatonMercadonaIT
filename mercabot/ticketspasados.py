from pathlib import Path

class tickets:
    def __init__(self):
        self.tickets = {}
        
    def agregarticket(self, fecha, ticket):
        if fecha not in self.tickets:
            self.tickets[fecha] = []
        if ticket not in self.tickets[fecha]:
            self.tickets[fecha].append(ticket)
    
    def mostrartickets(self, fecha):

        print(f"\n")
        print(f"=" * 50)
        print(f"Resultados de buscar tickets del {fecha}:")
        print(f"=" * 50)

        ##Muestra por pantalla los tickets guardados en una fecha, enumerados si hay varios.##
        if fecha not in self.tickets or not self.tickets[fecha]:
            print("No hay tickets para esa fecha.\n")
            return

        for i, ticket_path in enumerate(self.tickets[fecha], start=1):
            ruta = Path(ticket_path)
            
            print(f"-" * 50)
            print(f"Ticket {i}:")   #print(f"\nTicket {i}: {ticket_path}") 
            print(f"-" * 50)
            if ruta.exists():
                with open(ruta, "r", encoding="utf-8") as f:
                    contenido = f.read()
                print(contenido)
                print("\n")
            else:
                print("El archivo no existe o la ruta es incorrecta.")

# Ejemplo de uso
t = tickets()

# Agregamos todos los tickets al diccionario
t.agregarticket("01/01/2025", "../tickets/ticket1.txt")
t.agregarticket("01/01/2025", "../tickets/ticket2.txt")
t.agregarticket("02/01/2025", "../tickets/ticket3.txt")

#Hacemos las busquedas para cada fecha
t.mostrartickets("01/01/2025")
t.mostrartickets("02/01/2025")
t.mostrartickets("03/01/2025")