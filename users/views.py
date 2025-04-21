# users/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from django.utils import timezone
import calendar
from datetime import date, datetime, timedelta

from .models import CustomUser, Team, Player, PlayerStat, Game, Sport, PitchingStat
from .forms import (
    SignUpForm,
    TeamForm,
    PlayerForm,
    AddPlayerForm,
    PlayerStatForm,
    PitchingStatForm,
    GameForm
)


# -----------------------------
# Home
# -----------------------------
def home(request):
    return render(request, 'users/home.html')


# -----------------------------
# Authentication
# -----------------------------
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = form.cleaned_data['role']
            user.full_name = form.cleaned_data['full_name']
            user.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = SignUpForm()
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, "users/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')


# -----------------------------
# Dashboard
# -----------------------------
@login_required
def dashboard(request):
    user_role = request.user.role
    teams = Team.objects.filter(coach=request.user) if user_role == "coach" else None
    players = Player.objects.filter(user=request.user) if user_role == "player" else None
    return render(request, 'users/dashboard.html', {
        'user_role': user_role,
        'teams': teams,
        'players': players
    })


# -----------------------------
# Teams
# -----------------------------
@login_required
def create_team(request):
    if request.user.role != "coach":
        return HttpResponseForbidden("Only coaches can create teams.")

    if request.method == "POST":
        form = TeamForm(request.POST, user=request.user)
        if form.is_valid():
            team = form.save(commit=False)
            team.coach = request.user
            team.save()
            return redirect('dashboard')
    else:
        form = TeamForm(user=request.user)

    teams = Team.objects.all()
    return render(request, 'users/create_team.html', {'form': form, 'teams': teams})


@login_required
def view_roster(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = Player.objects.filter(team=team)
    return render(request, 'users/roster.html', {'team': team, 'players': players})


@login_required
def add_player(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.user != team.coach:
        return HttpResponseForbidden("Only the coach can add players.")

    if request.method == "POST":
        form = AddPlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team
            player.save()
            messages.success(request, "Player added successfully.")
            return redirect('view_roster', team_id=team.id)
    else:
        form = AddPlayerForm()

    return render(request, 'users/add_player.html', {'form': form, 'team': team})


@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    if Player.objects.filter(user=request.user, team=team).exists():
        messages.warning(request, "You are already on this team.")
        return redirect('view_roster', team_id=team.id)

    Player.objects.create(
        user=request.user,
        full_name=request.user.full_name,
        team=team,
        position="Undecided"
    )
    messages.success(request, f"You have joined {team.name}!")
    return redirect('view_roster', team_id=team.id)


# -----------------------------
# Player Stats (Batting)
# -----------------------------
@login_required
def add_stat(request):
    if request.user.role != "coach":
        return HttpResponseForbidden("Only coaches can add stats.")

    if request.method == "POST":
        form = PlayerStatForm(request.POST, coach=request.user)
        if form.is_valid():
            stat = form.save(commit=False)
            stat.game_date = timezone.now()
            stat.save()
            messages.success(request, "Player stat added successfully.")
            return redirect("dashboard")
    else:
        form = PlayerStatForm(coach=request.user)

    return render(request, "users/add_stat.html", {"form": form})



@login_required
def view_hitting_stats(request):
    if request.user.role != "coach":
        return HttpResponseForbidden("Only coaches can view hitting stats.")

    teams = Team.objects.filter(coach=request.user)
    players = Player.objects.filter(team__in=teams)

    player_totals = []

    for player in players:
        stats = PlayerStat.objects.filter(player=player)

        total_at_bats = sum(stat.at_bats for stat in stats)
        total_hits = sum(stat.hits for stat in stats)
        total_runs = sum(stat.runs for stat in stats)
        total_rbis = sum(stat.rbis for stat in stats)
        total_home_runs = sum(stat.home_runs for stat in stats)
        total_doubles = sum(stat.doubles for stat in stats)
        total_triples = sum(stat.triples for stat in stats)
        total_stolen_bases = sum(stat.stolen_bases for stat in stats)
        total_walks = sum(stat.walks for stat in stats)
        total_hit_by_pitch = sum(stat.hit_by_pitch for stat in stats)
        total_strikeouts = sum(stat.strikeouts for stat in stats)

        # Calculate singles
        total_singles = total_hits - total_doubles - total_triples - total_home_runs

        # Safeguard for zero at-bats
        avg = (total_hits / total_at_bats) if total_at_bats > 0 else 0
        obp = (total_hits + total_walks + total_hit_by_pitch) / (
            total_at_bats + total_walks + total_hit_by_pitch
        ) if (total_at_bats + total_walks + total_hit_by_pitch) > 0 else 0
        slg = (
            (total_singles + (total_doubles * 2) + (total_triples * 3) + (total_home_runs * 4))
            / total_at_bats
        ) if total_at_bats > 0 else 0
        ops = obp + slg

        player_totals.append({
            'player': player,
            'total_at_bats': total_at_bats,
            'total_hits': total_hits,
            'total_runs': total_runs,
            'total_rbis': total_rbis,
            'total_home_runs': total_home_runs,
            'total_doubles': total_doubles,
            'total_triples': total_triples,
            'total_stolen_bases': total_stolen_bases,
            'total_walks': total_walks,
            'total_hit_by_pitch': total_hit_by_pitch,
            'avg': avg,
            'obp': obp,
            'slg': slg,
            'ops': ops,
            'strikeouts': total_strikeouts,
        })

    return render(request, 'users/hitting_stats.html', {
        'player_totals': player_totals
    })



@login_required
def my_stats(request):
    if request.user.role != 'player':
        return HttpResponseForbidden("Only players can view their stats.")

    player = get_object_or_404(Player, user=request.user)
    stats = PlayerStat.objects.filter(player=player).order_by('-game_date')

    return render(request, 'users/my_stats.html', {'stats': stats, 'player': player})


@login_required
def view_stats(request):
    stats = PlayerStat.objects.all().order_by('-game_date')
    return render(request, 'users/view_stats.html', {'stats': stats})


# -----------------------------
# Pitching Stats
# -----------------------------
@login_required
def add_pitching_stat(request):
    if request.user.role != "coach":
        return HttpResponseForbidden("Only coaches can add pitching stats.")

    if request.method == "POST":
        form = PitchingStatForm(request.POST, coach=request.user)
        if form.is_valid():
            pitching_stat = form.save(commit=False)
            pitching_stat.game_date = timezone.now()
            pitching_stat.save()
            messages.success(request, "Pitching stat added successfully.")
            return redirect("dashboard")
    else:
        form = PitchingStatForm(coach=request.user)

    return render(request, "users/add_pitching_stat.html", {"form": form})



@login_required
def view_pitching_stats(request):
    if request.user.role != "coach":
        return HttpResponseForbidden("Only coaches can view pitching stats.")

    teams = Team.objects.filter(coach=request.user)
    players = Player.objects.filter(team__in=teams)

    from .models import PitchingStat  # Ensure import

    player_totals = []

    for player in players:
        stats = PitchingStat.objects.filter(player=player)

        total_innings_pitched = sum((stat.innings_pitched or 0) for stat in stats)
        total_hits_allowed = sum((stat.hits_allowed or 0) for stat in stats)
        total_runs_allowed = sum((stat.runs_allowed or 0) for stat in stats)
        total_earned_runs = sum((stat.earned_runs or 0) for stat in stats)
        total_walks = sum((stat.walks or 0) for stat in stats)
        total_strikeouts = sum((stat.strikeouts or 0) for stat in stats)
        total_pitches_thrown = sum((stat.pitches_thrown or 0) for stat in stats)

        # Safely calculate advanced stats
        if total_innings_pitched > 0:
            era = round((total_earned_runs * 9) / total_innings_pitched, 2)
            whip = round((total_walks + total_hits_allowed) / total_innings_pitched, 2)
        else:
            era = whip = "N/A"

        if total_walks > 0:
            kbb = round(total_strikeouts / total_walks, 2)
        else:
            kbb = "N/A"

        player_totals.append({
            'player': player,
            'innings_pitched': total_innings_pitched,
            'hits_allowed': total_hits_allowed,
            'runs_allowed': total_runs_allowed,
            'earned_runs': total_earned_runs,
            'walks': total_walks,
            'strikeouts': total_strikeouts,
            'home_runs_allowed': total_home_runs_allowed,
            'pitches_thrown': total_pitches_thrown,
            'era': era,
            'whip': whip,
            'kbb': kbb,
        })

    return render(request, 'users/pitching_stats.html', {
        'player_totals': player_totals
    })

# -----------------------------
# Combined Stats Page
# -----------------------------

@login_required
def combined_stats(request):
    teams = Team.objects.filter(coach=request.user)

    # Hitting Totals
    players_with_hitting_stats = Player.objects.filter(
        team__in=teams,
        playerstat__isnull=False
    ).distinct()

    player_hitting_totals = []

    for player in players_with_hitting_stats:
        stats = PlayerStat.objects.filter(player=player)

        total_at_bats = sum(stat.at_bats for stat in stats)
        total_hits = sum(stat.hits for stat in stats)
        total_runs = sum(stat.runs for stat in stats)
        total_rbis = sum(stat.rbis for stat in stats)
        total_home_runs = sum(stat.home_runs for stat in stats)
        total_doubles = sum(stat.doubles for stat in stats)
        total_triples = sum(stat.triples for stat in stats)
        total_stolen_bases = sum(stat.stolen_bases for stat in stats)
        total_walks = sum(stat.walks for stat in stats)
        total_hit_by_pitch = sum(stat.hit_by_pitch for stat in stats)
        total_strikeouts = sum(stat.strikeouts for stat in stats)

        singles = total_hits - (total_doubles + total_triples + total_home_runs)

        avg = round(total_hits / total_at_bats, 3) if total_at_bats else 0
        obp_denominator = total_at_bats + total_walks + total_hit_by_pitch
        obp = round((total_hits + total_walks + total_hit_by_pitch) / obp_denominator, 3) if obp_denominator else 0
        slg = round(((singles + 2 * total_doubles + 3 * total_triples + 4 * total_home_runs) / total_at_bats), 3) if total_at_bats else 0

        player_hitting_totals.append({
            'player': player,
            'total_at_bats': total_at_bats,
            'total_hits': total_hits,
            'total_runs': total_runs,
            'total_rbis': total_rbis,
            'total_home_runs': total_home_runs,
            'total_doubles': total_doubles,
            'total_triples': total_triples,
            'total_stolen_bases': total_stolen_bases,
            'total_walks': total_walks,
            'total_hit_by_pitch': total_hit_by_pitch,
            'total_strikeouts': total_strikeouts,
            'avg': avg,
            'obp': obp,
            'slg': slg,
        })

    # Pitching Totals
    from .models import PitchingStat

    players_with_pitching_stats = Player.objects.filter(
        team__in=teams,
        pitchingstat__isnull=False
    ).distinct()

    player_pitching_totals = []

    for player in players_with_pitching_stats:
        stats = PitchingStat.objects.filter(player=player)

        total_innings_pitched = sum((stat.innings_pitched or 0) for stat in stats)
        total_hits_allowed = sum((stat.hits_allowed or 0) for stat in stats)
        total_runs_allowed = sum((stat.runs_allowed or 0) for stat in stats)
        total_earned_runs = sum((stat.earned_runs or 0) for stat in stats)
        total_walks = sum((stat.walks or 0) for stat in stats)
        total_strikeouts = sum((stat.strikeouts or 0) for stat in stats)
        total_pitches_thrown = sum((stat.pitches_thrown or 0) for stat in stats)
        total_home_runs_allowed = sum((stat.home_runs_allowed or 0) for stat in stats)  # ✅ Add this

        era = round((total_earned_runs * 9) / total_innings_pitched, 2) if total_innings_pitched else 0.00
        whip = round((total_walks + total_hits_allowed) / total_innings_pitched, 2) if total_innings_pitched else 0.00
        k_bb_ratio = round(total_strikeouts / total_walks, 2) if total_walks else total_strikeouts

        player_pitching_totals.append({
            'player': player,
            'innings_pitched': total_innings_pitched,
            'hits_allowed': total_hits_allowed,
            'runs_allowed': total_runs_allowed,
            'earned_runs': total_earned_runs,
            'walks': total_walks,
            'strikeouts': total_strikeouts,
            'home_runs_allowed': total_home_runs_allowed,
            'pitches_thrown': total_pitches_thrown,
            'era': era,
            'whip': whip,
            'k_bb_ratio': k_bb_ratio,
        })

    # Final correct render!
    return render(request, 'users/combined_stats.html', {
        'player_hitting_totals': player_hitting_totals,
        'player_pitching_totals': player_pitching_totals,
    })


# -----------------------------
# Game Log
# -----------------------------


# Player Hitting Game Log
@login_required
def player_game_log(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    stats = PlayerStat.objects.filter(player=player).order_by('-game_date')

    return render(request, 'users/player_game_log.html', {
        'player': player,
        'stats': stats,
    })


# Player Pitching Game Log
@login_required
def player_pitching_log(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    from .models import PitchingStat
    pitching_logs = PitchingStat.objects.filter(player=player).order_by('-game_date')

    return render(request, 'users/player_pitching_log.html', {
        'player': player,
        'pitching_logs': pitching_logs,
    })

# -----------------------------
# Schedule
# -----------------------------

@login_required
def schedule_view(request):
    games = Game.objects.order_by('date')
    print(games)
    return render(request, 'users/schedule.html', {'games': games})



import calendar
from datetime import date, datetime, timedelta

@login_required
def calendar_view(request):
    user = request.user
    today = timezone.now().date()
    year = today.year
    month = today.month

    first_day = date(year, month, 1)
    _, last_day = calendar.monthrange(year, month)

    month_days = [first_day + timedelta(days=i) for i in range(last_day)]

    if user.role == 'coach':
        games = Game.objects.filter(team__coach=user, date__date__range=(first_day, first_day.replace(day=last_day)))
    else:
        games = Game.objects.all()

    game_map = {}
    for day in month_days:
        game_map[day] = [game for game in games if game.date.date() == day]

    # Convert game_map to list of (day, games)
    days_games = list(game_map.items())

    # Split into weeks (chunks of 7)
    calendar_data = [days_games[i:i + 7] for i in range(0, len(days_games), 7)]

    context = {
        'today': today,
        'calendar_data': calendar_data, 
    }

    return render(request, 'users/calendar.html', context)



@login_required
def create_game(request):
    if request.user.role != "coach":
        return HttpResponseForbidden("Only coaches can create games.")

    if request.method == "POST":
        form = GameForm(request.POST, coach=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Game created successfully.")
        return redirect("schedule")
    else:
        form = GameForm(coach=request.user)

    return render(request, "users/create_game.html", {"form": form})


# -----------------------------
# Edit Hitting/Pitching Stats
# -----------------------------

@login_required
def edit_player_stat(request, stat_id):
    stat = get_object_or_404(PlayerStat, id=stat_id)

    if request.method == 'POST':
        form = PlayerStatForm(request.POST, instance=stat, coach=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Player stat updated successfully!")
            return redirect('player_game_log', player_id=stat.player.id)
    else:
        form = PlayerStatForm(instance=stat, coach=request.user)

    return render(request, 'users/edit_player_stat.html', {'form': form, 'stat': stat})

# # # # # # # # #

@login_required
def edit_pitching_stat(request, stat_id):
    from .models import PitchingStat
    stat = get_object_or_404(PitchingStat, id=stat_id)

    if request.method == 'POST':
        form = PitchingStatForm(request.POST, instance=stat, coach=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Pitching stat updated successfully!")
            return redirect('player_pitching_log', player_id=stat.player.id)
    else:
        form = PitchingStatForm(instance=stat, coach=request.user)

    return render(request, 'users/edit_pitching_stat.html', {'form': form, 'stat': stat})

# -----------------------------
# Delete Hitting/Pitching Stats
# -----------------------------

@login_required
def delete_player_stat(request, stat_id):
    stat = get_object_or_404(PlayerStat, id=stat_id)

    if request.method == 'POST':
        player_id = stat.player.id
        stat.delete()
        messages.success(request, "Player stat deleted successfully!")
        return redirect('player_game_log', player_id=player_id)

    return render(request, 'users/confirm_delete_stat.html', {'object': stat, 'type': 'PlayerStat'})


# # # # # # # #

@login_required
def delete_pitching_stat(request, stat_id):
    from .models import PitchingStat
    stat = get_object_or_404(PitchingStat, id=stat_id)

    if request.method == 'POST':
        player_id = stat.player.id
        stat.delete()
        messages.success(request, "Pitching stat deleted successfully!")
        return redirect('player_pitching_log', player_id=player_id)

    return render(request, 'users/confirm_delete_stat.html', {'object': stat, 'type': 'PitchingStat'})


# -----------------------------
# Edit/Delete Scheduled Games
# -----------------------------

@login_required
def edit_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.user != game.team.coach:
        return HttpResponseForbidden("Only the coach can edit games.")

    if request.method == "POST":
        form = GameForm(request.POST, instance=game, coach=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Game updated successfully.")
            return redirect('schedule')
    else:
        form = GameForm(instance=game, coach=request.user)

    return render(request, 'users/edit_game.html', {"form": form, "game": game})


@login_required
def delete_game_view(request, game_id):
    game = get_object_or_404(Game, id=game_id)

    if request.user != game.team.coach:
        return HttpResponseForbidden("Only the coach can delete games.")

    if request.method == "POST":
        game.delete()
        messages.success(request, "Game deleted successfully.")
        return redirect('schedule')

    return render(request, 'users/confirm_delete_game.html', {"game": game})
