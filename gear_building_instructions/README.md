# Matlab Gear Instructions

# Stuff you’ll need

-	MATLAB compiler: We need this to compile our MATLAB functions. It can be downloaded through “Get More Apps” menu in MATLAB. Once it is installed, make sure you can call “mcc” on your Linux Terminal.
-	A Linux computer: Docker mainly works with Unix images and MATLAB compiler creates executables specific to the OS it is run under. So to be able to run MATLAB in Docker, we need to compile our code with a Unix Machine.
-	MATLAB Runtime: We will need this to test the compiled code to make sure it works before we stick it in a gear. Download it here: https://www.mathworks.com/products/compiler/matlab-runtime.html The version you install should match your MATLAB version or the version under which you compiled your MATLAB functions.
-	Flywheel CLI to make the gear. Download instructions here: https://docs.flywheel.io/hc/en-us/articles/360008162214-Installing-the-Flywheel-Command-Line-Interface-CLI-
Make sure you can call fw from a terminal. Set path to the binary if you cannot. Once you can call it run: “fw login -h <API-key>” with your API key.

# Instructions

Compile a MATLAB function
We first need to compile our matlab function. When we run the compiled function on a bash terminal, passing anything other than strings to it makes things a bit complicated. Therefore, it is a good idea to make a wrapper around the function we want to compile. This wrapper will receive every input we will use in our function as a string and then convert them to their appropriate type.

1 - Check out fwGearBuilder/gear_building_instructions/example_gear/exampleFunction.m. This function gets a text file (called exampletext.txt located on the same directory) which contains a comma separated vector, does some operations on it and saves a new text file.

2 - Now check out exampleWrapper.m. This is a wrapper that takes the variables as strings, converts them to appropriate type and pass them to the exampleFunction.m. You’ll need to make a wrapper like this for your own function. If your function uses a bunch of sub functions, no worries. You’ll need to make this wrapper just for your main function.

3 - Now we can compile the wrapper. If you use ToolboxToolbox, we need to disable it first as the startup options complicate the compiling process. Just go to your Documents/MATLAB folder and rename your startup.m to something else (e.g nostartup.m) until we finish compiling. Next call mcc from a bash terminal as following:

	mcc -m exampleWrapper.m -a exampleFunction.m -d <saveFolder>

This will compile the your wrapper and save the output to a folder you specify with the -d option. If your function calls any sub functions, you need to add path to them with more -a flags. In our case, our main function is the only sub function of the wrapper. If you have multiple sub functions in a folder, the compiler can search for them automatically if you use the -I <path_to_folder> option. Warning: This folder search option does not descent into sub folders automatically. If you have your sub functions in nested folders, set path to each of them with multiple -I options.

4 - Now we need to test the compiled code with MATLAB runtime to make sure it works. Here is how it is ran:
 
	‘<compiledBashFile>’  ‘<matlabRuntimeInstallationPath>’  ‘<input1>’  ‘<input2>’  ‘<input3>’ …

If you had two varargin options for example, say runSpeed and saveIntermediateFiles, in your script, here is how you would set those when you run the compiled code:
 
	‘<compiledBashFile>’  ‘<matlabRuntimeInstallationPath>’  ‘<input1>’  ‘<input2>’  ‘ runSpeed’  ‘fast’  ‘saveIntermediateFiles’  ‘true’

Note: This is how the matlabRuntimeInstallationPath looks like: '/usr/local/MATLAB/R2020a/MATLAB_Runtime/v98/'.
Don’t forget to include the “v98” subfolder part in it (your version can be different though, e.g v97, v99).

As an example, here is how we test the compiled exampleWrapper function:

	'/run_exampleWrapper.sh' '/usr/local/MATLAB/MATLAB_Runtime/v98/' '/exampletext.txt' '[1,1,1,1,1]' '2' 'true' '/home/outputText.txt'

This takes the vector in exampletext.txt, adds [1,1,1,1,1], scales by 2, transposes the vector, and saves it as outputText.txt to the home directory.

Assembling the gear files and making the gear

1 – Create an empty folder where we will assemble the gear files. Check out: /fwGearBuilder/gear_building_instructions/example_gear/gear_files

Once you are done with all the steps below, your gear folder should look this example one.  

2 – Even though we tested the compiled code with just the .sh executable, we’ll need every file that mcc created. So copy the entire folder that contains all the mcc output into the gear folder we created at step 1.

3 – In the gear folder we now need to create a Dockerfile. DockerFile is a template for our Docker image. Here we install every tool and software we’ll need in the gear including matlab runtime. Check out the Dockerfile example located in fwGearBuilder/gear_building_instructions/example_gear/gear_files. This example file has comments for each line explaining what we are doing. Continue reading the instructions once you have a Dockerfile for your gear.

4 – Next is the manifest.json file. This file decides the interface of our gear on the webpage (e.g. what will be the name of the gear, its inputs, and its config options.). Check out the example file and reorganize it to your needs. You can find the definition of some variables below. More options for different file type constraints and config styles can be found on the flywheel page: https://docs.flywheel.io/hc/en-us/articles/360037695713

-	name: machine friendly name for your gear (required)
-	label: human friendly name for your gear (required)
-	description: description of your gear
-	author: the name of the person who made the script you are running in the gear
-	maintainer: your name and email address
-	source: webpage to the gear files if you put them online somewhere
-	url: webpage to the code you used if available online
-	version: version of your gear. Can start with any number pattern (e.g. 0.1.0 or 0.1)
-	custom: contains some useful stuff
-	flywheel (subfield of custom): Flywheel related custom stuff
-	suite (subfield of flywheel): Under which lab the gear will be located. If you don’t include this, the gear will be listed independently which is fine if you don’t have your own suite on Flywheel webpage.
-	license: If you have a license for the software
-	config: Contains all the config options that will be passed to your compiled MATLAB   function. Can give these any name as we are going to parse them in the run script anyways. But it is a good idea to match them to the config options you have on your matlab script to keep your sanity.
-	default (subfield of config): Default config option must match the type
-	description (subfield of config): Description of the config option
-	type: type of the config option. Could be string, boolean, number. If you made your wrapper in a way that it only accepts strings and converts them to whatever type the main function needs as suggested, you can use all strings here
-	inputs: Contains the inputs of the gear. Create as many inputs as you need for your compiled function. It has similar subfields that the config fields have such as description and type. Optional decides whether the input is optional. If not and you leave it empty when running the gear on the Flywheel webpage, the gear doesn’t let you run it.  

5 - Finally check out the python run script. It has the comments for everything we need to do on there. Come back to the instructions when you have the Dockerfile, manifest.json, and run

6 – Once you have everything ready, open up a terminal, cd into the gear folder and run the following:

	docker build -t <a-name-for-your-docker-image>:<a-version-num> .

This builds the docker image with the instructions on we set on Dockerfile. The name and the version number you need to give don’t matter much for the gear so name it anything. Don’t forget the dot at the end of the command. It tells the function to use the files in the current directory. This operation might take a bit.

7  - Next, while still in the same directory, run:

	fw gear create

It will ask you to give your gear a human readable name. You can name it anything, but the convention is something like:

exampleGear: An example gear to do exemplary stuff

Then it will ask you for a machine friendly name (e.g examplegear)

Select Other as the base image NOT Docker. And type the name and the version of the Docker image you created at step 6 as

 	<a-name-for-your-docker-image>:<a-version-num>

Select analysis for the next question and then type “yes” when it asks you whether you want to replace run and manifest files.

The gear is now created in the gear folder.

8 – Now we need to test the gear before uploading. While in the gear folder on a terminal type:

	fw gear local --help

This tells you how to run your gear locally. Here is how we would run the exampleWrapper gear we made:

	fw gear local --vectorTextFile=’exampletext.txt’ --vectorToAdd=’[1,1,1,1,1]’ --scaleBy=’2’ –transpose=’true’

Calling this command will run the gear and create input and output folders and config.json briefly in your gear folders. Input and config will disappear as soon as the gear complete, but the output folder will stay containing the output of your gear now. If you have everything you need in the output folder, then your gear is successful.

9 – Due to a bug (or a Flywheel developer choice), every time you make the gear, some information on the manifest.json is replaced. For instance, the version is automatically set to 0. Go back in the manifest.json and put the version number you want again. It also replaces the maintainer and author names with your Flywheel login names. You can change these as well if you don’t like name Flywheel assigns to them. Finally, you can add gears to suites. For instance to make gears listed under GKAguirreLab on the Flywheel webpage, in manifest.json under “custom”, in line with gear-builder sub field, add flywheel and suite options. So the last few lines of your manifest should look like this if you want to add your gear into a suite:

	"custom": {
		"gear-builder": {
			"category": "analysis",
			"image": "test:latest"
		},
		“flywheel”: {
			“suite”: “GKAguirreLab”
		}
	}

10 – The gear is done! To upload it to the webpage, on a terminal window in the gear directory run:

	fw gear upload