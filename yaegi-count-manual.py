import datetime

f = open(datetime.datetime.now().isoformat().replace(':', '').replace('-','').split('.')[0] + '.txt', 'w')
count = 0

while True:
  input()
  count += 1
  print(f'{count:>3} {datetime.datetime.now().isoformat()}', end = '')
  f.write(f'{count:>3} {datetime.datetime.now().isoformat()}\n')
