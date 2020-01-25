
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

Make sure that your pip version is 3.7 compliant (within your `venv`).

First, install the dependencies for the translator project:

```bash
cd translator-modules

# sometimes better to use the 'python -m pip' version of pip rather than just 'pip'
# to ensure that the proper Python3.7 version of pip is used...
python -m pip install -r requirements.txt -e .
```

Note the use of the `-e` flag to keep changes to the module up-to-date.

The CWL server is the component that is run.  To installed dependencies specifically for that, first enter the *server* 
subdirectory (from the root *translator-modules-api* project directory) then run the `pip` command:

```bash
cd server

# sometimes better to use the 'python -m pip' version of pip rather than just 'pip'
# to ensure that the proper Python3.7 version of pip is used...
python -m pip install -r requirements.txt -e .
```

This also has the side effect of ensuring that the software is visible for execution as standalone programs using
the bare module names (without the **.py** file extension; Note that you may have to rerun this command for every new
terminal session on your operating system)

Developer mode may be necessary to run various debugging processes within Python IDE's such as PyCharms.

# Running the System

## Wes-Server

Open up a terminal 

# (Re-)Generating the Server and Client

The *client* is a direct Python web service client and the *server* is a simple Python Flask server implementation.

The implementation of the Workflow ARA API server and client uses code generation based on the OpenAPI specification 
in the [Trnslator  Modules API YAML](./translator-modules-api.yaml) file.

which is used as a template to generate the code base, which is then wired up by delegation to additional handler code.   
 
The generated and other client/server code is found in the *client* and  *server* subfolders.

By [installing a local copy of the OpenAPI Code Generator](https://openapi-generator.tech/docs/installation), 
modified OpenAPI 3.0 YAML specifications can be processed to recreate the Python client and Python Flask server stubs.
Note that depending on how you install the OpenAPI Code Generator, the manner in which you execute the 
 `openapi-generator` command below will change accordingly (Note that the code generation processes are a bit more 
 streamlined and robust under Linux and OSX than Microsoft Windows).

The code generation commands are generally run from the root project directory directory.  First, one should check 
your new or modified OpenAPI YAML specifications using the _validate_ command:

```bash
openapi-generator validate (-i | --input-spec=)translator-modules-api.yaml
```

If the specifications pass muster, then to recreate the Python Flask *server* stubs, the following command may 
be typed from within the root directory:

```bash
openapi-generator generate --input-spec=translator-modules-api.yaml \
                    --output=server \
                    --generator-name=python-flask \
                    --package-name=cwl_server \
	                --model-package=models \
	                --artifact-version=0.0.1 \
	                --additional-properties=\
"projectName=workflow_cwl_server,packageName=cwl_server,packageVersion=0.0.1,packageUrl=https://github.com/ncats/translator-modules-api/master/server,serverPort=8090"
```

and to recreate the KBA *client* Python access stubs, something along the lines of the following command is typed:

```bash
openapi-generator generate  --input-spec=translator-modules-api.yaml \
                    --output=client \
                    --generator-name=python \
                    --package-name=cwl_client \
	                --model-package=models \
	                --artifact-version=0.0.1 \
	                --additional-properties=\
"projectName=workflow_cwl_client,packageName=cwl_client,packageVersion=0.0.1,packageUrl=https://github.com/ncats/translator-modules-api/tree/master/client"
```

The [OpenAPI 3.0 'generate' command usage](https://openapi-generator.tech/docs/usage#generate) may be consulted
for more specific details on available code generation options and for acceptable program flag abbreviations (here we
used the long form of the flags).

The above commands are also wrapped inside of a `generate2.sh` shell script in the root project directory and 
may also be invoked using the provide Makefile targets.

#### Repairing the Generated Code

In both cases, after generating the code stubs, a developer likely needs to repair the regenerated code a bit.

First, the code stubs must be reconnected to the (delegated) business logic to the REST processing front end as 
required to get the system working again.  Developers can scrutinize recent working releases of the code to 
best understand how the code stubs need to be reconnected or how to add new business logic.

Also, the *server* and *client* subdirectory `README.md`, `setup.py`, `__main__.py` and `requirements.txt` files are 
overwritten by the code generation. These should be restored from the \*-master.\* versions of these files in 
each directory.
 
Finally, check if the `server/cwl_server/__main__.py` file has the correct Identifiers server port (8090).

For good measure, after such extensive rebuilding of the libraries, the 'pip' environment dependencies should also 
be updated, as documented for the client and server, prior to re-testing and using the updated software.
