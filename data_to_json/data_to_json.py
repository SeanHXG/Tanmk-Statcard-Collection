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
AMMO_FIELDS = {'Pen @ 0': 'pen0',
               'Pen @ 30': 'pen30',
               'Pen @ 60': 'pen60',
               'Velocity': 'velocity',
               'Ricochet Angle': 'ricochet_angle',
               'Fuse Sens': 'fuse_sensitivity',
               'Fuse Delay': 'fuse_delay',
               'Expl. Mass': 'filler',
               'Range': 'range',
               'Fuse Radius': 'fuse_radius',
               'Arming Distance': 'arming_distance',
               'Modifiers': 'modifiers'}
MODIFIERS = {'A-ERA': 'Anti-ERA',
             'OTA': 'OTA',
             'PF': 'PF',
             'Tandem': 'Tandem',
             'Tndm': 'Tandem'}


def to_snake_case(string: str) -> str:
    """Takes a string with spaces and returns it in snake_case"""
    return re.sub(' +', '_', string).lower()


def blueprint_helper(info: str) -> tuple:
    """Takes a string of aqcuisition information and returns a tuple
    containing a dictionary of materials if it is a blueprint, or None
    otherwise, and the method of aquisition.
    """
    material_dict = None
    if 'Blueprints' in info:
        materials = info.split('\n')[1:]
        # If the part is an unobtainable blueprint, remove this information
        # from the list of materials
        info = 'Blueprints'
        while ':' not in materials[0]:
            materials.pop(0)
            info = 'Unobtainable'
        # Populate our dictionary
        material_dict = {}
        for mat in materials:
            material_dict[mat[:mat.find(':')]]\
                = int(mat[mat.find(':') + 2:])
    return material_dict, info


def ammunition_helper(data_list: list, part_index: str) -> dict:
    """Takes the 'index' of a gun and returns a dictionary containing
    all the information of its shells from the data provided

    Args:
        data_list (list): The list of dictionaries representing raw_data
        part_index (str): The name of the hull which is in the same column
                          as the gun whose ammunition stats are to be recorded
    """
    # Initialize the returned dictionary
    result = {}
    # Iterate through the information of the part's ammunition
    for ammo in [data_list[n][part_index] for n in range(52, 56)]:
        # Stop looping if there is no ammunition info to read
        if ammo == '':
            break

        # Initialize a temporary dictionary for each ammo
        stat_list = {field: None for field in AMMO_FIELDS.values()}
        # Split our ammo data into a list
        ammo = ammo.split('\n')

        # Split the first element into the shell type
        # and its modifiers.
        name = ammo[0].split(' ')
        ammo_type = name[0]
        # If there are modifiers, we append them to a list and set their
        # key to 'modifiers'
        if name[1]:
            stat_list['modifiers'] = [MODIFIERS[mod] for mod in
                                      name[1].strip('()').split('/')]

        # Loop through every other field
        for field in ammo[1:]:
            # We remove all non-unicode degree symbols from field
            field = re.sub('° *', '', field)
            # Split each field into a tuple representing a key/value pair
            field = field.split(':')
            # Clean up the "value" string
            field[1] = field[1].strip()
            stat_list[AMMO_FIELDS[field[0]]] = field[1]

        # Append the new (ammo_type, ammo_stats) pair to the result
        result[ammo_type] = stat_list
    return result


def fill_fields(data_list: list, part_name: str, categories: list,
                part_type: str):
    """A helper function which returns a dictionary with all fields of a
    part filled, based on the data provided.

    Args:
        dat_alist (list): The list of dictionaries representing the raw data
        part_name (str): The name of the part to have its data filled
        categories (list): The list of fields to be filled
        part_type (str): The type of part that part_name is

    Returns:
        dictionary (dict): The populated dictionary for part_name
    """
    # Initialize our dictionary
    dictionary = {}
    # Modifier based on part type to ensure we use the correct information
    part_type_mod = {'Hull': 0, 'Turret': 22, 'Gun': 43}[part_type]
    # Loop through each field and append them to the dictionary
    for (n, field) in enumerate(categories):
        info = data_list[n+part_type_mod][part_name]
        # Remove the non-unicode 'degree' and horizontal/vertical arrow symbols
        info = info.replace('°', '').replace('↔', '').replace('↕', '')

        match(field):
            # If the info is crew data, split it into a list
            case 'crew':
                info = info.split()

            # Check if the ammunition has blowout protection
            case 'ammo_storage':
                info = info.split()
                dictionary['blowout'] = info[1].strip('()')\
                    if len(info) > 1 else None
                info = 0.0 if info[0] == 'None' else float(info[0])
            # If the info is ammunition for a gun, we create a dictionary
            # of its ammunition types
            case 'ammunition':
                info = ammunition_helper(data_list, part_name)
                # Increment our part type modifier to account for the 4
                # consecutive ammunition rows
                part_type_mod += 3

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
                dictionary['Materials'], info = blueprint_helper(info)
                # If it is not a blueprint, assign None to the materials

            # Split the based on and paired parts into a list,
            # if there is at least one element
            case 'based' | 'hulls' | 'turrets' | 'guns':
                # Remove the uncertain (?)s
                info = re.sub(r' \(\?\)', '', info)
                if info != 'none':
                    # Remove excess whitespace used in the csv
                    info = re.sub(r' *\n? +', ' ', info)
                    info = re.sub(r' *\n *\[', ' [', info)
                    # Remove tier information for paired parts
                    info = re.sub(r' *\[\d*\]', '', info)
                    # Split into an array based on remaining newlines
                    info = info.split('\n')
        # Add the (infoType, info) pair to the dictionary
        dictionary[field] = info
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
        category = row['Hull'].replace('↔', 'h').replace('↕', 'v')
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
                    case _:
                        gun_info.append(category)

    # Handle Hulls #
    # Get names of every hull
    hull_names = list(data[0])[1:]
    for hull in hull_names:
        # Append a dictionary populated with the hull's information to hulls
        hulls[re.sub(r' *\(!\)', '', hull)] = \
            fill_fields(data, hull, hull_info, 'Hull')

    # Write all hulls' information to HULL_JSON_PATH in JSON format
    with open(HULL_JSON_PATH, 'w',
              encoding="utf-8") as hull_file:
        json.dump(hulls, hull_file)

    # Handle Turrets #
    # Get names of every turret
    turret_names = zip([name for name in data[21].values() if name][1:],
                       hull_names)
    # Every dictionary will have hull names as keys, so we have to use them to
    # access data
    for (turret, index) in turret_names:
        # Append a dictionary populated with the turret's information to 
        # turrets
        turrets[re.sub(r' *\(!\)', '', turret)] = \
            fill_fields(data, index, turret_info, 'Turret')

    # Write all turrets' information to TURRET_JSON_PATH in JSON format
    with open(TURRET_JSON_PATH, 'w',
              encoding="utf-8") as turret_file:
        json.dump(turrets, turret_file)

    # Handle Guns #
    # Get names of every gun
    gun_names = zip([name for name in data[42].values() if name][1:],
                    hull_names)
    # Every dictionary will have hull names as keys, so we have to use them to
    # access data
    for (gun, index) in gun_names:
        # Append a dictionary populated with the gun's information to guns
        guns[re.sub(r' *\(!\)', '', gun)] = \
            fill_fields(data, index, gun_info, 'Gun')

    # Write all guns' information to GUN_JSON_PATH in JSON format
    with open(GUN_JSON_PATH, 'w',
              encoding="utf-8") as gun_file:
        json.dump(guns, gun_file)
