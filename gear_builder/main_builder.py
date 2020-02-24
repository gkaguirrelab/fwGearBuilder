import os
from compiler_functions import *
import sys
import json
import pwd

'''
This is an interaactive script which is used to assemble and update Flywheel
gears for the forwardModel and ldog projects.
'''

def main_builder():
    
###################### Set some initial paths #################################
    
    # Please login to docker with the "docker login" command first and to flywheel 
    # using "fw login <API-key>"
    
    # which_gear = bayesianfittinggear or forwardmodelgear
    # path_to_matlab_doc = path to your main MATLAB folder (usually in documents)
    # gear_version = the version number you want to bump the gear
    # test = Is whether you want to test the gear after building. Default n - false 
    print("The gear builder is starting.")    
    path_to_matlab_doc = '/home/%s/Documents/MATLAB/' % pwd.getpwuid(os.getuid()).pw_name

    print('Pulling the git repos')
    os.system('cd %s; git pull' % os.path.join(path_to_matlab_doc, 'projects', 'forwardModelWrapper'))
    os.system('cd %s; git pull' % os.path.join(path_to_matlab_doc, 'projects', 'forwardModel'))    
    os.system('cd %s; git pull' % os.path.join(path_to_matlab_doc, 'projects', 'mriLDOGAnalysis'))
      
    print('Running tbUSe')
    os.system('cd %s; matlab -r -nodisplay \'gearBuilderAutotbUse\(\);\'' % os.path.join(path_to_matlab_doc, 'projects', 'fwGearBuilder','gear_builder'))
    
    cont = input('\nWarning! This script temporarily renames your matlab startup file to nostartup.m for compiling. The script discards this change when the compiling process is done. Do you want to continue ? y/n ')
    if cont == 'y':
        if os.path.exists(os.path.join(path_to_matlab_doc, 'startup.m')):
            os.system('mv %s %s' % (os.path.join(path_to_matlab_doc, 'startup.m'), os.path.join(path_to_matlab_doc, 'nostartup.m')))
        startuptwo = '/home/%s/matlab/' % pwd.getpwuid(os.getuid()).pw_name
        if os.path.exists(startuptwo):        
            if os.listdir(startuptwo) != []:
                os.system('mv %s/startup.m %s/nastartup.m' % startuptwo)   
    else:
        sys.exit('Stopping the builder')

####################### Compile the required functions ########################        
  
    which_number = input('\nWhich gear would you like to update ? Enter a number:\n1-forwardmodel\n2-bayesianfitting\n3-ldogstruct\n4-ldogfunc\n5-ldogfix\nEnter a number:')
    if which_number == '1':
        gear_name = 'forwardmodel'
        gear_version = input('What will be the new gear version:')
        print('starting forwardmodel building')
        frame = os.path.join(path_to_matlab_doc, 'projects', 
                             'forwardModelWrapper', 
                             'fw_gears', 'forwardModel',
                             'forwardModel_frame')       
        func_input = os.path.join(frame, 'func_input')
        os.system('rm -r %s' % func_input)
        compile_forwardModel(path_to_matlab_doc, func_input)
        mainfold = os.path.join(path_to_matlab_doc, 'projects', 
                                'forwardModelWrapper', 
                                'fw_gears', 'forwardModel',
                                'main_gear')
    elif which_number == '2':
        gear_name = 'bayesianfitting'        
        gear_version = input('What will be the new gear version:')
        frame = os.path.join(path_to_matlab_doc, 'projects', 
                             'forwardMtheodelWrapper', 
                             'fw_gears', 'bayesianFitting',
                             'bayesianFittingGear_frame')
        cortmag_func = os.path.join(frame, 'cortmag_func')
        postproc_func = os.path.join(frame, 'postproc_func')
        render_func = os.path.join(frame, 'render_func')
        os.system('rm -r %s' % cortmag_func)
        os.system('rm -r %s' % postproc_func)
        os.system('rm -r %s' % render_func)
        compile_calcCorticalMag(path_to_matlab_doc, cortmag_func)
        compile_postprocessBayes(path_to_matlab_doc, postproc_func)
        compile_renderInferredMaps(path_to_matlab_doc, render_func)
        mainfold = os.path.join(path_to_matlab_doc, 'projects', 
                                'forwardModelWrapper', 
                                'fw_gears', 'bayesianFitting',
                                'main_gear')   
    elif which_number == '3':
        gear_name = 'ldogstruct'
        gear_version = input('What will be the new gear version:')
        frame = os.path.join(path_to_matlab_doc, 'projects', 
                             'mriLDOGAnalysis', 
                             'fw_gears', 'ldog_struct',
                             'ldog_struct_frame') 
        mainfold = os.path.join(path_to_matlab_doc, 'projects', 
                                'mriLDOGAnalysis', 
                                'fw_gears', 'ldog_struct',
                                'main_gear')     
        fw_download_command = '''
        fw download "gkaguirrelab/canineFovea/atlas/Canine Atlas/invivoTemplate/files/invivoTemplate.nii.gz" -o %s -f;
        fw download "gkaguirrelab/canineFovea/atlas/Canine Atlas/downsampled Atlas/files/2x2x2resampled_invivoTemplate.nii.gz" -o %s -f;
        fw download "gkaguirrelab/canineFovea/atlas/Canine Atlas/exvivo template/files/Woofsurfer.zip" -o %s -f;
        fw download "gkaguirrelab/canineFovea/atlas/Canine Atlas/invivo2exvivo warp calculations/files/exvivo_warp_files.zip" -o %s -f;
        fw download "gkaguirrelab/canineFovea/atlas/Canine Atlas/invivoTemplate-WithSkull/files/invivoTemplate-WithSkull.nii.gz" -o %s -f;        
        ''' % (os.path.join(path_to_matlab_doc, 'projects', 'mriLDOGAnalysis', 'fw_gears', 'ldog_struct', 'ldog_struct_frame', 'invivoTemplate.nii.gz'),
               os.path.join(path_to_matlab_doc, 'projects', 'mriLDOGAnalysis', 'fw_gears', 'ldog_struct', 'ldog_struct_frame', '2x2x2resampled_invivoTemplate.nii.gz'),
               os.path.join(path_to_matlab_doc, 'projects', 'mriLDOGAnalysis', 'fw_gears', 'ldog_struct', 'ldog_struct_frame', 'Woofsurfer.zip'),
               os.path.join(path_to_matlab_doc, 'projects', 'mriLDOGAnalysis', 'fw_gears', 'ldog_struct', 'ldog_struct_frame', 'exvivo_warp_files.zip'),
               os.path.join(path_to_matlab_doc, 'projects', 'mriLDOGAnalysis', 'fw_gears', 'ldog_struct', 'ldog_struct_frame', 'invivoTemplate-WithSkull.nii.gz'))
        print('Downloading the Atlases from Flywheel')
        os.system(fw_download_command)
        
    elif which_number == '4':
        gear_name = 'ldogfunc'
        gear_version = input('What will be the new gear version:')
        frame = os.path.join(path_to_matlab_doc, 'projects', 
                             'mriLDOGAnalysis', 
                             'fw_gears', 'ldog_func',
                             'ldog_func_frame') 
        mainfold = os.path.join(path_to_matlab_doc, 'projects', 
                                'mriLDOGAnalysis', 
                                'fw_gears', 'ldog_func',
                                'main_gear')     
    elif which_number == '5':
        gear_name = 'ldogfix'
        gear_version = input('What will be the new gear version:')
        frame = os.path.join(path_to_matlab_doc, 'projects', 
                             'mriLDOGAnalysis', 
                             'fw_gears', 'ldog_fix',
                             'ldog_fix_frame') 
        regressMotion = os.path.join(frame, 'regressMotion')
        os.system('rm -r %s' % regressMotion)   
        compile_regressMotion(path_to_matlab_doc, regressMotion)
        mainfold = os.path.join(path_to_matlab_doc, 'projects', 
                                'mriLDOGAnalysis', 
                                'fw_gears', 'ldog_fix',
                                'main_gear')          
    else:
        sys.exit("Invalid number entered or the gear is not yet supported.")
        
    
    os.system('mv %s %s' % (os.path.join(path_to_matlab_doc, 'nostartup.m'), os.path.join(path_to_matlab_doc, 'startup.m')))

##################### Build the docker images #################################
        
    # This process might take a while if you have not pulled the gear base before     
    os.system('cd %s; docker build -t gkaguirrelab/%s:%s .' % (frame,
                                                               gear_name,
                                                               gear_version))        
    # Delete the content of the main_gear folder
    if os.listdir(mainfold) != []:
        os.system('cd %s; rm *' % mainfold)

    if gear_name == 'forwardmodel':
        print('\n')
        print('-- When asked to chose a human readable name use the following without the quotation marks:  "forwardModel: non-linear fitting of models to fMRI data"')
        print('\n')
        print('-- When asked for a gear ID enter the following without the quotation marks:  "forwardmodel"')        
    elif gear_name == 'bayesianfitting':
        print('\n')
        print('-- When asked to chose a human readable name enter the following without the quotation marks:  "bayesPRF: template fitting of retinotopic maps using neuropythy"')
        print('\n')
        print('-- When asked for a gear ID enter the following without the quotation marks:  "bayesprf"')     
    elif gear_name == 'ldogstruct':
        print('\n')
        print('-- When asked to chose a human readable name use the following without the quotation marks:  "ldogStruct: anatomical pre-processing for the LDOG project"')
        print('\n')
        print('-- When asked for a gear ID enter the following without the quotation marks:  "ldogstruct"')     
    elif gear_name == 'ldogfunc':
        print('\n')
        print('-- When asked to chose a human readable name use the following without the quotation marks:  "ldogFunc: functional pre-processing for the LDOG project"')
        print('\n')
        print('-- When asked for a gear ID enter the following without the quotation marks:  "ldogfunc"')            
    elif gear_name == 'ldogfix':
        print('\n')
        print('-- When asked to chose a human readable name use the following without the quotation marks:  "ldogFix: archiving ldogfunc outputs"')
        print('\n')
        print('-- When asked for a gear ID enter the following without the quotation marks:  "ldogfix"')    
    else:
        print('Unknown gear')        
                
    print('\n-- Select "Other" for the third question and decide whether you want an Analysis or Converter gear and enter the following as the container name:   "gkaguirrelab/%s:%s"'% (gear_name, gear_version))
         
    os.system('cd %s; fw gear create' % mainfold)
        
###################### Modify the json and upload #############################
    
    with open('%s' % os.path.join(mainfold, 'manifest.json') , 'r+') as f:
        data = json.load(f)
        data['version'] = gear_version 
        if gear_name == 'forwardmodel':
            data['author'] = 'Geoffrey K. Aguirre'
        elif gear_name == 'bayesianfitting':
            data['author'] = 'Noah C. Benson'            
        else:
            data['author'] = 'Ozenc Taskin'
        data['maintainer'] = 'Ozenc Taskin' 
        data['custom'] = {'flywheel': {'suite': 'GKAguirreLab'}, 'gear-builder': {'category': 'analysis', 'image': 'gkaguirrelab/%s:%s' % (gear_name, gear_version)}}
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    testcall = input('Do you want to test the gear? Only available for the gear builder computer. Output can be found in repo directory/main_gear/output : y/n ')  
    if testcall == 'y':
        if gear_name == 'forwardmodel':
            which_forward = input('Which forwardmodel do you want to test? v for volumetric, c for cifti: v/c') 
            print('Starting forwardmodel gear')
            if which_forward == 'v':
                os.sytem('cd %s; fw gear local --averageAcquisitions 1 --dataFileType volumetric --dataSourceType ldogfix \
                         --funcZip01 /home/gear-builder/Desktop/gear_test_files/forward_model/volumetric/lefteye.zip \
                         --modelClass flobsHRF --modelOpts \'(polyDeg), 13\' --tr 3 \
                         --stimFile /home/gear-builder/Desktop/gear_test_files/forward_model/volumetric/lightFluxFlicker_1x112_On\=0.mat \
                         --structZip /home/gear-builder/Desktop/gear_test_files/forward_model/volumetric/M662_preprocessedStruct.zip' % mainfold)
            elif which_forward == 'c':
                os.sytem('cd %s; fw gear local --averageAcquisitions 1 --dataFileType cifti --dataSourceType icafix \
                         --funcZip01 /home/gear-builder/Desktop/gear_test_files/forward_model/cifti/icafix.zip \
                         --modelClass prfTimeShift --modelOpts \'(pixelsPerDegree),5.1751,(polyDeg),5,(screenMagnification),1.00,(hrfParams),[0.7476,-0.7178,-0.3492]\' --tr 0.8 \
                         --stimFile /home/gear-builder/Desktop/gear_test_files/forward_model/cifti/pRFStimulus_108x108x420.mat \
                         --structZip /home/gear-builder/Desktop/gear_test_files/forward_model/cifti/TOME_3043_hcpstruct.zip' % mainfold)      
            else:
                print('Unknown option entered, not testing')
        elif gear_name == 'ldogfix':
            print('Starting ldogfix gear')
            os.system('cd %s; fw gear local --EPI_01 /home/gear-builder/Desktop/gear_test_files/ldog_fix/M662_left1_preprocessedFunc.zip \
                      --EPI_02 /home/gear-builder/Desktop/gear_test_files/ldog_fix/M662_left2_preprocessedFunc.zip \
                      --stimFile /home/gear-builder/Desktop/gear_test_files/ldog_fix/lightFluxFlicker_1x112_On=0.mat \
                      --archiveName testArchive --smoothingSigma 2' % mainfold)
        elif gear_name == 'ldogstruct':
            print('Starting ldogstruct gear')
            os.system('cd %s; fw gear local --MPRAGE_01 /home/gear-builder/Desktop/gear_test_files/ldog_struct/rage1.nii.gz \
                      --MPRAGE_02 /home/gear-builder/Desktop/gear_test_files/ldog_struct/rage2.nii.gz \
                      --centreOfGravityX 91 --centreOfGravityY 42 --centreOfGravityZ 95 --numberOfThreads 6 --subjectId M662_test' % mainfold)
        elif gear_name == 'ldogfunc':
            print('Starting ldogfunc gear')
            os.system('cd %s; fw gear local --StructZip /home/gear-builder/Desktop/gear_test_files/ldof_func/M662_preprocessedStruct.zip \
                      --additionalWarpToTemplate True --fMRIScoutAP /home/gear-builder/Desktop/gear_test_files/ldof_func/AP.nii.gz \
                      --fMRIScoutPA /home/gear-builder/Desktop/gear_test_files/ldof_func/PA.nii.gz --fMRIName left1 \
                      --fMRITimeSeries /home/gear-builder/Desktop/gear_test_files/ldof_func/left1.nii.gz' % mainfold)
        elif gear_name == 'bayesianfitting':
            print('Starting bayesianfitting gear')
            os.system('cd %s; fw gear local --nativeMgzMaps /home/ozzy/Desktop/gear_test_files/bayessianfitting/TOME_3046_maps_nativeMGZ.zip \
                      --radius-weight 0.25 --scale 100 --structZip /home/ozzy/Desktop/gear_test_files/bayessianfitting/TOME_3046_hcpstruct.zip' % mainfold)    
        else:
            print('Gear not found')
    else:
        print("Not testing the gear")
        
    uploadcall = input('Do you want to upload the gear now? You can do it later by cd-ing into the main_folder and running fw gear upload : y/n ')  
    if uploadcall == 'y':
        os.system('cd %s; fw gear upload' % mainfold)
    else:
        print("Not uploading")

    if which_number == '3':
        delete_call = input('The files downloaded from Flywheel into ldgog_struct_frame will be deleted now. Do you want to continue : y/n ')
        if delete_call == 'y':
            frame_path = os.path.join(path_to_matlab_doc, 'projects', 'mriLDOGAnalysis', 'fw_gears', 'ldog_struct', 'ldog_struct_frame')
            os.system('cd %s; rm *.zip *.gz' % frame_path)
        if delete_call == 'n':
            print('Not deleting the files downloaded from Flywheel. These files are too large to store on the lab github repo. Consider deleting them')
            
main_builder()
