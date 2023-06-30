function glmSingleWrapper(designMatrixPath, dataPath1, dataPath02, dataPath03, ...
                          dataPath04, dataPath05, dataPath06, dataPath07, ...
                          dataPath08, dataPath09, dataPath10, stimdur,tr,outputdir, ...
                          wantlibrary, wantglmdenoise, wantfracridge, ...
                          chunknum, xvalscheme, sessionindicator, wantfileoutputs, ...
                          wantmemoryoutputs, extraregressors, maxpolydeg, ...
                          wantpercentbold, hrftoassume, hrflibrary, firdelay, ...
                          firpct, wantlss, numpcstotry, brainthresh, brainR2, ...
                          brainexclude, pcR2cutoff, pcR2cutoffmask, pcstop, ...
                          fracs, wantautoscale)
                                                 
% Every input to this wrapper should be string. The purpose of this wrapper 
% is to convert eveything from string to its propper form expected by the 
% glmSingle algorithm. We need this to make our life easier for the gear. 
% Note that most of these inputs have a default value. We won't code for
% them in this wrapper, but rather specify them in the gear config options
% so defaults will always be explicitly passed to this function unless of
% course the config is changed on the gear interface. 

%% Inputs that require files loading
% Load data Image
data = {};
allData = {dataPath1, dataPath02, dataPath03, dataPath04, ...
           dataPath05, dataPath06, dataPath07, ...
           dataPath08, dataPath09, dataPath10};
emptyCells = find(contains(allData,'[]'));
if ~isempty(emptyCells)
    allData(emptyCells) = [];
end
       
for ii = 1:length(allData)
    loadedData = MRIread(allData{ii});
    data{ii} = loadedData.vol;
end

% Load design matrix 
design = load(designMatrixPath); 
fieldName = fieldnames(design);
design = design.(fieldName{1});

% Load extra regressors if specified 
if ~strcmp(extraregressors, '[]')
    extraregressors = load(extraregressors);
    fieldName = fieldnames(extraregressors);
    opt.extraregressors = extraregressors.(fieldName{1});
else
    opt.extraregressors = [];
end

% Load assumed hrf if specified
if ~strcmp(hrftoassume, '[]')
    hrftoassume = load(hrftoassume);
    fieldName = fieldnames(hrftoassume);
    opt.hrftoassume = hrftoassume.(fieldName{1});    
else
    opt.hrftoassume = [];
end

% Load hrf library if specified
if ~strcmp(hrflibrary, '[]')
    hrflibrary = load(hrflibrary);
    fieldName = fieldnames(hrflibrary);
    opt.hrflibrary = hrflibrary.(fieldName{1});   
else
    opt.hrflibrary = [];
end

% Load brainexclude
if ~strcmp(brainexclude, '[]')
    brainexclude = MRIread(brainexclude);
    opt.brainexclude = brainexclude.vol;
else
    opt.brainexclude = [];
end

% Load R2 cutoff mask 
if ~strcmp(pcR2cutoffmask, '[]')
    pcR2cutoffmask = MRIread(pcR2cutoffmask);
    opt.pcR2cutoffmask = pcR2cutoffmask.vol;
else
    opt.pcR2cutoffmask = [];
end

% Fracs
if ~strcmp(fracs, '[]')
    fracs = load(fracs);
    fieldName = fieldnames(fracs);
    opt.fracs = fracs.(fieldName{1});  
else
    opt.fracs = [];
end

%% Config options that don't require any loading
% Convert config options 
stimdur = str2num(stimdur);
tr = str2num(tr);
outputdir = outputdir;
opt.wantlibrary = str2num(wantlibrary);
opt.wantglmdenoise = str2num(wantglmdenoise);
opt.wantfracridge = str2num(wantfracridge);
opt.chunknum = str2num(chunknum);
if ~strcmp(xvalscheme, 'use_default')
    % Use regexp to extract the individual items
    item_pattern = '\[(.*?)\]';
    item_matches = regexp(xvalscheme, item_pattern, 'match');
    % Initialize the output cell array of structs
    output_cell = cell(length(item_matches), 1);
    % Loop over the items and add them to the output cell array as structs
    for i = 1:length(item_matches)
        item_str = strsplit(item_matches{i}(2:end-1), ' ');
        item_arr = str2double(item_str);
        output_cell{i} = item_arr;
    end
    opt.xvalscheme = output_cell';
else
    opt.xvalscheme = [];
end

if ~strcmp(sessionindicator, 'use_default')
    opt.sessionindicator = str2num(sessionindicator);
else
    opt.sessionindicator = [];
end

opt.wantfileoutputs = str2num(wantfileoutputs);
opt.wantmemoryoutputs = str2num(wantmemoryoutputs);

if ~strcmp(maxpolydeg, 'use_default')
    opt.maxpolydeg = str2num(maxpolydeg);
else
    opt.maxpolydeg = [];
end

opt.wantpercentbold = str2num(wantpercentbold);
opt.firdelay = str2num(firdelay);
opt.firpct = str2num(firpct);
opt.wantlss = str2num(wantlss);
opt.numpcstotry = str2num(numpcstotry);
opt.brainthresh = str2num(brainthresh);
if ~strcmp(brainR2, '[]')
    opt.brainR2 = str2num(brainR2);
else
    opt.brainR2 = [];
end
if ~strcmp(pcR2cutoff, '[]')
    opt.pcR2cutoff = str2num(pcR2cutoff);
else
    opt.pcR2cutoff = [];
end
opt.pcstop = str2num(pcstop);
opt.wantautoscale = str2num(wantautoscale);

%% Call the function 
[results, resultsdesign] = GLMestimatesingletrial(design,data,stimdur,tr,outputdir,opt);
save(fullfile(outputdir,'results.mat'), 'results')
save(fullfile(outputdir,'resultsdesign.mat'), 'resultsdesign')
