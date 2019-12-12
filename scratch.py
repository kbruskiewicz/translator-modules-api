# WesClient
from glob import glob
from pprint import pprint

import os
import subprocess

import json

PRINT = False

service = {
    "proto":"http",
    "auth": None,
    "host":"localhost:8080"
}

# client = WESClient(service)

translator_modules_location="./translator-modules/"
tml = translator_modules_location

inputs_location = tml+"cwl/data/"
workflows_location = tml+"cwl/workflows/"
# TODO: implement recursive search in the location call. keeping it specialized for now
implementations_location = tml+"ncats/translator/modules/"

def locate_implementation(name, input_type="*", output_type="*", predicate=None):
    if input_type is locate_implementation.__defaults__[0]:
        pass
    if output_type is locate_implementation.__defaults__[1]:
        pass
    if predicate is locate_implementation.__defaults__[2]:
        pass

    return glob(implementations_location + input_type + "/" + output_type + "/" + name + ".py")

def locate_workflows(name, composite="*"):
    if composite is locate_implementation.__defaults__[0]:
        pass

    return glob(workflows_location + composite + "/" + name + ".cwl")

def locate_inputs(identifier, format="yaml"):
    return glob(inputs_location + identifier + "." + format)

TYPES = ["gene", "chemical_substance", "disease", "anatomical_entity", "phenotypic_feature", "cell_line"]
WORKFLOWS = ["wf2", "wf9"]  # how can I generate this dynamically?
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
        if PRINT: pprint(locate_implementation_result1)

        locate_implementation_result2 = locate_implementation(name, "disease")
        if PRINT: pprint(locate_implementation_result2)

        locate_implementation_result3 = locate_implementation(name, "disease", "gene")
        if PRINT: pprint(locate_implementation_result3)

        locate_workflows_result1 = locate_workflows(name)
        if PRINT: pprint(locate_workflows_result1)

        locate_workflows_result2 = locate_workflows(name, "wf2")
        if PRINT: pprint(locate_workflows_result2)

        identifier = "disease"
        locate_inputs_result1 = locate_inputs(identifier)
        if PRINT: pprint(locate_inputs_result1)

        # Use WESClient to run Disease Associated Genes workflow step
    
        # CLI commands for testing purposes
        """
        # os.system("echo hello")
        command_string = 'wes-client --host=localhost:8080 --proto=http --attachments="./translator-modules/cwl/workflows/wf2/disease_associated_genes.cwl,./translator-modules/cwl/data/disease.yaml,./translator-modules/ncats/translator/modules/disease/gene/disease_associated_genes.py" --run ./translator-modules/cwl/workflows/wf2/disease_associated_genes.cwl ./translator-modules/cwl/data/disease.yaml'
        pprint(command_string)
        os.system(command_string)
        """

        attachments = ",".join([locate_implementation_result1[0], locate_workflows_result1[0], locate_inputs_result1[0]])
        diy_command_string = "wes-client --host={} --proto={} --attachments={} --run {} {}".format(service["host"], service["proto"], attachments, locate_workflows_result1[0], locate_inputs_result1[0])
        #os.system(diy_command_string)
        result = subprocess.check_output(diy_command_string, shell=True)
        return json.loads(result)


        #os.system('wes-client --host=localhost:8080 --proto=http --attachments="./translator-modules/cwl/workflows/wf2/disease_associated_genes.cwl,./translator-modules/cwl/data/disease.yaml,{}" --run ./translator-modules/cwl/workflows/wf2/wf2.cwl ./translator-modules/cwl/data/disease.yaml'.format(",".join([ ])))


def tests2():
    name = "wf2"
    if name in WORKFLOWS:
        """
        if name is in workflows, we need to mount ALL of the files inside of the folder, AND their corresponding symbols

        so: get all the symbols in the dir with the workflow
        """
        workflow_location = locate_workflows(name)[0]
        workflow_dir = "/".join(workflow_location.split("/")[0:-1])+"/"
        pprint(workflow_location)
        pprint(workflow_dir)

        workflow_dir_abs = os.path.abspath(workflow_dir)

        symbols = []
        workflow_locations = []
        for root, dirs, files in os.walk(workflow_dir_abs, topdown=False):
             for filename in files:
                  #index = files.index(name+".cwl")
                  #files[index].pop()
                  #if filename != name+".cwl":
                  symbols += [filename.split(".cwl")[0]]
                  print filename.split(".cwl")[0]
                  workflow_locations += [root + "/"  + filename]
        print(symbols)
        print(workflow_locations)
        
        implementation_locations = []
        for symbol in symbols:
            print implementation_locations
            implementation_locations += locate_implementation(symbol)
        
        attachments = implementation_locations + ["./translator-modules/cwl/workflows/wf2/wf2.cwl", "./translator-modules/cwl/data/disease.yaml"] + workflow_locations
        command_string = 'wes-client --host=localhost:8080 --proto=http --attachments="./translator-modules/cwl/workflows/wf2/disease_associated_genes.cwl,./translator-modules/cwl/data/disease.yaml,{}" --run ./translator-modules/cwl/workflows/wf2/wf2.cwl ./translator-modules/cwl/data/disease.yaml'.format(",".join(attachments))
        pprint(command_string)
        os.system(command_string)


#tests2()
tests()

