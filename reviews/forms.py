from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=Review.RATING_CHOICES),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Заголовок отзыва'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Ваш отзыв о товаре...'}),
        }
        labels = {
            'rating': 'Оценка',
            'title': 'Заголовок',
            'comment': 'Комментарий',
        }
