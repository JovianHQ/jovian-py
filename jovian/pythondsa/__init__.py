"""
Utilities and helper functions for the course "Data Structures and Algorithms in Python". 
Visit http://pythondsa.com to learn more.
"""

from timeit import default_timer as timer
from textwrap import dedent
import math


from timeit import default_timer as timer
from textwrap import dedent
import math


def _show_test_case(test_case):
    inputs = test_case['input']
    expected = test_case['output']
    print(dedent("""
    Input:
    {}

    Expected Output:
    {}
    """.format(inputs, expected)))


def _show_result(result, runtime, message):
    print(dedent("""
    Actual Output:
    {}

    Execution Time:
    {} ms

    Test Result:
    {}
    """.format(result, runtime, message)))


def evaluate_test_case(function, test_case, display=True):
    """Check if `function` works as expected for `test_case`"""
    inputs = test_case['input']
    expected = test_case['output']

    if display:
        _show_test_case(test_case)

    start = timer()
    result = function(**inputs)
    end = timer()
    runtime = math.ceil((end - start)*1e6)/1000
    passed = result == expected
    message = "\033[92mPASSED\033[0m" if passed else "\033[91mFAILED\033[0m"

    if display:
        _show_result(result, runtime, message)

    return result, passed, runtime


def evaluate_test_cases(function, test_cases, error_only=False):
    results = []
    for i, test_case in enumerate(test_cases):
        if not error_only:
            print("\n\033[1mTEST CASE #{}\033[0m".format(i))
        result = evaluate_test_case(function, test_case, display=False)
        results.append(result)
        if error_only and not result[1]:
            print("\n\033[1mTEST CASE #{}\033[0m".format(i))
        if not error_only or not result[1]:
            _show_test_case(test_case)
            _show_result(*result)

    total = len(results)
    num_passed = sum([r[1] for r in results])
    print("\n\033[1mSUMMARY\033[0m")
    print("\nTOTAL: {}, \033[92mPASSED\033[0m: {}, \033[91mFAILED\033[0m: {}".format(
        total, num_passed, total - num_passed))
    return results


def binary_search(lo, hi, condition):
    while lo <= hi:
        mid = (lo + hi) // 2
        result = condition(mid)
        if result == 'found':
            return mid
        elif result == 'left':
            hi = mid - 1
        else:
            lo = mid + 1
    return -1
