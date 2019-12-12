import cwlgen
from glob import glob
from pprint import pprint
import os
import json
import subprocess

TYPES = ["gene", "chemical_substance", "disease", "anatomical_entity", "phenotypic_feature", "cell_line"]
WORKFLOWS = ["wf2", "wf9"]  # how can I generate this dynamically?

"""
single input || multi input -> input map? kwargs of lists of values
scatter || not scatter -> flag | size of each input
single step || multi-step -> symbol:str to paths of scripts and ||
"""

# homoiconic (more specific)
"""
{
    workflow_name: str(),
    inputs: dict(), # dict -> list
    # validate whether the inputs given correspond to the outputs needed based on the CWL file
    # compute whether it is multi step off of the CWL file
    # computer whether it is scatter based on the inputs
        # ensure integrity of inputs that each element in 
}
"""

# general
"""
{
    workflow_seq: tuple(), # tuple -> list -> str
    inputs: dict()  # dict -> list
}
"""

service = {
    "proto": "http",
    "auth": None,
    "host": "localhost:8080"
}

translator_modules_dir = "../translator-modules/"
inputs_dir = translator_modules_dir + "cwl/data/"
workflows_dir = translator_modules_dir + "cwl/workflows/"
implementations_dir = translator_modules_dir + "ncats/translator/modules/"

def find_or_make_input():
    pass

def handle_run_workflow(full_task_payload):

    """
    Failure cases:
    - Syntactic
        =>
    - Semantic
        =>
    """
    name = full_task_payload.workflow_name
    input_name = full_task_payload.input_mappings

    workflow = os.path.abspath(locate_workflows(name)[0])
    implementation = os.path.abspath(locate_implementation(name)[0])
    inputs = os.path.abspath(locate_inputs(input_name)[0])
    attachments = ",".join([implementation, workflow, inputs])
    wes_client_process_request = "wes-client --host={} --proto={} --attachments={} --run {} {}" \
        .format(service["host"], service["proto"], attachments, workflow, inputs)

    result = subprocess.check_output(wes_client_process_request, shell=True)
    result_json = json.loads(result)
    result_dict = dict(result_json)

    return result_dict

def handle_info_workflow(workflow_name):
    pass

def translate_payload(payload):
    """
    in: inputs -> inputs specification in python
    wf: [ symbol ] -> input symbols + steps + ?? + ??
    cwl specification: wf * in -> file -> path

    wes_client(cwl_specification)

    """
    pass

def resolve_resources():
    pass

def run_input(payload):
    task_resources = translate_payload(payload)
    pass

def run_workflow_int(int, payload):
    """
    1) get integer
    2) map integer to workflow in translator modules
    3) read from translator modules all the symbols within the workflow | if steps
       - approach 1: read off the file
         - this approach is bad because requires many searches?
           - optimize by single traverse
           - build index
       - approach 2: organize directories
         - this approach is bad because many to many correspondence of multi-workflows to steps?
           - optimize by redundancy?
           - build index?
    """
    pass

def run_workflow_symbol(symbol, payload):
    pass

def run_type_type_sub_symbol(inType, outType, symbol, payload):
    # scope is bounded by the API
    # Modify payload to be complete
    pass

def locate_implementation(name, input_type="*", output_type="*", predicate=None):
    if input_type is locate_implementation.__defaults__[0]:
        pass
    if output_type is locate_implementation.__defaults__[1]:
        pass
    if predicate is locate_implementation.__defaults__[2]:
        pass

    return glob(implementations_dir + input_type + "/" + output_type + "/" + name + ".py")


def locate_workflows(name, composite="*"):
    if composite is locate_implementation.__defaults__[0]:
        pass

    return glob(workflows_dir + composite + "/" + name + ".cwl")


def locate_inputs(identifier, format="yaml"):
    return glob(inputs_dir + identifier + "." + format)





def tests():
    name = "disease_associated_genes"

    if name in WORKFLOWS:
        """
        if name is in workflows, we need to mount ALL of the files inside of the folder, AND their corresponding symbols

        so: get all the symbols in the dir with the workflow
        """
        workflow_location = locate_workflows(name)
        os.listdir(workflow_location)

    else:

        locate_implementation_result1 = locate_implementation(name)
        pprint(locate_implementation_result1)

        locate_implementation_result2 = locate_implementation(name, "disease")
        pprint(locate_implementation_result2)

        locate_implementation_result3 = locate_implementation(name, "disease", "gene")
        pprint(locate_implementation_result3)

        locate_workflows_result1 = locate_workflows(name)
        pprint(locate_workflows_result1)

        locate_workflows_result2 = locate_workflows(name, "wf2")
        pprint(locate_workflows_result2)

        identifier = "disease"
        locate_inputs_result1 = locate_inputs(identifier)
        pprint(locate_inputs_result1)

        # Use WESClient to run Disease Associated Genes workflow step

        # CLI commands for testing purposes
        os.system("echo hello")
        command_string = 'wes-client --host=localhost:8080 --proto=http --attachments="./translator-modules/cwl/workflows/wf2/disease_associated_genes.cwl,./translator-modules/cwl/data/disease.yaml,./translator-modules/ncats/translator/modules/disease/gene/disease_associated_genes.py" --run ./translator-modules/cwl/workflows/wf2/disease_associated_genes.cwl ./translator-modules/cwl/data/disease.yaml'
        # pprint(command_string)
        # os.system(command_string)

        attachments = ",".join([locate_implementation_result1[0], locate_workflows_result1[0], locate_inputs_result1[0]])
        diy_command_string = "wes-client --host={} --proto={} --attachments={} --run {} {}".format(service["host"],
                                                                                                   service["proto"],
                                                                                                   attachments,
                                                                                                   locate_workflows_result1[
                                                                                                       0],
                                                                                                   locate_inputs_result1[
                                                                                                       0])
        os.system(diy_command_string)

        # print(locate)

        # os.system('wes-client --host=localhost:8080 --proto=http --attachments="./translator-modules/cwl/workflows/wf2/disease_associated_genes.cwl,./translator-modules/cwl/data/disease.yaml,{}" --run ./translator-modules/cwl/workflows/wf2/wf2.cwl ./translator-modules/cwl/data/disease.yaml'.format(",".join([ ])))


def tests2():
    name = "wf2"
    if name in WORKFLOWS:
        """
        if name is in workflows, we need to mount ALL of the files inside of the folder, AND their corresponding symbols

        so: get all the symbols in the dir with the workflow
        """
        workflow_location = locate_workflows(name)[0]
        workflow_dir = "/".join(workflow_location.split("/")[0:-1]) + "/"
        pprint(workflow_location)
        pprint(workflow_dir)

        workflow_dir_abs = os.path.abspath(workflow_dir)

        symbols = []
        workflow_locations = []
        for root, dirs, files in os.walk(workflow_dir_abs, topdown=False):
            for filename in files:
                # index = files.index(name+".cwl")
                # files[index].pop()
                # if filename != name+".cwl":
                symbols += [filename.split(".cwl")[0]]
                print(filename.split(".cwl")[0])
                workflow_locations += [root + "/" + filename]
        print(symbols)
        print(workflow_locations)

        implementation_locations = []
        for symbol in symbols:
            print(implementation_locations)
            implementation_locations += locate_implementation(symbol)

        attachments = implementation_locations + ["./translator-modules/cwl/workflows/wf2/wf2.cwl",
                                                  "./translator-modules/cwl/data/disease.yaml"] + workflow_locations
        command_string = 'wes-client --host=localhost:8080 --proto=http --attachments="./translator-modules/cwl/workflows/wf2/disease_associated_genes.cwl,./translator-modules/cwl/data/disease.yaml,{}" --run ./translator-modules/cwl/workflows/wf2/wf2.cwl ./translator-modules/cwl/data/disease.yaml'.format(
            ",".join(attachments))
        pprint(command_string)
        os.system(command_string)

