#!/bin/bash

poetry run uvicorn app:app --reload --host 0.0.0.0 --port 9200
