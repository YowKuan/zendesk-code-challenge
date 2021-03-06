import math


class AppView:
    def __init__(self):
        self.page_limit = 25
        self.errorCode = None

    def initialize(self):  # Displays Start message on CLI screen
        print("\n\n-------------------------WELCOME TO ZENDESK TICKET VIEWER-------------------------")
        print("This application allows you view tickets and their details on your zendesk account")
        print("Please enter a command, to view command options, type 'menu': ", end="")
        return 0

    def displayBadRequest(self, message):  # Displays bad request message on CLI screen
        if self.errorCode is not None:
            print("\n[Bad request] Error getting data from API. Error Code:", self.errorCode)
        print(message)
        
        return 1

    def display_message(self, message, type):
        print(message, end="")        
        if type == 1:
            print("[Redirect] Go back to main page......\n")
            print("Please enter a command, to view command options, type 'menu': ", end="")
        return type  # Returns 0 on input prompt type messages, returns 1 on input error type messages

    def show_menu(self):  # Displays Command Menu on CLI Screen
        print("\nCommand Options:")
        print("* Enter 1 to display all tickets")
        print("* Enter 2 to display single ticket")
        print("* Enter q to exit application")
        print("* Enter 'menu' to display Command Menu")
        print("\nEnter your choice: ", end="")
        return 0

    def quit(self):  # Displays quit message and quits the App.
        print("\nExiting Zendesk Ticket Viewer. . . . . .")
        print("Exiting successful, see you soon.\n")
        return 0

    def fetchTickets(self, ticketID):  # Displays loading tickets message on CLI screen
        if ticketID == "all":
            print("\nFetching tickets, please wait . . . . .")
        else:
            print("\nFetching ticket", ticketID + ",", "please wait . . . . .")
        return 0

    def displayTickets(self, ticketsJSON, pageNo):  # Displays tickets details with pagination on CLI screen
        ticketsArr = ticketsJSON["tickets"]
        # rounding up ticket pages
        totalPages = math.ceil(float(len(ticketsArr)) / float(self.page_limit))
        # circular rotation of pages after limit or before start
        if pageNo > totalPages:
            pageNo = 1
        elif pageNo < 1:
            pageNo = totalPages
        pageTickets = 0
        ticketOffset = (pageNo - 1) * self.page_limit
        print("")
        for i in range(int(ticketOffset), int(self.page_limit + ticketOffset)):
            if i < len(ticketsArr):
                if ticketsArr[i]["id"] is None:
                    continue
                else:
                    print("<" + ticketsArr[i]["status"] + ">", "Ticket", ticketsArr[i]["id"], '| ' "opened by",
                          ticketsArr[i]["requester_id"] ,'|', "updated at", ticketsArr[i]["updated_at"])
                pageTickets += 1
        print("\nDisplaying", pageTickets, "tickets on page", pageNo, "of", totalPages)
        print("\nEnter 'd' to go down, 'u' to go up, 'menu' for menu and 'q' for quit: ", end="")
        return pageNo  # Current page no

    def displayTicket(self, ticketsJSON):  # Displays one ticket details on CLI screen
        if ticketsJSON and "ticket" in ticketsJSON:
            print("\n")
            print("   ticket id:", ticketsJSON["ticket"]["id"])
            print("   ticket status:", ticketsJSON["ticket"]["status"])
            print("   subject:", ticketsJSON["ticket"]["subject"])
            print("   updated at:", ticketsJSON["ticket"]["updated_at"])
            print("[Redirect] Go back to main page......\n")
            print("\nPlease enter a command, to view command menu, type 'menu': ", end="")
            return 0
        else:
            return 1