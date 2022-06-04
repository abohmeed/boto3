from flask import Flask, jsonify, request
from aws import Aws

app = Flask(__name__)


@app.route('/ec2', methods=['GET', 'POST', 'DELETE'])
def ec2():
    if request.method == "POST":
        aws = Aws(instance_type="t3.micro", image_id="ami-05db0e60504db9e1b", tenant="Ahmed")
        output = aws.create_instances()
        print(output)
        return jsonify({
            'instance_ids': output['instances'],
            'private_key': output['private_key']
        })
