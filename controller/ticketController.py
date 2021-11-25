import sys
from os.path import dirname, abspath

from view.appView import AppView
from model.requestHandler import requestHandler

class TicketController:
    def __init__(self):
        self.view = AppView()
        self.api = requestHandler()
        self.input = ''
        self.id = 0
        self.page = 0
    
    def run(self):
        self.runMainProgram()
    
    def runMainProgram(self):
        self.view.initialize()
        self.input = ''
        
        while True:
            self.input = input()
            if self.input == 'menu':
                self.view.show_menu()
            elif self.input == '1':
                response = self.showAllTickets()
                if not response:
                    self.view.display_message("couldn't get all tickets\n", 1)
            elif self.input == '2':
                response = self.showOneTicket()
                if not response:
                    self.view.display_message("", 1)
            elif self.input == 'q' or self.input == 'Q':
                sys.exit(self.view.quit())  # Print quit message and quit
            else:
                self.view.display_message("Invalid input. Please type menu to see all options\n", 1)
        
    
    def showAllTickets(self):
        try:
            self.view.fetchTickets("all")  # Fetching display message
            tickets = self.api.get_tickets()  # Get all tickets
            assert tickets not in [401, 404, 503, -1]
            page = self.view.displayTickets(tickets, 1)
        except AssertionError as e:
            self.view.errorCode = self.api.errorCode
            if tickets == 401:  # No tickets on account
                self.view.displayBadRequest("No tickets on account to display")
            elif tickets == 404:  # Can't authenticate with API
                self.view.displayBadRequest("API authentication not permitted or invalid user credentials.")
            elif tickets == 503:  # API unavailable
                self.view.displayBadRequest("API unavailable. Please try again later")
            elif tickets -1:  # Other Bad Requests
                self.view.displayBadRequest("Unknown Bad Request")
            self.view.errorCode = None
            self.api.errorCode = None
            return tickets
        while True:
            self.input = input()
            if self.input == 'q':  # Quit app
                sys.exit(self.view.quit())  # Print quit message and quit
            elif self.input == "menu":  # Show menu
                self.view.show_menu()
                break
            elif self.input == "d":  # Page down
                page += 1
                page = self.view.displayTickets(tickets, page)
            elif self.input == "u":  # Page up
                page -= 1
                page = self.view.displayTickets(tickets, page)
            else:
                self.view.display_message(
                    "Page command error. 'd' to go down, 'u' to go up, 'menu' for menu and 'q' for quit: ", 1)
                # Invalid user input for ticket paging
            self.input = ""
            self.currPage = page
        return 0
    def showOneTicket(self):  # Controller method for displaying one ticket in view
        self.view.display_message("Enter the ticket ID: ", 0)  # Display ticket ID input message
        self.input = input() # Get ticket ID
        ticketID = self.input
        self.input = ""
        try:
            self.view.fetchTickets(ticketID)  # Get ticket
            ticket = self.api.get_ticket(ticketID)
            assert ticket not in [401, 404, 503, -1]
            self.view.displayTicket(ticket)  # Display ticket
            self.currID = int(ticketID)  # Current ticket ID
            return 1
        except AssertionError as e:
            self.view.errorCode = self.api.errorCode
            if ticket == 401:  # Can't authenticate with API
                self.view.displayBadRequest("API authentication not permitted or invalid user credentials.")
            elif ticket == 404:  # Ticket ID not valid
                self.view.displayBadRequest("The ticket ID you gave is not a valid ID")
            elif ticket == 503:  # API unavailable
                self.view.displayBadRequest("API unavailable. Please try again later")
            elif ticket -1:  # Other Bad Requests
                self.view.displayBadRequest("Unknown Bad Request")
            self.view.errorCode = None
            self.api.errorCode = None
            return False
                
                    
            

