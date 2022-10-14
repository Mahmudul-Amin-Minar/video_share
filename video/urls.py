from django.urls import path

from .views import home, upload_video, video_details, video_reaction

urlpatterns = [
    path('', home, name='homepage'),
    path('upload', upload_video, name='upload'),
    path('video_details/<int:id>', video_details, name='video_details'),
    path('react/<int:id>/<type>', video_reaction, name="react"),
]
