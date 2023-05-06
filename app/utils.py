from pathlib import Path
import sys
import pandas as pd


sys.path.append(str(Path(__file__).parents[1].absolute()))
data_path  = 'data/data.csv'
PERMISSION_URLS = [
    'https://apimocha.com/streamlituser/admin_permission',
    'https://apimocha.com/streamlituser/boothuser_permission',

]
 

summary_config = {
    "Impressions": {
        "image": "images/impression.png",
        "label": "Total Impressions",
    },
    "Clicks": {
        "image": "images/tap.png",
        "label": "Total Clicks",
    },
    "Spent": {
        "image": "images/hand.png",
        "label": "Total Spend",
    },
    "Total_Conversion": {
        "image": "images/conversion.png",
        "label": "Total Conversion",
    },
    "Approved_Conversion": {
        "image": "images/app_conversion.png",
        "label": "Approved Conversions",
    },
}

def load_data(data_path=data_path):
    df = pd.read_csv(data_path)
    return df
