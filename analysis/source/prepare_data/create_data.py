import yaml


def main():
    CONFIG = yaml.load(open('config_global.yaml', 'rU'))
    with open('%s/data.txt' % CONFIG['build']['prepare_data'], 'wb') as f:
        f.write('x\n')
        f.writelines(['%s\n' % x for x in range(1, 300001)])

main()
