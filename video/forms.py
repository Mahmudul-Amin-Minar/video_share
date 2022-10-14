from django import forms

class VideoUploadForm(forms.Form):
    video_link = forms.URLField(max_length=200)