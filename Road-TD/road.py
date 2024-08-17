import geojson
import csv

def extract_to_csv(geojson_file_path, csv_file_path):
    with open(geojson_file_path, 'r', encoding='utf-8') as file:
        data = geojson.load(file)

    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['STREET_NAME_EN', 'STREET_NAME_TC', 'STREET_CODE', 'STREET_CENTRELINE_ID']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        features = data['features']
        for feature in features:
            properties = feature.get('properties', {})
            street_name_en = properties.get('STREET_NAME_EN', '')
            street_name_tc = properties.get('STREET_NAME_TC', '')
            street_code = properties.get('STREET_CODE', '')
            street_centreline_id = properties.get('STREET_CENTRELINE_ID', '')

            if street_name_en and street_name_tc:
                row = {
                    'STREET_NAME_EN': street_name_en.strip() if street_name_en else '',
                    'STREET_NAME_TC': street_name_tc.strip() if street_name_tc else '',
                    'STREET_CODE': street_code,
                    'STREET_CENTRELINE_ID': street_centreline_id
                }
                writer.writerow(row)

file_path = '/Users/ottoyu/Downloads/Transportation_RoadCentreline_20240812.gdb_converted.json'  # Update this to your GeoJSON file path
csv_file_path = 'td_road.csv'
extract_to_csv(file_path, csv_file_path)

