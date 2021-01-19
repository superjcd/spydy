import yaml

file = open('config.yaml', 'r').read()

config = yaml.load(file, Loader=yaml.CLoader)
print(config)