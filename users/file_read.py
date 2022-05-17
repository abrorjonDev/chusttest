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
    print("file got: ", now)
    data = pd.read_excel(file)
    print("file read: ", datetime.now()-now)
    now = datetime.now()

    users = User.objects.all()
    print("users cached got: ", datetime.now()-now, users.count())

    data = data.to_numpy()
    now = datetime.now()
    print("numpy read: ", datetime.now()-now)

    for dt in data:
        username =dt[0] #ID
        full_name = names(dt[1]) #full_name
        school = dt[13]
        klass = dt[16]
        modified = 0
        created = 0

        try:
            student = User.objects.get(username=username)
            student.first_name=full_name[0]
            student.last_name=full_name[1]
            student.father_name=full_name[2]
            student.school = school
            student.klass = klass
            student.created_by = created_by
            if not student.password:
                student.set_password("1")
            student.save()
            created += 1
            # student = User.objects.create(
            #     username=username, 
            #     first_name=names(full_name)[0], 
            #     last_name=names(full_name)[1],
            #     father_name=names(full_name)[2],
            #     school=school, 
            #     klass=klass,
            #     created_by=created_by
            #     )
            # student.set_password("1")
            # student.save()
            # created +=1

        except Exception as e:
            student = User.objects.create(
                username=username, 
                first_name=full_name[0], 
                last_name=full_name[1],
                father_name=full_name[2],
                school=school, 
                klass=klass,
                created_by=created_by
            )
            student.set_password("1")
            student.save()
            modified +=1


            # student = User.objects.get_or_create(username=username)[0]
            # student.first_name=full_name.split(" ")[1]
            # student.last_name=full_name.split(" ")[0]
            # student.modified_by = created_by
            # student.school = school
            # student.klass = klass
            # if not student.password:
            #     print("password saved")
            #     student.set_password('1')
            # student.save()
            # modified += 1
        
        # start_index = 0
        # end_index = 1500
        # #bulk_create()   limit is 1600 so I have calculated as 1500.
        # if len(created_users)//1500:
        #     User.objects.bulk_create(created_users)
        # else:
        #     for i in range(len(created_users)//1500):
        #         User.objects.bulk_create(created_users[start_index:end_index])
        #         start_index = end_index
        #         end_index += end_index+1500
        #         if end_index > len(created_users):
        #             end_index = len(created_users)
        # if len(created_users)//1500:
        #     User.objects.bulk_update(modified_users)
        # else:
        #     start_index = 0
        #     end_index = 1500
        #     for i in range(len(modified_users)//1500):
        #         User.objects.bulk_update(modified_users[start_index:end_index])
        #         start_index = end_index
        #         end_index += end_index+1500
        #         if end_index > len(modified_users):
        #             end_index = len(modified_users)
    print("process finished: ", datetime.now().minute)

    return {'created':created, 'updated':modified, 'status':201}




# from openpyxl import load_workbook, Workbook
# from .models import User, UserDocs




# def create_students(file, created_by=None):
#     wb = load_workbook(file)
#     ws = wb.active

#     for i in range(2, ws.max_row+1):
#         username = ws.cell(i, 1).value #ID
#         full_name = ws.cell(i, 2).value #full_name
#         # birth_date = ws.cell(i, 3).value # birth_date
#         # genre = ws.cell(i, 4).value #genre
#         # nationality = ws.cell(i, 5).value
#         # citizen = ws.cell(i, 6).value
#         # state = ws.cell(i, 7).value
#         # region = ws.cell(i, 8).value
#         # pinfl = ws.cell(i, 9).value
#         # doc_type = ws.cell(i, 10).value
#         # serial = ws.cell(i, 11).value
#         # doc_number = ws.cell(i, 12).value
#         # who_gave = ws.cell(i, 13).value
#         school = ws.cell(i, 14).value
#         # state_organ = ws.cell(i, 15).value
#         # region_organ = ws.cell(i, 16).value
#         klass = ws.cell(i, 17).value
#         modified, created = 0, 0
#         
