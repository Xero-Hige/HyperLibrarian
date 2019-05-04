import os
from os import listdir
from os.path import isfile

import requests


class HyperClient:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def upload_file(self, filename, folder_name):
        with open(filename, 'rb') as upload_file:
            response = requests.request(
                "POST",
                f'http://{self.host}:{self.port}/upload',
                files=[("file", (filename, upload_file, "application/octet-stream"))],
                data={"folder": folder_name}
            )

            return response.status_code,response.status_code == 200

    def upload_folder(self, folder, folder_name):
        files = [f for f in listdir(folder) if isfile(os.path.join(folder, f))]

        files_to_send = []

        for filename in files:
            file_path = os.path.join(folder, filename)
            files_to_send.append(("file", (filename, open(file_path), "application/octet-stream")))

        response = requests.request(
            "POST",
            f'http://{self.host}:{self.port}/upload',
            files=files_to_send,
            data={"folder": folder_name}
        )

        for _, data in files_to_send:
            _, file, _ = data
            file.close()

        return response.status_code,response.status_code == 200
