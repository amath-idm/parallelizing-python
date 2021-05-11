# Code

This folder contains the code for the parallelization examples. Each example uses `model.py`; `model_no_numpy.py` is included as a curious edge case where parallelization is _slower_, for reasons I do not entirely understand! (Something to do with how very long for loops are handled by subprocesses, it seems.)