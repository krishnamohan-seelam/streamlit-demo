from pathlib import Path
import sys
import pandas as pd


sys.path.append(str(Path(__file__).parents[1].absolute()))
data_path  = 'data/data.csv'

def load_data(data_path=data_path):
    df = pd.read_csv(data_path)
    return df

def main():
    print(sys.path)

if __name__ == "__main__":
    main()