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
    
    cases = {}
    deaths = {}
    states = {}
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
      if state not in cases[date]:
        cases[date][state] = {}
        deaths[date][state] = {}
      cases[date][state][county] = c
      deaths[date][state][county] = d
  
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
        line_cases = []
        line_cases.append(date)
        line_deaths = []
        line_deaths.append(date)
        
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

if __name__== "__main__":
  main()

