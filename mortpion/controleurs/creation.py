from model.model_pg import *
from model.utils import *
from model.classes.morpion import *



list_morpions_bd = to_dict_morpions_list(get_list_morpions_bd(SESSION['CONNEXION']))

SESSION['morpion_bd'] = list_morpions_bd
REQUEST_VARS['team_name'] = ''

if 'team_name' in POST:
    REQUEST_VARS['team_name'] = POST['team_name'][0]


if 'submit_team_create' and 'color' and REQUEST_VARS['team_name'] != '' and 'team_morpion' in POST:

    selected_morpions = POST.get("team_morpion")[0]
    REQUEST_VARS['color'] = POST['team_color'][0]

"""
    for m in selected_morpions:
        json.loads(m)
        print(m)
        morpion_id = m["id_morpion"]
        print(morpion_id)
        # insert_morpion_appartenir_equipe(SESSION['CONNEXION'], morpion_id, REQUEST_VARS['color'])
"""
