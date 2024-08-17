import csv
import codecs

def extract_unique_elements(input_file, output_prefix):
    elements = {
        'ChiEstate': set(),
        'EngEstate': set(),
        'ChiVillage': set(),
        'EngVillage': set(),
        'ChiStreet': set(),
        'EngStreet': set(),
        'ChiBuilding': set(),
        'EngBuilding': set()
    }

    with codecs.open(input_file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # ChiEstate
            chi_estate = row['Chi_EstateName']
            if chi_estate:
                elements['ChiEstate'].add(chi_estate)

            # EngEstate
            eng_estate = row['Eng_EstateName']
            if eng_estate:
                elements['EngEstate'].add(eng_estate)

            # ChiVillage
            chi_village = row['Chi_VillageName']
            if chi_village:
                elements['ChiVillage'].add(chi_village)

            # EngVillage
            eng_village = row['Eng_VillageName']
            if eng_village:
                elements['EngVillage'].add(eng_village)

            # ChiStreet
            chi_street = row['Chi_StreetName']
            if chi_street:
                elements['ChiStreet'].add(chi_street)

            # EngStreet
            eng_street = row['Eng_StreetName']
            if eng_street:
                elements['EngStreet'].add(eng_street)

            # ChiBuilding
            chi_building = row['Chi_BuildingName']
            if chi_building:
                elements['ChiBuilding'].add(chi_building)

            # EngBuilding
            eng_building = row['Eng_BuildingName']
            if eng_building:
                elements['EngBuilding'].add(eng_building)

    for element_type, unique_elements in elements.items():
        output_file = f"{output_prefix}{element_type}.txt"
        with codecs.open(output_file, 'w', encoding='utf-8') as f:
            for element in sorted(unique_elements):
                f.write(element + '\n')
        print(f" {output_file}  with {len(unique_elements)} unique entries")

input_file = '/Users/ottoyu/PycharmProjects/csdi-address/als_addresses_(all).csv'
output_prefix = ''

extract_unique_elements(input_file, output_prefix)