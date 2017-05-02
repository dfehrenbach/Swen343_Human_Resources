# SWEN 343 Human Resources

## Setup

The following setup instructions should work on most systems, but are meant to work with Ubuntu.

To initialize the project create a file `setup.sh` and run it using `bash setup.sh`.

```
#!/bin/sh

apt-get update
apt-get -y upgrade
apt-get -y install git
apt-get -y install mysql-server
apt-get install libmysqlclient-dev


mkdir working_dir
cd working_dir
wget https://bootstrap.pypa.io/get-pip.py

python get-pip.py
pip install virtualenv

git clone https://github.com/dfehrenbach/Swen343_Human_Resources.git
cd Swen343_Human_Resources

virtualenv Env
source Env/bin/activate
export PYTHONPATH="${PYTHONPATH}:/root/working_dir/Swen343_Human_Resources/hr"
pip install -r requirements.pip

python hr/databasesetup.py
python hr/app.py
```

To reset the machine to the state before the project was created create a file `teardown.sh` and run it using `bash teardown.sh`.

```
#!/bin/sh
 
cd working_dir/Swen343_Human_Resources
 
cd ../..
 
rm -rf working_dir
pip uninstall -y virtualenv
pip uninstall -y pip
 
apt-get -y remove git
```

## Sample Data
Included in the application is a set of sample data that includes two employees and all of the relevant information for them.
