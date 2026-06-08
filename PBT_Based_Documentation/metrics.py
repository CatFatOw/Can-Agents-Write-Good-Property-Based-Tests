def test_metrics(test_func, n=50):
    """Function used to calculate the soundness and validity metrics for display on the website"""

    validity_failures = 0
    soundness_failures = 0

    # We run this for 300 times
    for i in range(n):
        try:
            test_func()
        except AssertionError as e:
            soundness_failures += 1
        except Exception as e:
            validity_failures += 1
    # Calculate the valid and soundness metrics 
    valid = 1 - validity_failures / n
    sound = 1 - soundness_failures / n
    return (valid, sound)
    
            