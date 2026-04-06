from extract import extract_data
from load import load_data
from visualize import visualize_main

def run_pipeline():
    file_path_extract = 'data/Events.csv'
    file_path_load = 'data/ufc_events.csv'
    table_name = 'ufc_events'

    print('Starting ETL Pipeline...')

    # Extract and Transform
    df = extract_data(file_path=file_path_extract)

    # DataFrame to the database and updating the csv
    load_data(df=df, file_path=file_path_load, table_name=table_name)

    print('Pipeline has been successfully finished!')

if __name__ == "__main__":
    run_pipeline()
    visualize_main()