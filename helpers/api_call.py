from pandas import json_normalize
from helpers.key_finder import api_key
import json
import requests
import random
import pandas as pd

def api_get_breeds_list_and_df():
    breeds_url=f'https://api.thecatapi.com/v1/breeds'
    cats_headers = {"x-api-key": api_key}
    cats_response = requests.get(breeds_url, cats_headers)
    cats_data = json.loads(cats_response.text)

    breeds_list=[]
    names_list=[]
    
    for breed in cats_data:
       breeds_list.append(breed['id'])
       names_list.append(breed['name'])
        
    cats_dict = pd.json_normalize(cats_response.json())
    cats_df = pd.DataFrame(cats_dict)
    cats_df.drop(['cfa_url', 'vetstreet_url', 'vcahospitals_url', 'country_codes', 'country_code', 'alt_names'], axis=1, inplace=True)
    return breeds_list, names_list, cats_df
    
def get_ratings_fig(breed_df):
    attrib_names=[]
    attrib_values=[]
    for attrib in attributes_df.columns:
        attrib_names.append(attrib)
        attrib_values.append(int(attributes_df.loc[0][attrib]))
        
    rankings_df = pd.DataFrame({
        "attribute": attrib_names, 
        "rating": attrib_values
    })
    rankings_df = rankings_df.set_index('attribute')
    fig = rankings_df.plot(kind="barh")
    return fig
