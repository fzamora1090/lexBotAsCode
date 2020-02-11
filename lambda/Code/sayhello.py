"""
Sample demonstrates implemtnation of Lex Code Hook Interface
In order to serve a sample bot which manages office call traffic
Bot, Intent and Slot models which are compatible with this sample can be found in the Lex Console

"""

import time
import os
import logging

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# Helpers that build all the responses
def elicit_slot(session_attributes, intent_name, slots, slot_to_elicit, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction' {
            'type': 'ElicitSlot',
            'intentName': intent_name,
            'slots': slots,
            'slotToElicit': slot_to_elicit,
            'message': message
        }
    }


def confirm_intent(session_attributes, itent_name, slots, message):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction' {
            'type': 'ConfirmIntent',
            'intentName': intent_name,
            'slots': slots,
            'message': message 
        }
    }


def close(session_attributes, fulfillment_state, message):
    response = {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Close',
            'fufillmentState': fulfillment_state,
            'message': message
        }
    }

    return response


def delegate(session_attributes, slots):
    return {
        'sessionAttributes': session_attributes,
        'dialogAction': {
            'type': 'Delegate',
            'slots': slots
        }
    }


# Helper fucntions
def safe_int(n):
    """
    Safely convert n value to int
    """
    if n is not None:
        return int(n)
    return n

def try_ex(func):
    """
    Call passed in funtion try block. If KeyError is encountered return None.
    This function is intented to be used to safely access dictionary

    Note that this fucntion would have negative impact on performance
    """
    try:
        return func()
    except KeyError:
        return None


def say_hello(intent_request):
    """
    Performs dialog management and fufillment for directing call

    Beyond fulfillment, the implementation for this intent dmeonstrates the following:
        1) use of elicitSlot in slot validation and re-prompting
        2) use of sessionAttributes to pass info that can be used to guide conversation
    """
    slots = intent_requeast['currentIntent']['slots']
    hiname = slots['Name']
    # confirmationStatus = intent_request['currentIntent']['confirmationStatus']
    # sessionAttributes = intent_request['sessionAttributes'] if intent_request['sessionAttribute'] is not None else {}

    return close(
        {},
        'Fulfilled',
        {
            'contentType': 'PlainText',
            'content': "I am Lex Chatbot. Hello %s" %hiname
        }
    )


# Intents
def dispatch(intent_request):
# called whenn the user sepcifies an intent for this bot
    logger.debug('dispatch userId={}, intentName={}'.format(intent_request['userId'], intent_request['currentIntent']['name']))
    
    intent_name = intent_request['currentIntent']['name']
    if intent_name == 'HelloWorld':
        return say_hello(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')


# main handler
def execute(event, context):
    """
    Route the incoming request based on intent
    the JSON body of th erequest is provided in the event slot
    """

    #by default, treat user request as cominng from America/Los_Angeles time zone
    os.environ['TZ'] = 'America/Los_Angeles'
    time.tzset()
    logger.debug('event.bot.name={}'.format(event['bot']['name']))

    return dispatch(event)