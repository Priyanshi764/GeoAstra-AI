import json
import fitz

def parse_file(filepath):

    if filepath.endswith(".txt"):

        with open(filepath,"r",encoding="utf-8") as f:

            return f.read()

    elif filepath.endswith(".json"):

        with open(filepath,"r",encoding="utf-8") as f:

            data=json.load(f)

            return json.dumps(data,indent=2)

    elif filepath.endswith(".pdf"):

        doc=fitz.open(filepath)

        text=""

        for page in doc:

            text+=page.get_text()

        return text

    elif filepath.endswith(".csv"):

        with open(filepath,"r",encoding="utf-8") as f:

            return f.read()

    return ""