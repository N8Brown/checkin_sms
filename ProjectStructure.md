# Checkin SMS

## Project Components
- Home Page
- User Registration Page
- User Login Page
- User Dashboard
- Client Sign Up Page

## Component Structure

### Home Page

### User Registration Page
Usernames should be unique with no duplicates as usernames are used to create custom urls for client sign up, as well as link client to.

### User Login Page

### User Dashboard
Edit Profile - User should be able to edit all registration information
- Username
    - Requires validation to ensure no duplicate usernames
- First Name
- Last Name
- Email Address
- Change Password

Custom URL - Show user's custom client sign up URL based on their username. User should be able to copy and paste this URL 

Client list - User should be able to view and delete entries from client list

Manage Phone Number - User should be able to add/remove phone number from account
- Add Phone Number
    - Form that allows user to enter preferred area code for phone number to based from
    - Form results should give user 3-5 phone number options to choose from
    - Limit number of phone numbers per user
- Remove Phone Number
    - Form that allows user to give up phone number
    - Warning informing user that action can't be undone

Message Frequency - User should be able to set the frequency in number of days in which to send automated message to client list

### Client Sign Up Page
Required Fields - Clients should provide the following
- First Name
- Last Name
- Email 
- Phone Number

Client should be linked to a user and a phone number should not be allowed more than once per user

Date of last text message should be stored for each client