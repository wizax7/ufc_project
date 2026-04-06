import pandas as pd 

def extract_data(file_path):
    df = pd.read_csv(file_path)

    # renaming columns
    renamed_columns = {
        'Event_Id': 'event_id', 
        'Name': 'name', 
        'Date': 'date', 
        'Location': 'location'
    }
    df = df.rename(columns=renamed_columns)

    # filling in empty data and changing the data format of the 'date' column

    df['event_id'] = df['event_id'].fillna('Unknown')
    df['name'] = df['name'].fillna('Unknown')
    df['location'] = df['location'].fillna('Unknown')

    df['date'] = pd.to_datetime(df['date'], errors='coerce') 

    return df