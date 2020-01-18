
## Getting and Configuring the Project

The **translator-modules-api** package is not yet available through PyPI, thus, to install, clone this repo using git.

```bash
git clone --recursive https://github.com/ncats/translator-modules-api.git

# ... then  enter  into your cloned project repository
cd translator-modules-api
```

Note the use of the *recursive* flag to include defined submodules of the project (in this case, Translator-Modules).

The code is now validated to work only with Python 3.7 only.  We recommend using a **virtualenv** to enforce this.

```
virtualenv -p python3.7 venv
source venv/bin/activate
```

or, alternately, use **python venv** to manage packages and the development environment:

```
python3.7 -m venv venv
source venv/bin/activate
```

To exit the environment, type:

```  
deactivate
```

To reenter, source the _activate_ command again.

Alternately, you can also use use **conda env** to manage packages and the development environment:

```
conda create -n translator-modules-api python=3.7
conda activate translator-modules-api
```

Some IDE's (e.g. PyCharm) may also have provisions for directly creating such a **virtualenv**. This should work fine.

## Installation of Dependencies and Make Modules Visible as Command Line Programs

Make sure that your pip version is 3.7 compliant. 
 
The CWL server is the component you will run.  To installed dependencies, you'll need to first enter the  *server*
subdirectory (from the root *translator-modules-api* project directory) then run the `pip` command:

```bash
cd server

# sometimes better to use the 'python -m pip' version of pip rather than just 'pip'
# to ensure that the proper Python3.7 version of pip is used...
python -m pip install -r requirements.txt .
```

This also has the side effect of ensuring that the software is visible for execution as standalone programs using
the bare module names (without the **.py** file extension; Note that you may have to rerun this command for every new
terminal session on your operating system)

To install the package in "developer" mode (such that code changes are automatically reflected in the local library), 
include the `-e` flag with the `pip` command, namely:

```
python -m pip install -r requirements.txt -e .
```

Developer mode may be necessary to run various debugging processes within Python IDE's such as PyCharms.

# Running the System

## Wes-Server

