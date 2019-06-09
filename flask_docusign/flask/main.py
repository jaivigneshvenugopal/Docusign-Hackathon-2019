#!flask/bin/python
from flask import Flask
from flask import render_template, url_for, redirect, session, flash, request
from os import path
import json
import base64
import re
from flask import *
import os
import base64
from docusign_esign import ApiClient, EnvelopesApi, EnvelopeDefinition, Signer, SignHere, Tabs, Recipients, Document, RecipientViewRequest

app = Flask(__name__)

# Settings
# Fill in these constants

#Local
#curl -X POST -H "Content-Type: application/json" -d '{"email":"gohchangming@gmail.com","name":"Clement"}' http://127.0.0.1:5000/requestsignature
#curl -X POST -H "Content-Type: application/json" -d '{"email":"gohchangming@gmail.com","name":"Clement"}' http://127.0.0.1:5000/sendemail

#Production
#curl -X POST -H "Content-Type: application/json" -d '{"email":"gohchangming@gmail.com","name":"Clement"}' https://hellodocusign.appspot.com/requestsignature
#curl -X POST -H "Content-Type: application/json" -d '{"email":"gohchangming@gmail.com","name":"Clement"}' https://hellodocusign.appspot.com/sendemail

# Obtain an OAuth access token from https://developers.hqtest.tst/oauth-token-generator
access_token = 'eyJ0eXAiOiJNVCIsImFsZyI6IlJTMjU2Iiwia2lkIjoiNjgxODVmZjEtNGU1MS00Y2U5LWFmMWMtNjg5ODEyMjAzMzE3In0.AQoAAAABAAUABwAAD_y-8OzWSAgAAE8fzTPt1kgCAEbEPnJQ6jlLn14649CC1dcVAAEAAAAYAAEAAAAFAAAADQAkAAAAZjBmMjdmMGUtODU3ZC00YTcxLWE0ZGEtMzJjZWNhZTNhOTc4EgABAAAACwAAAGludGVyYWN0aXZlMACAeGO-8OzWSDcAUxfloEHtykuVjAG7RfCZwg.an7XgHr3HsKWGN_ss7iOvcylXi7Py95O82eD-j6IxiK391cj5NYN8KkdwRKYTt-nFjRPqT9pnyNtRdwI4R-cD0ewmIPRBd693Sx907xpiFo80fwYECJJYzagFP2urwk4kVUkgwIIByRMSEvQ3iV_KmI_3jsTY_Ok_e0fu1_tIvgcT0_Yl709UlITo53bkM6ohycNsgyyzPCyrFxLFSAihnXvHmJt5yeGzozj_x9BxiAR29NDdL7uQXfFxdntfx2v18jLe92uVTwFscwesJv7u6imaOZZN3IUriAUhPjFshACfC4-nuwMLH_YML6JhQl8BKExLxxlsYcMQevXPusnwg'
#### Obtain your accountId from demo.docusign.com -- the account id is shown in the drop down on the
# upper right corner of the screen by your picture or the default picture. 
account_id = 'c1a625d3-27d3-4260-b4cd-f9c647e3618e'
## Recipient Information:
recipientname = 'Clement Goh'
recipientemail = 'clement@leadiq.com'
# The document you wish to send. Path is relative to the root directory of this repo.
file_name_path = 'demo_documents/Petition.pdf'
base_path = 'https://demo.docusign.net/restapi'
base_url = 'http://localhost:5000'
#base_url = 'https://docusignbackendproject.herokuapp.com/'
#base_url = 'https://hellodocusign.appspot.com'
client_user_id = 'c1a625d3-27d3-4260-b4cd-f9c647e3618e'
authentication_method = 'None' 

# Set FLASK_ENV to development if it is not already set
if 'FLASK_ENV' not in os.environ:
    os.environ['FLASK_ENV'] = 'development'

# Constants
APP_PATH = os.path.dirname(os.path.abspath(__file__))

@app.route('/sendemail', methods=['GET', 'POST'])
def sendemail():
    request_json = request.get_json()
    recipientemail = request_json['email']
    recipientname = request_json['name']
    send_document_for_signing(recipientemail, recipientname)
    return jsonify({'result':'Success!', 'name':recipientname, 'email':'recipientemail'})

@app.route('/requestsignature', methods=['GET', 'POST'])
def requestsignature():
    request_json = request.get_json()
    recipientemail = request_json['email']
    recipientname = request_json['name']
    link = embedded_signing_ceremony(recipientemail, recipientname)
    return redirect(link, code=302)

@app.route('/dsreturn')
def returntopage():
    return "docusign signing complete"

def send_document_for_signing(recipientemail, recipientname):
    #Sends the document <file_name> to be signed by <signer_name> via <signer_email>

    # Create the component objects for the envelope definition...
    with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    document = Document( # create the DocuSign document object 
        document_base64 = base64_file_content, 
        name = 'Example document', # can be different from actual file name
        file_extension = 'pdf', # many different document types are accepted
        document_id = 1 # a label used to reference the doc
    )

    # Create the signer recipient model 
    signer = Signer( # The signer
        email = recipientemail, name = recipientname, recipient_id = "1", routing_order = "1")

    # Create a sign_here tab (field on the document)
    sign_here = SignHere( # DocuSign SignHere field/tab
        document_id = '1', page_number = '1', recipient_id = '1', tab_label = 'SignHereTab',
        x_position = '100', y_position = '400')

    # Add the tabs model (including the sign_here tab) to the signer
    signer.tabs = Tabs(sign_here_tabs = [sign_here]) # The Tabs object wants arrays of the different field/tab types


    # Next, create the top level envelope definition and populate it.
    envelope_definition = EnvelopeDefinition(
        email_subject = "Please sign this document sent from the Python SDK",
        documents = [document], # The order in the docs array determines the order in the envelope
        recipients = Recipients(signers = [signer]), # The Recipients object wants arrays for each recipient type
        status = "sent" # requests that the envelope be created and sent.
    )
    # Ready to go: send the envelope request
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)
    return results

def embedded_signing_ceremony(recipientemail, recipientname):
    """
    The document <file_name> will be signed by <signer_name> via an
    embedded signing ceremony.
    """

    #
    # Step 1. The envelope definition is created.
    #         One signHere tab is added.
    #         The document path supplied is relative to the working directory
    #
    # Create the component objects for the envelope definition...
    with open(os.path.join(APP_PATH, file_name_path), "rb") as file:
        content_bytes = file.read()
    base64_file_content = base64.b64encode(content_bytes).decode('ascii')

    document = Document( # create the DocuSign document object 
        document_base64 = base64_file_content, 
        name = 'Example document', # can be different from actual file name
        file_extension = 'pdf', # many different document types are accepted
        document_id = 1 # a label used to reference the doc
    )

    # Create the signer recipient model 
    signer = Signer( # The signer
        email = recipientemail, name = recipientname, recipient_id = "1", routing_order = "1",
        client_user_id = client_user_id, # Setting the client_user_id marks the signer as embedded
    )

    sign_here = SignHere( # DocuSign SignHere field/tab
        document_id = '1', page_number = '1', recipient_id = '1', tab_label = 'SignHereTab',
        x_position = '100', y_position = '400')

    # Add the tabs model (including the sign_here tab) to the signer
    signer.tabs = Tabs(sign_here_tabs = [sign_here]) # The Tabs object wants arrays of the different field/tab types

    # Next, create the top level envelope definition and populate it.
    envelope_definition = EnvelopeDefinition(
        email_subject = "Please sign this document sent from the Python SDK",
        documents = [document], # The order in the docs array determines the order in the envelope
        recipients = Recipients(signers = [signer]), # The Recipients object wants arrays for each recipient type
        status = "sent" # requests that the envelope be created and sent.
    )

    #  Step 2. Create/send the envelope.
    #
    api_client = ApiClient()
    api_client.host = base_path
    api_client.set_default_header("Authorization", "Bearer " + access_token)

    envelope_api = EnvelopesApi(api_client)
    results = envelope_api.create_envelope(account_id, envelope_definition=envelope_definition)

    #
    # Step 3. The envelope has been created.
    #         Request a Recipient View URL (the Signing Ceremony URL)
    #
    envelope_id = results.envelope_id
    recipient_view_request = RecipientViewRequest(
        authentication_method = authentication_method, client_user_id = client_user_id,
        recipient_id = '1', return_url = base_url + '/dsreturn',
        user_name = recipientname, email = recipientemail
    )

    results = envelope_api.create_recipient_view(account_id, envelope_id,
        recipient_view_request = recipient_view_request)
    
    #
    # Step 4. The Recipient View URL (the Signing Ceremony URL) has been received.
    #         Redirect the user's browser to it.
    #
    return results.url

if __name__ == '__main__':
    app.run(debug=False)

