import configparser

config = configparser.ConfigParser()


config.read("spydy.cfg")

print(config.sections())

for arg, value in config["PipeLine"].items():
    print(arg)

print("PipeLine" in config)


