from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
import string

def US_home(request):
    return render(request,'US_home.html')

def calculator(request):
    if request.method == 'POST':
        try:
            str = request.POST.get('screen')
            result = eval(str)
            return render(request,'calculator.html',{'result': result})
        except:
            return render(request,'calculator.html',{'result': "Error"})
    return render(request,'calculator.html', {'result': 0})

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
    return render(request,'page.html')
