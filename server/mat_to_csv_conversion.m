rootdir = "C:\Users\garrett\Documents\ETTP\server\a-large-scale-12-lead-electrocardiogram-database-for-arrhythmia-study-1.0.0";
filelist = dir(fullfile(rootdir, '**\*.mat'));  %get list of files and folders in any subfolder
filelist = filelist(~[filelist.isdir]);  %remove folders from list

% We now have a struct of all matlab files in our folder. 
% Iterate through them and convert to CSV
for i=1 : length(filelist)
    file = filelist(i);
    fullFileName = fullfile(file.folder, file.name);
    [path, fileName, extension] = fileparts(fullFileName);

    fileData = load(fullFileName);
    csvwrite(strcat('./data/', fileName, '.csv'), fileData.val);
end