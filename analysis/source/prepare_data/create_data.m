clear all

CONFIG = ReadYaml('config_global.yaml');
x = 1:300000;

fid = fopen(sprintf('%s/data_matlab.txt', CONFIG.build.prepare_data), 'wt');
fprintf(fid, 'x\n');
fprintf(fid, '%d\n', x);
fclose(fid);

exit
