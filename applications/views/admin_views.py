from django.shortcuts import render, redirect
from django.contrib import messages



from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect("admin_dashboard")

        messages.error(request, "Invalid admin credentials")

    return render(request, "faculty_requirement/admin/admin_login.html")


@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_dashboard(request):
    return render(request, "faculty_requirement/admin/admin_dashboard.html")


def admin_logout(request):
    logout(request)
    return redirect("/")