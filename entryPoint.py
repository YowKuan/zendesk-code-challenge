from controller.ticketController import TicketController


def start_viewer():
    program = TicketController() 
    return program
if __name__ == "__main__":
    start_viewer()