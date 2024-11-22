from flask import Flask, request, jsonify  
import boto3  
import jwt  
import os  
import datetime  

app = Flask(__name__)  
dynamodb = boto3.resource('dynamodb')  
table = dynamodb.Table('Tokens')  

@app.route('/generate_token', methods=['POST'])  
def generate_token():  
    # Check if request JSON has required keys
    if not request.json or 'user_id' not in request.json or 'phone_number' not in request.json:
        return jsonify({'status': 'error', 'message': 'Missing user_id or phone_number'}), 400

    user_id = request.json['user_id']  
    phone_number = request.json['phone_number']  

    # Generate token
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
    token = jwt.encode({'user_id': user_id, 'exp': expiration_time}, os.environ['SECRET_KEY'], algorithm='HS256')  

    # Store token in DynamoDB
    try:
        table.put_item(Item={'token': token, 'user_id': user_id, 'status': 'unused', 'expiration': expiration_time.timestamp()})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    # Send token via SNS
    sns = boto3.client('sns')  
    try:
        sns.publish(PhoneNumber=phone_number, Message=f'Your token is: {token}')  
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

    return jsonify({'status': 'success', 'message': 'Token sent'})  

if __name__ == '__main__':  
    app.run(host='0.0.0.0', port=5000)
