import pwd,os,platform,sys,flywheel,json

def update_gears():
    # Define some color classes for warnings we will use
    class bcolors:
        HEADER = '\033[95m'
        OKBLUE = '\033[94m'
        OKGREEN = '\033[92m'
        WARNING = '\033[93m'
        FAIL = '\033[91m'
        ENDC = '\033[0m'
        BOLD = '\033[1m'
        UNDERLINE = '\033[4m'
        
    ###################### Set some initial paths #################################
    
    # Print what needs to be done 
    print("The gear updater is starting. Make sure you can call the command 'fw' "
          "from your terminal. Login to you flywheel account by running "
          "'fw login <your-API>' from the terminal. This script is not going to "
          "work if you do not do these.")
    
    fw = flywheel.Client()
    
    # Set paths for Linux or Mac
    if platform.system() == 'Linux':
        path_to_matlab_doc = '/home/%s/Documents/MATLAB/' % pwd.getpwuid(os.getuid()).pw_name
    else:
        path_to_matlab_doc = '/Users/%s/Documents/MATLAB/' % pwd.getpwuid(os.getuid()).pw_name
    
    # Pull the latest version of gear_updater
    print('Pulling the latest version of the gear builder from Git')
    gear_builder_repo = os.path.join(path_to_matlab_doc, 'projects', 'fwGearBuilder')
    os.system('cd %s; git pull' % gear_builder_repo)
    gear_folders = os.path.join(gear_builder_repo, 'flywheel_gears')
    
    # This portion will rename your startup functions so that tbUse will not be
    # run
    cont = input(bcolors.WARNING + '\nWarning! This script temporarily renames your matlab startup file to nostartup.m for compiling. The script discards this change when the compiling process is done. Do you want to continue ? y/n ' + bcolors.ENDC)
    if cont == 'y':
        if os.path.exists(os.path.join(path_to_matlab_doc, 'startup.m')):
            os.system('mv %s %s' % (os.path.join(path_to_matlab_doc, 'startup.m'), os.path.join(path_to_matlab_doc, 'nostartup.m')))
        startuptwo = '/home/%s/matlab/' % pwd.getpwuid(os.getuid()).pw_name
        if os.path.exists(startuptwo):        
            if os.listdir(startuptwo) != []:
                os.system('mv %s/startup.m %s/nastartup.m' % (startuptwo, startuptwo))   
    else:
        sys.exit('Stopping the builder')
        
    # Dictionary for the gear name 
    gear_names = {1:'ants-multivariate-template-construction', 2:'bayesprf',
                  3:'calculate-average-response-function',4:'calculate-fixels',
                  5:'calculate-mask-intersection',6:'create-group-fod-template',
                  7:'create-subject-fod-map', 8:'denoise-icaaroma',
                  9:'dilate-qsiprep-mask', 10:'extract-track-dti-values',
                  11:'extract-track-fixel-values', 12:'forwardmodel',
                  13:'glmsingle', 14:'ldogfix', 15:'ldogfunc',16:'ldogrest',
                  17:'ldogstruct',18:'localwhitematternoiseregression',
                  19:'register-thalamic-segmentations',20:'segmentthalamicnuclei',
                  21:'tome-calculate-inner-ear-angles',22:'trace-optic-radiation',
                  23:'track-single-fod-tract',24:'vol2surf'}
              
    # Dictionary for human-friendly name
    human_name = {1:'antsMultivariateTemplateConstruction: Make a template with ANTs multivariate template construction 2', 2:'bayesPRF: template fitting of retinotopic maps using neuropythy',
                  3:'calculateAverageResponseFunction: Calculate average response function from DWI images',4:'calculateFixels: Calculate fixels from FOD images',
                  5:'calculateMaskIntersection: Calculate intersection of multiple volumetric masks',6:'createGroupFODTemplate: MRtrix make FOD template',
                  7:'createSubjectFODMap: Make FOD image from HCP-diff output', 8:'denoise-icaaroma: Perform ICA denoising on native space fmriprep data',
                  9:'dilateQsiprepMask: Dilate qsiprep masks to include the optic chiasm', 10:'extractTrackdtiValues: Extract dti values from ROI tracks',
                  11:'extractTrackFixelValues: Extract fixel values from ROI tracks', 12:'forwardModel: non-linear fitting of models to fMRI data',
                  13:'glmSingle: single-trial estimates in fMRI time-series data', 14:'ldogFix: archiving ldogfunc outputs', 15:'ldogFunc: functional pre-processing for the LDOG project',16:'ldogRest: Resting state analysis of ldog data',
                  17:'ldogStruct: anatomical pre-processing for the LDOG project',18:'regressLocalWhiteMatter: Removes white matter noise from adjacent gray matter voxels',
                  19:'registerThalamicSegmentations: Register thalamic segmentations to FOD space',20:'segmentThalamicNuclei: Produce parcellation of the thalamus',
                  21:'tomeCalculateInnerEarAngles: Inner ear angles w.r.t B0 field',22:'traceOpticRadiation: Calculate optic radiation tractography',
                  23:'trackSingleFODTract: Create streamlines between two ROI masks',24:'vol2surf: Map volumetric MRI images to fsaverage and FSLR surfaces'}
    
    # Ask what gear to build
    which_number = input(bcolors.WARNING + f'\nWhich gear would you like to update? '
                          f'\n\n1-{gear_names[1]} \n2-{gear_names[2]} \n3-{gear_names[3]}'
                          f'\n4-{gear_names[4]} \n5-{gear_names[5]} \n6-{gear_names[6]}'
                          f'\n7-{gear_names[7]} \n8-{gear_names[8]} \n9-{gear_names[9]}'
                          f'\n10-{gear_names[10]} \n11-{gear_names[11]} \n12-{gear_names[12]}'
                          f'\n13-{gear_names[13]} \n14-{gear_names[14]} \n15-{gear_names[15]}'
                          f'\n16-{gear_names[16]} \n17-{gear_names[17]} \n18-{gear_names[18]}'
                          f'\n19-{gear_names[19]} \n20-{gear_names[20]} \n21-{gear_names[21]}'
                          f'\n22-{gear_names[22]} \n23-{gear_names[23]} \n24-{gear_names[24]}' 
                          f'\n\nEnter a number:' + bcolors.ENDC)
    
    # Ask for the version of the gear
    current_version = fw.lookup('gears/%s' % gear_names[int(which_number)]).gear.version
    new_version = input(f'Enter the new version of the gear. The current version of the selected gear on the webpage is {current_version} :') 
    
    # Build docker image
    os.system('cd %s; docker build -t gkaguirrelab/%s:%s .' % (os.path.join(gear_folders, gear_names[int(which_number)]),
                                                                gear_names[int(which_number)],
                                                                new_version))  
    
    # Print instructions and build the gear
    first_instructions = '-- When asked to chose a human readable name use the following without the quotation marks:  "%s"' % human_name[int(which_number)]
    print('\n')
    print(bcolors.WARNING + first_instructions + bcolors.ENDC)
    second_instructions = '-- When asked for a gear ID enter the following without the quotation marks:  "%s"' % gear_names[int(which_number)]
    print('\n')
    print(bcolors.WARNING + second_instructions + bcolors.ENDC)   
    print('\n')
    os.system('cd %s; fw gear create' % os.path.join(gear_folders, gear_names[int(which_number)]))
    
    # Update the manifest file. Everytime we build the gear, the manifest json
    # file is replaced. On this replacement, the author name is automatically 
    # set to your Flywheel username. So we need to modify the manifest file 
    # again with the correct author name. We also add the suite name, so the 
    # gear will go GKAguirreLab section on the webpage. Automatic manifest 
    # replacement also gets rid of the suite information
    with open('%s' % os.path.join(os.path.join(gear_folders, gear_names[int(which_number)], 'manifest.json')) , 'r+') as f:
        data = json.load(f)
        data['version'] = new_version 
        if gear_names(int(which_number)) == 'ants-multivariate-template-construction':
            data['author'] = 'Nick Tustison'
        elif gear_names(int(which_number)) == 'bayesprf':
            data['author'] = 'Noah C. Benson'       
        elif gear_names(int(which_number)) == 'forwardmodel':
            data['author'] = 'Geoffrey K. Aguirre' 
        else:
            data['author'] = 'Ozenc Taskin'
        data['maintainer'] = 'Ozenc Taskin' 
        data['custom'] = {'flywheel': {'suite': 'GKAguirreLab'}, 'gear-builder': {'category': 'analysis', 'image': 'gkaguirrelab/%s:%s' % (gear_names[int(which_number)], new_version)}}
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    
    # Ask if we want to upload the new version. Also print some instructions
    # for testing the gear
    upload_instructions = 'Do you want to upload the gear now? You can do it later by cd-ing into %s and running "fw gear upload". If you want to test the gear, go into the same folder and use "fw gear local" with the input/config flags you want to use. To print out all flags use "fw gear local --help" : y/n ' % os.path.join(gear_folders, gear_names[int(which_number)]) 
    uploadcall = input(bcolors.WARNING + upload_instructions + bcolors.ENDC)  
    if uploadcall == 'y':
        os.system('cd %s; GODEBUG=netdns=go fw gear upload' % os.path.join(gear_folders, gear_names[int(which_number)]))
    else:
        print("Not uploading the gear")
    
    # Revert the name change we made to the matlab startup file
    if os.path.exists(os.path.join(path_to_matlab_doc, 'nastartup.m')):
        os.system('mv %s %s' % (os.path.join(path_to_matlab_doc, 'nastartup.m'), os.path.join(path_to_matlab_doc, 'startup.m')))
    if os.path.exists(startuptwo):        
        if os.listdir(startuptwo) != []:
            os.system('mv %s/nastartup.m %s/startup.m' % (startuptwo, startuptwo))     
            
update_gears()