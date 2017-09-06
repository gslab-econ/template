clear all

paths_global = ReadYaml('config_global.yaml');
x = 1:300000;

fid = fopen(sprintf('%s/data.txt', paths_global.build.prepare_data), 'wt');
fprintf(fid, 'x\n');
fprintf(fid, '%d\n', x);
fclose(fid);

exit
