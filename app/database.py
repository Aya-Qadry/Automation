from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from directInfo import start_search , brand_info
import os

class Database:
    def __init__(self):
        username = os.getenv('aqadry')
        password = os.getenv('1234')
        cluster = os.getenv('Automation')
        
        connection_string = f"mongodb+srv://{username}:{password}{cluster}.mongodb.net/Automation?retryWrites=true&w=majority"
        
        try:
            self.client = MongoClient(connection_string)

            self.client.admin.command('ismaster')
            self.db = self.client['Automation']
            print("Connected to MongoDB successfully!")
        except ConnectionFailure:
            print("Failed to connect to MongoDB")
            self.client = None
            self.db = None

    mandataire = {
        "mandataire": True,
        "isCPI": False, 
        "deposant": "un_seul",
        "priorite": "non",
        "certificat": "non"
    }

    def add_personne_moral(json_document): 
        raison_sociale = json_document["raison_sociale"]
        
        url = "https://www.directinfo.ma/"
        page_source = start_search(url,raison_sociale)
        website_data = brand_info(page_source)
        extracted_raison_sociale = website_data["Dénomination"]

        #if raison_sociale == extracted_raison_sociale : 




    def __del__(self):
        if self.client:
            self.client.close()