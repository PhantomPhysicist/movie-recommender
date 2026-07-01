import numpy

def cosine(A: dict, B: dict) -> int:
    Array_A = numpy.array(list(A.values()))
    Array_B = numpy.array(list(B.values()))

    Mag_A = numpy.linalg.norm(Array_A)
    Mag_B = numpy.linalg.norm(Array_B)

    Dot = numpy.dot(Array_A, Array_B)

    CosineSimilarity = Dot/(Mag_A * Mag_B)

    return CosineSimilarity