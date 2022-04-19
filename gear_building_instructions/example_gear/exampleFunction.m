function exampleFunction(vectorTextFile, vectorToAdd, scaleBy, transpose, outputTextFile) 

    % Read in the vector on the text file
    data = importdata(vectorTextFile);
    
    % Add the vector
    data = data + vectorToAdd;
    
    % Scale 
    data = data*scaleBy;
    
    % Transpose 
    if transpose
        data = data';
    end
    
    % Write a new text file
    writematrix(data, outputTextFile)

end
    
    