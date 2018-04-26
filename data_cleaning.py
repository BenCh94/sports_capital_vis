import pandas as pd
import numpy as np

local_allocations = pd.read_csv('data/local_allocations.csv')
regional_allocations = pd.read_csv('data/regional_allocations.csv')
applications = pd.read_csv('data/applications_2017.csv')


def remove_commas(number):
    number = number.replace(',', '')
    return number


def convert_to_numeric(df, col):
    df['value'] = df[col].map(lambda x: x.lstrip('€').rstrip('aAbBcC'))
    df['value'] = df['value'].apply(remove_commas)
    df['value'] = pd.to_numeric(df['value'])


convert_to_numeric(local_allocations, 'Allocation')
convert_to_numeric(regional_allocations, 'ALLOCATION')
convert_to_numeric(applications, 'Amount Sought')
local_allocations['Organisation'] = local_allocations['Organisation'].str.lower()
regional_allocations['Organisation'] = regional_allocations['Organisation'].str.lower()
applications['Organisation'] = applications['Organisation'].str.lower()
local_allocations['Project Title'] = local_allocations['Project Title'].str.lower()
regional_allocations['Project Title'] = regional_allocations['Project Title'].str.lower()
applications['Project Title'] = applications['Project Title'].str.lower()
local_allocations['id'] = applications['Project Title'] + applications['Organisation']
regional_allocations['id'] = applications['Project Title'] + applications['Organisation']
applications['id'] = applications['Project Title'] + applications['Organisation']

local_orgs = set(local_allocations['id'])
regional_orgs = set(regional_allocations['id'])
applicant_orgs = set(applications['id'])

regional_success = applicant_orgs.intersection(regional_orgs)
local_success = applicant_orgs.intersection(local_orgs)
success_mapped = regional_success.union(local_success)
success_orgs = regional_orgs.union(local_orgs)
unmapped_orgs = success_orgs - success_mapped

ids = list(success_mapped)
applications['successful'] = applications['id'].isin(ids)


def find_local_allocation(ref):
    value_allocated = local_allocations[local_allocations['id'] == ref]['value']
    return value_allocated


def find_regional_allocation(ref):
    value_allocated = regional_allocations[regional_allocations['id'] == ref]['value']
    return value_allocated


applications['allocated_value'] = 0
for ref in regional_success:
    value = find_regional_allocation(ref)
    applications.loc[applications['id'] == ref, 'allocated_value'] = value

for ref in local_success:
    value = find_local_allocation(ref)
    applications.loc[applications['id'] == ref, 'allocated_value'] = value

applications['funding_diff'] = applications['value'] - applications['allocated_value']
grants = applications[applications['successful'] == True]
failed_applications = applications[applications['successful'] == False]
grants.to_json('data/grants_2017.json', orient='records')
failed_applications.to_json('data/failed_2017.json', orient='records')
