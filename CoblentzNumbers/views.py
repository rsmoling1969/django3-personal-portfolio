from django.shortcuts import render, redirect, get_object_or_404
from CoblentzNumbers.models import CoblentzNumbers
from datetime import date
from .forms import ShiftForm, ShiftDetailForm
from .models import CoblentzNumbers
from datetime import date, datetime, time, timedelta
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError

def all_shifts(request):
    #shift_count = CoblentzNumbers.objects.count()
    #rint(str(shift_count) + " is the number of shift objects")
    #shifts = CoblentzNumbers.objects.order_by('-date')[:10]
    shifts = CoblentzNumbers.objects.filter(user=request.user).order_by('-date')[:10]
    #print(str(shifts))
    #first_date = shifts[0].date
    #print(first_date)
    #second_date = shifts[1].date
    #print(second_date)
    random_text = 'Random Text'
    return render(request, 'CoblentzNumbers/all_shifts.html',
                  {'shifts': shifts})

def shift_detail(request, shift_id):
    shift = get_object_or_404(CoblentzNumbers, pk=shift_id)
    if request.method == 'GET':
        form = ShiftForm(instance=shift)
        return render(request, 'CoblentzNumbers/detail.html', {'shift': shift, 'form': form})
    else:
        try:
            form = ShiftDetailForm(request.POST, instance=shift)
            #print(f"The form itself: {str(form.shift)}")
            form_date = request.POST.get('date')
            print(f"The date retrieved from the form is {form_date}")
            if form.is_valid():
                form_numbers = request.POST.get('numbers')
                print(f"The form numbers are: {form_numbers}")
                form.save()
                return render(request,  'CoblentzNumbers/detail.html', {'shift': shift, 'form': form, 'success': 'Saved'})
            else:
                print('form error is: ' + str(form.errors))
                return render(request, 'CoblentzNumbers/detail.html', {'form': form})
        except ValueError as e:
            return render(request, 'CoblentzNumbers/detail.html', {'form': ShiftDetailForm(), 'error': f'Bad Data - {e}',})

def valid_numbers(numbers):
    # ensure that:
    # 1. every value is a number and/or whitespace, and not counted in the next thing
    # 2. all the *numbers* are strictly ascending (more important that the first point)
    highestNumber = 0
    currentLine = 1
    returnValue = 'Good'
    numberList = numbers.split(",")
    for number in numberList:
        if number.isspace()  or len(number) == 0:
            currentLine += 1
            continue
        elif number.isnumeric():
            if int(number) >= highestNumber:
                highestNumber = int(number)
            else:
                print(f"***highest number is {highestNumber}, current number is {number}, current line is {currentLine}")
                returnValue = 'Numbers must never be descending! Check line ' + str(currentLine)
                break
        else:
            returnValue = 'No non-numeric values allowed! Check line ' + str(currentLine)
        currentLine += 1
    return returnValue

#def create_shift(request):
#    today = date.today()
#    print(today)
#    return render(request, 'CoblentzNumbers/create.html', {'myToday': today})

def create_shift(request):
    if request.method == "GET":
        return render(request, 'CoblentzNumbers/create.html', {'form': ShiftForm()})
    else:
        try:
            print('CREATING NEW SHIFT')
            form = ShiftForm(request.POST)
            print('WE HAVE THE FORM')
            newShift = form.save(commit=False)
            print('WE HAVE THE NEW SHIFT')
            print(str(newShift))
            print(request.user)
            newShift.user = request.user
            print('request.user = ' + str(newShift.user))
            print(f"Day of week: {newShift.date.weekday()}")
            print(f"newShift.date is {newShift.date.weekday()}")
            print(f"Shift is {newShift.shift}")
            if newShift.date.weekday() < 4 or newShift.shift == 'AM':
                newShift.numbers = " , , , , , , , , , , , , , "
            else:
                newShift.numbers = " , , , , , , , , , , , "
            newShift.save()
            return redirect('CoblentzNumbers:shift_detail', newShift.id)
        except ValueError as error:
            print(error)
            return render(request, 'CoblentzNumbers/create.html', {'form': ShiftForm(), 'error': 'This shift already exists'})

def signupuser(request):
    if request.method == "GET":
        return render(request, 'CoblentzNumbers/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('CoblentzNumbers:all_shifts')
            except:
                return render(request, 'CoblentzNumbers/signupuser.html', {'form': UserCreationForm(), 'error': 'Username already in use - choose another'})
        else:
            print("The passwords don't match")
            return render(request, 'CoblentzNumbers/signupuser.html', {'form': UserCreationForm(), 'error': 'Passwords do not match'})

def logoutuser(request):
    if request.method == "POST":
        logout(request)
        return redirect('CoblentzNumbers:home')

def home(request):
    if request.user.is_authenticated:
        return redirect('CoblentzNumbers:all_shifts')
    else:
        return render(request, 'CoblentzNumbers/home.html')

def loginuser(request):
    if request.method == "GET":
        return render(request, 'CoblentzNumbers/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            print('user is none')
            return render(request, 'CoblentzNumbers/loginuser.html', {'form': AuthenticationForm(), 'error': 'Username and password did not match'})
        else:
            print('user is someone')
            login(request, user)
            print('login was successful?')
            return redirect('CoblentzNumbers:all_shifts')

