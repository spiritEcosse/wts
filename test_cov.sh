#!/bin/sh
mv -f app.db wts
export APP_SETTINGS=wts.config.TestingConfig && \
python -m pytest --cov-report term-missing --cov=. tests/
mv -f wts/app.db .
export APP_SETTINGS=wts.config.DevelopmentConfig
