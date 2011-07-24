'''
Created on Apr 30, 2011

@author: dlemel
'''
import unittest
import weighters
import scorers
from controller import Controller, is_print_debug
from web_operations.search_engines import BingSE

class ControllerTest(unittest.TestCase):
    
    def test_Depp_Basic_Basic(self):
        world = ["Johnny Depp", "Moshe Ivgy", "Tom Hanks"]
        context = ["Pirates of the Caribbean", "Corpse Bride", "Sweeney Todd", "Secret Window",  "sleepy hollow"]
        context += ["benny & joon", "ed wood", "Edward Scissorhands", "Tim Burton", "Charlie and the Chocolate Factory"]
        context += ["The Ninth Gate", "Fear and Loathing in Las Vegas", "Don Juan DeMarco"]
        Controller(weighters.BasicWeighter(), scorers.BasicScorer(), BingSE).run(world, context)
        # this method is so bad, we only check the algorithm finish...

    def test_Depp_NGD_NGD(self):
        world = ["Johnny Depp", "Moshe Ivgy", "Tom Hanks"]
        context = ["Pirates of the Caribbean", "Corpse Bride", "Sweeney Todd", "Secret Window",  "sleepy hollow"]
        context += ["benny & joon", "ed wood", "Edward Scissorhands", "Tim Burton", "Charlie and the Chocolate Factory"]
        context += ["The Ninth Gate", "Fear and Loathing in Las Vegas", "Don Juan DeMarco"]
        res = Controller(weighters.NGDWeighter(), scorers.NGDScorer(), BingSE).run(world, context)
        if is_print_debug:
            print res
        names = [x[0] for x in res]
        assert names == ["Johnny Depp", "Tom Hanks", "Moshe Ivgy"]   # great results :)
    
    
    def test_Depp_MutualInformation_MutualInformationNormalized(self):    
        world = ["Johnny Depp", "Moshe Ivgy", "Tom Hanks"]
        context = ["Pirates of the Caribbean", "Corpse Bride", "Sweeney Todd", "Secret Window",  "sleepy hollow"]
        context += ["benny & joon", "ed wood", "Edward Scissorhands", "Tim Burton", "Charlie and the Chocolate Factory"]
        context += ["The Ninth Gate", "Fear and Loathing in Las Vegas", "Don Juan DeMarco"]
        res = Controller(weighters.MutualInformationWeighter(), scorers.MutualInformationScorerNormalized(), BingSE).run(world, context)
        if is_print_debug:
            print "Result from search engine: "
            print res
        names = [x[0] for x in res]
        if is_print_debug:
            print "Test debug: "
            print names
        assert not names.index("Johnny Depp")
    
    def test_USA_Entropy_NGD(self):
        world = ["USA", "russia", "china", "israel", "iran", "north korea", "spain", "australia", "peru"]
        context = ["washington", "yankee", "california", "alaska", "new york", "los angeles", "hollywood"]
        res = Controller(weighters.EntropyWeighter(), scorers.NGDScorer(), BingSE).run(world, context)
        if is_print_debug:
            print "Result from search engine: "
            print res
        names = [x[0] for x in res]
        if is_print_debug:
            print "Test debug: "
            print names
        assert names.index("USA") < 6

    
    def test_Helicopter_MutualInformation_MutualInformationNormalized(self):
        world = ["aircraft", "airplane", "helicopter", "mouse"]
        context = ["Black Hawk", "Apache", "UH-1 HUEY", "SA 330 PUMA"]
        res = Controller(weighters.MutualInformationWeighter(), scorers.MutualInformationScorerNormalized(), BingSE).run(world, context)
        if is_print_debug:
            print "Result from test_synonyms: "
            print res
        names = [x[0] for x in res]
        assert names[0] == "helicopter"   # great results :)
    
    