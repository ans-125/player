from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Player
from .forms import PlayerForm


def player_list(request):
    """عرض قائمة اللاعبين مع التصفية"""
    players = Player.objects.filter(is_active=True).order_by('-created_at')
    
    # تطبيق التصفية
    position = request.GET.get('position')
    birth_year = request.GET.get('birth_year')
    city = request.GET.get('city')
    
    if position:
        players = players.filter(position=position)
    
    if birth_year:
        try:
            birth_year = int(birth_year)
            players = players.filter(birth_year=birth_year)
        except ValueError:
            pass
    
    if city:
        players = players.filter(city=city)
    
    # إعداد البيانات للقالب
    context = {
        'players': players,
        'birth_years': range(2003, 2015),
        'city_choices': Player.CITY_CHOICES,
    }
    
    return render(request, 'players/player_list.html', context)


@login_required
def add_player(request):
    """إضافة لاعب جديد"""
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, user=request.user)
        if form.is_valid():
            player = form.save()
            messages.success(request, f'تم إضافة اللاعب {player.name} بنجاح')
            return redirect('players:player_list')
    else:
        form = PlayerForm(user=request.user)
    
    return render(request, 'players/add_player.html', {'form': form})


@login_required
def edit_player(request, pk):
    """تعديل بيانات لاعب"""
    player = get_object_or_404(Player, pk=pk)
    
    # التحقق من الصلاحيات
    if not (request.user == player.user or request.user.is_superuser):
        messages.error(request, 'ليس لديك صلاحية لتعديل هذا الإعلان')
        return redirect('players:player_list')
    
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES, instance=player, user=request.user)
        if form.is_valid():
            player = form.save()
            messages.success(request, f'تم تحديث بيانات اللاعب {player.name} بنجاح')
            return redirect('players:player_list')
    else:
        form = PlayerForm(instance=player, user=request.user)
    
    return render(request, 'players/edit_player.html', {'form': form, 'player': player})


@login_required
def delete_player(request, pk):
    """حذف لاعب"""
    player = get_object_or_404(Player, pk=pk)
    
    # التحقق من الصلاحيات
    if not (request.user == player.user or request.user.is_superuser):
        messages.error(request, 'ليس لديك صلاحية لحذف هذا الإعلان')
        return redirect('players:player_list')
    
    if request.method == 'POST':
        player_name = player.name
        player.delete()
        messages.success(request, f'تم حذف اللاعب {player_name} بنجاح')
        return redirect('players:player_list')
    
    return render(request, 'players/confirm_delete.html', {'player': player})


@login_required
def my_ads(request):
    """عرض إعلانات المستخدم"""
    if request.user.is_superuser:
        # إذا كان المستخدم مدير عام، اعرض جميع الإعلانات
        players = Player.objects.filter(is_active=True).order_by('-created_at')
        total_players = players.count()
        remaining_ads = None
    else:
        # اعرض فقط إعلانات المستخدم الحالي
        players = Player.objects.filter(user=request.user, is_active=True).order_by('-created_at')
        total_players = players.count()
        remaining_ads = 3 - total_players
    
    context = {
        'players': players,
        'total_players': total_players,
        'remaining_ads': remaining_ads,
    }
    
    return render(request, 'players/my_ads.html', context)

