from flask import Flask
from wes_client import WESClient
import glob

app = Flask(__name__)

service = {
    "proto":"http",
    "auth": None,
    "host":"localhost:8080"
}
client = WESClient(service)

translator_modules_location="./translator-modules/"
tml = translator_modules_location

inputs_location = tml+"cwl/data/"
workflows_location = tml+"cwl/workflows/*/"
# TODO: implement recursive search in the location call. keeping it specialized for now
implementations_location=tml+"ncats/translator/modules/*/*/"

@app.route('/runs/workflows/<name>')
def run_workflow(name):
    """
    302: id is locatable, can continue call
    404: no id located
    """

    # seeking a workflow actually means seeking its CWL specification (a 'step') and its operation
    # as a part of developing new workflow steps, both CWL step and operation share a token name (but not and extension. They are also located in two different places. 
    # We search in both.

    # <'locate' calls, subsequently, returning truthy values for checking?
    workflow = locate_workflows(name)
    implementation = locate_implementations(name)

    return workflow, implementation

    """
    # ASSERT: are these uniques?
    if len(workflow) > 1 or len(implementation) > 1:
        return 500, "Can you be more specific? there was {} workflow/s and {} implementation/s for given {}".format(len(workflow), len(implementations), name)
    elif len(workflow) == 0 or len(implementation) == 0:
       return 500, "I'm not getting both a workflow and an implementation for {}".format(name)
    else:
       return 200, workflow, implementation
    """

    # If we find both the workflow name and its corresponding operation then we can resolve the workflow.
    # The workflow is linked to directly, the operation is used as an attachment for a call to be sent to
    # wes-server. After this delegation we wait for an input before sending off the response (what's returned is a prepared object which can be called again subsequently?)
 
    # <utils call, `build_wes_response`?>


    # return id

@app.route('runs/workflows/<name>/<input>')
def run_workflow_input(name, input):
    # POST call with inputs

    # inputs must actually become valid JSON that can be passed to a CWL execution

    return 200, run_workflow(name), input

# TODO: maybe a call where the app route is homoiconic to the directory structure of the location of workflows/modules
# make this guarantee and we can simplify these calls
@app.route('runs/workflows/<inputType>')
def steps_by_it(inputType):
    """
    Modifies workflow and implementation search by inputType token as dir
    """
    pass

@app.route('runs/steps/<inputType>/<outputType>'):
def steps_by_iot(inputType, outputType):
   """
   Modifies workflow and implementation search by inputType and outputType token as dir
   """
   pass

@app.route('runs/steps/<inputType>/<outputType>/<predicate>'):
def steps_by_iotp(inputType, outputType, predicate):
    """
    Resolves to a precise workflow step and implementation through inputType, outputType, and predicate.
    """
    pass

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)

def build_inputs():
    pass

def locate_inputs():
    pass

def locate_workflows(name):
    # search through the given workflows directory to find a workflow file with name `name`,
    # then return a list containing Paths to all the workflow files that match
    # return an empty list otherwise...

    # TODO: once we get to the point where we want to generalize, we'll use more wildcards
    # or add wildcards dynamically

    return glob.glob(workflows_location+name+".cwl")

def locate_implementation(name):
    # search throught the given workflows directory to find a workflow file with name `name`,
    # then return a list containig Paths to all the workflow files that match
    # return an empty list otherwise...

    # TODO: once we get to the point where we want to generalize, we'll use more wildcards
    # or add wildcards dynamically

    return glob.glob(implementations_location+name+".py")

if __name__ == '__main__':
    app.run()
