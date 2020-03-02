# fwGearBuilder
Code to assemble gears for use on the Flywheel platform

# Instructions

1 - Connect to the gear builder computer using TeamViewer.
2 - cd into "/home/gear-builder/Documents/MATLAB/projects/fwGearBuilder/gear_builder"
3 - run "python main_builder"
4 - Follow the instructions to update/rebuild gears.

# Scripts inside the repo

- main_builder.py = The main python script used for building the gear 
- compiler_functions.py = The script that contains the functions for compiling the Matlab scripts used in the gears.
- gearBuilderAutotbUse.m = The Matlab script which contains several tbUse commands. This script is called in main_builder.py to update several toolboxes for the Matlab operations. Requires ToolboxToolbox setup and path structures.
