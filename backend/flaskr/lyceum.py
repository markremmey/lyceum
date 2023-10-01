import functools
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import openai
import os
import logging
import re

from flask import (
    Blueprint, flash, jsonify, g, redirect, render_template, request, session, url_for
)

openai.api_type = "azure"
openai.api_base = os.getenv("AZ_BASE")
openai.api_version = "2023-07-01-preview"
openai.api_key = os.getenv("AZ_OPENAI_API_KEY")

# This creates a "Blueprint" or an organization of routes
logging.basicConfig(level=logging.DEBUG)
bp = Blueprint('lyceum', __name__, url_prefix='/lyceum')

@bp.route('/')
def index():
    return render_template('lyceum/index.html')

# now, rather than calling app.route() like we usually would with flask
# we are just calling the route for this blueprint
@bp.route('/next_text', methods=('GET', 'POST'))
def next_text():
    ## Create function to retrieve next item in blob storage after user clicks a button
    header = ""
    content = ""
    load_dotenv('../../.env')

    storageaccount = os.getenv('STORAGE_ACCOUNT')
    storage_creds = os.getenv('SAS_TOKEN')

    blob_service = BlobServiceClient(
        account_url=f"https://{storageaccount}.blob.core.windows.net", 
        credential=storage_creds
    )
    blob_container = blob_service.get_container_client('silver')

    file_number = session.get('file_number', 0)
    if file_number>39:
        file_number = 0
    

    logging.debug('File number (next Text): ' + str(file_number))

    title = 'The History Of The Decline And Fall Of The Roman Empire, Complete'
    path = title + '/' + str(file_number) + '.txt'

    logging.debug('Path: ' + path)
    content = blob_container.download_blob(path).readall()

    cleaned_text = re.sub(r"\\r\\n|b'", '', content.decode('utf-8'))

    session['file_number'] = file_number+1
    

    return render_template('lyceum/lyceum-extension.html', header=header, content=cleaned_text)

@bp.route('/prev_text', methods=('GET', 'POST'))
def prev_text():
    header = ""
    content = ""
    load_dotenv('../../.env')

    storageaccount = os.getenv('STORAGE_ACCOUNT')
    storage_creds = os.getenv('SAS_TOKEN')

    blob_service = BlobServiceClient(
        account_url=f"https://{storageaccount}.blob.core.windows.net", 
        credential=storage_creds
    )
    blob_container = blob_service.get_container_client('silver')
    
    file_number = session.get('file_number', 1)
    file_number = max(1, file_number - 1)  # Ensure file_number doesn't go below 1

    title = 'The History Of The Decline And Fall Of The Roman Empire, Complete'
    path = title + '/' + str(file_number) + '.txt'

    logging.info('Path: ' + path)
    content = blob_container.download_blob(path).readall()

    cleaned_text = re.sub(r"\\r\\n|b'", '', content.decode('utf-8'))

    session['file_number'] = file_number  # Update the session file_number

    logging.debug('File number (prev Text): ' + str(file_number))

    return render_template('lyceum/lyceum-extension.html', header=header)



@bp.route('/commentary', methods=('GET', 'POST'))
def commentary():
    messages = []
    # text=request.form['text']
    text = "Theodoric the Ostrogoth, the fourteenth in lineal descent of the royal line of the Amali, was born in the neighborhood of Vienna two years after the death of Attila."
    prompt = f"Can you explain the following text?  Text: {text}"
    openai.api_key = os.getenv("AZ_OPENAI_API_KEY")
    
    messages.append({"role": "user", "content": prompt})
    # messages.append({"role": "assistant", "content": f"{item['label']}"})
    
    response = openai.ChatCompletion.create(
                engine="chat",
                messages = messages,
                temperature=0.7,
                max_tokens=3,
                top_p=0.95,
                frequency_penalty=0,
                presence_penalty=0,
                stop=None)
    
    return render_template(content = jsonify(response.choices[0].message.content))
