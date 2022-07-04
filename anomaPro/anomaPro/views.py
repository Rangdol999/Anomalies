from django.http import HttpResponse
from django.shortcuts import render

def home(request):
  return render(request, 'home.html')
  
def main(request):
  return render(request, 'main.html')

def oneParis(request):
  return render(request, 'oneParis.html')