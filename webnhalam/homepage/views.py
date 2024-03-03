from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
import string
from .models import Category

def VN_home(request):
    context = {'item' : 123}
    return render(request,'VN_home.html',context)

def US_home(request):
    return render(request,'US_home.html')

def calculator(request):
    hisCal = request.session.get('hisCal', [])
    if request.method == 'POST':
        try:
            str = request.POST.get('screen')
            result = eval(str)
            #luu lich su
            hisCal.append({'str':str, 'result':result})
            request.session['hisCal'] = hisCal

            return render(request,'calculator.html',{'result': result, 'hisCal': hisCal})
        except:
            return render(request,'calculator.html',{'result': "Error", 'hisCal': hisCal})
    return render(request,'calculator.html', {'result': 0, 'hisCal': hisCal})

def RPSGame(request):
    if request.method == 'POST':
        mode = request.POST.get('submit')

        if mode == 'friend':
            letters = string.ascii_lowercase + string.digits
            id = ''.join(random.choice(letters) for i in range(6))
            return redirect('/RockPaperScissors/'+ id) #chuyển hướng url bằng url
        
        if mode == 'random':
            return redirect('RPSRandom') #chuyển hướng url bằng cách sử dụng name định tuyến thay vì url cụ thể.
        
    return render(request,'RPSGame.html')

def RPSMatch(request, id):
    full_url = request.build_absolute_uri()
    return render(request,'playRPS.html',{'link':full_url})

def RPSRandom(request):
    
    return render(request,'randomRPS.html')

def page(request):
    category = Category.objects.all()
    print(category)
    return render(request,'page.html',{"cate":category})
