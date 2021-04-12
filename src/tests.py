from os.path import basename, splitext, join, dirname, isfile
from os import listdir
from sys import exc_info, modules
from traceback import extract_tb
from inspect import getmembers, isfunction

def run_suite(cases, fname=None):
    """Runs a series of test cases and prints the results"""
    # run test cases
    passed = 0
    results = []
    for case in cases:
        try:
            case()
            passed += 1
            results.append(False)
        except Exception as err:
            trace = extract_tb(exc_info()[2])[-1]
            line = trace[1]
            statement = trace[3]
            reason = str(err)
            results.append((line,statement,reason))
    # format results
    header = "unit testing"
    header += " ("+str(fname)+"): " if fname else ": "
    header += str(passed)+"/"+str(len(results))
    strs = []
    nmax = 0
    for i,r in enumerate(results):
        log = [cases[i].__name__+":",cases[i].__doc__,None]
        if not r:
            log[0] = "- passed "+log[0]
        else:
            log[0] = "- failed "+log[0]
            log[2] = "\tline {} in statement \"{}\"\n\t{}".format(*r)
        strs.append(log)
        if len(log[0])>nmax:
            nmax = len(log[0])
    # print results
    print(header)
    for rs in strs:
        # print function info
        if rs[1]:
            print(rs[0].ljust(2+nmax)+rs[1])
        else:
            print(rs[0])
        # print failed reason
        if rs[2]:
            print(rs[2])

def get_suite(mname):
    """Returns a list of test cases for a given module"""
    cases = []
    try:
        __import__(mname)
        for fname, f in getmembers(modules[mname]):
            if isfunction(f) and fname[:4]=="test":
                cases.append(f)
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
        mname, type = splitext(fname)
        if isfile(join(src,fname)) and type==".py":
            suite = get_suite("tests."+mname)
            if suite:
                suites.append((suite,fname))
    # run test suites
    if len(suites)>0:
        for suite in suites[:-1]:
            run_suite(*suite)
            print("")
        run_suite(*suites[-1])
