from django.contrib.auth import get_user_model
from .forms import UserForm, ProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from forum.models import Bookmarks

from forum.models import Topic

User = get_user_model()


@login_required
def profile(request):
    return render(request, 'user.html')


def userpage(request, id):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, ('Your wishlist was successfully updated!'))
        else:
            messages.error(request, ('Unable to complete request'))
        return redirect("profile_user:userpage", id)
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user)
    return render(request=request, template_name="user.html", context={"user": request.user,
                                                                       "user_form": user_form,
                                                                        "bookmarks": Bookmarks.objects.filter(
                                                                            user=request.user),
                                                                        "profile_form": profile_form,
                                                                       })





def avatar_img(request):
    profile = request.user
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'user.html', context)
