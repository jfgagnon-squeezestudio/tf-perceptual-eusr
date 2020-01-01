import os
import platform
from tensorflow.python.client import device_lib

# validate setup before
print("Tensorflow test")
print(device_lib.list_local_devices())

pythonExec = "py" if (platform.system() == "Windows") else "python"

# data is assumed to be present and valid
# Pre-train EUSR model
eusrModelTrainingArguments = "train.py --data_input_path=./LR --data_truth_path=./HR --model=eusr --scales=2 --sleep_ratio=0.0 --save_freq=50 --log_freq=2"
pythonCmdLine = f"{pythonExec} {eusrModelTrainingArguments}"

print("Python command line:")
print(pythonCmdLine)
os.system(pythonCmdLine)
