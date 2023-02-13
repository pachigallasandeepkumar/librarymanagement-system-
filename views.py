from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render, redirect

from libraryapp.models import Student, Course, Book, Issue_Book


# Create your views here.
def regadm_fun(request):  # '''it will be redirect to register.html page'''

    return render(request, 'adminregister.html', {'data': ''})


def read_fun(request):
    user_name = request.POST['txtnm']
    user_email = request.POST['txtema']
    user_pswd = request.POST['txtpas']

    if User.objects.filter(Q(username=user_name) | Q(email=user_email)).exists():

        return render(request, 'adminregister.html', {'data': 'Username,email and password is already exists'})
    else:
        u1 = User.objects.create_superuser(username=user_name, email=user_email, password=user_pswd)
        u1.save()
        return redirect('log')

def regstu_fun(request):
    course=Course.objects.all()
    return render(request, 'studentregister.html', {'Course_data':course,'data': ''})



def readdata_fun(request):
    s1=Student()
    s1.Student_Name = request.POST['txtnm']
    s1.Student_Password  = request.POST['txtpas']
    s1.Student_Phno = request.POST['txtph']
    s1.Student_semester = request.POST['txtse']
    s1.Student_Course = Course.objects.get(Course_Name=request.POST['txtco'])
    s1.save()
    return redirect('log')

def log_fun(request):

    return render(request, 'login.html',{'data':''})


def logdata_fun(request):
    user_name = request.POST['txtnm']
    user_pswd = request.POST['txtpas']


    user1=authenticate(username=user_name, password=user_pswd)
    # Student1=Student.objects.filter(username=Stu_name, password=Stu_pswd)
    if user1 is not None:
        if user1.is_superuser:
            request.session['name'] = user_name
            return redirect('adhome')
        else:
            return render(request,'login.html',{'data':'User is not superuser'})
    elif Student.objects.filter(Q(Student_Name=user_name) | Q(Student_Password=user_pswd)).exists():
        request.session['name'] = user_name
        return redirect('sthome')
    else:
            return render(request,'login.html',{'data':'Enter Proper Details'})


def adhome_fun(request):
    return render(request,'adminhome.html',{'data':request.session["name"]})


def sthome_fun(request):
    return render(request,'studenthome.html',{'data':request.session["name"]})

def add_book_fun(request):

    course=Course.objects.all()
    return render(request, 'addbook.html',{'Course_data':course})

def adddata_fun(request):
    b1 = Book()
    b1.Book_Name = request.POST['txtB']
    b1.Author_Name = request.POST['txtA']
    b1.Course_Id = Course.objects.get(Course_Name=request.POST['txtco'])
    b1.save()
    return redirect('add')
    # return redirect(request,'add students.html',{'data':'student data inserted successfully'})

def display_fun(request):
    b1 = Book.objects.all()
    return render(request,'display.html',{'data':b1})


def update_fun(request,id):
    b1 = Book.objects.get(id=id)
    course=Course.objects.all()

    if request.method == 'POST':
        b1.Book_Name = request.POST['txtB']
        b1.Author_Name=request.POST['txtA']
        b1.Course_id = Course.objects.get(Course_Name=request.POST['txtco'])
        b1.save()

        return redirect('display')

    return render(request,'update.html',{'data':b1,'Course_data':course})


def delete_fun(request,id):
    b1 = Book.objects.get(id=id)
    b1.delete()
    return redirect('display')


def log_out_fun(request):

    return redirect('log')


def assi_fun(request):
    return render(request,'assignbook.html',{'msg':'','Student_data':'','Book_data':''})


def assign_fun(request):
         phno = request.POST['txtPhno']
         request.session['Phno'] = phno
         student=Student.objects.get(Student_Phno=phno)
         book = Book.objects.filter(Course_Id=student.Student_Course_id)
         if book.exists():
             return render(request,'assignbook.html',{'Student_data':student,'Book_data':book})
         else:
             return render(request,'assignbook.html',{'msg':'There is No students and Book Details '})

def readassign_fun(request):
    i1=Issue_Book()
    i1.Student_Name = Student.objects.get(Q(Student_Phno=request.session['Phno']))
    i1.Book_Name = Book.objects.get(Book_Name=request.POST['txtB'])
    i1.Start_Date = request.POST['txtst']
    i1.End_Date = request.POST['txten']
    i1.save()
    return redirect('assi')

def display1_fun(request):
    i1 = Issue_Book.objects.all()
    return render(request,'issuebook.html',{'Issue_data':i1})

def update1_fun(request,id):
    i1 = Issue_Book.objects.get(id=id)
    s1= Student.objects.get(id=i1.Student_Name_id)
    b1=Book.objects.filter(Course_Id=s1.Student_Course)
    if request.method  == 'POST':
        i1.Student_Name = Student.objects.get(Student_Name=request.POST['txtnm'])
        i1.Book_Name=Book.objects.get(Book_Name=request.POST['txtB'])
        i1.Start_Date = request.POST['txtStart']
        i1.End_Date = request.POST['txtEnd']
        i1.save()
        return redirect('issue')
    return render(request,'update1.html',{'Issue_data':i1,'book':b1})


def delete1_fun(request,id):
    i1 = Issue_Book.objects.get(id=id)
    i1.delete()
    return redirect('issue')


def issue1_fun(request):
    i1 = Issue_Book.objects.filter(Q(Student_Name=Student.objects.get(Student_Name=request.session['name']) ))
    return render(request,'issuestudent.html',{'Issue_data':i1})


