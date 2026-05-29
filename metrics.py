from tqdm import tqdm 
# Currently metrics only has validity and soundness. Will add mutation killing 
def evaluate_test(test_func, n=1000):
    validity_errors = set()
    soundness_errors = set()

    validity_failures = 0
    soundness_failures = 0

    for _ in tqdm(range(n)):
        try:
            test_func()

        except AssertionError as e:
            soundness_failures += 1
            soundness_errors.add(str(e))

        except Exception as e:
            validity_failures += 1
            validity_errors.add(type(e).__name__)

    validity = 1 - validity_failures / n
    soundness = 1 - soundness_failures / n

    return {
        "validity": validity,
        "soundness": soundness,
        "validity_errors": validity_errors,
        "soundness_errors": soundness_errors,
    }