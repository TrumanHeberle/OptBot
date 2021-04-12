from os.path import basename, splitext, join, dirname, isfile
from os import listdir
from sys import exc_info, modules
from traceback import extract_tb
from inspect import getmembers, isfunction
from multiprocessing import Pool, TimeoutError

TIMEOUT = 1 # seconds

def run_case(case):
    """Safely executes a test case and returns an error string on fail"""
    try:
        case()
        return None
    except Exception as err:
        trace = extract_tb(exc_info()[2])[-1]
        line = trace[1]
        statement = trace[3]
        reason = str(err)
        return f"line {line} in statement '{statement}'"+(f"\n\t{reason}" if reason else "")

def run_suite(cases, fname="unspecified"):
    """Runs a series of test cases and prints the results"""
    # run test cases safely
    with Pool() as pool:
        results = [pool.apply_async(run_case,[case]) for case in cases]
        for i,result in enumerate(results):
            try:
                results[i] = result.get(TIMEOUT)
            except TimeoutError as err:
                results[i] = f"timed out after {TIMEOUT} seconds"
    # formatting functions
    passed = sum(error is None for error in results)
    status = lambda r: "failed" if r else "passed"
    name = lambda i: cases[i].__name__
    doc = lambda i: cases[i].__doc__ if cases[i].__doc__ else ""
    reason = lambda r: f"\n\t{r}"
    log_str = lambda i,r: (f"- {status(r)} {name(i)}:",f"{doc(i)}{reason(r) if r else ''}")
    # print results
    print(f"unit testing ({fname}): {passed}/{len(results)}")
    log_strs = [log_str(i,r) for i,r in enumerate(results)]
    n = max([len(ls[0]) for ls in log_strs])+2
    for l1,l2 in log_strs:
        print(f"{l1.ljust(n)}{l2}")

def get_suite(mname):
    """Returns a list of test cases for a given module"""
    cases = []
    try:
        __import__(mname)
        is_case = lambda f, fname: isfunction(f) and fname[:4]=="test"
        cases = [f for fname, f in getmembers(modules[mname]) if is_case(f,fname)]
    except Exception as err:
        print(err)
    finally:
        return cases

# main code
if __name__=="__main__":
    # check tests folder for python files
    src = join(dirname(__file__),"tests")
    suites = []
    # import test cases
    for fname in listdir(src):
        mname, fext = splitext(fname)
        if isfile(join(src,fname)) and fext==".py":
            suite = get_suite("tests."+mname)
            if suite:
                suites.append((suite,fname))
    # run test suites
    if len(suites)>0:
        for suite in suites[:-1]:
            run_suite(*suite)
            print("")
        run_suite(*suites[-1])
