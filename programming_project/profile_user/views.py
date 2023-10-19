from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView, UpdateView

from .forms import UserForm, ProfileForm, UserProfileForm
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from forum.models import Topic

from .models import Profile

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

                                                                       "profile_form": profile_form,
                                                                       })


class DeleteProfile(DeleteView):
    model = User

    # success_url = reverse_lazy("forum:main")
    def get_success_url(self):
        return reverse('forum:main')


class ProfileUpdate(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'profile_form.html'

    def get_success_url(self):
        return reverse('profile_user:userpage', kwargs={"id": self.object.id})


def avatar_img(request):
    profile = request.user
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'user.html', context)
