from pathlib import Path
import sys
import pandas as pd
import streamlit as st
from functools import wraps
from enum import IntEnum,Enum
sys.path.append(str(Path(__file__).parents[1].absolute()))

data_path  = 'data/data.csv'
PERMISSION_URLS = [
    'https://apimocha.com/streamlituser/admin_permission',
    'https://apimocha.com/streamlituser/boothuser_permission',

]

class Role(Enum):
    DEFAULT=1
    ADMIN = 2
    AGENT = 3


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

def assign_role(role="default"):
    if role is None:
       return Role.DEFAULT

    if role.lower() in ("admin","owner"):
        return Role.ADMIN
    elif role.lower() in ("agent","boothuser"):
        return Role.AGENT
    else:
        return Role.DEFAULT

def check_access(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if st.session_state.role == access_level:
                return f(*args, **kwargs)
        return decorated_function
    return decorator