from django import forms
from .models import Review, ReviewPhoto

class ReviewForm(forms.ModelForm):
    photo1 = forms.ImageField(required=False, label='Hình ảnh 1')
    photo2 = forms.ImageField(required=False, label='Hình ảnh 2')
    photo3 = forms.ImageField(required=False, label='Hình ảnh 3')

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Chia sẻ trải nghiệm của bạn về sản phẩm này'})
        }

    def save(self, commit=True):
        review = super().save(commit=False)
        if commit:
            review.save()
            for i in range(1, 4):
                photo = self.cleaned_data.get(f'photo{i}')
                if photo:
                    ReviewPhoto.objects.create(review=review, image=photo)
        return review
