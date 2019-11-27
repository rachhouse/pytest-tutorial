# pytest-tutorial

## Introduction
---
This repo hosts a hands-on tutorial on using the excellent [`pytest`](https://docs.pytest.org/en/latest/) library to write test suites that support your code.

Tutorial development is still in-progress as of this latest README commit.

There is a companion slide deck, also under construction, which can be found here: [https://slides.com/rachhouse/pytest](https://slides.com/rachhouse/pytest)

## Tutorial Contents
---
The tutorial is divided into three main sections:
1. `swapy/`. This folder contains the code for a simple, but functional, API wrapper around [SWAPI](https://swapi.co/), the Star Wars API. 

1. `tests/example_test_suite/`. This folder contains - you guessed it - an example test suite for the `swapy` library. Clearly, this is not the only, or most exhaustive, way to design and create a test suite for a chunk of code like `swapy`; however, it does reflect how I would develop a test suite for any similar, real-world library. The example test suite is intended to showcase how you can use `pytest` to build an understandable, maintainable, extensible (all the best `.*[a|i]bles`, really), and robust test suite, as well as highlight the use of goodies like monkeypatching, `conftest.py`, and `pytest.ini`. 

1. `tests/test_tutorials/`. This folder contains a variety of subfolders which allow you to run smaller sets of test (or even a single test) to demonstrate various testing and pytest principles. At present, this is the section of the tutorial that needs the most work. It's still pretty lacking.

I've also added a bonus folder, `notebooks/` which contains some examples of how you can use the `swapy` library to play around with SWAPI data. Well, TBH, "bonus" is an exaggeration. As is "example*s*". There's presently one sparse, lame example - I hope to add cooler and more imaginative examples as I continue to develop this tutorial.