from django.urls import path
from . import views

urlpatterns = [
    path('', views.US_home, name='home'),
    path('Calculator/', views.calculator, name='calculator'),
    #Rock Paper Scissors
    path('RockPaperScissors/', views.RPSGame, name='RPSGame'),
    path('RockPaperScissors/random', views.RPSRandom, name='RPSRandom'),
    path('RockPaperScissors/<str:id>', views.RPSMatch, name='RPSMatch'),
    
    path('Chatbot/', views.chatbot, name='chatbot'),
    path('bot/', views.bot, name='bot'),
]