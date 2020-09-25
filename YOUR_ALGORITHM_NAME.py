#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import Algorithmia
import json
import os.path
import joblib
import hashlib


# In[ ]:


client = Algorithmia.client("YOUR_API_KEY")

def load_model_config(config_rel_path="model_config.json"):
    """Loads the model manifest file as a dict. 
    A manifest file has the following structure:
    {
      "model_filepath": Uploaded model path on Algorithmia data collection
      "model_md5_hash": MD5 hash of the uploaded model file
      "model_origin_repo": Model development repository having the Github CI workflow
      "model_origin_commit_SHA": Commit SHA related to the trigger of the CI workflow
      "model_origin_commit_msg": Commit message related to the trigger of the CI workflow
      "model_uploaded_utc": UTC timestamp of the automated model upload
    }
    """
    config = []
    config_path = "{}/{}".format(os.getcwd(), (config_rel_path))
    if os.path.exists(config_path):
        with open(config_path) as json_file:
            config = json.load(json_file)
    return config


def load_model(config):
    """Loads the model object from the file at model_filepath key in config dict"""
    model_path = config["model_filepath"]
    model_file = client.file(model_path).getFile().name
    model = joblib.load(model_file)
    return model_file, model

def assert_model_md5(model_file):
    """
    Calculates the loaded model file's MD5 and compares the actual file hash with the hash on the model manifest
    """
    md5_hash = None
    DIGEST_BLOCK_SIZE = 128 * 64
    with open(model_file, "rb") as f:
        hasher = hashlib.md5()
        buf = f.read(DIGEST_BLOCK_SIZE)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(DIGEST_BLOCK_SIZE)
        md5_hash = hasher.hexdigest()
    assert config["model_md5_hash"] == md5_hash
    print("Model file MD5 assertion done.")


config = load_model_config()
model_file, model = load_model(config)
assert_model_md5(model_file)
print("MD5 assertion is okay, we have a perfectly uploaded model!")


# API calls will begin at the apply() method, with the request body passed as 'input'
# For more details, see algorithmia.com/developers/algorithm-development/languages
def apply(input):
    print(f"Echoing back input: {input}")


# In[ ]:


if __name__ == "__main__":
    algo_input = "Simple test input"
    print(f"Calling algorithm apply() func with input: {algo_input}")

    algo_result = apply(algo_input)
    print(algo_result)

