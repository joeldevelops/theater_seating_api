#!/usr/bin/env bash

hypercorn src:app --bind $HOST:$PORT --log-level=$LOG_LEVEL --workers=$WORKERS