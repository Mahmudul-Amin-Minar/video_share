from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .models import Video
from .forms import VideoUploadForm
# Create your views here.

def home(request):
    videos = Video.objects.all()
    return render(request, 'video/home.html', {'videos':videos})

@login_required
def upload_video(request):
    if request.method == 'POST':
        form = VideoUploadForm(request.POST)
        if form.is_valid():
            video_link = form.cleaned_data.get('video_link')
            short_link = video_link.split('/')[3]
            thumbnail = "https://img.youtube.com/vi/"+ short_link + "/hqdefault.jpg"
            obj = Video.objects.create(uploader=request.user, video_link=video_link, short_link=short_link, thumbnail=thumbnail)
            obj.save()
        return redirect('homepage')
    else:
        form = VideoUploadForm()
    return render(request, 'video/upload-form.html', {'form':form})


def video_details(request, id):
    requested_video = Video.objects.get(id=id)
    requested_video.views = requested_video.views+1
    requested_video.save()

    likes = requested_video.likes.all()
    dislikes = requested_video.dislikes.all()
    views = requested_video.views
    uploaded_by = requested_video.uploader
    is_user_liked = False
    is_user_disliked = False

    if request.user in likes:
        is_user_liked = True
    if request.user in dislikes:
        is_user_disliked = True

    context = {
        'likes': likes,
        'dislikes': dislikes,
        'views': views,
        'uploaded_by': uploaded_by,
        'video': requested_video,
        'is_user_liked': is_user_liked,
        'is_user_disliked': is_user_disliked,
    }
    return render(request, 'video/details.html', context)



def video_reaction(request, id, type):
    if not request.user.is_authenticated:
        return redirect('/account/login')
    requested_video = Video.objects.get(id=id)
    likes = requested_video.likes.all()
    dislikes = requested_video.dislikes.all()

    if type == "like":
        if request.user not in likes:
            requested_video.likes.add(request.user)
        if request.user in dislikes:
            requested_video.dislikes.remove(request.user)
    elif type == "dislike":
        if request.user not in dislikes:
            requested_video.dislikes.add(request.user)
        if request.user in likes:
            requested_video.likes.remove(request.user)
    requested_video.save()

    return redirect('video_details', id)