from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .forms import CreateUserForm,LoginForm,BookSearchForm,BookForm,ProfileForm
from .models import Profile,Book

labels = {
     'title_label': 'Title',
     'author_label': 'Author',
     'edition_label': 'Edition',
     'course_label': 'Course',
}

def home(request):
    
    return render(request, 'shareab/index.html')

#Register

def register(request):
   
    form = CreateUserForm()

    if request.method == "POST":
          form = CreateUserForm(request.POST,request.FILES)

          if form.is_valid():
               user=form.save()
               Profile.objects.create(user=user,profile_image=form.cleaned_data['profile_image'], campus=form.cleaned_data['campus'])
               return redirect('login')
          
    else:
         form = CreateUserForm()            
    context = {"form": form}
    return  render(request, 'shareab/register.html', context)


#login user
def my_login(request):
     
    form = LoginForm()

    if request.method == 'POST':
          
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
               
               username = request.POST.get('username')
               password = request.POST.get('password')

               user = authenticate(request, username=username, password=password)
               if user is not None:
                    auth.login(request,user)
                    request.session['profile_image'] = user.profile.profile_image.url if user.profile.profile_image else '/path/to/default/image.jpg'
                    return redirect("dashboard")
    context = {'form':form}

    return render (request,'shareab/login.html',context=context)

@login_required(login_url='login')
def dashboard(request):
    form = BookSearchForm()
    return render(request, 'shareab/dashboard.html', {'form': form})

@login_required(login_url='login')
def search_books(request):
    results = None
    if request.method == 'GET' and 'search_query' in request.GET:
        form = BookSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['search_query']
            results = Book.objects.filter(title__icontains=query)
    else:
        form = BookSearchForm()

    return render(request, 'shareab/dashboard.html', {'form': form, 'results': results})

    


# adding a book
@login_required(login_url='login')
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            author = form.cleaned_data['author']
            course = form.cleaned_data['course']
            edition = form.cleaned_data['edition']
            image = form.cleaned_data['image']
            user = request.user
            new_book = Book.objects.create(title=title, author=author, course=course, edition=edition, image=image, user=user)
            
            books = Book.objects.filter(user=user).values('title', 'author', 'course', 'edition', 'image')

    else:
        form = BookForm()

    user_books = Book.objects.filter(user=request.user)
    return render(request, 'shareab/add_book.html', {'form': form, 'user_books': user_books, 'labels': labels})


#delelte a book

@login_required(login_url='login')
def delete_book(request,book_id):
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('add_book')
    return render(request, 'shareab/confirm_delete.html', {'book': book}) 

@login_required(login_url='login')
def profile(request):
    user_profile= get_object_or_404(Profile,user=request.user)
    user_books = Book.objects.filter(user=request.user)
    if request.method == 'POST' and 'delete_account' in request.POST:
        user = request.user
        logout(request)
        user.delete()
        return redirect('home')
    return render(request, 'shareab/profile.html', {'user_profile': user_profile, 'user_books': user_books})

#user profile view
@login_required(login_url='login')
def Profile_view(request):
    user_profile, created = Profile.objects.get_or_create(user=request.user)
    user_books_count = Book.objects.filter(user=request.user).count()
    return render(request, 'shareab/profile.html', {
        'user_profile': user_profile,
        'user_books_count': user_books_count,
        'user': request.user
    })

# delete account function
@login_required(login_url='login')
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, 'Account deleted successfully')
        return redirect('')
    return render(request, 'shareab/delete_account.html')   


#update user profile
@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():  
            updated_profile = form.save()
            request.session['profile_image'] = updated_profile.profile_image.url if updated_profile.profile_image else '/path/to/default/image.jpg'
            messages.success(request, "Your profile has been updated.")
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user.profile)
    return render(request, 'shareab/edit_profile.html', {'form': form})
    
    
    #logout user
def my_logout(request):
     
     auth.logout(request)

     return redirect("login")
          
