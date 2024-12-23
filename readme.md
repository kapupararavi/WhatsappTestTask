# Installation
Make sure you have python 3.11+ and redis installed in your system.

Create & Activate a virtual environment
```
$ python3 -m venv env
$ source env/bin/activate
```

Install the required dependencies
```
$ pip install -r requirements.txt
```

Create a .env file and add the following variables in it
```
WA_BUSINESS_PHONE_NUMBER_ID=
WA_ACCESS_TOKEN=
```

Run the migrations
```
$ python manage.py migrate
```

Run the server
```
$ python manage.py runserver
```

Run the celery to send the message in background
```
$ cd wa_integration
$ celery -A wa_integration worker -c 1 -l info
```

## Create token to use the the API
Use following token to use the API endpoint
```
$ python manage.py new_token <user's email here>
```

Assuming the server is running on http://127.0.0.1:8000, Call the following API endpoint to send the message to another number.
```
curl --location 'http://127.0.0.1:8000/api/wa/v1/send' \
--header 'Authorization: Token <Replace the token>' \
--header 'Content-Type: application/json' \
--data '{
    "phone_number": "<phone number with country code>",
    "message": "<Message you want to send>""
}'
```

"""
Currently the webhook has the code to save the text messages, its not updating the read receipt. Also for the models we can update them for filtering the message sent to/received from to perform operations, currently they're all separated so it may hard to filter records of specific person.

To send the test message, a record should be added from admin panel to Test whatsapp message, and all other messages sent from API shown to the another model.
"""

I was thinking about adding the other apps like for authentication and adding the authentication classes to the separate app but since the API view and models were not too complex I decided to add it in one, I was also planning add the exception handler but its not required since its a demonstration.

The structure basically I decided to add was adding the accounts and authentication app and the models in the separate apps and the functions and utilties to specific app.
