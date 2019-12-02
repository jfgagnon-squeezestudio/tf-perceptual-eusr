import os
from tensorflow.python.client import device_lib

# validate setup before
print(device_lib.list_local_devices())

# data is assumed to be present and valid
# Pre-train EUSR model
# os.system("py train.py --data_input_path=./LR --data_truth_path=./HR --model=eusr --scales=2,4")
