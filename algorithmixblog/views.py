import datetime
import itertools
import json
import random
import time
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django import forms

import markdown2

from .models import (
    User,
    BlogPost,
    BlogPostTag,
    BlogPostComment,
)

class BlogPostForm(forms.Form):
    tags = forms.CharField(label="Tags", min_length=0, max_length=1024, required=False)
    cover_url = forms.URLField(label="Cover", min_length=0, max_length=1024, required=False)

    title = forms.CharField(label="Title", max_length=128)
    description = forms.CharField(label="Description", widget=forms.Textarea, min_length=0, max_length=256, required=False)
    visibility = forms.ChoiceField(label="Visibility", widget=forms.Select, choices=[("public", "public"), ("private", "private")])
    text = forms.CharField(label="Text", widget=forms.Textarea, min_length=1, max_length=40960)


class UserProfileBioForm(forms.Form):
    bio = forms.CharField(label="Bio", widget=forms.Textarea, min_length=0, max_length=20480)

def index(request):
    return render(request, "algorithmixblog/index.html")

def about(request):
    return render(request, "algorithmixblog/about.html")

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "algorithmixblog/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "algorithmixblog/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        if "," in username:
            return render(request, "algorithmixblog/register.html", {
                "message": "Your username cannot contain the ',' character."
            })

        elif len(username) > 64:
            return render(request, "algorithmixblog/register.html", {
                "message": "Your username cannot exceed 64 characters in length."
            })

        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        if len(password) < 8 or len(confirmation) < 8:
            return render(request, "algorithmixblog/register.html", {
                "message": "Passwords must be at least 8 characters in length."
            })

        elif password != confirmation:
            return render(request, "algorithmixblog/register.html", {
                "message": "Passwords must match."
            })

        # Try to create a new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "algorithmixblog/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "algorithmixblog/register.html")


def discover(request):
    return render(request, "algorithmixblog/discover.html")


def search(request):
    if request.method == "GET":
        if request.GET.get("q") or request.GET.get("tags") or request.GET.get("authorname"):
            results = []
            author_names = request.GET.get("authornames", "")
            author_names_set = set(author_name.strip() for author_name in author_names.split(",") if author_name and not author_name.isspace())

            query = request.GET.get("q", "")
            query_split = query.split()
            query_parts = { *(itertools.chain(*([qs.upper() for qs in query_split], [qs.lower() for qs in query_split], [qs.title() for qs in query_split]))) }
            tags_string = request.GET.get("tags", "")
            date_sort = request.GET.get("date_sort", "newest")
            search_tags_models_qs = None

            if tags_string:           
                search_tags_names = [tname.strip().upper() for tname in tags_string.split(",") if tname and not tname.isspace()]
                search_tags_models_qs = BlogPostTag.objects.filter(name__in=search_tags_names)

                if search_tags_models_qs.exists():
                    query_parts |= { tmodel.name for tmodel in search_tags_models_qs }

            bp_ids = set()
            for bp in BlogPost.objects.all().order_by("-created" if date_sort == "newest" else "created"):
                if bp.is_private and bp.author.id != request.user.id:
                    continue

                bp_tag_names = set(tmodel.name for tmodel in bp.tags.all())

                if not query_parts and not search_tags_models_qs and bp.author.username in author_names_set:
                    if bp.id not in bp_ids:
                        bp_ids.add(bp.id)
                        results.append(bp)
                
                elif not author_names or bp.author.username in author_names_set:
                    for tmodel in ( search_tags_models_qs if search_tags_models_qs else ()):
                        if tmodel.name in bp_tag_names:
                            if bp.id not in bp_ids:
                                bp_ids.add(bp.id)
                                results.append(bp)
                                break
                    else:
                        for query_part in query_parts:
                            if (
                                query_part in bp.title
                                or query_part in bp.description
                                or query_part in bp_tag_names
                                or query_part in bp.text
                                and (True if not author_names else bp.author.username in author_names_set)            
                            ):
                                if bp.id not in bp_ids:
                                    bp_ids.add(bp.id)
                                    results.append(bp)
                                    break


            paginator = Paginator(results, 50)
            search_page_num = request.GET.get("searchpage")
            search_page_obj = paginator.get_page(search_page_num)
            return render(
                request,
                "algorithmixblog/search.html",
                dict(
                    search_page_obj=search_page_obj,
                    result_count=len(results),
                    query=query,
                    author_names=request.GET.get("authornames"),
                    tag_str=tags_string,
                    date_sort=date_sort,
                    no_query=False
                )
            )

    return render(request, "algorithmixblog/search.html", dict(no_query=True))

def user_profile(request, user_id):
    target_user = None
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, "algorithmixblog/notfound.html", status=404)

    public_blogpost_count = target_user.blogposts.filter(is_private=False).count()
   
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        bio = request.POST.get("bio")
        password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        new_password_confirm = request.POST.get("new_password_confirm")

        if password:
            if not target_user.check_password(password):
                return render(
                    request,
                    "algorithmixblog/userprofile.html",
                    dict(
                        target_user=target_user,
                        public_blogpost_count=public_blogpost_count,
                        info_error="Invalid password.",
                    ),
                )
        else:
            return render(
                request,
                "algorithmixblog/userprofile.html",
                dict(
                    target_user=target_user,
                    public_blogpost_count=public_blogpost_count,
                    info_error="Your old password is required.",
                ),
            )

        if username and username != target_user.username:
            username_error = None
            if "," in username:
                username_error = "Your new username cannot contain the ',' character."
            elif len(username) > 64:
                username_error = "Your new username cannot exceed 64 characters in length."
            elif User.objects.exclude(pk=target_user.id).filter(username=username).exists():
                username_error = "Your new username was already taken."
            else:
                target_user.username = username
            
            if username_error:
                return render(
                    request,
                    "algorithmixblog/userprofile.html",
                    dict(
                        target_user=target_user,
                        public_blogpost_count=public_blogpost_count,
                        info_error=username_error,
                    ),
                )

        if email and email != target_user.email:
            target_user.email = email
        
        if bio:
            if bio != target_user.bio and 0 <= len(bio) < 1025:
                target_user.bio = bio
            else:
                return render(
                    request,
                    "algorithmixblog/userprofile.html",
                    dict(
                        target_user=target_user,
                        public_blogpost_count=public_blogpost_count,
                        info_error="Could not update user bio. Be sure to keep the character limits of 1024.",
                    ),
                )
            

        new_password_set = False
        if new_password and new_password_confirm and new_password != password:
            new_password_error = None
            if len(new_password) < 8 or len(new_password_confirm) < 8:
                new_password_error = "Passwords must be at least 8 characters in length."
            elif new_password != new_password_confirm:
                new_password_error = "The new passwords must match."
            else:
                target_user.set_password(new_password)
                new_password_set = True

            if new_password_error:
                return render(
                    request,
                    "algorithmixblog/userprofile.html",
                    dict(
                        target_user=target_user,
                        public_blogpost_count=public_blogpost_count,
                        info_error=new_password_error,
                    ),
                )
        
        target_user.save()
        if new_password_set:
            return HttpResponseRedirect(reverse("login"))
        else:
            return HttpResponseRedirect(reverse("user_profile", args=(user_id,)))
        
    
    return render(request, "algorithmixblog/userprofile.html", dict(target_user=target_user, public_blogpost_count=target_user.blogposts.filter(is_private=False).count()))


def user_followers(request, user_id):
    target_user = None
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, "algorithmixblog/notfound.html", status=404)
    else:
        return render(request, "algorithmixblog/followers.html", dict(target_user=target_user))

def user_following(request, user_id):
    target_user = None
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return render(request, "algorithmixblog/notfound.html", status=404)
    else:
        return render(request, "algorithmixblog/following.html", dict(target_user=target_user))

@login_required(login_url="login")
def liked_blogposts(request):
    if request.method == "GET":
        blogposts = request.user.liked_blogposts.all().filter(is_private=False).order_by("-created")
        paginator = Paginator(blogposts, 50)
        feed_page_num = request.GET.get("page")
        feed_page_obj = paginator.get_page(feed_page_num)

    return render(request, "algorithmixblog/likedblogposts.html", dict(feed_page_obj=feed_page_obj))

@login_required(login_url="login")
def following_feed_blogposts(request):
    if request.method == "GET":
        blogposts = BlogPost.objects.filter(is_private=False).filter(
            author__id__in=request.user.following.all().values("id")
        ).order_by("-created")

        paginator = Paginator(blogposts, 10)
        feed_page_num = request.GET.get("page")
        feed_page_obj = paginator.get_page(feed_page_num)
    
    return render(request, "algorithmixblog/followingfeed.html", dict(feed_page_obj=feed_page_obj))

@login_required(login_url="login")
def favorite_blogposts(request):
    if request.method == "GET":
        blogposts = request.user.favorite_blogposts.all().filter(is_private=False).order_by("-created")
        paginator = Paginator(blogposts, 10)
        feed_page_num = request.GET.get("page")
        feed_page_obj = paginator.get_page(feed_page_num)

    return render(request, "algorithmixblog/favoriteblogposts.html", dict(feed_page_obj=feed_page_obj))

@login_required(login_url="login")
def create_blogpost(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        if form.is_valid():

            bp = BlogPost(
                author=request.user,
                title=form.cleaned_data["title"],
                text=form.cleaned_data["text"],
                is_private=form.cleaned_data["visibility"] == "private",
            )

            if form.cleaned_data["description"]:
                bp.description = form.cleaned_data["description"]

            if form.cleaned_data["cover_url"]:
                bp.cover_url = form.cleaned_data["cover_url"]

            bp.save()
            if form.cleaned_data["tags"]:
                tag_name_list = None
                tag_model_list = []
                tag_name_list = sorted(tname.strip().upper() for tname in form.cleaned_data["tags"].split(",") if tname and not tname.isspace())

                for tname in tag_name_list:
                    tmodel = None
                    try:
                        tmodel = BlogPostTag.objects.get(name=tname)
                    except BlogPostTag.DoesNotExist:
                        tmodel = BlogPostTag(name=tname)
                        tmodel.save()
                
                    tag_model_list.append(tmodel)
                
                bp.tags.add(*tag_model_list)

            bp.save()

            return HttpResponseRedirect(reverse("view_blogpost", args=(bp.id,)))
        else:
            return render(
                request,
                "algorithmixblog/create.html",
                dict(
                    form=BlogPostForm(),
                    message="Invalid inputs. Be sure to stay below the character limits."
                )
            )


    return render(request, "algorithmixblog/create.html", dict(form=BlogPostForm()))

@login_required(login_url="login")
def edit_blogpost(request, blogpost_id):
    try:
        bp = BlogPost.objects.get(pk=blogpost_id)
    except BlogPost.DoesNotExist:
        return render(request, "algorithmixblog/notfound.html", status=404)
    else:
        if bp.author.id != request.user.id:
            return render(request, "algorithmixblog/noaccess.html", status=403)

    
    if request.method == "POST":
        form = BlogPostForm(request.POST)
        
        if form.is_valid():

            bp.title = form.cleaned_data["title"]
            bp.text = form.cleaned_data["text"]

            if form.cleaned_data["description"]:
                bp.description = form.cleaned_data["description"]
            else:
                bp.description = ""

            if form.cleaned_data["cover_url"]:
                bp.cover_url = form.cleaned_data["cover_url"]
            else:
                bp.cover_url =  ""

            bp.is_private = form.cleaned_data["visibility"] == "private"

            if form.cleaned_data["tags"]:
               
                remove_model_list = None
                old_tag_model_list = [tag for tag in bp.tags.all()]

                new_tag_name_list = sorted(tname.strip().upper() for tname in form.cleaned_data["tags"].split(",") if tname and not tname.isspace())
                new_tag_name_set = set(new_tag_name_list)
                old_tag_name_set = set(tag.name for tag in old_tag_model_list)
                final_tag_model_list = []

                for tname in new_tag_name_list:
                    if tname not in old_tag_name_set:
                        tmodel = None
                        try:
                            tmodel = BlogPostTag.objects.get(name=tname)
                        except BlogPostTag.DoesNotExist:
                            tmodel = BlogPostTag(name=tname)
                            tmodel.save()

                        final_tag_model_list.append(tmodel)
                
                remove_model_list = [tmodel for tmodel in old_tag_model_list if tmodel.name not in new_tag_name_set]

                if remove_model_list:
                    bp.tags.remove(*remove_model_list)
                    
                    for tmodel in remove_model_list:
                        if not tmodel.related_blogposts.exists():
                            tmodel.delete()
                
                if final_tag_model_list:
                    bp.tags.add(*final_tag_model_list)

            bp.updated = datetime.datetime.now().astimezone(tz=datetime.timezone.utc)
            bp.save()

            return HttpResponseRedirect(reverse("view_blogpost", args=(bp.id,)))
        else:
            return render(
                request,
                "algorithmixblog/edit.html",
                dict(
                    blogpost=bp,
                    blogpost_id=bp.id,
                    blogpost_tag_str=", ".join(tag.name for tag in bp.tags.all()),
                    form=BlogPostForm(),
                    message="Invalid inputs. Be sure to stay below the character limits"
                )
            )

    return render(
        request,
        "algorithmixblog/edit.html",
        dict(
            blogpost=bp,
            blogpost_id=bp.id,
            blogpost_tag_str=", ".join(tag.name for tag in bp.tags.all()),
            form=BlogPostForm()
        )
    )


def view_blogpost(request, blogpost_id):

    try:
        bp = BlogPost.objects.get(pk=blogpost_id)
    except BlogPost.DoesNotExist:
        return render(request, "algorithmixblog/notfound.html", status=404)
    else:
        if bp.is_private and bp.author.id != request.user.id:
            return render(request, "algorithmixblog/notfound.html", status=404)

    blogpost_text_md = markdown2.markdown(
        bp.text,
        safe_mode=False,
        extras=[
            "break-on-newline",
            "fenced-code-blocks",
            "strike",
            "tables",
            "header-ids",
            "spoiler",
        ]
    )

    if request.method == "POST":
        text = request.POST.get("text")
        if text and len(text) <= 4096:
            if "edit" in request.POST:
                try:
                    comment_id = int(request.POST.get("edit"))
                    comment = bp.comments.get(pk=comment_id)
                except (ValueError, BlogPostComment.DoesNotExist):
                    return render(
                        request,
                        "algorithmixblog/blogpost.html",
                        dict(
                            blogpost=bp,
                            comments=bp.comments.all().order_by("-created"),
                            blogpost_text_md=blogpost_text_md,
                            comment_error="Could not find comment to edit."
                        )
                    )
                
                if comment.author.id == request.user.id:
                    comment.text = text
                    comment.updated = datetime.datetime.now().astimezone(tz=datetime.timezone.utc)
                    comment.save()
                    return HttpResponseRedirect(reverse("view_blogpost", args=(blogpost_id,)))

            elif "reply" in request.POST:
                try:
                    reply_comment_id = int(request.POST.get("reply"))
                    reply_comment = bp.comments.get(pk=reply_comment_id)
                except (ValueError, BlogPostComment.DoesNotExist):
                    return render(
                        request,
                        "algorithmixblog/blogpost.html",
                        dict(
                            blogpost=bp,
                            comments=bp.comments.all().order_by("-created"),
                            blogpost_text_md=blogpost_text_md,
                            comment_error="Could not find comment to reply to."
                        )
                    )
                
                comment = BlogPostComment(
                    author=request.user,
                    post=bp,
                    created=datetime.datetime.now().astimezone(tz=datetime.timezone.utc),
                    updated=datetime.datetime.now().astimezone(tz=datetime.timezone.utc),
                    text=text,
                    reference=reply_comment,
                    had_reference=True,
                )

                comment.save()
                bp.save()

                return HttpResponseRedirect(reverse("view_blogpost", args=(blogpost_id,)))

            else:
                comment = BlogPostComment(
                    author=request.user,
                    post=bp,
                    created=datetime.datetime.now().astimezone(tz=datetime.timezone.utc),
                    updated=datetime.datetime.now().astimezone(tz=datetime.timezone.utc),
                    text=text,
                )

                comment.save()
                bp.save()

                return HttpResponseRedirect(reverse("view_blogpost", args=(blogpost_id,)))
            
        return render(
            request,
            "algorithmixblog/blogpost.html",
            dict(
                blogpost=bp,
                comments=bp.comments.all().order_by("-created"),
                blogpost_text_md=blogpost_text_md,
                comment_error="Could not create/edit comment. Be sure to keep the character limit of 4096."
            )
        )


    bp_comments = bp.comments.all().order_by("created")
    paginator = Paginator(bp_comments, 10)
    comment_page_num = request.GET.get("commentpage")
    comment_page_obj = paginator.get_page(comment_page_num)

    return render(
        request,
        "algorithmixblog/blogpost.html",
        dict(
            blogpost=bp,
            comment_page_obj=comment_page_obj,
            blogpost_text_md=blogpost_text_md
        )
    )


# API

def users_preview(request):

    sort_type = request.GET.get("sort")
    target_user_id = request.GET.get("target_user", "")
    target_user = None
    view_mode = request.GET.get("view_mode", "")
    if target_user_id.isnumeric():
        try: 
            target_user_id = int(target_user_id)
            target_user = User.objects.get(pk=target_user_id)
        except (ValueError, User.DoesNotExist):
            pass

    user_previews = None

    try:
        start = int(request.GET.get("start"))
        end = int(request.GET.get("end"))
    except ValueError:
        start = None
        end = None

    if target_user is not None:
        if sort_type == "top":
            if view_mode == "followers" or view_mode != "following":
                user_previews = User.objects.filter(id__in=target_user.followers.values("id")).annotate(follower_count=Count("followers")).order_by("-follower_count")[slice(start, end)]
            elif view_mode == "following":
                user_previews = User.objects.filter(id__in=target_user.following.values("id")).annotate(follower_count=Count("followers")).order_by("-follower_count")[slice(start, end)]
        else:
            if view_mode == "followers" or view_mode != "following":
                user_previews = User.objects.filter(id__in=target_user.followers.values("id")).reverse()[slice(start, end)]
            elif view_mode == "following":
                user_previews = User.objects.filter(id__in=target_user.following.values("id")).reverse()[slice(start, end)]
    else:
        user_previews = User.objects.all()[slice(start, end)]

    time.sleep(0.5)

    user_prev_dicts = [user.serialize_preview() for user in user_previews]

    return JsonResponse(user_prev_dicts, safe=False)

def blogposts_preview(request):

    sort_type = request.GET.get("sort")
    target_user_id = request.GET.get("user", "")
    if target_user_id.isnumeric():
        target_user_id = int(target_user_id)

    public_only = True if request.GET.get("publiconly", "true") == "true" else False

    bp_previews = None

    try:
        start = int(request.GET.get("start"))
        end = int(request.GET.get("end"))
    except ValueError:
        start = None
        end = None


    if sort_type == "top":
        bp_previews = BlogPost.objects.filter(is_private=False).annotate(like_count=Count("likers")).order_by("-like_count")[slice(start, end)]
    elif sort_type == "oldest":
        bp_previews = BlogPost.objects.filter(is_private=False).order_by("created")[slice(start, end)]
    elif sort_type == "newest":
        bp_previews = BlogPost.objects.filter(is_private=False).order_by("-created")[slice(start, end)]
    elif sort_type == "mostactive":
        bp_previews = BlogPost.objects.filter(is_private=False).annotate(like_count=Count("likers"), comment_count=Count("comments")).order_by("-comment_count", "-like_count", "-updated")[slice(start, end)]
    elif sort_type == "discover":
        order_types = ["-like_count", "-comment_count", "-updated", "-created"]
        random.shuffle(order_types)
        bp_previews = BlogPost.objects.filter(is_private=False).annotate(like_count=Count("likers"), comment_count=Count("comments")).order_by(*order_types)[slice(start, end)]
    elif sort_type.startswith("userprofile"):
        if public_only:
            if sort_type == "userprofilemostactive" and target_user_id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id, is_private=False).annotate(like_count=Count("likers"), comment_count=Count("comments")).order_by("-comment_count", "-like_count", "-updated", "-created")[slice(start, end)]
            elif sort_type == "userprofilenewest" and target_user_id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id, is_private=False).order_by("-created")[slice(start, end)]
            elif sort_type == "userprofileoldest" and target_user_id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id, is_private=False).order_by("created")[slice(start, end)]
            elif sort_type == "userprofileoldest" and target_user_id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id, is_private=False).order_by("created")[slice(start, end)]
            else:
                bp_previews = set()
        else:
            if sort_type == "userprofilemostactive" and target_user_id == request.user.id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id).annotate(like_count=Count("likers"), comment_count=Count("comments")).order_by("-comment_count", "-like_count", "-updated", "-created")[slice(start, end)]
            elif sort_type == "userprofilenewest" and target_user_id == request.user.id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id).order_by("-created")[slice(start, end)]
            elif sort_type == "userprofileoldest" and target_user_id == request.user.id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id).order_by("created")[slice(start, end)]
            elif sort_type == "userprofileoldest" and target_user_id == request.user.id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id).order_by("created")[slice(start, end)]
            elif sort_type == "userprofilepublic" and target_user_id == request.user.id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id).order_by("is_private", "-created", "-updated")[slice(start, end)]
            elif sort_type == "userprofileprivate" and target_user_id == request.user.id:
                bp_previews = BlogPost.objects.filter(author__id=target_user_id).order_by("-is_private", "-created", "-updated")[slice(start, end)]
            else:
                bp_previews = set()
    else:
        bp_previews = BlogPost.objects.filter(is_private=False)[slice(start, end)]

    time.sleep(0.5)

    bp_prev_dicts = [bp.serialize_preview() for bp in bp_previews]

    for d in bp_prev_dicts:
        d.update(request_user_id=request.user.id)

    return JsonResponse(bp_prev_dicts, safe=False)

@login_required(login_url="login")
def get_blogpost_comment(request, comment_id):
    try:
        bp_comment = BlogPostComment.objects.get(pk=comment_id)
    except BlogPostComment.DoesNotExist:
        return JsonResponse({"error": "Blog post comment not found."}, status=404)

    if request.method == "GET":
        return JsonResponse(bp_comment.serialize(), safe=True)
    else:
        return JsonResponse(
            {"error": "GET request required."},
            status=400
        )


def get_blogpost_comments(request):
    sort_type = request.GET.get("sort")
    post_id = request.GET.get("post", -1)

    try:
        bp = BlogPost.objects.get(post__id=post_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({"error": "Blog post not found."}, status=404)
    else:
        if bp.is_private and bp.author.id != request.user.id:
            return JsonResponse({"error": "Blog post not found."}, status=404)

    bp_comments = None

    try:
        start = int(request.GET.get("start"))
        end = int(request.GET.get("end"))
    except ValueError:
        start = None
        end = None

    if sort_type == "top":
        bp_comments = BlogPostComment.objects.filter(post__id=bp.id).annotate(like_count=Count("likers")).order_by("-like_count")[slice(start, end)]
    elif sort_type == "oldest":
        bp_comments = BlogPostComment.objects.filter(post__id=bp.id).order_by("created")[slice(start, end)]
    elif sort_type == "newest":
        bp_comments = BlogPostComment.objects.filter(post__id=bp.id).order_by("-created")[slice(start, end)]
    elif sort_type == "mostactive":
        bp_comments = BlogPostComment.objects.annotate(reply_count=Count("replies")).order_by("-reply_count", "-updated")[slice(start, end)]
    else:
        bp_comments = BlogPostComment.objects.filter(post__id=bp.id)[slice(start, end)]

    time.sleep(0.5)
    return JsonResponse([bp_comment.serialize() for bp_comment in bp_comments], safe=False)

@login_required(login_url="login")
def toggle_follow_user(request, user_id):
    session_user = request.user
    target_user = None
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    else:
        if target_user.id == request.user.id:
            return JsonResponse({"error": "Invalid action."}, status=403)
    
    if request.method == "PUT":
        followdata = json.loads(request.body)
        has_followed = target_user.followers.filter(pk=session_user.id).exists()

        if followdata["value"] is not None:
            if followdata["value"] and not has_followed:
                target_user.followers.add(session_user)
                
            elif not followdata["value"] and has_followed:
                target_user.followers.remove(session_user)
        
            target_user.save()
            session_user.save()
            return HttpResponse(status=204)
        
        else:
            return JsonResponse(
                {"error": "'value' must be either true or false"},
                status=400
            )

    else:
        return JsonResponse({
            "error": "PUT request required."
        }, status=400)
        
@login_required(login_url="login")
def toggle_blogpost_like(request, blogpost_id):
    try:
        bp = BlogPost.objects.get(pk=blogpost_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({"error": "Blog post not found."}, status=404)

    if request.method == "PUT":
        likedata = json.loads(request.body)
        if likedata["value"] is not None:
            has_liked = bp.likers.filter(pk=request.user.id).exists()

            if likedata["value"] and not has_liked:
                bp.likers.add(request.user)
            elif not likedata["value"] and has_liked:
                bp.likers.remove(request.user)
                
            bp.save()
            return HttpResponse(status=204)

        else:
            return JsonResponse(
                {"error": "'value' must be either true or false"},
                status=400
            )
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)

@login_required(login_url="login")
def toggle_blogpost_favorites(request, blogpost_id):
    try:
        bp = BlogPost.objects.get(pk=blogpost_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({"error": "Blog post not found."}, status=404)

    if request.method == "PUT":
        favoritedata = json.loads(request.body)
        if favoritedata["value"] is not None:
            has_favorited = bp.favorers.filter(pk=request.user.id).exists()

            if favoritedata["value"] and not has_favorited:
                bp.favorers.add(request.user)
            elif not favoritedata["value"] and has_favorited:
                bp.favorers.remove(request.user)
                
            bp.save()
            return HttpResponse(status=204)

        else:
            return JsonResponse(
                {"error": "'value' must be either true or false"},
                status=400
            )
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


@login_required(login_url="login")
def toggle_blogpost_visibility(request, blogpost_id):
    try:
        bp = BlogPost.objects.get(pk=blogpost_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({"error": "Blog post not found."}, status=404)
    else:
        if bp.author.id != request.user.id:
            return JsonResponse({"error": "You do not have enough permissions to run this action."}, status=403)

    if request.method == "PUT":
        visibilitydata = json.loads(request.body)
        if visibilitydata["value"] is not None:
            is_private = bp.is_private

            if visibilitydata["value"] and not is_private:
                bp.is_private = True
            elif not visibilitydata["value"] and is_private:
                bp.is_private = False
                
            bp.save()
            return HttpResponse(status=204)

        else:
            return JsonResponse(
                {"error": "'value' must be either true or false"},
                status=400
            )
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)

@login_required(login_url="login")
def toggle_blogpost_comment_like(request, comment_id):
    try:
        bp_comment = BlogPostComment.objects.get(pk=comment_id)
    except BlogPostComment.DoesNotExist:
        return JsonResponse({"error": "Blog post comment not found."}, status=404)

    if request.method == "PUT":
        likedata = json.loads(request.body)
        
        if likedata["value"] is not None:
            has_liked = bp_comment.likers.filter(pk=request.user.id).exists()

            if likedata["value"] and not has_liked:
                bp_comment.likers.add(request.user)
            elif not likedata["value"] and has_liked:
                bp_comment.likers.remove(request.user)
            
            bp_comment.save()
            return HttpResponse(status=204)

        else:
            return JsonResponse(
                {"error": "'value' must be either true or false"},
                status=400
            )
    
    else:
        return JsonResponse({"error": "PUT request required."}, status=400)


@login_required(login_url="login")
def user_delete(request, user_id):
    try:
        target_user = User.objects.get(pk=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    else:
        if target_user.id != request.user.id:
            return JsonResponse({"error": "You do not have enough permissions to run this action."}, status=403)

    if request.method == "DELETE":
        logout(request)
        target_user.delete()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "DELETE request required."}, status=400)

@login_required(login_url="login")
def blogpost_delete(request, blogpost_id):
    try:
        bp = BlogPost.objects.get(pk=blogpost_id)
    except BlogPost.DoesNotExist:
        return JsonResponse({"error": "Blog post not found."}, status=404)
    else:
        if bp.author.id != request.user.id:
            return JsonResponse({"error": "You do not have enough permissions to run this action."}, status=403)

    if request.method == "DELETE":
        bp.delete()
        return HttpResponse(status=204) 
    else:
        return JsonResponse({"error": "DELETE request required."}, status=400)

@login_required(login_url="login")
def blogpost_comment_delete(request, comment_id):
    try:
        bp_comment = BlogPostComment.objects.get(pk=comment_id)
    except BlogPostComment.DoesNotExist:
        return JsonResponse({"error": "Blog post comment not found."}, status=404)
    else:
        if bp_comment.author.id != request.user.id:
            return JsonResponse({"error": "You do not have enough permissions to run this action."}, status=403)

    if request.method == "DELETE":
        bp = bp_comment.post
        bp_comment.delete()
        bp.save()

        return HttpResponse(status=204) 
    else:
        return JsonResponse({"error": "DELETE request required."}, status=400)


