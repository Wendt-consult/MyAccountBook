import json
from collections import defaultdict

#
# Return form data in json form
#
def get_form_data(form_instance = None):
    html_data = defaultdict()

    for field in form_instance.fields:
        html_data[field] = str(form_instance[field]).replace("\n","") 
    return json.dumps(html_data)