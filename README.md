# Sober Selector

Sober selector automates the process of assigning sober monitors for social events.

## Key Features
1. Allows exemption of members from sobering for a single event.
2. Updates each member's total sober count and most recent sober date.
3. Records all sober assignments from past events, can be reviewed later.

## Roster Updates
The `members.csv` file contains the full roster of brothers and pledges (current as of June 2022). At the beginning of each semester, update this file with new pledges and switch the status of outgoing pledges to brothers.

The "status" column has 3 possible values:

`e` - long term exemption (ie: already sobered for 3 semesters)

`b` - brother eligible to sober

`p` - pledge eligible to sober


## Installation

Follow [this guide](https://docs.python-guide.org/starting/install3/osx/) to install Python 3.

You may need to install pandas manually as well:
```bash
pip3 install pandas
```

At the top of this repo, navigate to `Code` > `Download ZIP`. Extract the ZIP file onto your Desktop and ensure the resulting folder is named `soberselector`.

## Usage
Open a new Terminal window and run the following commands (assuming the program is saved to the Desktop in a folder named `soberselector`).

```bash
cd ~/Desktop/soberselector
python3 selector.py
```

The program will then launch and ask you to select the appropriate menu option.
