#!/usr/bin/python

import pandas as pd
from datetime import datetime
import re
import random

def assign(eligible_members):
    sober_positions = dict.fromkeys(['head_sober', 'door1', 'door2', 'bar1', 'bar2', 'c1_stairs', 'spiral_stairs', 'dj_stand'])
    eligible_brothers = eligible_members[eligible_members['status'] == 'b']

    # If we have pledges
    if eligible_members['status'].str.contains('p').any():
        eligible_pledges = eligible_members[eligible_members['status'] == 'p']

        assigned_brothers = assign_helper(eligible_brothers, 3)
        assigned_pledges = assign_helper(eligible_pledges, 5)

        random.shuffle(assigned_brothers)
        random.shuffle(assigned_pledges)

        # Assigning brother positions
        sober_positions['head_sober'] = assigned_brothers[0]
        sober_positions['door1'] = assigned_brothers[1]
        sober_positions['bar1'] = assigned_brothers[2]

        # Assigning pledge positions
        sober_positions['door2'] = assigned_pledges[0]
        sober_positions['bar2'] = assigned_pledges[1]
        sober_positions['c1_stairs'] = assigned_pledges[2]
        sober_positions['spiral_stairs'] = assigned_pledges[3]
        sober_positions['dj_stand'] = assigned_pledges[4]
    else:
        assigned_brothers = assign_helper(eligible_brothers, 8)
        random.shuffle(assigned_brothers)

        # Assigning brothers to all positions
        sober_positions['head_sober'] = assigned_brothers[0]
        sober_positions['door1'] = assigned_brothers[1]
        sober_positions['bar1'] = assigned_brothers[2]
        sober_positions['door2'] = assigned_brothers[3]
        sober_positions['bar2'] = assigned_brothers[4]
        sober_positions['c1_stairs'] = assigned_brothers[5]
        sober_positions['spiral_stairs'] = assigned_brothers[6]
        sober_positions['dj_stand'] = assigned_brothers[7]

    return sober_positions

def assign_helper(subgroup_members, num_open_positions):
    least_sobers = subgroup_members[subgroup_members['sober_count'] == subgroup_members['sober_count'].min()]
    assigned_sobers = []

    while len(assigned_sobers) != num_open_positions:
        # Number of people with fewest sobers equals available positions
        if len(least_sobers) == num_open_positions:
            assigned_sobers += least_sobers['name'].tolist()
        # Number of people with fewest sobers is greater than available positions
        elif len(least_sobers) > num_open_positions:
            random_sample = least_sobers.sample(num_open_positions)
            assigned_sobers += random_sample['name'].tolist()
        # Number of people with fewest sobers is less than available positions
        else:
            assigned_sobers += least_sobers['name'].tolist()
            num_open_positions -= len(assigned_sobers)
            least_sobers = subgroup_members[subgroup_members['sober_count'] == subgroup_members['sober_count'].min() + 1]

    return assigned_sobers

def assign_interface():
    event_date = input("Please enter the event date (MM/DD/YYYY): ")
    event_date = datetime.strptime(event_date, '%m/%d/%Y')
    
    event_r = lookup_event(event_date)
    if (not event_r.empty):
        print("Here are events on " + event_date.strftime('%m/%d/%Y') + " that you've already assigned sobers for:")
        print(event_r)
        choice = input("Would you like to assign sobers for another event on " + event_date.strftime('%m/%d/%Y') + "? [y/n] ")

        if choice == "n":
            return

    event_name = input("Please enter the event name: ")
        
    eligible_members = get_members()
    eligible_members = eligible_members[eligible_members['status'] != 'e']

    choice = input("Would you like to exclude any members from sobering " + event_name + " on " + event_date.strftime('%m/%d/%Y') + "? [y/n] ")
    if choice == 'y':
        print(eligible_members)
        exclude_str = input("Please enter a list of IDs of members to exclude (ex: 3,14,27,28) ")

        # String processing and list-ifying
        exclude_str = re.sub('[\s+]', '', exclude_str)
        exclude_list = exclude_str.split(",")

        # Convert list of strings to list of ints
        exclude_list = [int(i) for i in exclude_list]

        # Remove duplicates
        exclude_list = list(set(exclude_list))

        for e in exclude_list:
            print("EXCLUDED: " + eligible_members.loc[e]['name'])

        eligible_members.drop(exclude_list, axis=0, inplace=True)

    sobers = assign(eligible_members)
    for k, v in sobers.items():
        print ("{:<14} {:<14}".format(k, v))

    confirmation = input("Type 1 to confirm sobers: ")

    if confirmation == '1':
        write_events(event_date.strftime('%m/%d/%Y'), event_name, sobers)
        write_sobers(event_date, sobers)
    else:
        print("No sobers were assigned.")

def write_events(date, name, assignments):
    events = pd.read_csv('events.csv')
    positions = ['head_sober', 'door1', 'door2', 'bar1', 'bar2', 'c1_stairs', 'spiral_stairs', 'dj_stand']
    output_data = [date, name]

    for pos in positions:
        output_data.append(assignments[pos])

    events.loc[len(events)] = output_data
    events.to_csv('events.csv', index=False)

def write_sobers(date, assignments):
    members = pd.read_csv('members.csv')
    members['last_sober']= pd.to_datetime(members['last_sober'])

    for k, v in assignments.items():
        members.loc[members.name == v, 'sober_count'] = members.loc[members.name == v, 'sober_count'] + 1

        if pd.isnull(members.loc[members.name == v, 'last_sober'].iloc[0]) | (date > members.loc[members.name == v, 'last_sober'].iloc[0]):
            members.loc[members.name == v, 'last_sober'] = date

    members['last_sober'] = members['last_sober'].apply(lambda x: x.strftime('%m/%d/%Y') if not pd.isnull(x) else pd.NaT)
    members.to_csv('members.csv', index=False)

def lookup_event(target_date):
    events = pd.read_csv('events.csv')
    events['date']= pd.to_datetime(events['date'])

    return events[events['date'] == target_date]

def lookup_interface():
    event_date = input("Please enter the event date that you would like to view (MM/DD/YYYY): ")
    event_date = datetime.strptime(event_date, '%m/%d/%Y')

    event_r = lookup_event(event_date)
    if (event_r.empty):
        print("Sorry, you did not assign sobers for any event on " + event_date.strftime('%m/%d/%Y'))
        choice = input("Would you like to assign sobers now? [y/n] ")

        if choice == "y":
            event_name = input("Please enter the event name: ")
            assign(event_date, event_name)
    else:
        print("Here are events on " + event_date.strftime('%m/%d/%Y') + " that you've already assigned sobers for:")
        print(event_r)

def get_members():
    members = pd.read_csv('members.csv')
    members['last_sober']= pd.to_datetime(members['last_sober'])
    return members

def print_summary(members):
    summary = members['status'].value_counts().to_frame().reset_index()
    print("Exempt: " + str(summary.loc[summary['index'] == 'e', 'status'].iloc[0]))
    print("Brothers: " + str(summary.loc[summary['index'] == 'b', 'status'].iloc[0]))
    print("Pledges: " + str(summary.loc[summary['index'] == 'p', 'status'].iloc[0]))

def main():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    print("Welcome to the Sigma Nu Sober Selector")
    print("© Drishaan Jain 2022")
    print("1. Assign sobers for an event")
    print("2. View sobers for an event")
    print("3. Review the list of brothers and pledges")
    choice = input("Type the number of what you would like to do: ")

    if choice == "1":
        assign_interface()
    if choice == "2":
        lookup_interface()
    if choice == "3":
        members = get_members()
        print(members)
        print_summary(members)

if __name__ == '__main__':
    main()