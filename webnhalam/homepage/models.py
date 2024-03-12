from django.db import models

# Create your models here.
# tạo model từ db có sẵn: python manage.py inspectdb > models.py
# còn nếu chưa có db thì tạo bằng cơm xong đẩy lên database ngược lại vs dòng trên 
# Class khóa chính phải nằm trước class khóa phụ nếu class sau thì để 'nameClass'
# python manage.py makemigrations và python manage.py migrate để update model
