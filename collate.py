#! /usr/local/bin/python3

def main():
  import argparse
  parser = argparse.ArgumentParser(description='Collate county data from the NY times covid data: '
                                   'https://github.com/nytimes/covid-19-data.git.')
  parser.add_argument('--data',
                      default='../covid-19-data/us-counties.csv',
                      help='Data to collate (us-counties.csv)')
  args = parser.parse_args()

  # define state populations from https://en.wikipedia.org/wiki/List_of_U.S._states_and_territories_by_population
  population = {}
  population['Alabama'] = 5024279
  population['Alaska'] = 733391
  population['American Samoa'] = 49437
  population['Arizona'] = 7151502
  population['Arkansas'] = 3011524
  population['California'] = 39538223
  population['Colorado'] = 5773714
  population['Connecticut'] = 3605944
  population['Delaware'] = 989948
  population['District of Columbia'] = 689545
  population['Florida'] = 21538187
  population['Georgia'] = 10711908
  population['Guam'] = 168485
  population['Hawaii'] = 1455271
  population['Idaho'] = 1839106
  population['Illinois'] = 12812508
  population['Indiana'] = 6785528
  population['Iowa'] = 3190369
  population['Kansas'] = 2937880
  population['Kentucky'] = 4505836
  population['Louisiana'] = 4657757
  population['Maine'] = 1362359
  population['Maryland'] = 6177224
  population['Massachusetts'] = 7029917
  population['Michigan'] = 10077331
  population['Minnesota'] = 5706494
  population['Mississippi'] = 2961279
  population['Missouri'] = 6154913
  population['Montana'] = 1084225
  population['Nebraska'] = 1961504
  population['Nevada'] = 3104614
  population['New Hampshire'] = 1377529
  population['New Jersey'] = 9288994
  population['New Mexico'] = 2117522
  population['New York'] = 20201249
  population['North Carolina'] = 10439388
  population['North Dakota'] = 779094
  population['Northern Mariana Islands'] = 51433
  population['Ohio'] = 11799448
  population['Oklahoma'] = 3959353
  population['Oregon'] = 4237256
  population['Pennsylvania'] = 13011844
  population['Puerto Rico'] = 3285874
  population['Rhode Island'] = 1097379
  population['South Carolina'] = 5118425
  population['South Dakota'] = 886667
  population['Tennessee'] = 6910840
  population['Texas'] = 29145505
  population['U.S. Virgin Islands'] = 106235
  population['Utah'] = 3271616
  population['Vermont'] = 643077
  population['Virginia'] = 8631393
  population['Washington'] = 7705281
  population['West Virginia'] = 1793716
  population['Wisconsin'] = 5893718
  population['Wyoming'] = 576851
  population['Virgin Islands'] = population['U.S. Virgin Islands']
  
  # read in data
  with open(args.data, 'r') as file:
    # ignore header
    file.readline().split(',')
    
    cases = {}       # cases[date][state][county] = number of cases for that point
    deaths = {}      # cases[date][state][county] = number of deaths for that point

    cases_sum = {}   # cases_sum[date][state] = total number of cases for that state
    deaths_sum = {}  # deaths_sum[date][state] = total number of deaths for that state

    states = {}      # states[state]['counties'] = list of counties for that state
                     # states[state]['fips'] = corresponding list of fips for that state
    for line in file:
      # columns are: date, county, state, fips, cases, deaths
      [date, county, state, f, c, d] = line.split(',')
      d = d.rstrip()  # ignore newlines at the end
      
      # add to state and county lists
      if state not in states:
        states[state] = {'counties': [], 'fips': []}
      if county not in states[state]['counties']:
        states[state]['counties'].append(county)
        states[state]['fips'].append(f)
      
      # add to cases and deaths data
      if date not in cases:
        cases[date] = {}
        deaths[date] = {}
        cases_sum[date] = {}
        deaths_sum[date] = {}
      if state not in cases[date]:
        cases[date][state] = {}
        deaths[date][state] = {}
        cases_sum[date][state] = 0
        deaths_sum[date][state] = 0
      cases[date][state][county] = c
      deaths[date][state][county] = d
      cases_sum[date][state] += int(c)
      if d != '':
        deaths_sum[date][state] += int(d)

  # write out per-state data
  for state in states:
    # create file for number of cases
    file_cases = open('_'.join(state.split(' ')) + '_cases.csv', 'w')
    file_cases.write(',' + ','.join(states[state]['counties']) + '\n')
    #file_cases.write(',' + ','.join(states[state]['fips']) + '\n')
    
    # create file for number of deaths
    file_deaths = open('_'.join(state.split(' ')) + '_deaths.csv', 'w')
    file_deaths.write(',' + ','.join(states[state]['counties']) + '\n')
    #file_deaths.write(',' + ','.join(states[state]['fips']) + '\n')

    for date in sorted(cases):
      if state in cases[date]:
        # initialize data for current date
        line_cases = [date]
        line_deaths = [date]
        
        # collect the data
        for county in states[state]['counties']:
          if county in cases[date][state]:
            line_cases.append(cases[date][state][county])
            line_deaths.append(deaths[date][state][county])
          else:
            line_cases.append('')
            line_deaths.append('')
          
        # write out the data
        file_cases.write(','.join(line_cases) + '\n')
        file_deaths.write(','.join(line_deaths) + '\n')
    file_cases.close()
    file_deaths.close()

  # write out state aggregate cases data
  file_cases = open('states_cases_per_million.csv', 'w')
  file_deaths = open('states_deaths_per_million.csv', 'w')
  state_list = sorted(list(states))  # make sure we use the same order of states everywhere
  # state split by 2016 vote
  # state_list = ['California', 'Colorado', 'Connecticut', 'Delaware', 'Hawaii', 'Illinois', 'Maine', 'Maryland', 'Massachusetts', 'Minnesota', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'Oregon', 'Rhode Island', 'Vermont', 'Virginia', 'Washington', 'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'Florida', 'Georgia', 'Idaho', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Michigan', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Pennsylvania', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'West Virginia', 'Wisconsin', 'Wyoming']


  header = ['date'] + state_list
  file_cases.write(','.join(header) + '\n')
  file_deaths.write(','.join(header) + '\n')
  for date in sorted(cases):
    line_cases = [date]
    line_deaths = [date]
    for state in state_list:
      if state in cases_sum[date]:
        line_cases.append(str(cases_sum[date][state] * 1000000 / population[state]))
        line_deaths.append(str(deaths_sum[date][state] * 1000000 / population[state]))
      else:
        line_cases.append('0')
        line_deaths.append('0')
    file_cases.write(','.join(line_cases) + '\n')
    file_deaths.write(','.join(line_deaths) + '\n')
  file_cases.close()
  file_deaths.close()

if __name__== "__main__":
  main()

