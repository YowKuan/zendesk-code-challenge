import requests
from datetime import datetime
from dotenv import load_dotenv
import os

class requestHandler:
    def __init__(self):
        load_dotenv()
        self.URL = ""
        self.data = {}  # This is where ticket data goes
        self.subdomain = os.getenv('ZENDESK_SUBDOMAIN')  # Zendesk API subdomain
        self.email = os.getenv('ZENDESK_EMAIL')  # Zendesk API username
        self.password = os.getenv('ZENDESK_PASSWORD')  # Zendesk API password
        self.errorCode = None

    def get_tickets(self):
        ticketsJSON = self.zendeskRequest("all")
        if ticketsJSON in [401, 404, 503, -1] or "tickets" not in ticketsJSON:
            print("ticketsJson", ticketsJSON)
            if ticketsJSON == 401:
                return 401  # Invalid user credentials or authentication not enabled
            elif ticketsJSON == 503:
                return 503  # If API is unavailable
            elif ticketsJSON == 404:
                return 404  # All other bad requests
            elif ticketsJSON == -1:
                # For if no tickets exist
                return -1

        elif ticketsJSON not in [1, False, None, 0] and "tickets" in ticketsJSON:
            for i in range(len(ticketsJSON["tickets"])):
                updated, created = self.formatDates(ticketsJSON["tickets"][i]["updated_at"],
                                                    ticketsJSON["tickets"][i]["created_at"])
                ticketsJSON["tickets"][i]["updated_at"] = str(updated)  # Setting the formatted dates
                ticketsJSON["tickets"][i]["created_at"] = str(created)  # Setting the formatted dates
            return ticketsJSON

    # Method to get one ticket details from API and return it, or return appropriate error value
    def get_ticket(self, ticketID):
        ticketsJSON = self.zendeskRequest('single_ticket', ticketID)
        if ticketsJSON not in [401, 404, 503, -1] and "ticket" in ticketsJSON:
            updated, created = self.formatDates(ticketsJSON["ticket"]["updated_at"],
                                                ticketsJSON["ticket"]["created_at"])
            ticketsJSON["ticket"]["updated_at"] = str(updated)
            ticketsJSON["ticket"]["created_at"] = str(created)
            return ticketsJSON
        elif ticketsJSON in [401, 404, 503, -1]:
            return ticketsJSON
    
    def zendeskRequest(self, option='all', ticket_id=''):
        if option == 'all':
            self.URL = "https://" + self.subdomain + ".zendesk.com/api/v2/tickets.json"
        else:
            self.URL = "https://" + self.subdomain + ".zendesk.com/api/v2/tickets/" + str(ticket_id) + ".json"
        response = requests.get(self.URL, auth=(self.email, self.password))
        if response.status_code != 200:
            self.errorCode = response.status_code
            if response.status_code == 401:  # Authentication not allowed or invalid user credentials
                return 401
            elif response.status_code == 404:  # 404 = No tickets or invalid ticket ID
                return 404
            elif response.status_code == 503:  # API unavailable
                return 503
            return -1  # For all other bad requests
        self.data = response.json()
        new = self.data
        next_page = []
        # Go through all web pages containing tickets and add them to tickets json. One page can contain 100 tickets
        # Make sure user has chosen to display all tickets, next page exists and has not been already visited.
        while option == 'all' and new["next_page"] is not None and new["next_page"] not in next_page:
            self.URL = new["next_page"]
            next_page.append(self.URL)
            response = requests.get(self.URL, auth=(self.email, self.password))
            new = response.json()
            # print("Next: ", new["next_page"])
            self.data["tickets"].extend(new["tickets"])  # Adding new tickets found in the next API web page.
        #print("final_data:",self.data)
        return self.data
        
    def formatDates(self, updatedAt, createdAt):
        t1 = datetime.strptime(updatedAt, "%Y-%m-%dT%H:%M:%SZ")
        t2 = datetime.strptime(createdAt, "%Y-%m-%dT%H:%M:%SZ")
        updated = "%d-%d-%d %d:%d:%d" % (t1.year, t1.month, t1.day, t1.hour, t1.minute, t1.second)
        created = "%d-%d-%d %d:%d:%d" % (t2.year, t2.month, t2.day, t2.hour, t2.minute, t2.second)
        return updated, created
        

