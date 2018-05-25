config_common = {
    'static_folder': 'D:\\player'
}

config_dev = dict(config_common, **{
})

config = {
    'dev': config_dev,
    'common': config_common
}

current_config = config['dev']