import geojson
from pyproj import Transformer

def extract_and_convert_features(geojson_file_path, output_file_path):
    transformer = Transformer.from_crs("EPSG:2326", "EPSG:4326", always_xy=True)

    with open(geojson_file_path, 'r', encoding='utf-8') as file:
        data = geojson.load(file)

    new_feature_collection = {
        "type": "FeatureCollection",
        "features": []
    }

    for feature in data.get('features', []):
        geometry = feature.get("geometry", {})
        properties = feature.get("properties", {})
        street_centreline_id = properties.get("STREET_CENTRELINE_ID", None)
        street_code = properties.get("STREET_CODE", None)

        if geometry and street_centreline_id and street_code:
            if geometry.get("type") == "LineString":
                converted_coordinates = [
                    [round(coord[0], 6), round(coord[1], 6)]
                    for coord in (transformer.transform(x, y) for x, y in geometry["coordinates"])
                ]

                new_feature = {
                    "type": feature.get("type", "Feature"),
                    "geometry": {
                        "type": "LineString",
                        "coordinates": converted_coordinates
                    },
                    "properties": {
                        "STREET_CENTRELINE_ID": street_centreline_id,
                        "STREET_CODE": street_code
                    }
                }
                new_feature_collection["features"].append(new_feature)

    with open(output_file_path, 'w', encoding='utf-8') as outfile:
        geojson.dump(new_feature_collection, outfile, ensure_ascii=False, separators=(',', ':'))  # Compressed format

file_path = '/Users/ottoyu/Downloads/Transportation_RoadCentreline_20240812.gdb_converted.json'
output_file_path = 'td_roadline_compressed.geojson'
extract_and_convert_features(file_path, output_file_path)
