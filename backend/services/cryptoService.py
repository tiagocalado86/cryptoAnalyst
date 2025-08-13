import requests
import json
import shutil
import os
from dotenv import load_dotenv


class CryptoService:

    @staticmethod
    def getCryptoInfo(url, headers, params):
        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            try:
                data = response.json()
                with open("cryptoData.json", 'w') as file:
                    json.dump(data, file, indent=4)
                    CryptoService.__moveJson()
            except Exception as e:
                print(f"An error occurred: {e}")
        else:
            print(f"Error: {response.status_code}")

    @staticmethod
    def __moveJson():
        load_dotenv()
        try:
            shutil.move(os.getenv("SRC_FILE_PATH_DATA"), os.getenv("DEST_FILE_PATH"))
        except:
            os.remove(os.getenv("DEST_FILE_PATH_REMOVE_DATA"))
            shutil.move(os.getenv("SRC_FILE_PATH_DATA"), os.getenv("DEST_FILE_PATH"))
