#!/bin/sh
mv -f app.db wts
export APP_SETTINGS=wts.config.TestingConfig && \
python -m pytest tests/ -vv
mv -f wts/app.db .
export APP_SETTINGS=wts.config.DevelopmentConfig
