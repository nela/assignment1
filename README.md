# IN5410 Assignment1

Delivery for project assignment1 in IN5410 Energy Informatics course at UiO.
Project done by:
- Øvind Anders Anrtzen Toftegaard
- Finn Eivind Aasen
- Nemanja Lakicevic

## Requirements

Required packages are listed in requirements.txt.
Program has been tested with Python 3.9.1. Operating systems Windows and MacOs.

## Usage

For solving the tasks run the ´solution.py´ script. The output will be printed to stdout.

Task 1:

`
$ python solution.py --task1
`

Task 2:

Create a house with varied appliances:

`
$ python solution.py --task2
`

Execute this command to get the same results as described in the report for task 2.
Create a house with the predetermined set of additional appliances:

`
$ python solution.py --task2 single
`

Task 3:

`
$ python solution.py --task3 <number-of-houses>
`

Task 4:

Create a house with varied appliances and specified peak load:

`
$ python solution.py --task4 <hourly-peak-load>
`

Create a house with the predetermined set of additional appliances (same appliances as for task 2):

`
$ python solution.py --task4 <hourly-peak-load> single
`

For the 'single' house with predetermined set of additional appliances the
lowest peak load for a successfull optimization is 3.6. In order to get the same
results as described in the report, execute:

`
$ python solution.py --task4 3.6 single
`
