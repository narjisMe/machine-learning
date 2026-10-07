import csv
from matplotlib import pyplot as plt 

type AgePyramidRow = tuple[str, str, int]

def parse_row(row: list) -> AgePyramidRow:
    return (row[0], row[1], int(row[2]))

labels: list[str] = []
hommes: list[int] = []
femmes: list[int] = []


with open("Belgique.csv", 'r', encoding='utf-8-sig') as fp:
    reader = csv.reader(fp, quoting=csv.QUOTE_NONNUMERIC)
    next(reader)
    for row in reader:
        age, sex, num = parse_row(row)
        if sex == 'Hommes':
            labels.append(age)
            hommes.append(num)
        else:
            femmes.append(num)    

for age, num_hommes, num_femmes in zip(labels, hommes, femmes):
    print(age, num_hommes, num_femmes)

y = range(len(labels), 0, -1) 

plt.figure()
plt.barh(y, [-h for h in hommes], label= 'hommes')

plt.barh(y, femmes, label='femmes')
plt.yticks(y, labels)
plt.legend()
plt.savefig()
plt.show()