import scipy, numpy
a = numpy.asarray([[0, 0, 0, 0],
                 [0, 0, 0.5, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]])
b = numpy.asarray([[(0/9), (0/9), (1/9)],
                 [2, 2.9, 2.5],
                 [0.1, (0/9), 0.25]])
# [0, 0, 0, 0]
# [(0/9), (0/9), (0/9)]
print(a)
print(b)
print(numpy.array(list(map(lambda x: [round(i, 4) for i in x], scipy.signal.fftconvolve(a, b, 'same')))))
