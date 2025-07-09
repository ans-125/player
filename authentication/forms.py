from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """نموذج إنشاء مستخدم جديد"""
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل اسمك'
        }),
        label="الاسم"
    )
    
    phone = forms.CharField(
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل رقم الهاتف بالأرقام الإنجليزية'
        }),
        label="رقم الهاتف"
    )
    
    birth_year = forms.IntegerField(
        required=False,
        widget=forms.Select(
            choices=[(year, year) for year in range(2003, 2015)],
            attrs={'class': 'form-control'}
        ),
        label="سنة الميلاد"
    )
    
    city = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل اسم المدينة'
        }),
        label="المدينة"
    )

    class Meta:
        model = CustomUser
        fields = ('phone', 'first_name', 'birth_year', 'city', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # إزالة حقل username من النموذج
        if 'username' in self.fields:
            del self.fields['username']
        
        # تخصيص widgets لحقول كلمة المرور
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'أعد إدخال كلمة المرور'
        })

    def clean_phone(self):
        """التحقق من صحة رقم الهاتف"""
        phone = self.cleaned_data.get('phone')
        
        # التحقق من أن الرقم يحتوي على أرقام إنجليزية فقط
        if not phone.isdigit():
            raise ValidationError('يرجى إدخال رقم الهاتف بالأرقام الإنجليزية فقط')
        
        # التحقق من عدم وجود مستخدم آخر بنفس رقم الهاتف
        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError('رقم الهاتف مستخدم بالفعل. يرجى استخدام رقم هاتف آخر.')
        
        return phone

    def save(self, commit=True):
        """حفظ المستخدم الجديد"""
        user = super().save(commit=False)
        user.username = self.cleaned_data['phone']  # استخدام رقم الهاتف كاسم مستخدم
        if commit:
            user.save()
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """نموذج تسجيل الدخول المخصص"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل رقم الهاتف'
        }),
        label="رقم الهاتف"
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'أدخل كلمة المرور'
        }),
        label="كلمة المرور"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # تغيير اسم الحقل في النموذج
        self.fields['username'].label = "رقم الهاتف"

    def clean_username(self):
        """التحقق من صحة رقم الهاتف"""
        username = self.cleaned_data.get('username')
        
        # التحقق من أن الرقم يحتوي على أرقام إنجليزية فقط
        if not username.isdigit():
            raise ValidationError('يرجى إدخال رقم الهاتف بالأرقام الإنجليزية فقط')
        
        return username

