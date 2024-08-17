import json
import csv
import os
import glob
import codecs

def decompose_geojson_to_csv(geojson_data, output_file):
    if geojson_data['type'] != 'FeatureCollection':
        raise ValueError("Input GeoJSON must be a FeatureCollection")

    fieldnames = [
        'Geometry_Type', 'Longitude', 'Latitude', 'Northing', 'Easting',
        'CSU_ID',
        'Chi_BuildingName', 'Chi_District', 'Chi_Region',
        'Chi_UnitDescriptor', 'Chi_UnitNo', 'Chi_UnitPortion',
        'Chi_FloorNum', 'Chi_FloorDescription',
        'Chi_BlockDescriptor', 'Chi_BlockNo',
        'Chi_EstateName', 'Chi_PhaseName', 'Chi_PhaseNo',
        'Chi_VillageLocationName', 'Chi_VillageName', 'Chi_VillageBuildingNoFrom', 'Chi_VillageBuildingNoTo',
        'Chi_StreetLocationName', 'Chi_StreetName', 'Chi_StreetBuildingNoFrom', 'Chi_StreetBuildingNoTo',
        'Eng_BuildingName', 'Eng_District', 'Eng_Region',
        'Eng_UnitDescriptor', 'Eng_UnitNo', 'Eng_UnitPortion',
        'Eng_FloorNum', 'Eng_FloorDescription',
        'Eng_BlockDescriptor', 'Eng_BlockNo', 'Eng_BlockDescriptorPrecedenceIndicator',
        'Eng_EstateName', 'Eng_PhaseName', 'Eng_PhaseNo',
        'Eng_VillageLocationName', 'Eng_VillageName', 'Eng_VillageBuildingNoFrom', 'Eng_VillageBuildingNoTo',
        'Eng_StreetLocationName', 'Eng_StreetName', 'Eng_StreetBuildingNoFrom', 'Eng_StreetBuildingNoTo',
        'GeoAddress'
    ]

    with codecs.open(output_file, 'w', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for feature in geojson_data['features']:
            row_data = extract_feature_data(feature)
            writer.writerow({k: row_data.get(k, '') for k in fieldnames})


def extract_feature_data(feature):
    geometry = feature['geometry']
    properties = feature['properties']
    address = properties['Address']
    premises_address = address['PremisesAddress']
    chi_address = premises_address.get('ChiPremisesAddress', {})
    eng_address = premises_address.get('EngPremisesAddress', {})

    data = {
        'Geometry_Type': geometry['type'],
        'Longitude': geometry['coordinates'][0],
        'Latitude': geometry['coordinates'][1],
        'Northing': properties.get('Northing'),
        'Easting': properties.get('Easting'),
        'CSU_ID': premises_address.get('BuildingCsuInformation', {}).get('CsuId'),
        'Chi_BuildingName': chi_address.get('BuildingName'),
        'Chi_District': chi_address.get('ChiDistrict'),
        'Chi_Region': chi_address.get('Region'),
        'Eng_BuildingName': eng_address.get('BuildingName'),
        'Eng_District': eng_address.get('EngDistrict'),
        'Eng_Region': eng_address.get('Region'),
        'GeoAddress': premises_address.get('GeoAddress')
    }

    # Chinese Address
    chi_3d_addresses = chi_address.get('Chi3dAddress', [])
    if chi_3d_addresses:
        chi_3d = chi_3d_addresses[0]
        chi_unit = chi_3d.get('ChiUnit', {})
        chi_floor = chi_3d.get('ChiFloor', {})
        data.update({
            'Chi_UnitDescriptor': chi_unit.get('UnitDescriptor'),
            'Chi_UnitNo': chi_unit.get('UnitNo'),
            'Chi_UnitPortion': chi_unit.get('UnitPortion'),
            'Chi_FloorNum': chi_floor.get('FloorNum'),
            'Chi_FloorDescription': chi_floor.get('FloorDescription')
        })

    chi_block = chi_address.get('ChiBlock', {})
    data.update({
        'Chi_BlockDescriptor': chi_block.get('BlockDescriptor'),
        'Chi_BlockNo': chi_block.get('BlockNo')
    })

    chi_estate = chi_address.get('ChiEstate', {})
    chi_phase = chi_estate.get('ChiPhase', {})
    data.update({
        'Chi_EstateName': chi_estate.get('EstateName'),
        'Chi_PhaseName': chi_phase.get('PhaseName'),
        'Chi_PhaseNo': chi_phase.get('PhaseNo')
    })

    chi_village = chi_address.get('ChiVillage', {})
    data.update({
        'Chi_VillageLocationName': chi_village.get('LocationName'),
        'Chi_VillageName': chi_village.get('VillageName'),
        'Chi_VillageBuildingNoFrom': chi_village.get('BuildingNoFrom'),
        'Chi_VillageBuildingNoTo': chi_village.get('BuildingNoTo')
    })

    chi_street = chi_address.get('ChiStreet', {})
    data.update({
        'Chi_StreetLocationName': chi_street.get('LocationName'),
        'Chi_StreetName': chi_street.get('StreetName'),
        'Chi_StreetBuildingNoFrom': chi_street.get('BuildingNoFrom'),
        'Chi_StreetBuildingNoTo': chi_street.get('BuildingNoTo')
    })

    eng_3d_addresses = eng_address.get('Eng3dAddress', [])
    if eng_3d_addresses:
        eng_3d = eng_3d_addresses[0]
        eng_unit = eng_3d.get('EngUnit', {})
        eng_floor = eng_3d.get('EngFloor', {})
        data.update({
            'Eng_UnitDescriptor': eng_unit.get('UnitDescriptor'),
            'Eng_UnitNo': eng_unit.get('UnitNo'),
            'Eng_UnitPortion': eng_unit.get('UnitPortion'),
            'Eng_FloorNum': eng_floor.get('FloorNum'),
            'Eng_FloorDescription': eng_floor.get('FloorDescription')
        })

    eng_block = eng_address.get('EngBlock', {})
    data.update({
        'Eng_BlockDescriptor': eng_block.get('BlockDescriptor'),
        'Eng_BlockNo': eng_block.get('BlockNo'),
        'Eng_BlockDescriptorPrecedenceIndicator': eng_block.get('BlockDescriptorPrecedenceIndicator')
    })

    eng_estate = eng_address.get('EngEstate', {})
    eng_phase = eng_estate.get('EngPhase', {})
    data.update({
        'Eng_EstateName': eng_estate.get('EstateName'),
        'Eng_PhaseName': eng_phase.get('PhaseName'),
        'Eng_PhaseNo': eng_phase.get('PhaseNo')
    })

    eng_village = eng_address.get('EngVillage', {})
    data.update({
        'Eng_VillageLocationName': eng_village.get('LocationName'),
        'Eng_VillageName': eng_village.get('VillageName'),
        'Eng_VillageBuildingNoFrom': eng_village.get('BuildingNoFrom'),
        'Eng_VillageBuildingNoTo': eng_village.get('BuildingNoTo')
    })

    eng_street = eng_address.get('EngStreet', {})
    data.update({
        'Eng_StreetLocationName': eng_street.get('LocationName'),
        'Eng_StreetName': eng_street.get('StreetName'),
        'Eng_StreetBuildingNoFrom': eng_street.get('BuildingNoFrom'),
        'Eng_StreetBuildingNoTo': eng_street.get('BuildingNoTo')
    })

    return data


def process_all_geojson_files(input_folder, output_folder, merged_file):
    os.makedirs(output_folder, exist_ok=True)

    for geojson_file in glob.glob(os.path.join(input_folder, '*.geojson')):
        base_name = os.path.basename(geojson_file)
        csv_file = os.path.join(output_folder, base_name.replace('.geojson', '.csv'))

        with codecs.open(geojson_file, 'r', encoding='utf-8') as file:
            geojson_data = json.load(file)

        decompose_geojson_to_csv(geojson_data, csv_file)
        print(f"Processed: {base_name}")

    csv_files = glob.glob(os.path.join(output_folder, '*.csv'))
    with codecs.open(merged_file, 'w', encoding='utf-8-sig') as outfile:
        first_file = True
        for fname in csv_files:
            with codecs.open(fname, 'r', encoding='utf-8-sig') as infile:
                if first_file:
                    outfile.write(infile.read())
                    first_file = False
                else:
                    next(infile)
                    outfile.write(infile.read())

    print(f"All CSV files merged into: {merged_file}")


input_folder = 'ALS_GeoJSON_296'
output_folder = 'CSV_Output'
merged_file = 'merged_addresses.csv'

process_all_geojson_files(input_folder, output_folder, merged_file)