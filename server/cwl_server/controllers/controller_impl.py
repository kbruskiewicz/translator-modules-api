import logging
logger = logging.getLogger(__name__).setLevel(logging.DEBUG)

from glob import glob
from pprint import pprint

import json
import yaml
import uuid

import os
import subprocess

DEBUG = True


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

service = {
    "proto": "http",
    "auth": None,
    "host": "localhost:8080"
}

# translator_modules_dir must be absolute path
ctrl_path = os.path.abspath(__file__)
ctrl_dir = os.path.dirname(ctrl_path)
translator_modules_dir = os.path.abspath(ctrl_dir+"../../../../translator-modules")+"/"

inputs_dir = translator_modules_dir + "cwl/data/"
workflows_dir = translator_modules_dir + "cwl/workflows/"
implementations_dir = translator_modules_dir + "ncats/translator/modules/"


def find_or_make_input():
    """
    in: string OR array OR object
    out: input file and input directory
    """
    pass


def make_input(raw_inputs, format="yaml"):
    """
    in: list of key-value pairs
    out: json file or yaml file, and file location
    """

    file_name = uuid.uuid4() + "." + format
    data = None
    if type(raw_inputs) is list:
        """
        CASE: array of key-value pairs (indexed by either {[key]:<value>}? or by {"key":<key>, "value": <value>}?)
        """
        pass
    elif type(raw_inputs) is str:
        """
        CASE: string of equalities
        """
        pass
    elif type(raw_inputs) is dict:
        data = raw_inputs

    file_location = inputs_dir + file_name
    with open(file_location, "x+") as inputs_file:

        assert (type(data) is dict)

        if format is "yaml":
            yaml.dump(data, inputs_file)
            assert (yaml.safe_load(inputs_file) == data)
        elif format is "json":
            json.dump(data, inputs_file)
            assert (json.load(inputs_file) == data)

        return inputs_file, file_location


def validate_input():
    # TODO: validation criterion for inputs?
    """
    Semantic Validity
    Syntactic Validity
    Structural Valdity
    Schema Consistency

    cf correspondence with James Eddy on Sun, Jun 30, 2019, 11:13 PM via GMail
    """
    pass


def validate_input_against_schema(worklow_cwl_inst):
    """
    in: instance of a cwl workflow in memory (equivalent to type CommandLineTool e.g.)
    out: boolean

    steps:
    1) get the inputs used by the cwl spec
    2) see if the json or yaml inputs have all the necessary keys, of the necessary types
    3) return true if they do, false if they don't
    """
    pass


def handle_run_workflow(full_task_payload):
    name = full_task_payload.workflow_name
    input_name = full_task_payload.input_mappings

    result_dict = start_workflow("disease_associated_genes", "disease")
    pprint(result_dict)
    status_code: int
    if result_dict is not None:
        status_code = 200
    elif result_dict is None:
        status_code = 500

    # mimics output signature of an openapi controller call
    # DONE: must adhere to the output shape of WorkflowResults
    return translate_results_to_workflow_results(result_dict), status_code

def handle_info_workflow(workflow_name):
    pass


from openapi_server.models import WorkflowResults
from openapi_server.models import TaskId
import re

def translate_results_to_workflow_results(results_dict):
    """
    Goal: convert the results from wes-client into a WorkflowResults object.

    Example Input + Input Shape:
    {'disease_list': {'basename': 'disease_associated_genes.records.json',
                      'checksum': 'sha1$eaa1086aa296e369355577f7ecb06497001ac40e',
                      'class': 'File',
                      'location': 'file:///Users/kenneth/workflows/e89dc709536d4fc2b80b104462e1abb4/outdir/disease_associated_genes.records.json',
                      'path': '/Users/kenneth/workflows/e89dc709536d4fc2b80b104462e1abb4/outdir/disease_associated_genes.records.json',
                      'size': 6488}}
    """
    if results_dict:
        results_body = results_dict[list(results_dict.keys())[0]]
        results_path = results_body['path']
        pprint(results_path)
        # TODO: always assumes that the location is id-specific, is this true, or does it change with runner configuration?
            # I don't want to have to deal with coupling with the config just to get the task-id
            # How can I get the client to emit this information?
        # TODO: is the task id returned by wes-client a uuid?
        # TODO: capture the task_id of WorkflowResults as type TaskID?
        # TODO: generalize the match!
        # TODO: always assumes a succesful match!
        match = re.search(r'\/workflows/(\w+)\/outdir\/', results_body['path'])
        results_taskid = None
        if match:
            results_taskid = match.group(1)  # nota bene! the zeroth group is the total matching string, not the capture group

        return WorkflowResults(task_id=results_taskid, results_path=results_path)
    return "No Workflow Results"

from openapi_server.models import FullTaskPayload
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


from functools import reduce


def make_command(workflow, implementation, inputs):
    try:
        assert len(workflow) > 0
        assert len(implementation) > 0
        assert len(inputs) > 0

        attachments_list = list(map(os.path.abspath, reduce(list.__add__, [implementation, workflow, inputs])))
        attachments_str = ",".join(attachments_list)
        wes_client_process_request = "wes-client --host={} --proto={} --attachments={} --run {} {}" \
            .format(service["host"], service["proto"], attachments_str, os.path.abspath(workflow[0]),
                    os.path.abspath(inputs[0]))
        return wes_client_process_request
    except Exception:
        return None


def symbols_from_steps_of(workflow_location_list):
    try:
        assert len(workflow_location_list) > 0
        with open(os.path.abspath(workflow_location_list[0]), "r") as file:
            # Can I find out if a workflow has steps?
            wf_cwl = yaml.load(file)
            if 'steps' in wf_cwl:
                # If a workflow has steps, can I find out what symbols those steps are named for?
                return list(wf_cwl["steps"].keys())
            else:
                return []
    except Exception as e:
        logger.error(str(e))
        return []


def start_workflow_step(step_name, input_identifier):
    workflow_location = locate_workflows(step_name)
    implementation_location = locate_implementation(step_name)
    input_location = locate_inputs(input_identifier)
    command_str = make_command(workflow_location, implementation_location, input_location)

    try:
        result = subprocess.check_output(command_str, shell=True)
        result_json = json.loads(result)
        result_dict = dict(result_json)
        return result_dict
    except Exception as e:
        logger.error(str(e))
        return None


def start_workflow_composite(name, input_identifier):
    workflow_location = locate_workflows(name)
    workflow_locations = workflow_location + []

    input_location = locate_inputs(input_identifier)
    symbols = symbols_from_steps_of(workflow_location)

    if name in WORKFLOWS:
        workflow_dir = "/".join(workflow_location[0].split("/")[0:-1]) + "/"
        workflow_dir_abs = os.path.abspath(workflow_dir)
        for root, dirs, files in os.walk(workflow_dir_abs, topdown=False):
            for filename in files:
                symbols += [filename.split(".cwl")[0]]
                workflow_locations += [root + "/" + filename]
    else:
        # If I can find out what symbols those steps have, can I see if they have equivalent workflows and implementations?
        for symbol in symbols:
            maybe_workflow_location = locate_workflows(symbol)
            if len(maybe_workflow_location) > 0:
                workflow_locations += maybe_workflow_location

    implementation_locations = []
    for symbol in symbols:
        implementation_locations += locate_implementation(symbol)

    command_str = make_command(workflow_locations, implementation_locations, input_location)

    try:
        result = subprocess.check_output(command_str, shell=True)
        result_json = json.loads(result)
        result_dict = dict(result_json)
        return result_dict
    except Exception:
        return None


def start_workflow(name, input_identifier):
    workflow_location = locate_workflows(name)
    symbols = symbols_from_steps_of(workflow_location)
    if len(symbols) > 0:
        # TODO: optimize the subsequent calls on `symbol`
        return start_workflow_composite(name, input_identifier)
    else:
        return start_workflow_step(name, input_identifier)


def is_composite_workflow(spec_filename):
    """
    Check if the workflow spec is composite or not
    - APPROACH 1: Extrinsic
        - Does it obey the location-and-filename conventions?
        - PROS: faster...? maybe?
        - CONS: unscalable, enforced by humans
    - APPROACH 2: Intrinsic
        - Does the CWL specs contain steps that we have?
        - PROS: structural on the spec - conventions enforced by CWL rather than ourselves
        - CONS: file operation, not necessarily a workflow
    """
    # TODO: could I just check if the key exists or not rather than finding symbols length? would that be faster?
    return len(symbols_from_steps_of(spec_filename)) > 0


def test1():
    name = "disease_associated_genes"
    input_name = "disease"
    pprint(start_workflow_step(name, input_name))


def test2():
    name = "wf2"
    input_name = "disease"
    pprint(start_workflow_composite(name, input_name))


import cwlgen
import cwltool


def access_cwl(cwl_path):
    assert True  # TODO guarantee it's a CWL file
    with open(cwl_path, "r") as cwl_file:
        return yaml.safe_load(cwl_file)


def test3():
    """
    Manipulating CWL Specs for use in the API

    SCENARIOS:
    - Finding all the attachments required for a given workflow input (OK)
    - Constructing a custom multi-step worfklow from a sequence of resolved step data (OK)
    """

    # CASE: extracting symbols from existing multi-step workflows
    # Can I find out if a workflow has steps?
    # If a workflow has steps, can I find out what symbols those steps are named for?
    # If I can find out what symbols those steps have, can I see if they have equivalent workflows and implementations?
    # QED If I can do all these things, then I can find all of the attachments required for a multi-step workflow

    # APPROACH 1: Treat it as a YAML Document
    maybe_wf2_location = locate_workflows("wf2", "wf2")
    step_list = []
    if len(maybe_wf2_location) > 0:

        with open(os.path.abspath(maybe_wf2_location[0]), "r") as file:
            # Can I find out if a workflow has steps?
            wf2_cwl = yaml.load(file)
            if 'steps' in wf2_cwl:
                # If a workflow has steps, can I find out what symbols those steps are named for?
                step_names = list(wf2_cwl["steps"].keys())
                # If I can find out what symbols those steps have, can I see if they have equivalent workflows and implementations?
                for step_name in step_names:
                    maybe_workflow_step = locate_workflows(step_name)
                    maybe_implementation_step = locate_implementation(step_name)
                    if len(maybe_workflow_step) > 0 and len(maybe_implementation_step) > 0:
                        spec_input_pair = (step_name, maybe_workflow_step[0], maybe_implementation_step[0])
                        step_list.append(spec_input_pair)

    # CASE: creating a workflow from given implementations
    # Let's create WF2 from scratch (assuming we've assembled all the symbols we wanted)
    assert len(step_list) > 0

    # APPROACH 1: YAML, again
    # PROBLEM: How do we know how to chain together the different workflows?
    # The key issue is the ambiguity of order
    # WF2 is parallel
    # In the parallel case, we can maybe default to the first
    # WF9 is sequential
    # In the sequential case, we can maybe default to the order
    # The second issue is ambiguity of interface
    # ERROR 1 (FN): Different tokens, same information and type
    # ERROR 2 (FP): Same tokens, different information or type
    # This implies that a third piece of information is required -- the input token -- for at least the sequential case
    # TODO: PROBLEM: how does this work in the parallel case?
    # Defaults based on the order of inputs specified would be unsafe and counterintuitive to debug

    # (1) Find the token names of workflow steps
    # this is a constant because we assume that worklows use the same input type and token name
    # at the very least we would hope for this in the parallel case

    # CONVENTION: Let it be the case (if it's not already) that there should be only one unbound parameter
    # (including a parameter with no defaults) so that chaining/composing modules can be full specified upto values
    # that are optional yet provided defaults. It would ensure requiring no external info or user input for generating
    # the multi-step CWL spec to succeed.
    # TODO: this convention is invalidated by at least `disease_associated_genes`!

    INPUT_TOKEN = "input_genes"  # how to make this computable?
    OUTPUT_TYPE = "File"

    gen_wf2_dict = {
        "cwlVersion": "v1.0",
        "class": "Workflow"
    }

    # (2) Process the initial steps
    # BASE CASE for establishing multi-step CWL workflow
    # DISTINCTION: Input to step equal to itself, *rather than* a previous step
    # I: Establish multi-workflow inputs === initial step inputs
    # 1. Access the CWL file corresponding to the initial step
    # 2. Parse the input segment of the CWL file - copy over
    # II: Establish multi-workflow step as runnable
    # 1. Make step entry from step token name
    # 2. Add a run entry equivalent to step cwl filename
    # e.g. "run: <token>.cwl"
    # 3. Map inputs to workflow inputs (or input of another step)
    # Initial step inputs correspond to initial workflow inputs in symbolic name
    # e.g. make "disease_list: disease_list" if disease_list is set as an input in workflow being generated
    # Step inputs in general correspond to tokens labeling outputs within CWL spec of appropriate step
    # Non-initial step inputs correspond to the outputs of a previous step
    # If parallel (collection is Sum-type?), then equal to output of initial input
    # CONVENTION: It is possible to resolve the ambiguity of multiple inputs by
    # If sequential (collection is Product-type?), then equal to output of previous step
    # PROBLEM: How do we resolve which interface parameters correspond to output of previous step?
    # It would have to be clarified on a step-by-step basis
    # This implies extra data would have to be equipped onto the s-exp (in it, or externally "on"/"onto" it?)
    # 4. Establish outputs to emit from CWL step using CWL file
    # Why be explicit here? imagine having multiple outputs from the CWL file
    # III: Establish outputs
    # 1. Access the CWL file corresponding to the initial step
    # 2. Parse the output segment - copy token - change type to File from i.e. stdout
    # `type` is changed to File because that appears to be the singular means for composing workflow steps
    # 3. Establish `outputSource` as equal to step token name

    # I don't like these expressions, but Python doesn't create unknown keys on assignment (unlike Javascript)
    gen_wf2_dict["steps"] = {}
    gen_wf2_dict["inputs"] = {}
    gen_wf2_dict["outputs"] = {}

    init_step = step_list[0]
    init_step_name = init_step[0]
    init_step_cwl = access_cwl(init_step[1])
    # initialize the step entry with the known values of the step entry if not exists, else return new step entry
    # (with `in` because we have to handle it in the loop) subsequent initializations will preserve the content of
    # the previous loop, since after the first `get` the value will already exist (and not
    # reinitialize to the blank version of the step.) `update` is used a the way of extending this with multiple a
    gen_wf2_dict["steps"][init_step_name] = gen_wf2_dict["steps"].get(init_step_name, {"in": {}})
    for input_key in init_step_cwl["inputs"].keys():
        # NOTA BENE: this step, where `in` is defined, is affected by the induction
        # BASE CASE: steps are equal to itself
        # DISTINCTION: steps are equal to the outputs of previous steps
        gen_wf2_dict["steps"][init_step_name]["in"].update({input_key: input_key})
        gen_wf2_dict["inputs"][input_key] = {
            "type": init_step_cwl["inputs"][input_key]["type"]
        }
    workflow_return_value_reference_keys = list(init_step_cwl["outputs"].keys())
    pprint(workflow_return_value_reference_keys)
    gen_wf2_dict["steps"][init_step_name]["run"] = init_step_name + ".cwl"
    gen_wf2_dict["steps"][init_step_name]["out"] = [workflow_return_value_reference_keys[0]]
    gen_wf2_dict["outputs"] = {
        workflow_return_value_reference_keys[0]: {
            "type": "File",
            "outputSource": init_step_name + "/" + workflow_return_value_reference_keys[0]
        }
    }
    if DEBUG: pprint(gen_wf2_dict)

    # generalize the above logic
    # we must generalize across all of the step's token names
    SEQUENTIAL = False
    PARALLEL = True

    gen_dict = {
        "cwlVersion": "v1.0",
        "class": "Workflow"
    }
    gen_dict["steps"] = {}
    gen_dict["inputs"] = {}
    gen_dict["outputs"] = {}
    i = 0
    for step in step_list:
        assert i < len(step_list)
        step_name = step[0]
        step_cwl = access_cwl(step[1])
        for input_key in step_cwl["inputs"].keys():
            # initialize the step entry with the known values of the step entry if not exists, else return new step entry
            # (with `in` because we have to handle it in the loop) subsequent initializations will preserve the content of
            # the previous loop, since after the first `get` the value will already exist (and not
            # reinitialize to the blank version of the step.) `update` is used a the way of extending this with multiple a
            gen_dict["steps"][step_name] = gen_dict["steps"].get(step_name, {"in": {}})

            # NOTA BENE: this step, where `in` is defined, is affected by the induction
            # BASE CASE: steps are equal to itself when tracking the init step
            # (the init step is the first one in the current step_list)
            # DISTINCTION: steps are equal to the outputs of previous steps
            if i <= 0:
                for input_key in init_step_cwl["inputs"].keys():
                    gen_dict["steps"][step_name]["in"].update({input_key: input_key})
                    gen_dict["inputs"][input_key] = {
                        "type": step_cwl["inputs"][input_key]["type"]
                    }
            elif i > 0:
                if SEQUENTIAL:
                    assert not PARALLEL
                    # In the sequential case, equal to the output of the previous case
                    # TODO: doing a lot of file access here... could insert a form of memoization?
                    prev_step_cwl = access_cwl(step_list[i - 1][1])
                    # remember that the assumption here is that all Translator Modules produce a single output
                    output_key = step_list[i - 1][0] + "/" + list(prev_step_cwl["outputs"].keys())[0]
                    gen_dict["steps"][step_name]["in"].update({
                        INPUT_TOKEN: output_key,
                        "type": OUTPUT_TYPE
                    })
                elif PARALLEL:
                    assert not SEQUENTIAL
                    # In the parallel case, equal to the output of the initial case
                    # TODO: doing a lot of file access here... could insert a form of memoization?
                    prev_step_cwl = access_cwl(step_list[0][1])
                    # remember that the assumption here is that all Translator Modules produce a single output
                    output_key = step_list[0][0] + "/" + list(prev_step_cwl["outputs"].keys())[0]
                    gen_dict["steps"][step_name]["in"].update({
                        INPUT_TOKEN: output_key,
                        "type": OUTPUT_TYPE
                    })

        workflow_return_value_reference_keys = list(step_cwl["outputs"].keys())
        gen_dict["steps"][step_name]["run"] = step_name + ".cwl"
        gen_dict["steps"][step_name]["out"] = [workflow_return_value_reference_keys[0]]
        gen_dict["outputs"].update({
            workflow_return_value_reference_keys[0]: {
                "type": "File",
                "outputSource": step_name + "/" + workflow_return_value_reference_keys[0]
            }
        })
        i += 1

    if DEBUG: pprint(gen_dict)

    # Write to file

    # CASE: extracting inputs from a workflow to server as basis for schema check against inputs to be served


def test31():
    """
    - Modifying a workflow specification to scatter on inputs
        - APPROACH: Scatter by default?
        - APPROACH: Inject scattering at runtime?
    - Constructing temporary files for inputs and workflows
        - Temporary working directory?
            - Temporary CWL files (for multi-step)?
            - Temporary input file?
            - Temporary CWL files (for scatter)?
    - Validating an input payload, that it can actually satisfy a workflow step
        - APPROACH: Schema-based?
    """

    # CASE: Scattering!
    # What triggers scattering?
    # How does a workflow know to scatter, and on what values?
    # STEP 1: The CWL specification must know that it must scatter
    # STEP 2: The inputs must have one or more entries for the scatterable value

    pass


def make_cwl(step_list):
    INPUT_TOKEN = "input_genes"  # how to make this derived?
    OUTPUT_TYPE = "File"

    # generalize the above logic
    # we must generalize across all of the step's token names
    SEQUENTIAL = False
    PARALLEL = True

    init_step = step_list[0]
    init_step_name = init_step[0]
    init_step_cwl = access_cwl(init_step[1])

    gen_dict = {
        "cwlVersion": "v1.0",
        "class": "Workflow"
    }
    gen_dict["steps"] = {}
    gen_dict["inputs"] = {}
    gen_dict["outputs"] = {}
    i = 0
    for step in step_list:
        assert i < len(step_list)
        step_name = step[0]
        step_cwl = access_cwl(step[1])
        for input_key in step_cwl["inputs"].keys():
            # initialize the step entry with the known values of the step entry if not exists, else return new step entry
            # (with `in` because we have to handle it in the loop) subsequent initializations will preserve the content of
            # the previous loop, since after the first `get` the value will already exist (and not
            # reinitialize to the blank version of the step.) `update` is used a the way of extending this with multiple a
            gen_dict["steps"][step_name] = gen_dict["steps"].get(step_name, {"in": {}})

            # NOTA BENE: this step, where `in` is defined, is affected by the induction
            # BASE CASE: steps are equal to itself when tracking the init step
            # (the init step is the first one in the current step_list)
            # DISTINCTION: steps are equal to the outputs of previous steps
            if i <= 0:
                for input_key in init_step_cwl["inputs"].keys():
                    gen_dict["steps"][step_name]["in"].update({input_key: input_key})
                    gen_dict["inputs"][input_key] = {
                        "type": step_cwl["inputs"][input_key]["type"]
                    }
            elif i > 0:
                if SEQUENTIAL:
                    assert not PARALLEL
                    # In the sequential case, equal to the output of the previous case
                    # TODO: doing a lot of file access here... could insert a form of memoization?
                    prev_step_cwl = access_cwl(step_list[i - 1][1])
                    # remember that the assumption here is that all Translator Modules produce a single output
                    output_key = step_list[i - 1][0] + "/" + list(prev_step_cwl["outputs"].keys())[0]
                    gen_dict["steps"][step_name]["in"].update({
                        INPUT_TOKEN: output_key,
                        "type": OUTPUT_TYPE
                    })
                elif PARALLEL:
                    assert not SEQUENTIAL
                    # In the parallel case, equal to the output of the initial case
                    # TODO: doing a lot of file access here... could insert a form of memoization?
                    prev_step_cwl = access_cwl(step_list[0][1])
                    # remember that the assumption here is that all Translator Modules produce a single output
                    output_key = step_list[0][0] + "/" + list(prev_step_cwl["outputs"].keys())[0]
                    gen_dict["steps"][step_name]["in"].update({
                        INPUT_TOKEN: output_key,
                        "type": OUTPUT_TYPE
                    })

        workflow_return_value_reference_keys = list(step_cwl["outputs"].keys())
        gen_dict["steps"][step_name]["run"] = step_name + ".cwl"
        gen_dict["steps"][step_name]["out"] = [workflow_return_value_reference_keys[0]]
        gen_dict["outputs"].update({
            workflow_return_value_reference_keys[0]: {
                "type": "File",
                "outputSource": step_name + "/" + workflow_return_value_reference_keys[0]
            }
        })
        i += 1

    return gen_dict


def test4():
    """
    Representations of queries to the Workflow ARA

    SCENARIOS:
    - CASE 1: Command Line.
        We want to offer a series of arguments to a command that feels like rudimentary natural language, particularly
        English (which is the language that the Biolink Model is documented in).

        Solving this problem will make using the Translator Workflow system more accessible than it otherwise would have
        been if the primary mode of interaction was through CWL specifications. Furthermore, certain subsystems must be
        created for CLI-based queries, which can be reused for more complicated forms of input (such as GUI diagrams),
        while letting us keep our initial scope manageable.

        Our parse structure will be subject-verb-object, which corresponds in Biolink to a relation of Category-Slot-Category.
        TODO: as of December 17 2019 we'll restrict ourselves to not dealing with attribute specifications (like thresholds of
            association relations) for now, but should pick this up towards middle-end of January

        Composition of verbs involves overloading on right-category of the left-most slot, to the left-category of the right-most slot,
            i.e. if `a`, `b`, and `c` are categories, then aPbQc where `P/Q` are potentially different slots,
            and `b` is the overloaded term (as it's both left and right to a slot).

        Concretely it just means we want to say things like...

        # the first compositional step of Workflow 2
            $ workflow-ara disease associated_to gene phenotypically_similar_to gene

        ... where the results of the step corresponding to `disease associated_to gene` becomes the input step for
        `gene phenotypically_similar_to gene`, because the middlemost category "gene" is right of "associated_to" AND left of
        "phenotypically_similar_to".

        In essence, all slots are asymmetric binary operators with strict left-to-right evaluation order.

        TODO: Schema validation at the CLI parsing level and at the CWL level should be necessary, drawn upon as derived
            information to do checks whether or not the tokens are in the right part of the vocabulary. This probably
            requires some use of OWL/RDF parsing libraries?

        However, the above case lacks four forms of generality (one of which we'll discuss here).
        To be fully general our language must allow for:
        - Custom Inputs
            There is an implicit distinction in the type of inputs taken by a slot.

            Some inputs are categorical: they are lists of things in a namespace of information relevant to understanding a
            particular biological kind; consider lists of genes or lists of diseases.

            Some inputs

        - Scatterable Inputs
            TODO
        - Constrained Slots and Categories
            TODO

        - Parallel Slots

        We'll speak on Parallel Slots as it requires only a minimal extension to the proposed grammar.

        We can represent branches in the workflow by setting up slots consecutively, *given that they all share a valid right-category*
        * aPb,aQb,aRb
        * aPQRb

        What about the case of listing consecutive categories?
        !!! aPQRab ##this is invalid
        !!! abPQRc ##this is invalid

        it's ambiguous which categories each of PQR takes, or in the case where

        Notice that you can only stack relations of similar kind, else it's ambiguous or more to validate.
        * aPQRb,aSc

        ------


    """
    pass


t = {
    "test1": False,
    "test2": False,
    "test3": False,
    "test31": False,
    "test4": False
}


def tests():
    # Test1: Call Rest API for a Workflow Step
    if t["test1"]: test1()
    # Test2: Call Rest API for a composite workflow
    if t["test2"]: test2()
    # Test3: Compile a Worfklow from a chain of identifying information
    if t["test3"]: test3()
    # Test31:
    if t["test31"]: test31()
    # Test 4: ???
    if t["test4"]: test4()

    value = start_workflow("disease_associated_genes", "disease")
    pprint(value)

    tp_test = FullTaskPayload("disease_associated_genes", "disease")
    api_hook_result = handle_run_workflow(tp_test)
    pprint(api_hook_result)



tests()
