# Semantic Rider
## Milestones
- v0.0.1: First version of tab search plugin
- v0.0.2: Initial version with cleanup popup UI
- v0.0.3: Refactored code, for ease of testing + Extendability (In Progress)
- v0.0.4: TBD

## Running the Program

#### Basic
1. Ensure that your virtual env is setup and activated (assuming you are at base of repo)
   - `virtualenv venv`
   - `source venv/bin/activate`
   - `pip install -r serv/requirements.txt`
2. Ensure that you have fetched all files
   - Create serv/res folder if one is not there, and get `meta_train_*.pkl` and `embed_train_*.pkl` inside res
     - git lfs pull <filename>
3. Please download encoder model from `https://drive.google.com/file/d/1JLTYMaCtY4pkl4oeygXVnk_GxJpOWxKH/view?usp=drive_link` and put it in the server folder.

#### Testing It
1. Ensure that all files `model_file`, `ort_format` file etc are available.
   - You gan git lfs pull the files
   - Or you can get all files by doing `git lfs pull`

2. Now run the program
   - Do `python serv/test_algo.py` from base path, this should give you 90% accuracy
   - This will take about 10-12 hrs if you don't have embed_data and meta_file or your are reindexing, else about 1min

#### Using It
1. 

2. 
