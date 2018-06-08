import csv
from accounts.models import User
file = open('../../../Downloads/MOCK_DATA_ALL.csv', 'r')
reader = csv.reader(file)
num = 0
for line in reader:
    user = User.objects.get_or_create(username=line[0], first_name=line[1], last_name=line[2], email=line[3], user_type=line[4])[0]
    user.set_password('randompass')
    num += 1
    user.save()
    print(num)


    
