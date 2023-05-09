import datetime
from django.shortcuts import redirect, render, get_object_or_404
import json
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from smsApp import models, forms
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
import pandas as pd
from smsApp.models import Members


# function is used to obtain some context data for a web page, such as the base URL of the web application and some default values for various variables that control the rendering of the page.


def context_data(request):
    fullpath = request.get_full_path()
    abs_uri = request.build_absolute_uri()
    abs_uri = abs_uri.split(fullpath)[0]
    context = {
        "system_host": abs_uri,
        "page_name": "",
        "page_title": "",
        "system_name": "Membership Managament System",
        "topbar": True,
        "footer": True,
    }

    return context


#  This function handles the user registration page request by rendering the registration form to the user.
def userregister(request):
    context = context_data(request)
    context["topbar"] = False
    context["footer"] = False
    context["page_title"] = "User Registration"
    if request.user.is_authenticated:
        return redirect("page")
    return render(request, "register.html", context)


def save_register(request):
    resp = {"status": "failed", "msg": ""}
    if not request.method == "POST":
        resp["msg"] = "No data has been sent on this request"
    else:
        form = forms.SaveUser(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Account has been created succesfully")
            resp["status"] = "success"
        else:
            for field in form:
                for error in field.errors:
                    if resp["msg"] != "":
                        resp["msg"] += str("<br />")
                    resp["msg"] += str(f"[{field.name}] {error}.")

    return HttpResponse(json.dumps(resp), content_type="application/json")


# This function handles the user profile update request by rendering the profile update form to the user and processing the form submission.
@login_required
def update_profile(request):
    context = context_data(request)
    context["page_title"] = "Update Profile"
    user = User.objects.get(id=request.user.id)
    if not request.method == "POST":
        form = forms.UpdateProfile(instance=user)
        context["form"] = form
        print(form)
    else:
        form = forms.UpdateProfile(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile has been updated")
            return redirect("profile-page")
        else:
            context["form"] = form

    return render(request, "manage_profile.html", context)


@login_required
def update_password(request):
    context = context_data(request)
    context["page_title"] = "Update Password"
    if request.method == "POST":
        form = forms.UpdatePasswords(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your Account Password has been updated successfully"
            )
            update_session_auth_hash(request, form.user)
            return redirect("profile-page")
        else:
            context["form"] = form
    else:
        form = forms.UpdatePasswords(request.POST)
        context["form"] = form
    return render(request, "update_password.html", context)


# Create your views here.
def login_page(request):
    context = context_data(request)
    context["topbar"] = False
    context["footer"] = False
    context["page_name"] = "login"
    context["page_title"] = "Login"
    return render(request, "login.html", context)


def login_user(request):
    logout(request)
    resp = {"status": "failed", "msg": ""}
    username = ""
    password = ""
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                resp["status"] = "success"
            else:
                resp["msg"] = "Incorrect username or password"
        else:
            resp["msg"] = "Incorrect username or password"
    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def home(request):
    context = context_data(request)
    context["page"] = "home"
    context["page_title"] = "Home"
    context["groups"] = (
        models.Groups.objects.filter(delete_flag=0, status=1).all().count()
    )
    context["active_members"] = (
        models.Members.objects.filter(delete_flag=0, status=1).all().count()
    )
    context["inactive_members"] = (
        models.Members.objects.filter(delete_flag=0, status=0).all().count()
    )
    context["users"] = User.objects.filter(is_superuser=False).all().count()
    return render(request, "home.html", context)


def logout_user(request):
    logout(request)
    return redirect("login-page")


@login_required
def profile(request):
    context = context_data(request)
    context["page"] = "profile"
    context["page_title"] = "Profile"
    return render(request, "profile.html", context)


@login_required
def users(request):
    context = context_data(request)
    context["page"] = "users"
    context["page_title"] = "User List"
    context["users"] = (
        User.objects.exclude(pk=request.user.pk).filter(is_superuser=False).all()
    )
    return render(request, "users.html", context)


@login_required
def save_user(request):
    resp = {"status": "failed", "msg": ""}
    if request.method == "POST":
        post = request.POST
        if not post["id"] == "":
            user = User.objects.get(id=post["id"])
            form = forms.UpdateUser(request.POST, instance=user)
        else:
            form = forms.SaveUser(request.POST)

        if form.is_valid():
            form.save()
            if post["id"] == "":
                messages.success(request, "User has been saved successfully.")
            else:
                messages.success(request, "User has been updated successfully.")
            resp["status"] = "success"
        else:
            for field in form:
                for error in field.errors:
                    if not resp["msg"] == "":
                        resp["msg"] += str("<br/>")
                    resp["msg"] += str(f"[{field.name}] {error}")
    else:
        resp["msg"] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def manage_user(request, pk=None):
    context = context_data(request)
    context["page"] = "manage_user"
    context["page_title"] = "Manage User"
    if pk is None:
        context["user"] = {}
    else:
        context["user"] = User.objects.get(id=pk)

    return render(request, "manage_user.html", context)


@login_required
def delete_user(request, pk=None):
    resp = {"status": "failed", "msg": ""}
    if pk is None:
        resp["msg"] = "user ID is invalid"
    else:
        try:
            User.objects.filter(pk=pk).delete()
            messages.success(request, "User has been deleted successfully.")
            resp["status"] = "success"
        except:
            resp["msg"] = "Deleting user Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def groups(request):
    context = context_data(request)
    context["page"] = "groups"
    context["page_title"] = "Group List"
    context["groups"] = models.Groups.objects.filter(delete_flag=0).all()
    return render(request, "groups.html", context)


@login_required
def save_group(request):
    resp = {"status": "failed", "msg": ""}
    if request.method == "POST":
        post = request.POST
        if not post["id"] == "":
            group = models.Groups.objects.get(id=post["id"])
            form = forms.SaveGroup(request.POST, instance=group)
        else:
            form = forms.SaveGroup(request.POST)

        if form.is_valid():
            form.save()
            if post["id"] == "":
                messages.success(request, "Group has been saved successfully.")
            else:
                messages.success(request, "Group has been updated successfully.")
            resp["status"] = "success"
        else:
            for field in form:
                for error in field.errors:
                    if not resp["msg"] == "":
                        resp["msg"] += str("<br/>")
                    resp["msg"] += str(f"[{field.name}] {error}")
    else:
        resp["msg"] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
def view_group(request, pk=None):
    context = context_data(request)
    context["page"] = "view_group"
    context["page_title"] = "View Group"
    if pk is None:
        context["group"] = {}
    else:
        context["group"] = models.Groups.objects.get(id=pk)

    return render(request, "view_group.html", context)


@login_required
def manage_group(request, pk=None):
    context = context_data(request)
    context["page"] = "manage_group"
    context["page_title"] = "Manage Group"
    if pk is None:
        context["group"] = {}
    else:
        context["group"] = models.Groups.objects.get(id=pk)

    return render(request, "manage_group.html", context)


@login_required
def delete_group(request, pk=None):
    resp = {"status": "failed", "msg": ""}
    if pk is None:
        resp["msg"] = "Group ID is invalid"
    else:
        try:
            models.Groups.objects.filter(pk=pk).update(delete_flag=1)
            messages.success(request, "Group has been deleted successfully.")
            resp["status"] = "success"
        except:
            resp["msg"] = "Deleting Group Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


@login_required
# def members(request):
#     context = context_data(request)
#     context['page'] = 'Members'
#     context['page_title'] = "Member List"
#     context['members'] = models.Members.objects.filter(delete_flag = 0).all()
#     return render(request, 'members.html', context)


@login_required
def members(request):
    context = context_data(request)
    context["page"] = "Members"
    context["page_title"] = "Member List"
    context["members"] = models.Members.objects.filter(delete_flag=0).all()

    if request.method == "POST":
        file = request.FILES.get("file")
        if file:
            create_db(file)
            # Redirect back to members page after processing the file
            return redirect("smsApp:member-page")

    return render(request, "members.html", context)


@login_required
def save_member(request):
    resp = {"status": "failed", "msg": ""}
    if request.method == "POST":
        post = request.POST
        if not post["id"] == "":
            member = models.Members.objects.get(id=post["id"])
            form = forms.SaveMember(request.POST, request.FILES, instance=member)
        else:
            form = forms.SaveMember(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            if post["id"] == "":
                messages.success(request, "Member has been saved successfully.")
            else:
                messages.success(request, "Member has been updated successfully.")
            resp["status"] = "success"
        else:
            for field in form:
                for error in field.errors:
                    if not resp["msg"] == "":
                        resp["msg"] += str("<br/>")
                    resp["msg"] += str(f"[{field.name}] {error}")
    else:
        resp["msg"] = "There's no data sent on the request"

    return HttpResponse(json.dumps(resp), content_type="application/json")



def view_member(request, pk=None):
    context = context_data(request)
    context["page"] = "view_member"
    context["page_title"] = "View Member"
    if pk is None:
        context["member"] = {}
    else:
        context["member"] = models.Members.objects.get(id=pk)

    return render(request, "view_member.html", context)


@login_required
def manage_member(request, pk=None):
    context = context_data(request)
    context["page"] = "manage_member"
    context["page_title"] = "Manage Member"
    context["groups"] = models.Groups.objects.filter(delete_flag=0, status=1).all()
    if pk is None:
        context["member"] = {}
    else:
        context["member"] = models.Members.objects.get(id=pk)

    return render(request, "manage_member.html", context)


@login_required
def delete_member(request, pk=None):
    resp = {"status": "failed", "msg": ""}
    if pk is None:
        resp["msg"] = "Member ID is invalid"
    else:
        try:
            models.Members.objects.filter(pk=pk).update(delete_flag=1)
            messages.success(request, "Member has been deleted successfully.")
            resp["status"] = "success"
        except:
            resp["msg"] = "Deleting Member Failed"

    return HttpResponse(json.dumps(resp), content_type="application/json")


def view_card(request, pk=None):
    if pk is None:
        return HttpResponse("Member ID is Invalid")
    else:
        context = context_data()
        context["member"] = models.Members.objects.get(id=pk)
        return render(request, "view_id.html", context)

# def scanner_view(request):
#     group = request.GET.get('group', '')
#     name = request.GET.get('name', '')
#     gender = request.GET.get('gender', '')
#     contact = request.GET.get('contact', '')
#     email = request.GET.get('email', '')
#     address = request.GET.get('address', '')

#     url = '/view_member/?group={}&name={}&gender={}&contact={}&email={}&address={}'.format(
#         group, name, gender, contact, email, address
#     )

#     return redirect(url)

def scanner_view(request):
    if request.method == 'POST' and 'scan-result' in request.POST:
        scan_result = request.POST.get('scan-result')
        member = models.Members.objects.get(member_code=scan_result)
        return redirect('/view-member/' + str(member.id))

@login_required
def view_scanner(request):
    context = context_data(request)  # Pass request object to context_data function
    return render(request, "scanner.html", context)


def scanner_view(request):
    return render(request, "scanner.html")


@login_required
def view_details(request, code=None):
    if code is None:
        return HttpResponse("Member code is Invalid")
    else:
        context = context_data()
        context["member"] = models.Members.objects.get(member_code=code)
        return render(request, "view_member.html", context)


@login_required
def per_group(request):
    context = context_data(request)
    context["page"] = "per_group"
    context["page_title"] = "Member List Per Group"
    context["groups"] = models.Groups.objects.filter(delete_flag=0, status=1).all()
    context["members"] = {}
    if "group" in request.GET and "status" in request.GET:
        try:
            context["members"] = models.Members.objects.filter(
                group__id=request.GET["group"], status=request.GET["status"]
            ).all()
            context["selected_group"] = models.Groups.objects.get(
                pk=request.GET["group"]
            )
            context["status"] = request.GET["status"]
        except Exception as err:
            print(err)
    return render(request, "per_group.html", context)


from .models import Groups

import random


def generate_code():
    code = "".join(str(random.randint(0, 11)) for _ in range(11))
    return code


def create_db(file_path):
    print("hello")
    df = pd.read_csv(file_path, delimiter=",", header=None)
    print(df)
    list_of_csv = [list(row) for row in df.values]
    print(list_of_csv)
    for row in list_of_csv:
        print(row)
        test = Members.objects.create(
            code=generate_code(),
            group=Groups.objects.get(pk=1),
            first_name=row[0],
            middle_name=row[1],
            last_name=row[2],
            gender=row[3],
            contact=row[4],
            email=row[5],
            address=row[6],
            image_path="default.png",
        )
        test.save()


def main(request):
    if request.method == "POST":
        file = request.FILES["file"]
        file.objects.create(file=file)
    return render(request, "main.html")


def member_detail(request, pk):
    member = get_object_or_404(members)
    context = {"member": member}
    return render(request, "member_detail.html", context)


def error_404(request, exception):
    return render(request, "404.html")


def error_500(request):
    return render(request, "404.html")


def error_403(request, exception):
    data = {}
    return render(request, "404.html", data)


def error_400(request, exception):
    return render(request, "404.html")


def error_405(request, exception):
    data = {}
    return render(request, "404.html", data)


def error_410(request, exception):
    data = {}
    return render(request, "404.html", data)


def error_415(request, exception):
    data = {}
    return render(request, "404.html", data)


def handler403(request, exception):
    return render(request, "403.html", status=403)
