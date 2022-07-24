#!/bin/sh

port=${PORT-8000};
workers=${WORKERS-1};

uvicorn main:app --host=0.0.0.0 --port=$port --workers=$workers