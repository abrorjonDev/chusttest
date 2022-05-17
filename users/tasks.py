from venv import create
from celery import shared_task

#local imports
from.file_read import create_students

@shared_task
def student_register_by_file(file, created_by=None):
    print("creating students..")
    create_students(file=file, created_by=created_by)
    print("created students!")
    return {"status": "Students have been created!"}