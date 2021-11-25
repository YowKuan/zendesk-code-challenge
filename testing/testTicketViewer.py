
   
"""
Testing for Ticket Viewer App. 
Tests for:
    - (application model): API Requests and Response, by mocking Network Access 
    - (application controller): Controller paths, by user input simulation and API access simulation through mocks. 
    - (application view): Correct functionality of View 
"""

import unittest
from unittest.mock import patch
import json
import sys
from os.path import dirname, abspath

sys.path.insert(0, dirname(dirname(abspath(__file__))))

from view.appView import AppView
from model.requestHandler import requestHandler
from controller.ticketController import TicketController
from entryPoint import start_viewer


class MockResponse:
    def __init__(self, json_data="", status_code=""):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


# noinspection PyTypeChecker
def test_get_one_ticket(url="", auth=""):
    f2 = open('data (1).json', 'r')  # Sample json ticket data for one ticket.
    j2 = json.load(f2)
    f2.close()
    mockObject = MockResponse(j2, 200)
    return mockObject


# noinspection PyTypeChecker
def test_get_all_tickets(url="", auth=""):  # Sample json ticket data for bulk tickets
    f1 = open('data.json', 'r')
    # This file has 'next_page' as null so that tests don't get stuck in infinite loop trying to refer the same link
    # in this file again and again.
    j1 = json.load(f1)
    f1.close()
    mockObject = MockResponse(j1, 200)
    return mockObject


# NOTE: The following 3 responses don't return a json, so we don't need one in our mockObject
# noinspection PyTypeChecker
def test_get_bad_request_response(url="", auth=""):
    mockObject = MockResponse(status_code=400)
    return mockObject


# noinspection PyTypeChecker
def test_get_unauthorized_response(url="", auth=""):
    mockObject = MockResponse(status_code=401)
    return mockObject


# noinspection PyTypeChecker
def test_api_unavailable_response(url="", auth=""):
    mockObject = MockResponse(status_code=503)
    return mockObject


# noinspection PyTypeChecker
def test_invalid_ticket_id_response(url="", auth=""):
    mockObject = MockResponse({'error': 'RecordNotFound', 'description': 'Not found'}, 404)
    return mockObject


# Tests for requestHandler.py module
class ModelTester(unittest.TestCase):
    # Happy unit test to get one ticket from API
    @patch('model.requestHandler.requests.get', side_effect=test_get_one_ticket)
    # replace requests.get with my dummy function to simulate API network access.
    def test_api_get_one(self, test_get):  # mocking api interaction, response status code = 200
        api = requestHandler()
        ticket_raw = api.zendeskRequest(False, 2)  # Raw ticket with unformatted dates
        self.assertEqual(len(ticket_raw), 1)
        assert "ticket" in ticket_raw
        self.assertEqual(ticket_raw["ticket"]["id"], 1)
        ticket = api.get_ticket(1)  # Processed ticket with formatted dates
        self.assertEqual(len(ticket), 1)
        assert "ticket" in ticket
        self.assertEqual(ticket["ticket"]["id"], 1)

    # Happy unit test to get all tickets from API
    @patch('model.requestHandler.requests.get', side_effect=test_get_all_tickets)
    # replace requests.get with my dummy function to simulate API network access.
    def test_api_get_all(self, test_get):  # mocking api interaction, response status code = 200
        api = requestHandler()
        ticket_raw = api.zendeskRequest('all')  # Raw tickets with unformatted dates
        self.assertEqual(ticket_raw["tickets"][-1]['id'], 100)
        assert "tickets" in ticket_raw
        assert "next_page" in ticket_raw
        assert "previous_page" in ticket_raw
        assert "count" in ticket_raw
        ticket = api.get_tickets()  # Processed tickets with formatted dates
        assert "tickets" in ticket
        assert "next_page" in ticket
        assert "previous_page" in ticket
        assert "count" in ticket
        self.assertEqual(ticket_raw["tickets"][-1]['id'], 100)  # count = 101 in data.json, but actual length of json file = 100

    # Happy unit test
    def test_date_formatting(self):  # test date is formatted correctly
        api = requestHandler()
        updated, created = api.formatDates("2017-11-13T12:34:23Z", "2017-10-13T12:34:23Z")
        self.assertEqual(updated, "2017-11-13 12:34:23")
        self.assertEqual(created, "2017-10-13 12:34:23")
    
    # Test to get bad request response from API
    @patch('model.requestHandler.requests.get', side_effect=test_get_bad_request_response)
    # Test to get bad request from API, mocking the network access to simulate API call/request.
    def test_bad_request(self, test_get):
        api = requestHandler()
        self.assertEqual(api.zendeskRequest(), -1)
        # testing that api.zendeskRequest returns -1 on general bad request (response status code = 400 in this case)
        self.assertEqual(api.get_tickets(), -1)
        # api.get_tickets() returns -1, if api.zendeskRequest() returns -1 (bad request)
        self.assertEqual(api.get_ticket('1'), -1)
        # api.get_ticket() returns -1, if api.zendeskRequest() returns -1 (bad request)
    
    # Test to get unauthorized response from API 
    @patch('model.requestHandler.requests.get', side_effect=test_get_unauthorized_response)
    def test_unauthorized_request(self, test_get):
        api = requestHandler()
        self.assertEqual(api.zendeskRequest(), 401)
        # testing that api.zendeskRequest returns 401 on 401 unauthorized request
        #self.assertEqual(api.get_tickets(), 401)
        # api.get_tickets() returns 1, if api.zendeskRequest() returns None (user not authorized)
        self.assertEqual(api.get_ticket('1'), 401)
        # api.get_ticket() returns 1, if api.zendeskRequest() returns None (user not authorized)

    # Test to get unavailable response from API    
    @patch('model.requestHandler.requests.get', side_effect=test_api_unavailable_response)
    def test_api_unavailable_request(self, test_get):
        api = requestHandler()
        self.assertEqual(api.zendeskRequest(), 503)
        # testing that api.zendeskRequest returns 503 on 503 API unavailable response
        self.assertEqual(api.get_tickets(), 503)
        # Checking that api.get_tickets() returns 503, if api.zendeskRequest() returns 503 (API unavailable)
        self.assertEqual(api.get_ticket('1'), 503)
        # Checking that api.get_ticket() returns 503, if api.zendeskRequest() returns 503 (API unavailable)

    # Test to get 404 Invalid ticket ID response from API, on requesting non-existent ticket ID    
    @patch('model.requestHandler.requests.get', side_effect=test_invalid_ticket_id_response)
    def test_invalid_ticket_id_request(self, test_get):  # 404 Invalid Ticket ID Response
        api = requestHandler()
        self.assertEqual(api.zendeskRequest(), 404)
        self.assertEqual(api.get_ticket('abcd'), 404)  # Invalid ticket ID 'abcd', fetches a response of -1 from get_ticket


# Tests for appView.py module
class ViewTester(unittest.TestCase):
    # Happy unit test
    # Testing that basic functionality of view is working as expected
    def test_view(self):
        j1 = test_get_one_ticket()
        j2 = test_get_all_tickets()
        view = AppView()
        self.assertEqual(view.displayTicket(j1.json_data), 0)
        self.assertEqual(view.displayTickets(j2.json_data, 1), 1)
        self.assertEqual(view.initialize(), 0)
        self.assertEqual(view.quit(), 0)
        self.assertEqual(view.fetchTickets("all"), 0)
        self.assertEqual(view.show_menu(), 0)


class MainMenuTester(unittest.TestCase):
    @patch("builtins.input", side_effect=['menu', '1', 'd', 'q']) 
    def test_user_quit(self, input):
        viewer = start_viewer()
        with self.assertRaises(SystemExit) as cm:
            viewer.run()
        self.assertEqual(viewer.currPage, 2) 


# Tests for TicketController.py module
class ControllerTester(unittest.TestCase):
    # Happy unit test
    @patch("builtins.input", return_value='q')  # Simulate user quitting correctly to test quitting functionality
    def test_user_quit(self, input):
        controller = TicketController()
        with self.assertRaises(SystemExit) as cm:
            controller.run()
        self.assertEqual(cm.exception.code, 0)  # Confirming system raising expected exception code
        

    # Happy unit test
    # Simulate and test user inputs and related outputs to show all tickets then quit, followed by display all & paging.
    # ['1', 'q', '1', 'd', 'q']: Show all tickets (1) through menu then quit (q). Then display all (1), go down one page
    # (d) & quit (q)
    @patch("builtins.input", side_effect=['menu', 'random command', 'q','1','menu', 'q', '1', 'd','q', '2', '3','q'])
    @patch('model.requestHandler.requests.get', side_effect=test_get_all_tickets)
    def test_show_all(self, input, test_get):
        controller = TicketController()
        with self.assertRaises(SystemExit) as cm:
            controller.run()
        self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            controller.run()
        self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            controller.run()
        self.assertEqual(cm.exception.code, 0)
        with self.assertRaises(SystemExit) as cm:
            controller.run()
        self.assertEqual(cm.exception.code, 0)
        self.assertEqual(controller.currPage, 2) # We scrolled down one page, so checking if paging happened correctly.
    
    #testing circular pagination   
    @patch("builtins.input", side_effect=['1','d','u','u','d', 'random_message', 'q'])
    @patch('model.requestHandler.requests.get', side_effect=test_get_all_tickets)
    def test_show_all_uppage(self, input, test_get):
        controller = TicketController()
        with self.assertRaises(SystemExit) as cm:
            controller.run()
        self.assertEqual(cm.exception.code, 0)
        self.assertEqual(controller.currPage, 1)
    
        # Test to get unauthorized response from API 
    @patch('model.requestHandler.requests.get', side_effect=test_get_unauthorized_response)
    def test_unauthorized_request(self, test_get):
        controller = TicketController()
        self.assertEqual(controller.showAllTickets(), 401)
    
    @patch("builtins.input", side_effect=['1'])
    @patch('model.requestHandler.requests.get', side_effect=test_get_bad_request_response)
    # Test to get bad request from API, mocking the network access to simulate API call/request.
    def test_bad_request(self, input, test_get):
        controller = TicketController()
        self.assertEqual(controller.showAllTickets(), -1)
        self.assertEqual(controller.showOneTicket(), False)
    
    
    # Test to get 404 Invalid ticket ID response from API, on requesting non-existent ticket ID    
    @patch('model.requestHandler.requests.get', side_effect=test_invalid_ticket_id_response)
    def test_invalid_ticket_id_request(self, test_get):  # 404 Invalid Ticket ID Response
        controller = TicketController()
        self.assertEqual(controller.showAllTickets(), 404)
    
        # Test to get unavailable response from API    
    @patch('model.requestHandler.requests.get', side_effect=test_api_unavailable_response)
    def test_api_unavailable_request(self, test_get):
        controller = TicketController()
        # Checking that acontroller.showAllTickets() returns 503 when API is unavailable
        self.assertEqual(controller.showAllTickets(), 503)
        
    @patch("builtins.input", side_effect=['2'])
    @patch('model.requestHandler.requests.get', side_effect=test_get_unauthorized_response)
    def test_api_one_ticket_unauthorized_request(self, input, test_get):
        controller = TicketController()
        # Checking that acontroller.showOneTicket() returns 401 when API is unavailable
        self.assertEqual(controller.showOneTicket(), False)
    
    @patch("builtins.input", side_effect=['2'])
    @patch('model.requestHandler.requests.get', side_effect=test_api_unavailable_response)
    def test_api_one_ticket_unavailable_request(self, input, test_get):
        controller = TicketController()
        # Checking that acontroller.showOneTicket() returns False when API is unavailable
        self.assertEqual(controller.showOneTicket(), False)
       
    


    # Simulate and test user inputs for getting ticket ID's 2, 3 and 4 to get correct respective outputs.
    @patch("builtins.input", side_effect=['2', '3', '4'])
    @patch('model.requestHandler.requests.get', side_effect=test_get_one_ticket)
    def test_show_one(self, input, test_get):  # Happy unit test
        controller = TicketController()
        self.assertEqual(controller.showOneTicket(), 1)
        self.assertEqual(controller.currID, 2)
        self.assertEqual(controller.showOneTicket(), 1)
        self.assertEqual(controller.currID, 3)
        self.assertEqual(controller.showOneTicket(), 1)
        self.assertEqual(controller.currID, 4)

    # Testing invalid ticket ID request response
    @patch("builtins.input", side_effect=['199'])  # Ticket ID 199 doesn't exist. Testing that we get invalid response.
    @patch('model.requestHandler.requests.get', side_effect=test_invalid_ticket_id_response)
    def test_invalid_ticket_id(self, input, test_get):
        controller = TicketController()
        self.assertEqual(controller.showOneTicket(), False)  # Invalid ticket ID gets False response from showTicket()


if __name__ == "__main__":
    unittest.main()