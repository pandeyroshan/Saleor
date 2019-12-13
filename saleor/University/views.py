from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# This view will be used for the end users of the website, that means that if they want to see how many
# university have the center and from where they can buy from


def home(request):
    return HttpResponse("<h1>This is sample URL of University</h1>")

def show_details(request):
    # Here I will use a good looking frontend template and list all the university
    pass


'''
We will include serveral functions here, as per the requirements


'''
