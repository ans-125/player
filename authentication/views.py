from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import CustomUser


class CustomLoginView(LoginView):
    """عرض تسجيل الدخول المخصص"""
    form_class = CustomAuthenticationForm
    template_name = 'authentication/login.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('players:player_list')
    
    def form_valid(self, form):
        messages.success(self.request, f'تم تسجيل الدخول بنجاح! مرحباً بك {form.get_user().get_full_name()}')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, 'خطأ في تسجيل الدخول. يرجى التحقق من رقم الهاتف وكلمة المرور.')
        return super().form_invalid(form)


class CustomRegisterView(CreateView):
    """عرض إنشاء حساب جديد"""
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = 'authentication/register.html'
    success_url = reverse_lazy('players:player_list')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        # تسجيل الدخول تلقائياً بعد إنشاء الحساب
        login(self.request, self.object)
        messages.success(self.request, f'تم إنشاء حساب جديد باسم {self.object.get_full_name()} بنجاح وتسجيل الدخول تلقائياً.')
        return response
    
    def form_invalid(self, form):
        messages.error(self.request, 'حدث خطأ أثناء إنشاء الحساب. يرجى التحقق من البيانات المدخلة.')
        return super().form_invalid(form)


def custom_logout_view(request):
    """عرض تسجيل الخروج"""
    if request.user.is_authenticated:
        user_name = request.user.get_full_name()
        logout(request)
        messages.success(request, f'تم تسجيل الخروج بنجاح. وداعاً {user_name}!')
    return redirect('players:player_list')

