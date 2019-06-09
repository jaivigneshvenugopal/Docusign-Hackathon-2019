# ds_config.py
#
# DocuSign configuration settings
import os

DS_CONFIG = {
    'ds_client_id': 'a38f0eb5-f525-4ff3-952e-35b56a4c1187', # The app's DocuSign integration key
    'ds_client_secret': 'b142eb81-2f68-4283-8309-4831f250147b', # The app's DocuSign integration key's secret
    'signer_email': 'gohchangming@gmail.com',
    'signer_name': 'Goh Chang Ming Clement',
    'app_url': 'http://127.0.0.1:5000/', # The url of the application. Eg http://localhost:5000
    # NOTE: You must add a Redirect URI of appUrl/ds/callback to your Integration Key.
    #       Example: http:#localhost:5000/ds/callback
    'authorization_server': 'https://account-d.docusign.com',
    'session_secret': 'b142eb81-2f68-4283-8309-4831f250147b', # Secret for encrypting session cookie content
                                          # Use any random string of characters
    'allow_silent_authentication': True, # a user can be silently authenticated if they have an
    # active login session on another tab of the same browser
    'target_account_id': None, # Set if you want a specific DocuSign AccountId, 
                               # If None, the user's default account will be used.
    'demo_doc_path': 'demo_documents',
    'doc_docx': 'World_Wide_Corp_Battle_Plan_Trafalgar.docx',
    'doc_pdf':  'World_Wide_Corp_lorem.pdf',
    # Payment gateway information is optional
    'gateway_account_id': '{DS_PAYMENT_GATEWAY_ID}',
    'gateway_name': "stripe",
    'gateway_display_name': "Stripe",
    'github_example_url': 'https://github.com/docusign/eg-03-python-auth-code-grant/tree/master/app/',
    'documentation': '' # Use an empty string to indicate no documentation path.
}
