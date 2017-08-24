clear all

PATHS = ReadYaml('config_global.yaml');
data = dataset('File', sprintf('%s/data_matlab.txt', PATHS.build.prepare_data));

fid = fopen(sprintf('%s/table_matlab.txt', PATHS.build.descriptive), 'wt');
fprintf(fid, '<tab:table>\n');
fprintf(fid, '%.1f\n%.3f\n%g\n%g', mean(data.x), std(data.x), max(data.x), min(data.x));
fclose(fid);

set(figure, 'visible', 'off');
hist(data.x);
print(sprintf('%s/plot_matlab.eps', PATHS.build.descriptive), '-depsc');

exit