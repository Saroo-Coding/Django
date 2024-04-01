from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import Category, Products, Oder, Cart, Customer, Payments, Coupon
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import datetime
import json
from django.db.models import F,Q #F() thực hiện các phép toán toán học #Q() sử dụng để tạo điều kiện tìm kiếm phức tạp AND, OR, và NOT.
from django.db.models.functions import Random 
from django.core.paginator import Paginator
import re
import hashlib

#filter(): Chọn các bản ghi từ cơ sở dữ liệu dựa trên điều kiện: queryset = MyModel.objects.filter(some_field=some_value) 
#Trong filler có: (name__icontains = value) = %value% || (name__contains = value) tìm kiếm chính xác || (name__startswith = value) = value% || (name__endswith = value) = %value
#exclude(): Loại bỏ các bản ghi từ cơ sở dữ liệu dựa trên điều kiện: queryset = MyModel.objects.exclude(some_field=some_value)
#get(): Lấy một bản ghi duy nhất từ cơ sở dữ liệu dựa trên điều kiện: obj = MyModel.objects.get(some_field=some_value)
#all(): Lấy tất cả các bản ghi từ cơ sở dữ liệu: queryset = MyModel.objects.all()
#create(): tạo ra một bản ghi mới trong cơ sở dữ liệu và lưu nó: YourModel.objects.create(field1=value1, field2=value2, ...)
#update(): Cập nhật tất cả hoặc có điều kiện: YourModel.objects.filter(điều kiện).update(field1=new_value1, field2=new_value2)
#delete(): Xóa bản ghi: YourModel.objects.filter(điều kiện).delete()
#order_by(): Sắp xếp kết quả theo một hoặc nhiều trường: queryset = MyModel.objects.all().order_by('some_field')
#annotate(): Thêm các trường tính toán vào kết quả truy vấn: queryset = MyModel.objects.values('some_field').annotate(count=Count('id'))
#select_related(): sử dụng cho quan hệ one-to-one hoặc quan hệ one-to-many: MyModel.objects.select_related('tên khóa ngoại').all()
#prefetch_related(): sử dụng cho quan hệ many-to-many và quan hệ one-to-many ngược: MyModel.objects.prefetch_related('tên khoá ngoại').all()
#Sử dụng filter với các điều kiện so sánh __gte và __lte: queryset = YourModel.objects.filter(from__gte=start, to__lte=end)

def home(request):
    topPro = Products.objects.all().order_by(Random())[:3]
    return render(request,'home.html',{'topPro':topPro})

def shop(request):
    cate = Category.objects.all()
    page_number = request.GET.get('page')
    if request.method == 'POST':
        price = request.POST.get('range')
        if price == '0' : price = 100000
        category = request.POST.get('cate')
        if category == 'hiden' : category = Q()
        name = request.POST.get('namePro')
        if not name : name = Q()

        filterPro = Products.objects.filter(unitprice__gte=0, unitprice__lte=price, idcategory = category, name__icontains = name)
        paginator = Paginator(filterPro, 8 ) #Lấy 8 pro mỗi trang
        pro = paginator.get_page(page_number)
    else:
        allPro = Products.objects.all()
        paginator = Paginator(allPro, 8 ) #Lấy 8 pro mỗi trang
        pro = paginator.get_page(page_number)
        
    return render(request,'shop.html',{'pro':pro, 'cate':cate})

def services(request):
    topPro = Products.objects.all().order_by(Random())[:3]
    return render(request,'services.html',{'topPro':topPro})

def contact(request):
    return render(request,'contact.html')

#profile
def profile(request):
    if request.user.is_authenticated:
        cus = Customer.objects.filter(idcus = request.user.id).first()
        bill = Oder.objects.filter(idcus = request.user.id)
        return render(request,'profile.html',{'cus':cus,'bill':bill})
    else:
        return redirect('homeshop')

def detail(request, idDetail):
    if request.user.is_authenticated:
        cart_list = Cart.objects.prefetch_related('idpro').filter(idcus = request.user.id, idoder = idDetail) # sử dụng 2 gạch (__) để lấy trường qua khóa
        bill = Oder.objects.prefetch_related('coupon').filter(idcus = request.user.id, idoder = idDetail).first()
        return render(request,'detail.html',{'cart_list':cart_list, 'bill':bill})
    else:
        return redirect('homeshop')

def coupon(request):
    if request.user.is_authenticated:
        cp = Coupon.objects.filter(idcus = request.user.id)
        return render(request,'coupon.html',{'cp':cp})
    else:
        return redirect('homeshop')

#cart 
def cart(request):
    if request.user.is_authenticated:
        cart_list = Cart.objects.prefetch_related('idpro').filter(idcus = request.user.id, idoder = None) # sử dụng 2 gạch (__) để lấy trường qua khóa
        total = sum([x.total for x in cart_list])
        return render(request,'cart.html',{'cart_list':cart_list, 'total':total})
    else:
        return redirect('homeshop')

def addPro(request):
    if request.user.is_authenticated:
        data = json.loads(request.body) #lay body tu fetch 
        idPro = int(data['idPro'])
        quantity = 1
        idCus = request.user.id
        
        cart_item = Cart.objects.filter(idpro=idPro, idcus=idCus, idoder = None).first() # Nếu sản phẩm đã tồn tại quantity += 1
        if cart_item:
            cart_item.quantity += 1
            cart_item.total += cart_item.total 
            cart_item.save()
            return JsonResponse('Cộng thêm vào giỏ hàng thành công !!!', safe=False)
        else: # thêm mới
            product = Products.objects.get(idpro=idPro)
            customer = Customer.objects.get(idcus=idCus)
            Cart.objects.create(idpro=product, quantity=quantity, idcus=customer, total = product.unitprice)
            return JsonResponse('Thêm mới vào giỏ hàng thành công !!!', safe=False)
    else:
        return redirect('homeshop')

def updateCart(request):
    if request.user.is_authenticated:
        data = json.loads(request.body) #lay body tu fetch 
        idDetail = int(data['idDetail'])
        acction = data['acction']
        idCus = request.user.id

        cart_item = Cart.objects.filter(iddetail = idDetail, idcus=idCus).first()
        product_item = Products.objects.filter(idpro = cart_item.idpro_id).first()
        if acction == 'add':
            cart_item.quantity += 1
            cart_item.total = cart_item.quantity * product_item.unitprice
            cart_item.save()
        if acction == 'minus':
            cart_item.quantity -= 1
            cart_item.total = cart_item.quantity * product_item.unitprice
            cart_item.save()
        if acction == 'remove':
            Cart.objects.filter(iddetail = idDetail).delete()

        #tính tổng tiền ở đây
        cart_list = Cart.objects.filter(idcus = request.user.id, idoder = None)
        newTotal = sum([x.total for x in cart_list])

        return JsonResponse({"total":cart_item.total,"newTotal":newTotal, "acction":acction}, safe=False)
    else:
        return redirect('homeshop')

#pay bill
def bill(request):
    if request.user.is_authenticated:
        cart_list = Cart.objects.filter(idcus = request.user.id, idoder = None)
        if not cart_list:
            return redirect('homeshop')
        else:
            cus = Customer.objects.filter(idcus = request.user.id).first()
            coupons = Coupon.objects.filter(idcus = request.user.id)
            total = sum([x.total for x in cart_list])
            return render(request,'bill.html',{'cus':cus, 'total':total,'cart_list':cart_list,'coupons':coupons})
    else:
        return redirect('homeshop')

def addCoupon(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        name = data['name'].upper()
        idCus = request.user.id
        
        dis = Coupon.objects.filter(name = name, idcus = idCus).first()
        if dis:
            cart_list = Cart.objects.filter(idcus = request.user.id, idoder = None)
            total = sum([x.total for x in cart_list])
            
            newTotal = total * ((100 - dis.discount) / 100)
            return JsonResponse({"dis":dis.discount, "newTotal":newTotal}, safe=False)
        else:
            return JsonResponse({}, safe=False)
    else:
        return redirect('homeshop')

def pay(request):
    if request.user.is_authenticated:
        try:
            data = json.loads(request.body)
            oderDate = datetime.now()
            cus = Customer.objects.filter(idcus = request.user.id).first()
            idPay = Payments.objects.filter(idpay = data['idPay']).first()
            cart_list = Cart.objects.filter(idcus = request.user.id, idoder = None)
            amount = sum([x.total for x in cart_list])
            quantity = sum([x.quantity for x in cart_list])
            coupon = data['idCoupon']
            if coupon == '':
                coupon = None
                total = amount
            else:
                dis = Coupon.objects.filter(name = coupon, idcus = request.user.id).first()
                coupon = dis
                total = amount * ((100 - dis.discount) / 100)
            #lưu mới oder
            oder = Oder.objects.create(oderdate = oderDate, idcus = cus, idpay = idPay, amount = amount, coupon = coupon, total = total, quantity = quantity)
            #cập nhật cart
            for x in cart_list:
                x.idoder = oder
                x.save()
            return JsonResponse('succes',safe=False)
        except:
            return JsonResponse('error',safe=False)
    else:
        return redirect('homeshop')

#login & register
def hash_password(password):
    # Sử dụng thuật toán băm SHA256
    hash_object = hashlib.sha256(password.encode())
    # Lấy chuỗi băm dưới dạng hex
    hashed_password = hash_object.hexdigest()
    return hashed_password    

def login_view(request):
    if request.user.is_authenticated:
        return redirect('homeshop')
    else:
        if request.method == 'POST':
            acc = request.POST.get('email')
            pas = request.POST.get('pass')

            try:
                pas = hash_password(pas)
                #cách đăng nhập bằng query rồi lưu vào session và đây là cách đưa ra temaplate {{request.session.user_name}}
                # user = Customer.objects.get(email = acc, pass_field = pas)
                # request.session['user_id'] = user.idcus
                # request.session['user_name'] = user.lastname
                # request.session['user_email'] = user.email

                #cách đăng nhập bằng auth_user
                # user = authenticate(request, email = acc, password = pas) #bi lỗi gì á 
                if User.objects.filter(email = acc, password = pas).exists():
                    login(request, User.objects.get(email = acc, password = pas))
                    return redirect('homeshop')
                else:
                    messages.error(request, 'Tài khoản hoặc mật khẩu không đúng.')
                    return redirect('login')
                
            except Exception as e:
                print(e)
                messages.error(request, 'Đã có lỗi xảy ra !!!')
            
    return render(request,'login.html')

def sign_view(request):
    if request.user.is_authenticated:
        return redirect('homeshop')
    else:
        if request.method == 'POST':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            acc = request.POST.get('email')
            pas = request.POST.get('pass')
            created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S %z')
            regex = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"
            try:
                if Customer.objects.filter(email = acc).exists():
                    messages.info(request, 'Email đã được đăng ký.')
                    return redirect('sign')
                elif Customer.objects.filter(phone = phone).exists():
                    messages.info(request, 'Số điện thoại đã được đăng ký.')
                    return redirect('sign')
                elif bool(re.match(regex, pas)) == False:
                    messages.info(request, 'Mật khẩu không phù hợp.')
                    return redirect('sign')      
                else:
                    pas = hash_password(pas)
                    cus = Customer.objects.create(created_at = created_at, lastname=name, phone=phone, email=acc, pass_field=pas)
                    # request.session['user_id'] = cus.idcus
                    # request.session['user_name'] = cus.lastname
                    # request.session['user_email'] = cus.email
                    
                    #cách tạo và đăng nhập bằng auth_user
                    user = User.objects.create(id = cus.idcus, date_joined = created_at, username = name, last_name = name, email = acc, password = pas) #tạo auth_user
                    # user = authenticate(request, email=acc, password=pas) #xác thực người dùng # bi lỗi gì á 
                    if user is not None:
                        login(request, user)
                        return redirect('homeshop')
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
    return redirect('homeshop')