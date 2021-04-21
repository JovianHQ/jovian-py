import traceback
import re

TESTS = {}

def format_exc(e):
    """Format the exception message"""
    msg = ": {}".format(str(e)) if str(e).strip() else ""
    error_type = type(e).__name__
    return "\n{} {}".format(error_type, msg)

def testcase(test_id, error_msg):
    """A decorator for marking functions as test cases""" 
    def decorator(fun):        
        def wrapper(*args, **kwargs):
            try:
                result = fun(*args, **kwargs)
                if result is None: result = ""
                return True, str(result)
            except Exception as e:
                print(traceback.format_exc())
                return False, error_msg + format_exc(e)
        TESTS[test_id] = wrapper
        return wrapper
    return decorator

def replace_regex(tb, pattern_map):
    for cell in filter(lambda cell: cell.cell_type == "code", tb.cells):
        for pattern, replace_with in pattern_map.items():
            cell.source = re.sub(pattern, replace_with, cell.source, flags=re.MULTILINE)

def run_tests(nb):
    if type(nb) != dict:
        pattern_map = {
                r"! *pip *install.*$": "",
                r"jovian *. *commit": "",
            }
        replace_regex(nb, pattern_map)
        nb.execute()
    
    all_passed, comments = True, ""
    
    for test_id, test in TESTS.items():
        comment = "{}: ".format(test_id)
        passed, msg = test(nb)
        if passed:
            comment += "PASS\n\n"
        else:
            comment += "FAIL\n{}\n\n".format(msg)
            all_passed = False
        comments += comment
    
    return (all_passed, comments), None

def contains_output(nb, text):
    """Check if the one of the output cells contains the given text"""
    code_cell_outputs = [cell.outputs for cell in nb.cells if cell.cell_type == "code"]
    for outputs in code_cell_outputs:
        for output in outputs:
            if output["output_type"] == "stream":
                output_text = ''.join(list(output["text"]))
                if str(text) in output_text:
                    return True
    return False


def contains_code(nb, code):
    """Check if one of the code cells contains the given code"""
    code_cell_sources = [''.join(list(cell.source)) for cell in nb.cells if cell.cell_type == "code"]
    for source in code_cell_sources:
        if str(code) in source:
            return True
    return False
