"""
This script converts 'Raw Data.csv' (of the Tanmk Statcard Collection)
into JSON format.
"""
import csv
import re
import json

RAW_DATA_PATH = r'Tanmk Statcard Collection - Raw Data.csv'
HULL_JSON_PATH = r'data_to_json/hull-data.json'
TURRET_JSON_PATH = r'data_to_json/turret-data.json'
GUN_JSON_PATH = r'data_to_json/gun-data.json'


def to_snake_case(string: str):
    """Takes a string with spaces and returns it in snake_case"""
    return re.sub(' +', '_', string).lower()


def fill_fields(data: list, part_name: str, categories: list, type: str):
    """A helper function which returns a dictionary with all fields of a
    part filled, based on the data provided.

    Args:
        data (list): The list of dictionaries representing the raw data
        part_name (str): The name of the part to have its data filled
        categories (list): The list of fields to be filled
        type (str): The type of part that part_name is

    Returns:
        dictionary (dict): The populated dictionary for part_name
    """
    # Initialize our dictionary
    dictionary = {}
    # Modifier based on part type to ensure we use the correct information
    part_type_mod = 0 if type == 'Hull' else 22 if type == 'Turret' else 43
    # Loop through each category and append them to the dictionary
    for (n, category) in enumerate(categories):
        # Remove the trailing information in related part data
        info = re.sub(r' *\[.*\]', '', data[n+part_type_mod][part_name])

        # Remove the non-unicode 'degree' and horizontal/vertical arrow
        # symbols
        info = info.replace('°', '').replace('↔', '').replace('↕', '')

        match(category):
            # If the info is crew data, split it into a list
            case 'crew':
                info = info.split()

            # Handle obtain-specific issues
            case 'obtain':

                # Some parts require ownership of another part to purchase
                # Check and add the "Requires" field to the dictionary
                # If there is no required part, it will be assigned 'None'
                dictionary['Requires'] = \
                    info[info.find('Requires'):].split('\n')[0] \
                    if 'Requires' in data[n + part_type_mod][part_name] \
                    else None

                # Clean up info, removing certain unecessary phrases
                info = re.sub(r'Requires .*\n', '',
                              info.replace('\n(Starter Item)', 'h'))

                # If the part is a blueprint, we need to create a
                # dictionary of its materials
                dictionary['Materials'] = None
                if 'Blueprints' in info:
                    materials = info.split('\n')[1:]
                    # If the part is an offsale or unobtainable blueprint,
                    # remove this information from the list
                    while ':' not in materials[0]:
                        materials.pop(0)
                        info = 'Unobtainable'
                    # Populate our dictionary
                    material_dict = {}
                    for mat in materials:
                        material_dict[mat[:mat.find(':')]]\
                            = int(mat[mat.find(':') + 2:])
                    dictionary['Materials'] = material_dict
        # Add the (infoType, info) pair to the dictionary
        dictionary[category] = info
    return dictionary


with open(RAW_DATA_PATH, 'r', encoding="utf-8") as raw_data:
    # Prepare raw data for reading
    data = list(csv.DictReader(raw_data))

    # Initialize some lists
    hulls = {}
    turrets = {}
    guns = {}

    # Prepare the stat categories for each part type #
    hull_info = []
    turret_info = []
    gun_info = []
    # We need an accumulator to indicate when each part type is complete
    # The order is Hulls -> Turrets -> Guns
    ACC = 0
    for row in data:
        # 'Hull' is the first element in the first column which contains
        # the category names
        # We clean them up to remove non-unicode characters and convert them
        # to snake_case
        category = row['Hull'].replace('↔ ', 'h').replace('↕ ', 'v')
        category = to_snake_case(category)
        match(category):
            # Part type sections are seperated by a single blank row
            # so we increase the accumulator when we encounter one.
            case '':
                ACC += 1
            # After each blank row, the next category name is simply the
            # type of part. We don't need this so we skip in these cases.
            case 'turret' | 'gun':
                pass
            case _:
                match(ACC):
                    case 0:
                        hull_info.append(category)
                    case 1:
                        turret_info.append(category)
                    case 2:
                        gun_info.append(category)

    # Handle Hulls #
    # Get names of every hull
    hullNames = list(data[0])[1:]
    for hull in hullNames:
        # Append a dictionary populated with the hull's information to hulls
        hulls[re.sub(r' *\(!\)', '', hull)] = \
            fill_fields(data, hull, hull_info, 'Hull')

    # Write all hulls' information to hull_file in JSON format
    with open(HULL_JSON_PATH, 'w',
              encoding="utf-8") as hull_file:
        json.dump(hulls, hull_file)

    # Handle Turrets #
    # Get names of every turret
    turretNames = [name for name in data[21].values() if name][1:]
    turretNames = zip(turretNames, hullNames)
    for turret in turretNames:
        # Append a dictionary populated with the hull's information to hulls
        turrets[re.sub(r' *\(!\)', '', turret[0])] = \
            fill_fields(data, turret[1], turret_info, 'Turret')

    # Write all turrets' information to hull_file in JSON format
    with open(TURRET_JSON_PATH, 'w',
              encoding="utf-8") as turret_file:
        json.dump(turrets, turret_file)
