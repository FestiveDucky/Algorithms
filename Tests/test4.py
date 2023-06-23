from multiprocessing import Pool
import time

def square(x):
    count = 0
    for i in range(10000000 * x): count += 1
    # calculate the square of the value of x
    return count
if __name__ == '__main__':

    # Define the dataset
    dataset = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

    # Output the dataset
    print ('Dataset: ' + str(dataset))

    start = time.time()
    # Run this with a pool of 5 agents having a chunksize of 3 until finished
    agents = 20
    chunksize = 1
    with Pool(processes=agents) as pool:
        result = pool.map(square, dataset, chunksize)

    print("Time: " + str(time.time() - start))
    # Output the result
    print ('Result:  ' + str(result))