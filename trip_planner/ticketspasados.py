import os
from pathlib import Path


class tickets():
    def __init__(self):
        self.tickets = {}
        
    def buscarticket(self, fecha):
        if fecha in self.tickets:
            return self.tickets[fecha]
        else:
            return None
        
    def agregarticket(self, fecha, ticket):
        if fecha not in self.tickets:
            self.tickets[fecha] = []
        if ticket not in self.tickets[fecha]:
            self.tickets[fecha].append(ticket)
