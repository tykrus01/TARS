import time

start_time = 0

def tito():
    global start_time

    if start_time == 0:
        # First time function is called, start the timer
        start_time = time.perf_counter()
    else:
        # Second time function is called, stop the timer and calculate elapsed time
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print("Elapsed time: {:.6f} seconds".format(elapsed_time))
        # Reset start_time for next call
        start_time = 0
