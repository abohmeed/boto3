from flask import Flask, jsonify, request
from instance import Instance

app = Flask(__name__)


@app.route('/ec2', methods=['GET', 'POST', 'DELETE'])
def ec2():
    if request.method == "POST":
        tenant = request.json['tenant']
        aws = Instance(instance_type="t3.micro", image_id="ami-05db0e60504db9e1b", tenant=tenant)
        output = aws.create_instances()
        return jsonify({
            'instance_ids': output['instances'],
            'private_key': output['private_key']
        })
