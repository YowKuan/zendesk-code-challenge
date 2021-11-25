
# Zendesk-Coding-Challenge

In this project, I followed standard MVC (Model-Controller-View) pattern to build a ticketing viewing system by calling API endpoints using Zendesk API.


### Major tasks:

- Connect to the Zendesk API
- Request all the tickets for your account
- Display them in a list
- Display individual ticket details
- Page through tickets when more than 25 are returned
- Test all the code


### Segmentation of Tasks 

Model - For communication with Zendesk API to fetch existing tickets 

Controller - Responsible for major usage logics. Request data from Model, and pass to View.

View - Display message to users.


## Installation
First, please clone this repo using the following command:

```bash
git clone https://github.com/YowKuan/zendesk-code-challenge.git
```


This repo is developed in Python3.7. 
Apart from the standard library, I used requests for making the HTTP request,
dotenv for storing environment variables.

```bash
  pip3 install requests
  pip3 install dotenv
  pip3 install coverage
```

### Setup environment variables
In a production ready code, we shouldn't put important user credential in public. 
Instead we store it in the separate .env file.

Please put the .env file under /model folder, which is the place we performs connection to the Zendesk API.

```bash
ZENDESK_SUBDOMAIN = {'zendeskcodingchallengedomain'}
ZENDESK_EMAIL = 'zendeskaccountemail@gmail.com'
ZENDESK_PASSWORD = 'your p@ssw0rd'
```
    
## Usage

Use the following command to start the application:

```bash
python3 entryPoint.py
```


## Test

Use the following command to start the test(remember to change {directory of this repo} into your current directory

```bash
cd testing
coverage run --source {directory of this repo}/zendesk-coding-challenge testTicketViewer.py
coverage html
open htmlcov/index.html
```

#### The last open command opens the coverage file in this repository. We've reached 99% overall testing coverage. 



