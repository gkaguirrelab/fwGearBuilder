function exampleWrapper(vectorTextFile, vectorToAdd, scaleBy, transpose, outputTextFile)

    % This wrapper gets every input as text and converts them to the
    % whatever format the main function requires.
    
    % vectorTextFile is already a string path
    vectorTextFile = vectorTextFile;
    
    % vectorToAdd and scaleBy need to be converted to vector and num 
    % respectively. str2num can do both of these operations
    vectorToAdd = str2num(vectorToAdd);
    scaleBy = str2num(scaleBy);
    
    % Convert transpose to boolean 
    if strcmp(transpose, 'true')
        transpose = true;
    elseif strcmp(transpose, 'false')
        transpose = false;
    else
        error('transpose input is not recognized. Either use true or false')
    end
    
    % OutputTextFile is already a string 
    outputTextFile = outputTextFile;
    
    exampleFunction(vectorTextFile, vectorToAdd, scaleBy, transpose, outputTextFile)
end
    