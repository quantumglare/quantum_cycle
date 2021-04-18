import time

import minorminer


def find_embedding(S, T, **kwargs):
    """Return an embedding for the edges S of the source and the edges T of
    the target. We use the function minorminer.

    :param S: an iterable of label pairs representing the edges in the source
    graph, or a NetworkX Graph
    :param T: an iterable of label pairs representing the edges in the target
    graph, or a NetworkX Graph
    :param kwargs: keyword arguments containing th random seed to be
    used in the embedding initialisation

    :return: an embedding

    """
    t0 = time.time()
    embedding = minorminer.find_embedding(S, T, **kwargs)
    t1 = time.time()
    print(f"\nTime to get embedding: {t1-t0:.2f} s")
    return embedding
