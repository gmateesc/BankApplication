#!/usr/bin/env python3

#from __future__ import print_function

from flask import Flask, jsonify, abort
from flask import request, make_response

import util

#
# Create app instance
#
app = Flask(__name__)


#
# Accounts cache
#
accounts = [ ]



#
# Associate URI /bank/api/v1/accounts and method GET 
# with the function get_accounts
#
@app.route('/banking/api/v1/accounts', methods=['GET'])
def get_accounts():
    return jsonify({'accounts': accounts})


#
# Associate URI /banking/api/v1/account/<account_id> and method GET 
# with the function get_account
#
@app.route('/banking/api/v1/accounts/<account_id>', methods=['GET'])
def get_account(account_id):

    # <account_id> from URI is translated to thr account_id param 
    # of the func get_account()

    #account = [account for account in accounts if account['id'] == account_id]
    account = util.load_account(app.config, accounts, account_id)
    if len(account) == 0:
        abort(404)

    return jsonify({'account': account[0]})


#
# Associate URI /banking/api/v1/accounts and method POST
# with the function create_account
#
@app.route('/banking/api/v1/accounts', methods=['POST'])
def create_account():

    print("POST /banking/api/v1/account")

    if not request.is_json:
        abort(400)

    json_obj = request.get_json()
    print("POST request.json = ", json_obj)

    try:
      account = {
        'iban':      json_obj['iban'],
        'type':      json_obj['type'],
        'customer_id':  json_obj['customer_id'],          
        'currency':  json_obj.get('currency', "")
      }

      print("POST account = ", account)
      util.request_check(account)

    except (TypeError, KeyError) as err:
      abort(400)

    util.save_account(app.config, accounts, account)

    #return jsonify({'foo': 'bar'}), 201
    return jsonify(account), 201


#
# Associate URI /banking/api/v1/accounts/<account_id> and method DELETE
# with the function delete_account
#
@app.route('/banking/api/v1/accounts/<int:account_id>', methods=['DELETE'])
def delete_account(account_id):
    account = [account for account in accounts if account['id'] == account_id]
    if len(account) == 0:
        abort(404)
    accounts.remove(account[0])
    return jsonify({'result': True})


#
# Error handlers
#

@app.errorhandler(400)
def bad_request(error):
    if request.method == 'POST':
        msg = "Ensure payload is a valid JSON, e.g., "
        msg += "{'iban':<str>,'type':<str>,'currency':<str>,'customer_id':<int>}"
    else:
        msg =""
    return make_response(jsonify({"error": "Bad request (400). " + msg}), 400)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found (404)'}), 404)


@app.errorhandler(405)
def not_allowed(error):
    return make_response(jsonify({'error': 'Method not allowed (405)'}), 405)




#
# Run app when this file is the main program
#

if __name__ == '__main__':

    #
    # Configure the app
    #
    app.config.from_object("conf")

    # 
    # Load SSL certificate and key into the context object
    # 
    #context = (app.config['SSL_CERT_DIR'] + '/cert.pem', app.config['SSL_CERT_DIR'] + '/key.pem')

    #
    # Run the app
    #

    # using an SSL context
    #app.run(host=app.config['HOST'], port=app.config['PORT'], ssl_context=context, threaded=True)
    
    # not using and SSL context
    app.run(host=app.config['HOST'], port=app.config['PORT'], threaded=True)        
    

