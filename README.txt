1. Alec Rajeev
CSC 242
Uncertain Inference: Bayesian Networks

2. The purpose of this project was to write a program that built a Bayesian network that could perform exact inference and approximate inference.

3. To run this program python 2.7.10 and numpy are required. Also the python packages xml.etree.ElementTree, itertools, copy, and sys are required however most installations of python include all of these already.

This program essentially has its own xml parses, so only xml files are allowed. For example the aima-alarm.xml works because it is an XMLBIF file.

To run the program the exact inference do:
python exact_inference.py alarm.xml B M true J true

To run the approximate inference do:
python rejection_sampling.py 50000 alarm.xml B J true M true

This is the same format as is in the pdf that he gave us.