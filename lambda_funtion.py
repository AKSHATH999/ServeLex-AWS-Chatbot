import json
import boto3

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('ServeLexOrders')

def lambda_handler(event, context):

    try:
        # Get orderId from Lex slot
        order_id = event['sessionState']['intent']['slots']['orderId']['value']['interpretedValue']

        # Query DynamoDB
        response = table.get_item(
            Key={
                'orderId': order_id
            }
        )

        item = response.get('Item')

        if item:
            status = item.get('status')
            delivery = item.get('deliveryDate')

            message = f"Your order {order_id} is {status}. Expected delivery is {delivery}."

        else:
            message = f"Sorry, I could not find order {order_id}."

    except Exception as e:
        message = "There was an error checking your order status."

    # Send response back to Lex
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                "name": "OrderStatementIntent",
                "state": "Fulfilled"
            }
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ]
    }