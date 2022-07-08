from django.contrib import messages

from .forms import ProfileForm, UserForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse
from .forms import ProfileForm


def userpage(request):
    # user_form = UserForm(instance=request.user)
    # profile_form = ProfileForm(instance=request.user)
    #
    # return render(request=request, template_name="user.html",
    #               context={"user": request.user, "user_form": user_form, "profile_form": profile_form})
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, ('Your wishlist was successfully updated!'))
        else:
            messages.error(request, ('Unable to complete request'))
        return redirect("main:userpage")
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user)
    return render(request=request, template_name="user.html", context={"user": request.user,
                                                                            "user_form": user_form,
                                                                            "profile_form": profile_form})
