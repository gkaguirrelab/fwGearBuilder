import os 

'''
This script contains the functions which compile matlab code for various 
projects. These functions here are called by the main_builder.py
'''

def compile_bayesprf(path_to_matlab_in_documents, bayesprf_gear_folder):
    ### Compile calcCorticalMag.m function loacted located in forwardModel 
    cortmag_funcPath = os.path.join(bayesprf_gear_folder, 'cortmag_func')
    if os.path.exists(cortmag_funcPath):
        os.system('rm -r %s' % cortmag_funcPath)    
    os.system('mkdir %s' % cortmag_funcPath)
        
    mcc_call = 'mcc -m -R -nodisplay %s -I %s -I %s -a %s -d %s -v' % (os.path.join(path_to_matlab_in_documents,'projects/forwardModelWrapper/code/bayesPRF/calcCorticalMag.m'),
                                                                       os.path.join(path_to_matlab_in_documents,'toolboxes/freesurferMatlab/matlab/'),
                                                                       os.path.join(path_to_matlab_in_documents,'projects/forwardModelWrapper/code/utilities'),
                                                                       os.path.join(path_to_matlab_in_documents,'toolboxes/matlabcentral/TheilSen/'),
                                                                       cortmag_funcPath)     

    print('Compiling calcCorticalMag.m \n')
    os.system(mcc_call)

    ### Compile postprocessBayes.m function located in forwardModel 
    postproc_funcPath = os.path.join(bayesprf_gear_folder, 'postproc_func')
    if os.path.exists(postproc_funcPath):
        os.system('rm -r %s' % postproc_funcPath) 
    os.system('mkdir %s' % postproc_funcPath)
    
    mcc_call = 'mcc -m -R -nodisplay %s -I %s -I %s -d %s -v' % (os.path.join(path_to_matlab_in_documents,'projects/forwardModelWrapper/code/bayesPRF/postprocessBayes.m'),
                                                                 os.path.join(path_to_matlab_in_documents,'toolboxes/ciftiMatlab/'),
                                                                 os.path.join(path_to_matlab_in_documents,'toolboxes/freesurferMatlab/matlab/'),
                                                                 postproc_funcPath)
    
    print('Compiling postprocessBayes.m \n')
    os.system(mcc_call)
    
    ### Compile renderInferredMaps.m function located in forwardModel 
    render_funcPath = os.path.join(bayesprf_gear_folder, 'render_func')
    if os.path.exists(render_funcPath):
        os.system('rm -r %s' % render_funcPath) 
    os.system('mkdir %s' % render_funcPath)
        
    mcc_call = 'mcc -m -R -nodisplay %s -I %s -I %s -I %s -d %s -v' % (os.path.join(path_to_matlab_in_documents,'projects/forwardModelWrapper/code/bayesPRF/renderInferredMaps.m'),
                                                                       os.path.join(path_to_matlab_in_documents,'projects/forwardModelWrapper/code/'),
                                                                       os.path.join(path_to_matlab_in_documents,'projects/forwardModelWrapper/code/utilities/'),
                                                                       os.path.join(path_to_matlab_in_documents,'toolboxes/freesurferMatlab/matlab/'),
                                                                       render_funcPath)
    
    print('Compiling renderInferredMaps.m \n')
    os.system(mcc_call)    
    
def compile_createSubjectFodMap(path_to_matlab_in_documents, createSubjectFodMap_gear_folder):
    ### Compile fodMakerWrapper.m function located in fixelTOMEAnalysis
    adaptConOpt_funcPath = os.path.join(createSubjectFodMap_gear_folder, 'adaptConOpt')
    if os.path.exists(adaptConOpt_funcPath):
        os.system('rm -r %s' % adaptConOpt_funcPath)    
    os.system('mkdir %s' % adaptConOpt_funcPath)
    
    mcc_call = 'mcc -m -R -nodisplay %s -I %s -I %s -a %s -d %s -v' % (os.path.join(path_to_matlab_in_documents,'projects/fixelTOMEAnalysis/code/AdaptConOpt_TranAndShi_2015/fodMakerWrapper.m'),
                                                                       os.path.join(path_to_matlab_in_documents,'projects/fixelTOMEAnalysis/code/AdaptConOpt_TranAndShi_2015/General_Tools/'),
                                                                       os.path.join(path_to_matlab_in_documents,'projects/fixelTOMEAnalysis/code/AdaptConOpt_TranAndShi_2015/NIfTI_Tools/'),
                                                                       os.path.join(path_to_matlab_in_documents,'projects/fixelTOMEAnalysis/code/AdaptConOpt_TranAndShi_2015/qpc'),
                                                                       adaptConOpt_funcPath)
    
    print('Compiling fodMakerWrapper.m \n')
    os.system(mcc_call)
                                                                       
    
    
  
    
  
    
  
    
  
    
  
    
  
    

def compile_forwardModel(path_to_matlab_documents, output_folder):
    
    # Create the output folder if doesn't exist
    if not os.path.exists(output_folder):
        os.system("mkdir %s"%output_folder)
    
    mcc_path = 'mcc'
    mcc_call2 = '%s -m -R -nodisplay %s -a %s -a %s -a %s -a %s -a %s -a %s -a %s -I %s -I %s -I %s \
    -I %s -d %s -v'%(mcc_path, os.path.join(path_to_matlab_documents,'projects/forwardModelWrapper/code/mainWrapper.m'),
    os.path.join(path_to_matlab_documents,'projects/forwardModelWrapper/code/handleInputs.m'),
    os.path.join(path_to_matlab_documents,'projects/forwardModelWrapper/code/handleOutputs.m'),
    os.path.join(path_to_matlab_documents,'projects/forwardModelWrapper/code/makeSurfMap.m'),
    os.path.join(path_to_matlab_documents,'projects/forwardModelWrapper/code/startParpool.m'),
    os.path.join(path_to_matlab_documents,'projects/forwardModelWrapper/code/handleInputs.m'),
    os.path.join(path_to_matlab_documents,'projects/forwardModelWrapper/code/bayesPRF/renderInferredMaps.m'),
    os.path.join(path_to_matlab_documents,'projects/forwardModel/'),
    os.path.join(path_to_matlab_documents,'toolboxes/ciftiMatlab'),
    os.path.join(path_to_matlab_documents,'projects/forwardModelWrapper/code/utilities/'),    
    os.path.join(path_to_matlab_documents,'toolboxes/freesurferMatlab/matlab/'),
    os.path.join(path_to_matlab_documents,'toolboxes/progressBar/'),
    output_folder)
    
    print('Compiling mainWrapper.m')
    os.system(mcc_call2)
    
def compile_regressMotion(path_to_matlab_documents, output_folder):

    # Create the output folder if doesn't exist
    if not os.path.exists(output_folder):
        os.system("mkdir %s"%output_folder)
    
    #mcc_path = '/usr/local/MATLAB/R2018b/bin/mcc'
    mcc_path = 'mcc'
    mcc_call5 = '%s -m -R -nodisplay %s -I %s -d %s -v'%(mcc_path, os.path.join(path_to_matlab_documents,'projects/mriLDOGAnalysis/matlab/regressMotion.m'),  
                                                        os.path.join(path_to_matlab_documents,'toolboxes/freesurferMatlab/matlab/'),
                                                        output_folder)
    
    print('Compiling regressMotion.m')
    os.system(mcc_call5)

def compile_localWM(path_to_matlab_documents, output_folder):

    # Create the output folder if doesn't exist
    if not os.path.exists(output_folder):
        os.system("mkdir %s"%output_folder)
    
    #mcc_path = '/usr/local/MATLAB/R2018b/bin/mcc'
    mcc_path = 'mcc'
    mcc_call6 = '%s -m -R -nodisplay %s -I %s -I %s -d %s -v'%(mcc_path, os.path.join(path_to_matlab_documents,'projects/localWhiteMatterNoiseRegression/code/remove_localWM_FwVersion.m'),  
                                                               os.path.join(path_to_matlab_documents,'toolboxes/freesurferMatlab/matlab/'),
                                                               os.path.join(path_to_matlab_documents,'toolboxes/flywheelMRSupport/code/'),
                                                               output_folder)
    
    print('Compiling remove_localWM_FwVersion.m')
    os.system(mcc_call6)
    
def compile_psdFunc(path_to_matlab_documents, output_folder):

    # Create the output folder if doesn't exist
    if not os.path.exists(output_folder):
        os.system("mkdir %s"%output_folder)
    
    #mcc_path = '/usr/local/MATLAB/R2018b/bin/mcc'
    mcc_path = 'mcc'
    mcc_call7 = '%s -m -R -nodisplay %s -I %s -I %s -a %s -d %s -v'%(mcc_path, os.path.join(path_to_matlab_documents,'projects/localWhiteMatterNoiseRegression/code/calcOneSidedPSD_FwVersion.m'),  
                                                                     os.path.join(path_to_matlab_documents,'toolboxes/freesurferMatlab/matlab/'),
                                                                     os.path.join(path_to_matlab_documents,'toolboxes/flywheelMRSupport/code/'),
                                                                     os.path.join(path_to_matlab_documents,'projects/forwardModel/code/utilities/calcOneSidedPSD.m'),
                                                                     output_folder)
    
    print('Compiling calcOneSidedPSD.m')
    os.system(mcc_call7)
