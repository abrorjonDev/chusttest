from datetime import datetime
import pandas as pd
import numpy as np
from django.contrib.auth import get_user_model

User = get_user_model()


def names(full_name):
    first_name = None
    last_name = None
    father_name = None
    name = full_name.split(" ")
    if len(name)>3:
        first_name = name[1]
        last_name = name[0]
        father_name = name[2]+ ' '+ name[3]
    elif len(name)==3:
        first_name = name[1]
        last_name = name[0]
        father_name = name[2]
    else:
        first_name = name[1]
        last_name = name[0]
    return first_name, last_name, father_name

def create_students(file, created_by=None):
    now = datetime.now()
    print("file got: ", now )
    print(file)

    data = pd.read_excel(file)
    print("file read: ", datetime.now()-now)
    now = datetime.now()

    users = User.objects.all()
    print("users cached got: ", datetime.now()-now, users.count())

    data = data.to_numpy()
    now = datetime.now()
    print("numpy read: ", datetime.now()-now)
    created_users = []
    modified_users = []
    users = User.objects.all()
    for dt in data:
        username =dt[0] #ID
        full_name = names(dt[1]) #full_name
        school = dt[13]
        klass = dt[16]
        print(username)
        try:
            user = users.get(username=username)
            if user.first_name != full_name[0]:
                user.first_name = full_name[0]
            if user.last_name != full_name[1]:
                user.last_name = full_name[1]
            if user.father_name != full_name[2]:
                user.father_name = full_name[2]
            if user.school != school:
                user.school = school
            if user.klass != klass:
                user.klass = klass
            if not user.password:
                user.set_password("1")
            print(user, " will modified.")
            
            modified_users.append(user)  
            print("in try..")  
        #if exception, it means that the user must be created
        except:
            user = User(
                username=username, 
                first_name=full_name[0], 
                last_name=full_name[1],
                father_name=full_name[2],
                school=school,
                klass=klass
                )
            # if user not in modified_users and user not in created_users:
            print(user, " will created.")
            created_users.append(user)
            print("In except..")
        
    # bulk_create and bulk_update only create, modify objects till 1600
    start_index = 0
    end_index = 1600
    print("created users length(): ", len(created_users))
    for i in range(len(created_users)//1600):
        User.objects.bulk_create(created_users[start_index:end_index], ignore_conflicts=True)
        print("BUlk_create : ", start_index, end_index)
        start_index = end_index
        end_index = end_index + 1600
        if end_index > len(created_users):
            end_index = len(created_users)

    print("modified users length(): ", len(modified_users))
    for i in range(len(created_users)//1600):
        User.objects.bulk_update(modified_users[start_index:end_index], ['first_name','last_name','father_name', 'school', 'klass'])
        print("Bulk update:   ", start_index, end_index)
        start_index = end_index
        end_index = end_index + 1600
        if end_index > len(modified_users):
            end_index = len(modified_users)
    return {
        'created':len(created_users),
        'modified': len(modified_users),
        
        }