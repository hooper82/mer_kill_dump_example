# Introduction
As of [Feb 2023, the Monthly Economic Report](https://www.eveonline.com/news/view/monthly-economic-report-february-2023) contains a `kill_dump.json` file. This file contains a list of all kills that happened in EVE Online Tranquility over the last month. This includes the battle_id associated with each kill ID, and participating characters/ship types.

Its encoraged that those interested, can read this file and run analysis on it.

This is an example python script, reading the file and looking at the participiaton of different ship types in larger battles.

## How-To
After cloneing this repository, you'll need to:
1. Install required packages : `pip install -r requirements.txt`
1. Download the MER Zip, and extract the `kill_dump.json` file into the same directory as `main.py`
1. Download the required csvs from the EVE Static Dump (details below) and put them in the same directory as the `main.py` file.
1. Run : `python main.py`

I recommend you use a virtualenv rather than messing up your base python install. But thats beyond the scope of this document.

## Static Dump Source
Get the following files here : https://www.fuzzwork.co.uk/dump/latest/
 * `invTypes.csv`
 * `invGroups.csv`

