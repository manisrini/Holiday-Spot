from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.http import HttpResponse
from .models import Location,Review,Visited
from datetime import  datetime
from .forms import CommentForm,SearchForm,FeedBackForm
import urllib.request
import json


def removespace(word):
  newword = ''
  for i in word:
    if i!= ' ':
      newword = newword + i
  return newword



def home(request):

    if request.method == 'POST':
     
        print("hi")
        searchlist = []
        try:
          if(request.POST['query']):
              query = request.POST['query'].lower()
              locations = Location.objects.all()
              
              for loc in locations:
                
                statesearch = loc.state.lower() 
                citysearch =  loc.city.lower()
                
                
                if removespace(statesearch) == removespace(query) or removespace(citysearch) == query.lower().strip():
                  searchlist.append(loc)

        except:
            print("here")
            feedform = FeedBackForm(request.POST)
            if feedform.is_valid():
              feedform.save()
              
            else:
              print("error")
              return HttpResponse("Error in form")

        form = SearchForm()
        feedform = FeedBackForm()
        print(searchlist)
        context = {
        'location' : searchlist,
        'form' : form,
        'feedform' : feedform
          }    

        return render(request,'holspot/index.html',context)

    # get 
    else:

      form = SearchForm()
      feedform = FeedBackForm()
      locations = Location.objects.all()
      context = {
        'location' : locations,
        'form' : form,
        'feedform' : feedform
      }    

      return render(request,'holspot/index.html',context)


@login_required(login_url="/login")
def detailed_location(request,pk_from_url):

    
    if request.method == "POST":
      print(request.POST)

      form = CommentForm(request.POST)
      if form.is_valid():
        print("here")
        findlocation = Location.objects.get(id=pk_from_url)
        review = form.save(commit=False)
        review.author = request.user
        review.location = findlocation
        myDate = datetime.now()
    
    # Give a format to the date
    # Displays something like: Aug. 27, 2017, 2:57 p.m.
        review.currentdate= myDate.strftime("%Y-%m-%d %H:%M:%S")
        print(review.currentdate)
        review.save()


      return redirect(request.path)

    else:
    
      findlocation = Location.objects.get(id=pk_from_url)
      comments = Review.objects.filter(location=findlocation)
      form = CommentForm()

      # get visited list
      # visitedplaces = []
      
      try:
        source = urllib.request.urlopen("http://api.openweathermap.org/data/2.5/forecast?q="+ findlocation.state + "&appid=0b6d16ca7474370fb60576f0a081d169").read()
        list_of_data = json.loads(source)
      except:
        return redirect("/")
      days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

      currDate = datetime.now()
      
      weekdayindex = currDate.weekday()
      temperature=[]
      weather = []
     

    
      for i in range(7):
        temperature.append(list_of_data['list'][i]['main']['temp']-273.15)
        weather.append(list_of_data['list'][i]['weather'][0]['main'])

      next7days = []
      temp = {}
      for i in days[weekdayindex:]:
          next7days.append(i)

      for i in range(7-len(next7days)):
          next7days.append(days[i])
      
      for i in range(7):
        temp[next7days[i]] = [temperature[i],weather[i]]

      # print(temp)
      context = {
        'foundloc' : findlocation,
        'form' : form,
        'comments' : comments,
        'weekdays' : next7days,
        'temperature' : temp,
        }
      return render(request,'holspot/detail_location.html',context)



  
@login_required(login_url="/login")
def profile(request,pk_from_url):
  mycomments = Review.objects.filter(author = request.user)
  myvisits = Visited.objects.filter(user = request.user)
  context = {
    'user' : request.user,
    'comments' : mycomments,
    'visits' : myvisits
  }
  return render(request,'holspot/profile.html',context)


