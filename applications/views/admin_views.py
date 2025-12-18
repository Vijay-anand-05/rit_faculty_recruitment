from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Count, Max


from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from applications.models import AdminLoginLog


def is_admin(user):
    return user.is_authenticated and user.is_superuser and user.is_active

@csrf_protect
def admin_login(request):

    # Already authenticated
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect("admin_dashboard")
        return HttpResponseForbidden("Unauthorized")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()

        ip = get_client_ip(request)
        ua = get_user_agent(request)

        user = authenticate(request, username=username, password=password)

        if user and is_admin(user):
            # ✅ Django already protects against session fixation
            login(request, user)

            # ✅ Rotate session key SAFELY (no CSRF break)
            request.session.cycle_key()

            AdminLoginLog.objects.create(
                user=user,
                username_attempted=username,
                action="LOGIN_SUCCESS",
                ip_address=ip,
                user_agent=ua,
                session_key=request.session.session_key,
            )

            return redirect("admin_dashboard")

        # ❗ Failed login audit
        AdminLoginLog.objects.create(
            user=None,
            username_attempted=username,
            action="LOGIN_FAILED",
            ip_address=ip,
            user_agent=ua,
        )

        messages.error(request, "Invalid admin credentials")

    return render(request, "faculty_requirement/admin/admin_login.html")
@login_required(login_url="admin_login")
@user_passes_test(is_admin, login_url="admin_login")
def admin_dashboard(request):
    """
    Admin-only dashboard
    """
    return render(request, "faculty_requirement/admin/admin_dashboard.html")


@login_required(login_url="admin_login")
def admin_logout(request):
    AdminLoginLog.objects.create(
        user=request.user,
        username_attempted=request.user.username,
        action="LOGOUT",
        ip_address=get_client_ip(request),
        user_agent=get_user_agent(request),
        session_key=request.session.session_key,
    )

    logout(request)
    request.session.flush()
    return redirect("/")

def logs(request):
    return render(request, "faculty_requirement/admin/logs.html")


@login_required(login_url="admin_login")
@user_passes_test(is_admin)
def admin_logs(request):

    # ---------------- BASE QUERYSET ----------------
    base_qs = AdminLoginLog.objects.all()

    # ---------------- FILTER VALUES ----------------
    username = request.GET.get("username", "")
    action = request.GET.get("action", "")
    ip = request.GET.get("ip", "")
    ua = request.GET.get("ua", "")

    if username:
        base_qs = base_qs.filter(username_attempted=username)

    if action:
        base_qs = base_qs.filter(action=action)

    if ip:
        base_qs = base_qs.filter(ip_address=ip)

    if ua:
        base_qs = base_qs.filter(user_agent=ua)

    # ---------------- ANALYTICS (FILTER AWARE) ----------------
    analytics = {
        "total": base_qs.count(),
        "success": base_qs.filter(action="LOGIN_SUCCESS").count(),
        "failed": base_qs.filter(action="LOGIN_FAILED").count(),
        "unique_users": base_qs.values("username_attempted").distinct().count(),
        "unique_ips": base_qs.values("ip_address").distinct().count(),
        "last_login": base_qs.aggregate(last=Max("timestamp"))["last"],
    }

    # ---------------- LOG TABLE ----------------
    logs_qs = (
        base_qs.only(
            "timestamp",
            "username_attempted",
            "action",
            "ip_address",
            "user_agent",
        )
        .order_by("-timestamp")
    )

    paginator = Paginator(logs_qs, 50)
    page_obj = paginator.get_page(request.GET.get("page"))

    # ---------------- DROPDOWNS (NO DUPLICATES – MySQL SAFE) ----------------
    usernames = (
        AdminLoginLog.objects
        .exclude(username_attempted__isnull=True)
        .exclude(username_attempted="")
        .order_by("username_attempted")
        .values_list("username_attempted", flat=True)
        .distinct()[:200]
    )

    ips = (
        AdminLoginLog.objects
        .exclude(ip_address__isnull=True)
        .order_by("ip_address")
        .values_list("ip_address", flat=True)
        .distinct()[:200]
    )

    user_agents = (
        AdminLoginLog.objects
        .exclude(user_agent__isnull=True)
        .exclude(user_agent="")
        .order_by("user_agent")
        .values_list("user_agent", flat=True)
        .distinct()[:200]
    )

    return render(
        request,
        "faculty_requirement/admin/admin_logs.html",
        {
            "page_obj": page_obj,
            "analytics": analytics,
            "usernames": usernames,
            "ips": ips,
            "user_agents": user_agents,
            "filters": {
                "username": username,
                "action": action,
                "ip": ip,
                "ua": ua,
            },
        },
    )




def get_client_ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


def get_user_agent(request):
    return request.META.get("HTTP_USER_AGENT", "unknown")
