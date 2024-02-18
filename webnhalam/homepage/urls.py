from django.urls import path
from . import views

urlpatterns = [
    path('', views.US_home, name='home'),
    path('us/', views.US_home, name='us'),
    path('vn/', views.VN_home, name='vn'),
    path('Calculator/', views.calculator, name='calculator'),
    #Rock Paper Scissors
    path('RockPaperScissors/', views.RPSGame, name='RPSGame'),
    path('RockPaperScissors/random', views.RPSRandom, name='RPSRandom'),
    path('RockPaperScissors/<str:id>', views.RPSMatch, name='RPSMatch'),
    
    path('page/', views.page, name='page'),
]