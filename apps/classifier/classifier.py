import sys
sys.path.insert(0, '..')
from include import *

try:

    def getResults():
        hashes = Evaluations.getResultstoClassify(number_indicators)
        return hashes


    hashes = getResults()

    with open('../../config/classifier.ini', 'r') as f:
        array = json.load(f)

    classifier = array['classifier']

    for c in classifier:
        config = classifier[c]
        classifier_id = config['id']
        classifier_file = config['file']
        print(classifier_id)
        print(classifier_file)
        class_module = __import__(classifier_file)
        class_module.classify(classifier_id, hashes)




except Exception as e:
    print(e)

else:
    exit()
