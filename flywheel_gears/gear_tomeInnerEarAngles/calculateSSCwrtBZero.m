function calculateSSCwrtBZero(B0, normalFolder, subID, outputFolder)

% This is example code that provides the Euler angles that describe the
% orientation of each of the semi-circular canals with respect to the B0
% magnetic field.
%
% The example is performed for one subject (TOME_3045). The demo requires
% the "normals" directory that Ozzy is able to produce using Ahmad's SCC
% template fitting code. The demo also accesses the T2 NIFTI file
% associated with this subject to obtain the angles of the FOV of the
% imaging acquisition w.r.t. the B0 field.


load(B0)
iop = iop';
% Derive rotation matrix m from ImageOrientationPatientDICOM
xyzR = iop(1:3);
xyzC = iop(4:6);
xyzS = [ (xyzR(2) * xyzC(3)) - (xyzR(3) * xyzC(2)) ; ...
    (xyzR(3) * xyzC(1)) - (xyzC(1) * xyzC(3)) ; ...
    (xyzR(1) * xyzC(2)) - (xyzR(2) * xyzC(1))  ...
    ];
m = [xyzR xyzC xyzS];

% adjust m to wrap the Euler angles and center them on zero
m = eul2rotm(deg2rad(rad2deg(rotm2eul(m,'ZYX')) + [-90 0 90]),'ZYX');

% Prepare plot elements
sccList = {'lat','ant','post'};
sideList = {'right','left'};
colorList = {'r','g','b'};
figHandle=figure('visible','off');

% Set up a table to hold the results
T = table('Size',[6 4],'VariableTypes',{'string','string','double','double'});
T.Properties.VariableNames = {'Side','Canal','angle_xy','angle_xz'};
sides = {'right','left'};
canals = {'lat','ant','post'};

normalSet = cell(2,3);

for ss=1:2
    for cc=1:3
        % Load file
        fileName = fullfile(normalFolder,[sideList{ss} '_' sccList{cc} '.mat']);
        point_array = [];
        R = [];
        offset = [];
        normal = [];
        load(fileName);
        
        % Rotate the plane normal, offset, and point array by the IOP
        % rotation matrix
        offset = m*offset';
        normal = m*normal';
        point_array=(m*point_array')';
        
        R1 = [offset, normal];

        normalSet{ss,cc}=R1;

%         R2 = [0 0 0; 1 0 0]';
%         [~,angle_xz] = angleRays( R1, R2 );
%         
%         
%         % Report the values for this subject to the screen
%         str = sprintf([sideList{ss} '_' sccList{cc} ' (' colorList{cc} '), angle w.r.t B0: %2.1f degrees'],angle_xz);
%         disp(str);
%         
%         % Save the value in the table
%         row = 2*(cc-1)+ss;
%         T(row,1)=sides(ss);
%         T(row,2)=canals(cc);
%         T(row,3)={angle_xy};
%         T(row,4)={angle_xz};
        
        % Construct the plot if requested
        plot3(point_array(:,1),point_array(:,2),point_array(:,3),['*' colorList{cc}])
        hold on
        quiver3(offset(1),offset(2),offset(3),normal(1),normal(2),normal(3),5,['-' colorList{cc}],'LineWidth',3)        
    end
end

% Clean up plot
axis equal
xlabel('Left (-) -- Right (+)')
ylabel('Posterior (-) -- Anterior (+)')
zlabel('Inferior (-) -- Superior (+)')

savefig(figHandle, fullfile(outputFolder, [subID 'AnglesPlot.fig']))
saveas(figHandle, fullfile(outputFolder, [subID 'AnglesPlot.pdf']))

% % Save the table
% tableName = fullfile(outputFolder, [subID '_CanalAnglesWithB0.csv']);
% writetable(T,tableName)

% Save the normalSet
fileName = fullfile(outputFolder, [subID '_NormalSetWRT_B0.mat']);
save(fileName,'normalSet')

%% LOCAL FUNCTION
function [angle_xy, angle_xz] = angleRays( R1, R2 )
% Returns the angle in degrees between two rays
%
% Syntax:
%  [angle_xy, angle_xz] = angleRays( R1, R2 )
%
% Description:
%   Just what it says on the tin.
%
% Inputs:
%   R1, R2                - 3x2 matrix that specifies a vector of the form
%                           [p; u], corresponding to
%                               R = p + t*u
%                           where p is vector origin, u is the direction
%                           expressed as a unit step, and t is unity for a
%                           unit vector.
%
% Outputs:
%   angle_xy, angle_xz    - Scalars. Angles in degrees between the rays
%                           projected on the xy and xz planes.
%
% Examples:
%{
    p = [0;0;0];
    u = [1;0;0];
    R1 = quadric.normalizeRay([p, u]);
    p = [0;0;0];
    u = [1;tand(15);tand(-7)];
    R2 = quadric.normalizeRay([p, u]);
    [angle, angle_xy, angle_xz] = quadric.angleRays( R1, R2 );
%}

% Obtain the angles as projected on the xy and xz planes
u1_xy = [R1(1,2);R1(2,2);0];
u2_xy = [R2(1,2);R2(2,2);0];
angle_xy = rad2deg(atan2(norm(cross(u1_xy,u2_xy)), dot(u1_xy,u2_xy)));

% Make the angle signed with respect to the R1 vector
angle_xy = angle_xy*sign(dot([0;0;1],cross(u1_xy,u2_xy)));

u1_xz = [R1(1,2);0;R1(3,2)];
u2_xz = [R2(1,2);0;R2(3,2)];
angle_xz = rad2deg(atan2(norm(cross(u1_xz,u2_xz)), dot(u1_xz,u2_xz)));

% Make the angle signed with respect to the R1 vector
angle_xz = angle_xz*sign(dot([0;1;0],cross(u1_xz,u2_xz)));


end

end
