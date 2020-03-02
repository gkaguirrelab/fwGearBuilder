import json
import os

def append_gear_builder(path_to_matlab, new_gear_json):
    
    # Get the new_gear info
    with open(new_gear_json) as json_file:
        data = json.load(json_file)
    new_gear_number = int(data['how_many_gears_do_you_already_have_in_the_builder_script']) + 1
    frame_folder = data['path_to_the_frame_folder']
    mainfolder = data['path_to_the_mainfolder']
    gear_manifest = data['path_to_the_gear_manifest_json_file_in_gear_frame']
    
    # Get some more info from the original json
    with open(gear_manifest) as gear_mani:
        gear_info = json.load(gear_mani)
    machine_name = gear_info['name']
    human_name = gear_info['label']
    author = gear_info['author']
    maintianer = gear_info['maintainer']
    
    # Get the to-be-compiled matlab functions from the json files and update the compiler_functions.py script
    script_name_all =  data['name_of_the_matlab_script(s)_you_want_to_compile(without_the_extension)'].split(',')
    script_path_all = data['path_to_the_matlab_script(s)_you_want_to_compile'].split(',')   
    secondary_functions_all_all = data['path_to_the_secondary_function(s)_that_is_used_by_the_compiled_script(s)'].split(';')
    secondary_folders_all_all = data =['path_to_the_secondary_function_folder(s)_that_is_used_by_the_compiled_script(s)']
    script_length = len(script_name_all)
    for i in range(script_length):
        script_name = script_name_all[i]
        script_path = script_path_all[i]
        secondary_functions_all = secondary_functions_all_all[i].split(',') # All functions list no need to separate as there is one script
        secondary_folders_all = secondary_folders_all_all[i].split(',') # All folders list
        frame_function_string_draft = "\ndef compile_{script_path}(path_to_matlab_documents, output_folder):\n\n    if not os.path.exists(output_folder):\n    os.system('mkdir %s'%output_folder)\n\n    mcc_path = 'mcc'\n    mcc_call{new_gear_number} = '%s -m -R -nodisplay %s".format(script_path=script_path, new_gear_number=new_gear_number)
        for i in secondary_functions_all:
            frame_function_string_draft = frame_function_string_draft + ' -a {function}'.format(i)
        for i in secondary_folders_all:
            frame_function_string_draft = frame_function_string_draft + ' -I {folders}'.format(i)
        frame_function_string = frame_function_string_draft  + ' -d %s -v\' % output_folder' + '\nCompiling {script_name}'.format(script_name) + '\nos.system(mcc_call)'
        file_object = open(os.path.join(path_to_matlab, 'projects/fwGearBuilder/gear_builder/compiler_functions.py'), 'a')
        file_object.write(frame_function_string)
        file_object.close()
    
                
    

        
        