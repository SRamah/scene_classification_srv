#! /usr/bin/env bash

MODEL=/workspace/plugins/scenes/algos/cnn/top_model_weights.h5
if [ -f "$MODEL" ]; then
    echo "$MODEL exists."
    uvicorn --host=0.0.0.0 main:app --reload
else 
    echo "$MODEL does not exist."
    wget -P /workspace/plugins/scenes/algos/cnn/ https://mys3db.s3.eu-west-3.amazonaws.com/public_repo/Scene_Classification_Models/cnn/top_model_weights.h5
    uvicorn --host=0.0.0.0 main:app --reload
fi