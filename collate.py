#! /usr/local/bin/python3

def main():
  import argparse
  parser = argparse.ArgumentParser(description='Collate county data from the NY times covid data: '
                                   'https://github.com/nytimes/covid-19-data.git.')
  parser.add_argument('--data',
                      default='../covid-19-data/us-counties.csv',
                      help='Data to collate (us-counties.csv)')
  args = parser.parse_args()
  
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
  file_cases = open('states_cases.csv', 'w')
  file_deaths = open('states_deaths.csv', 'w')
  state_list = list(states)  # make sure we use the same order of states everywhere
  header = ['date'] + state_list
  file_cases.write(','.join(header) + '\n')
  file_deaths.write(','.join(header) + '\n')
  for date in sorted(cases):
    line_cases = [date]
    line_deaths = [date]
    for state in state_list:
      if state in cases_sum[date]:
        line_cases.append(str(cases_sum[date][state]))
        line_deaths.append(str(deaths_sum[date][state]))
      else:
        line_cases.append('0')
        line_deaths.append('0')
    file_cases.write(','.join(line_cases) + '\n')
    file_deaths.write(','.join(line_deaths) + '\n')
  file_cases.close()
  file_deaths.close()

if __name__== "__main__":
  main()

