import unittest
from Testing.UnitTesting import TestAStar
from Testing.UnitTesting import TestDancefloor
from Testing.UnitTesting import TestMapData
from Testing.UnitTesting import TestPerson
from Testing.UnitTesting import TestStateMachine
from Testing.UnitTesting import TestToilet
from Testing.UnitTesting import TestBar
from Testing.UnitTesting import TestbaseObject
from Testing.IntegrationTesting import IntegrationTests

# def suite():
#     suite = unittest.TestSuite()
#     suite.addTest(TestAStar.TestAStar('test_astar'))
#     return suite
#
# if __name__ == '__main__':
#     runner = unittest.TextTestRunner()
#     runner.run(suite())

if __name__ == '__main__':
    # Run only the tests in the specified classes

    test_classes_to_run = [TestAStar.TestAStar, TestDancefloor.TestDanceFloor, TestMapData.TestMapData,
                           TestPerson.TestPerson, TestStateMachine.TestStateMachine,
                           TestToilet.TestToilet, TestBar.TestBar, TestbaseObject.TestBaseObject,
                           TestPerson.TestPerson, IntegrationTests.IntegrationTest]
    # test_classes_to_run = [TestPerson.TestPerson, IntegrationTests.IntegrationTest]

    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)

