from tqdm import tqdm 

def evaluate_test(test_func, n=1000):
    validity_errors = []
    soundness_errors = []

    for _ in tqdm(range(n)):
        try:
            test_func()
        except AssertionError as e:
            soundness_errors.append(str(e))
        except Exception as e:
            validity_errors.append(type(e).__name__)

    validity = 1 - len(validity_errors) / n
    soundness = 1 - len(soundness_errors) / n

    return {
        "validity": validity,
        "soundness": soundness,
        "validity_errors": validity_errors,
        "soundness_errors": soundness_errors,
    }