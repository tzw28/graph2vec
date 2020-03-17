import networkx as nx
import numpy as np
import os
from scipy import sparse
from sklearn import manifold
import unittest
import warnings

import csrgraph
import nodevectors


class TestGraphEmbedding(unittest.TestCase):
    """
    higher level tests
    """
    def test_n2v(self):
        tt = nx.generators.complete_graph(50)
        wordsize = 32
        # Gensim triggers deprecation warnings...
        warnings.simplefilter("ignore", category=PendingDeprecationWarning)
        warnings.simplefilter("ignore", category=DeprecationWarning)
        g2v = nodevectors.Node2Vec(
            walklen=5, 
            epochs=5,
            threads=6,
            n_components=wordsize,
            keep_walks=True,
            w2vparams={"window":3, "negative":3, "iter":3,
                       "batch_words":32, "workers": 2})
        g2v2 = nodevectors.Node2Vec(
            walklen=5, 
            epochs=5,
            threads=6, 
            n_components=wordsize,
            keep_walks=False,
            w2vparams={"window":3, "negative":3, "iter":3,
                       "batch_words":32, "workers": 2})
        g2v.fit(tt, verbose=False)
        g2v2.fit(tt, verbose=False)
        res_v = g2v.predict(9)
        self.assertTrue(len(res_v) == wordsize)
        self.assertTrue(len(g2v2.predict(9)) == wordsize)
        self.assertTrue(hasattr(g2v, 'walks'))
        self.assertFalse(hasattr(g2v2, 'walks'))
        warnings.resetwarnings()
        # Test save/load
        fname = 'test_saving'
        try:
            g2v.save(fname)
            g2v_l = nodevectors.Node2Vec.load(fname + '.zip')
            res_l = g2v_l.predict(9)
            self.assertTrue(len(res_l) == wordsize)
            np.testing.assert_array_almost_equal(res_l, res_v)
        finally:
            os.remove(fname + '.zip')

    def test_skl(self):
        tt = nx.generators.complete_graph(25)
        ndim = 3
        skle = nodevectors.SKLearnEmbedder(
            manifold.Isomap, 
            n_components=ndim,
            n_neighbors=3)
        skle.fit(tt)
        res_v = skle.predict(9)
        self.assertTrue(len(res_v) == ndim)
        # Test save/load
        fname = 'test_saving'
        try:
            skle.save(fname)
            g2v_l = nodevectors.SKLearnEmbedder.load(fname + '.zip')
            res_l = g2v_l.predict(9)
            self.assertTrue(len(res_l) == ndim)
            np.testing.assert_array_almost_equal(res_l, res_v)
        finally:
            os.remove(fname + '.zip')

    def test_glove(self):
        tt = nx.generators.complete_graph(25)
        ndim = 3
        skle = nodevectors.Glove(
            n_components=ndim,
            tol=0.005,
            max_loss=15,
            learning_rate=0.1,
            max_epoch=2000)
        skle.fit(tt)
        res_v = skle.predict(9)
        self.assertTrue(len(res_v) == ndim)
        # Test save/load
        fname = 'test_saving'
        try:
            skle.save(fname)
            g2v_l = nodevectors.SKLearnEmbedder.load(fname + '.zip')
            res_l = g2v_l.predict(9)
            self.assertTrue(len(res_l) == ndim)
            np.testing.assert_array_almost_equal(res_l, res_v)
        finally:
            os.remove(fname + '.zip')
