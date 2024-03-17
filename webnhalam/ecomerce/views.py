from django.shortcuts import render, redirect
from .models import Category, Products, Oder, Cart, Customer, Payments
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime

#filter(): Chọn các bản ghi từ cơ sở dữ liệu dựa trên điều kiện: queryset = MyModel.objects.filter(some_field=some_value) 
#exclude(): Loại bỏ các bản ghi từ cơ sở dữ liệu dựa trên điều kiện: queryset = MyModel.objects.exclude(some_field=some_value)
#get(): Lấy một bản ghi duy nhất từ cơ sở dữ liệu dựa trên điều kiện: obj = MyModel.objects.get(some_field=some_value)
#all(): Lấy tất cả các bản ghi từ cơ sở dữ liệu: queryset = MyModel.objects.all()
#order_by(): Sắp xếp kết quả theo một hoặc nhiều trường: queryset = MyModel.objects.all().order_by('some_field')
#annotate(): Thêm các trường tính toán vào kết quả truy vấn: queryset = MyModel.objects.values('some_field').annotate(count=Count('id'))

def home(request):
    topPro = Products.objects.all()[:3]
    return render(request,'home.html',{'topPro':topPro})

def shop(request):
    pro = Products.objects.all()
    return render(request,'shop.html',{'pro':pro})

def services(request):
    topPro = Products.objects.all()[:3]
    return render(request,'services.html',{'topPro':topPro})

def contact(request):
    return render(request,'contact.html')

def cart(request):
    return render(request,'cart.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            acc = request.POST.get('email')
            pas = request.POST.get('pass')

            try:
                #cách đăng nhập bằng query rồi lưu vào session và đây là cách đưa ra temaplate {{request.session.user_name}}
                # user = Customer.objects.get(email = acc, pass_field = pas)
                # request.session['user_id'] = user.idcus
                # request.session['user_name'] = user.lastname
                # request.session['user_email'] = user.email

                #cách đăng nhập bằng auth_user
                # user = authenticate(request, email = acc, password = pas) #bi lỗi gì á 
                if User.objects.filter(email = acc, password = pas).exists():
                    login(request, User.objects.get(email = acc, password = pas))
                    return redirect('home')
                else:
                    messages.error(request, 'Tài khoản hoặc mật khẩu không đúng.')
                    return redirect('login')
                
            except Exception as e:
                print(e)
                messages.error(request, 'Đã có lỗi xảy ra !!!')
            
    return render(request,'login.html')

def sign_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        acc = request.POST.get('email')
        pas = request.POST.get('pass')
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S %z')
        
        try:
            if Customer.objects.filter(email = acc).exists():
                messages.info(request, 'Email đã được đăng ký.')
                return redirect('sign')
            elif Customer.objects.filter(phone = phone).exists():
                messages.info(request, 'Số điện thoại đã được đăng ký.')
                return redirect('sign')
            else:
                cus = Customer.objects.create(created_at = created_at, lastname=name, phone=phone, email=acc, pass_field=pas)
                # request.session['user_id'] = cus.idcus
                # request.session['user_name'] = cus.lastname
                # request.session['user_email'] = cus.email
                
                #cách tạo và đăng nhập bằng auth_user
                user = User.objects.create(id = cus.idcus, date_joined = created_at, username = name, last_name = name, email = acc, password = pas) #tạo auth_user
                # user = authenticate(request, email=acc, password=pas) #xác thực người dùng # bi lỗi gì á 
                if user is not None:
                    login(request, user)
                    return redirect('home')
        except :
            messages.error(request, 'Đã có lỗi xảy ra !!!')
    return render(request,'sign.html')

def logout_view(request):
    #logout khi đăng nhập bằng session
    # request.session['user_id'] = None
    # request.session['user_name'] = None
    # request.session['user_email'] = None

    #logout khi đăng nhập bằng auth_user
    logout(request)
    return redirect('home')