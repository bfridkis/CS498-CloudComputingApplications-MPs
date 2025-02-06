# Modified from: https://aws.amazon.com/blogs/machine-learning/creating-a-bankingbot-on-amazon-lex-v2-console-with-support-for-english-and-spanish/

import json
import boto3
What is the distance from Chicago to Springfield?

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('MP3-DistanceGraph')

def lambda_handler(event, context):
    response = dispatch(event)
    return response

def dispatch(intent_request):
    intent_name = intent_request['sessionState']['intent']['name']
    response = None
    # Dispatch to bot's intent handlers
    if intent_name == 'DetermineDistance_CitiesProvided':
        return DetermineDistance_CitiesProvided(intent_request)
    elif intent_name == 'DetermineDistance_CitiesNotProvided':
        return DetermineDistance_CitiesNotProvided(intent_request)

    raise Exception('Intent with name ' + intent_name + ' not supported')
    
def get_slots(intent_request):
    return intent_request['sessionState']['intent']['slots']
    
def get_slot(intent_request, slotName):
    slots = get_slots(intent_request)
    if slots is not None and slotName in slots and slots[slotName] is not None:
        return slots[slotName]['value']['interpretedValue']
    else:
        return None
        
def get_session_attributes(intent_request):
    sessionState = intent_request['sessionState']
    if 'sessionAttributes' in sessionState:
        return sessionState['sessionAttributes']

    return {}
    
def elicit_intent(intent_request, session_attributes, message):
    return {
        'sessionState': {
            'dialogAction': {
                'type': 'ElicitIntent'
            },
            'sessionAttributes': session_attributes
        },
        'messages': [ message ] if message != None else None,
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }
    
def DetermineDistance_CitiesProvided(intent_request):
    print(intent_request)
    session_attributes = get_session_attributes(intent_request)
    source = intent_request['inputTranscript'].split(' from ')[1].split(' to ')[0]
    destination = intent_request['inputTranscript'].split(' from ')[1].split(' to ')[1]
    response = table.query(
        KeyConditionExpression=Key('source').eq(source) & Key('destination').eq(destination),
        #FilterExpression=Attr('name').eq('SomeName')
    )
    print(f"RESPONSE: {response}")
    message =  {
            'contentType': 'PlainText',
            'content': response['Items'][0]['distance']
        }
    fulfillment_state = "Fulfilled"
    return close(intent_request, session_attributes, fulfillment_state, message)
    
def DetermineDistance_CitiesNotProvided(intent_request):
    print(intent_request)
    session_attributes = get_session_attributes(intent_request)
    slots = get_slots(intent_request)
    source = get_slot(intent_request, 'Source')
    destination = get_slot(intent_request, 'Destination')
    response = table.query(
        KeyConditionExpression=Key('source').eq(source) & Key('destination').eq(destination),
        #FilterExpression=Attr('name').eq('SomeName')
    )
    print(f"RESPONSE: {response}")
    message =  {
            'contentType': 'PlainText',
            'content': response['Items'][0]['distance']
        }
    fulfillment_state = "Fulfilled"
    return close(intent_request, session_attributes, fulfillment_state, message)
    

def close(intent_request, session_attributes, fulfillment_state, message):
    intent_request['sessionState']['intent']['state'] = fulfillment_state
    return {
        'sessionState': {
            'sessionAttributes': session_attributes,
            'dialogAction': {
                'type': 'Close'
            },
            'intent': intent_request['sessionState']['intent']
        },
        'messages': [message],
        'sessionId': intent_request['sessionId'],
        'requestAttributes': intent_request['requestAttributes'] if 'requestAttributes' in intent_request else None
    }
    
    
# References
# https://aws.amazon.com/blogs/machine-learning/creating-a-bankingbot-on-amazon-lex-v2-console-with-support-for-english-and-spanish/