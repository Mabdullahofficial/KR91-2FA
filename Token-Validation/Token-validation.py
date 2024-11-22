from flask import Flask, request, jsonify  
import boto3  
import jwt  
import os  
import logging  

# Set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)  
dynamodb = boto3.resource('dynamodb')  
table = dynamodb.Table('Tokens')  

@app.route('/validate_token', methods=['POST'])  
def validate_token():  
    # Check if the request has a JSON body and contains the token
    if not request.json or 'token' not in request.json:
        logging.error('Missing token in request')
        return jsonify({'status': 'fail', 'message': 'Missing token'}), 400

    token = request.json['token']  

    try:  
        # Decode and validate the token  
        decoded = jwt.decode(token, os.environ['SECRET_KEY'], algorithms=['HS256'])  
        
        # Check token status in DynamoDB  
        response = table.get_item(Key={'token': token})  
        item = response.get('Item')  
        
        if item and item['status'] == 'unused':  
            # Mark token as used  
            table.update_item(  
                Key={'token': token},   
                UpdateExpression="set #status = :s",   
                ExpressionAttributeNames={'#status': 'status'},   
                ExpressionAttributeValues={':s': 'used'}  
            )  
            return jsonify({'status': 'success', 'message': 'Token is valid'}), 200  
        
        return jsonify({'status': 'fail', 'message': 'Token is invalid or already used'}), 401  
    
    except jwt.ExpiredSignatureError:  
        logging.error('Token has expired')
        return jsonify({'status': 'fail', 'message': 'Token has expired'}), 401  
    except jwt.InvalidTokenError:  
        logging.error('Invalid token')
        return jsonify({'status': 'fail', 'message': 'Token is invalid'}), 401  
    except Exception as e:  
        logging.error(f'An error occurred: {e}')
        return jsonify({'status': 'fail', 'message': 'An error occurred during validation'}), 500  

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5001)  
