from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm

# Signup View
def signup_view(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            user.role = form.cleaned_data['role']  # Assign role manually
            user.save()  # Now save
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard
    else:
        form = SignUpForm()

    return render(request, 'users/signup.html', {'form': form})

# Login View
def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session["role"] = user.role  # Store role in session
            return redirect("dashboard")
    return render(request, "users/login.html")

# Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# Protected Dashboard View
@login_required
def dashboard(request):
    # Get user role
    user_role = request.user.role

    # Get teams where the user is the coach
    teams = Team.objects.filter(coach=request.user)

    # Get all players from those teams
    players = Player.objects.filter(team__in=teams)

    return render(request, 'users/dashboard.html', {
        'user_role': user_role,  # Send role to the template
        'teams': teams,
        'players': players
    })


## Add Views for CRUD Operations

from django.shortcuts import render, redirect, get_object_or_404
from .models import Team, Player
from .forms import TeamForm, PlayerForm
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from .forms import TeamForm, PlayerForm

@login_required
def create_team(request):
    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.coach = request.user  # Assign logged-in user as coach
            team.save()
            return redirect('dashboard')  # Redirect back to dashboard
    else:
        form = TeamForm()
    
    return render(request, 'users/create_team.html', {'form': form})

@login_required
def create_player(request):
    if request.method == "POST":
        form = PlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            return redirect('dashboard')
    else:
        form = PlayerForm()
    return render(request, 'users/create_player.html', {'form': form})

@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    # Ensure user is a player and not already in the team
    if request.user.role == "player" and not Player.objects.filter(user=request.user, team=team).exists():
        Player.objects.create(user=request.user, team=team, full_name=request.user.username, position="Undecided")

    return redirect('view_roster', team_id=team.id)


from django.contrib.auth.decorators import login_required
from .decorators import coach_required

@login_required
def create_team(request):
    if request.user.role != "coach":
        return HttpResponseForbidden("You are not authorized to view this page")  # Show error for non-coaches

    if request.method == "POST":
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.coach = request.user
            team.save()
            return redirect('dashboard')
    else:
        form = TeamForm()

    return render(request, 'users/create_team.html', {'form': form})

def home(request):
    return render(request, 'users/home.html')  # This template will be your home page

from django.shortcuts import render, get_object_or_404
from .models import Team, Player

@login_required
def view_roster(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = Player.objects.filter(team=team)  # Get all players on the team
    return render(request, 'users/roster.html', {'team': team, 'players': players})


@login_required
def add_player(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    if request.user != team.coach:
        return HttpResponseForbidden("You are not authorized to add players to this team.")

    if request.method == "POST":
        form = AddPlayerForm(request.POST)
        if form.is_valid():
            player = form.save(commit=False)
            player.team = team
            player.save()
            return redirect('view_roster', team_id=team.id)
    else:
        form = AddPlayerForm()

    return render(request, 'users/add_player.html', {'form': form, 'team': team})


### Joining Team via a Link

@login_required
def join_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)

    # Prevent duplicates
    if Player.objects.filter(user=request.user, team=team).exists():
        messages.warning(request, "You are already on this team.")
        return redirect('view_roster', team_id=team.id)

    # Add the player to the team
    Player.objects.create(user=request.user, full_name=request.user.username, team=team, position="Unknown")
    
    messages.success(request, f"You have joined {team.name}!")
    return redirect('view_roster', team_id=team.id)


###

@login_required
def view_roster(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    players = Player.objects.filter(team=team)  # Get all players for the team
    return render(request, 'users/roster.html', {'team': team, 'players': players})
