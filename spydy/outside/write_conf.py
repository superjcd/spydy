import configparser

config = configparser.ConfigParser()

config['PipeLine'] = {
    'url':'RedisListUrls',
    'request':'LinearRequest',
    'parser' :'DmozParser',
    'store':'CscStore'
}


with open('config.ini', 'w') as configfile:
    config.write(configfile)