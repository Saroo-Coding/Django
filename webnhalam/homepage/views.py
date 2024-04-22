from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
import random
import string
import json
from difflib import get_close_matches

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

#chatbot
def load_knowledge_base(file_knowledge):
    with open(file_knowledge, 'r', encoding='utf-8') as file:
        return json.load(file)

def save_knowledge_base(file_knowledge, data):
    with open(file_knowledge, 'w', encoding='utf-8') as file:#mở viết file
        json.dump(data, file, indent=2, ensure_ascii=False)#data python đc viết vào file theo type json

def find_best_match(user_quest, data_quest): #tìm câu hỏi gần đúng nhất
    matches = get_close_matches(user_quest, data_quest, n=1, cutoff=0.7) #n là số lượng kết quả gần giống nhất bạn muốn
    return matches[0] if matches else None

def answer_quest(quest, knowledge_base):
    for q in knowledge_base["question"]:
        if q["question"] == quest:
            return q["answer"]
    return None
        
def bot(request):
    knowledge_base = load_knowledge_base('knowledge_base.json') #load file json
    data = json.loads(request.body) #lay body tu fetch 
    user_input = str(data['input'])

    while True:
        if user_input.lower() == 'quit':
            return JsonResponse('See you later !', safe=False)
        
        best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["question"]])
        
        if best_match:
            answer = answer_quest(best_match, knowledge_base)
            if answer == "none":
                return JsonResponse("Sorry, I don't understand what you mean !")
            else:
                return JsonResponse(answer, safe=False)
        else:
            knowledge_base["question"].append({"question": user_input, "answer": "Sorry, I don't understand what you mean !"})
            save_knowledge_base('knowledge_base.json', knowledge_base)
            return JsonResponse("Sorry, I don't understand what you mean !", safe=False)

def chatbot(request):
    return render(request,'chatbot.html')