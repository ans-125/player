from django import forms
from django.core.exceptions import ValidationError
from .models import Player


class PlayerForm(forms.ModelForm):
    """نموذج إضافة وتعديل اللاعب"""
    
    class Meta:
        model = Player
        fields = [
            'name', 'position', 'birth_year', 'city', 'nationality', 
            'phone', 'previous_clubs', 'description', 'video'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل اسم اللاعب'
            }),
            'position': forms.Select(attrs={'class': 'form-control'}),
            'birth_year': forms.Select(
                choices=[(year, year) for year in range(2003, 2015)],
                attrs={'class': 'form-control'}
            ),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'أدخل الأرقام باللغة الإنجليزية'
            }),
            'previous_clubs': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'اكتب أسماء الأندية السابقة وعدد السنوات'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'اكتب وصفاً للاعب'
            }),
            'video': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'video/*'
            }),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        """التحقق من صحة رقم الهاتف"""
        phone = self.cleaned_data.get('phone')
        
        # التحقق من أن الرقم يحتوي على أرقام إنجليزية فقط
        if not phone.isdigit():
            raise ValidationError('يرجى إدخال رقم الهاتف بالأرقام الإنجليزية فقط')
        
        return phone

    def clean(self):
        """التحقق من الحد الأقصى للإعلانات"""
        cleaned_data = super().clean()
        
        if self.user and not self.instance.pk:  # فقط عند إضافة لاعب جديد
            # التحقق من عدد الإعلانات للمستخدم الحالي (الحد الأقصى 3 إعلانات)
            if not self.user.is_superuser:
                user_ads_count = Player.objects.filter(user=self.user, is_active=True).count()
                if user_ads_count >= 3:
                    raise ValidationError('لقد وصلت للحد الأقصى من الإعلانات (3 إعلانات)')
        
        return cleaned_data

    def save(self, commit=True):
        """حفظ اللاعب مع ربطه بالمستخدم"""
        player = super().save(commit=False)
        if self.user and not player.user_id:
            player.user = self.user
        if commit:
            player.save()
        return player

