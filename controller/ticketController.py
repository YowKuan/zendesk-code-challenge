import sys
from os.path import dirname, abspath

from view.appView import appView
from model.requestHandler import requestHandler

class TicketController:
    def __init__(self):
        self.view = appView
        self.api = requestHandler
        self.input = ''
        self.id = 0
        self.page = 0
    
    def run(self):
        self.runMainProgram()
    
    def runMainProgram(self):
        self.view.initialize()
        
        while True:
            self.input = input()
            if self.input == 'menu':
                self.view.show_menu()
            elif self.input == '1':
                response = self.showAllTickets()
                if not response:
                    self.view.display_message("couldn't get all tickets")
            elif self.input == '2':
                response = self.showOneTicket()
                if not response:
                    self.view.display_message("couldn't get the ticket")
            elif self.input == 'q' or self.input == 'Q':
                self.view.display_message("Thank you for using our ticket checking system, bye.")
                break
            else:
                self.view.display_message("Invalid input. Please type menu to see all options")
        self.input = ''
    
    def showAllTickets(self):
        try:
            tickets = self.api.getTickets()
        except:
            return
                
                
        

