import functools
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

# This creates a "Blueprint" or an organization of routes
# 
bp = Blueprint('lyceum', __name__, url_prefix='/lyceum')

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
    
    file_number = session.get('file_number', 1)

    title = 'The History Of The Decline And Fall Of The Roman Empire, Complete'
    path = title + '/' + file_number + '.txt'

    content = blob_container.download_blob(file_number).readall()

    session[file_number] = file_number+1

    return header, content