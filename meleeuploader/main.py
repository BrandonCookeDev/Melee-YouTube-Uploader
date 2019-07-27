#!/usr/bin/env python3

import os
import sys
import logging as log

from . import forms
from . import consts
from . import youtube as yt
from .utils import setupLogger

import pyforms_lite


def main():
    form_height = 300
    form_width = 300

    try:
        print('starting')
        log_level = os.getenv('LOG_LEVEL')
        setupLogger(log_level)
        log.info('Logging setup complete! Log Level is {}'.format(log.Logger.getEffectiveLevel()))

        log.debug('Setting up melee uploader with dimensions: ({}, {})'.format(form_width, form_height))
        if os.path.isfile(consts.youtube_file) or not len(os.listdir(consts.smash_folder)):
            consts.youtube = yt.get_youtube_service()
        elif len(os.listdir(consts.smash_folder)):
            pyforms_lite.start_app(forms.YouTubeSelector, geometry=(form_width, form_height, 1, 1))
            consts.youtube = yt.get_youtube_service()
    except Exception as e:
        print(e)
        print("There was an issue with getting Google Credentials")
        sys.exit(1)
    try:
        consts.sheets = yt.get_spreadsheet_service()
    except Exception as e:
        print(e)
    try:
        if os.path.isfile(consts.partner_file):
            consts.partner = yt.get_partner_service()
    except Exception as e:
        print(e)
    try:
        pyforms_lite.start_app(forms.MeleeUploader, geometry=(form_width, form_height, 1, 1))
    except Exception as e:
        print("Error:", e)
        sys.exit(1)


def ult():
    consts.melee = False
    main()


if __name__ == "__main__":
    main()
