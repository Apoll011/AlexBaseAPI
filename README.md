# Alex Base Api

This repository contains the source code to run the Alex Base Api. Witch is the server that handles the heaviest request from my Home assitant Alex.

# Instalation
##Install VirtualEnv
### MacOS
Install VirtualEnv
```bash
>>>brew install virtualenv
```
### Win
```bash
>>>pip install virtualenv
```
Create a 3.8 python virtual env
```bash
>>>virtualenv /path/to/your/python3.8 baseApi
```
It has to be 3.8 or the snips wont work.


```bash
>>>source ./baseApi/bin/activate
>>>pip install requirements.txt
>>>snips-nlu download <lang>
```
For more info on snips see [Snips Instalation Guide](https://snips-nlu.readthedocs.io/en/latest/installation.html)

# Usage

The first time is recomended to train snips so try `python main.py -t` or `python main.py --train`. There is alredy a pre built set of sentences in 
```bash
nano features/intent_recognition/snips/data/en.yaml
```

After that you can run `python main.py -s` to start the program or use the flag `--list-routes` to list all the possible api routes. The Api Code and api routes are inpired in Flask but they dont use then so they might not be as secure.