# Check-in Text App

## DESIRED FEATURES
* User registration/opt-in form
    * First Name
    * Last Name
    * Email address
    * Phone number
    * Is Active (true/not searching for job)
* Check-in text message sent at user selected frequency
* Text replies returned to Taylor in email form

## PROJECT PHASE 1
Phase 1 of the project will look to establish baseline functionality of sending texts, receiving text replies, and forwarding those replies via email. This phase will make use of the Twilio SMS API and will require setting up free trial account for development purposes. 

### PHASE 1 MILESTONES
- Write a script to send a text message
- Write a script to receive a response text message 
- Write a script to send received text message as an email
- Create a Django app with a user registration/opt-in form page

## Script to send text message
- Go through the [Twilio Python Quickstart](https://www.twilio.com/docs/sms/quickstart/python) to learn the basics of sending text messages with the API.

## Script to receive text message
- Go through the [Twilio Receive & Reply](https://www.twilio.com/docs/sms/tutorials/how-to-receive-and-reply) guide to learn the basics of receiving and replying to text messages with the API.

## Script to send received text message as an email
- Utilize standard Python email library to test functionality and ensure that it is compatible with Django

## Create a Django app with a user registration/opt-in form page

### Design Considerations
Proof of concept design will be modeled after https://www.taylordesseyn.com and utilize the following:

#### Fonts
* Bebas-neue-pro (headings)
* Fjalla One (sub-headings)
* Libre Franklin (general text)

Add to HTML
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Fjalla+One&family=Libre+Franklin&display=swap" rel="stylesheet">
```

Add to CSS
```css
font-family: 'Bebas Neue', cursive;
font-family: 'Fjalla One', sans-serif;
font-family: 'Libre Franklin', sans-serif;
```

#### Colors
* Red - #7f0518
* Light Red - #A40E1A
* Black - #000000
* White - #ffffff

