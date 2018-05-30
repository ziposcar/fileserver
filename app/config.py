#!/usr/bin/python 
# -*- coding: utf-8 -*-

config_common = {
    'static_folder': '/home/zip/'
}

config_dev = dict(config_common, **{
})

config = {
    'dev': config_dev,
    'common': config_common
}

current_config = config['dev']