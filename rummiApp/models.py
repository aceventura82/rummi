from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User


class Game(models.Model):
    name = models.CharField(max_length=50)
    date = models.DateTimeField(auto_now_add=True)
    private = models.BooleanField(default=False, db_index=True)
    started = models.CharField(max_length=1, default="0")
    fullDraw = models.CharField(max_length=6, default='')
    speed = models.IntegerField(default=5)
    maxPlayers = models.IntegerField(default=4)
    code = models.CharField(max_length=10, unique=True)
    current_set = models.IntegerField(default=1)
    current_stack = models.CharField(max_length=500, default='')
    current_discarded = models.CharField(max_length=500, default='||||')
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    playersPos = models.CharField(max_length=100, default=',,,,')
    currentPlayerPos = models.IntegerField(default=0)
    moveStatus = models.IntegerField(default=1)


class GameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'private', 'fullDraw', 'speed', 'maxPlayers']


class GameFormEdit(ModelForm):
    class Meta:
        model = Game
        fields = ['name', 'private', 'speed', 'maxPlayers']


class Player(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True, db_index=True)
    city = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    country = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    birthDate = models.DateField(null=True, blank=True)
    extension = models.CharField(max_length=5, null=True, blank=True)
    notifications = models.CharField(max_length=5, null=True, blank=True, default='OFF')
    status = models.CharField(max_length=1, null=True, blank=True, db_index=True)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)


class PlayerForm(ModelForm):
    class Meta:
        model = Player
        fields = ['status', 'nickname', 'name', 'lastname', 'city', 'country', 'birthDate', 'extension', 'gender', 'notifications']


class GameSet(models.Model):
    set = models.IntegerField(default=1)
    date = models.DateTimeField(auto_now_add=True)
    fullDraw = models.BooleanField(default=False)
    points = models.IntegerField(default=0)
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    gameId = models.ForeignKey(Game, on_delete=models.CASCADE)
    current_cards = models.CharField(max_length=500, default='')
    drawn = models.CharField(max_length=100, default='')

    class Meta:
        unique_together = ('userId', 'gameId', 'set')


class GameSetForm(ModelForm):
    class Meta:
        model = GameSet
        fields = ['set', 'fullDraw', 'points', 'userId', 'gameId']


class GameMessages(models.Model):
    userId = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    msg = models.CharField(max_length=150)
    gameId = models.ForeignKey(Game, on_delete=models.CASCADE)


class GameMessagesForm(ModelForm):
    class Meta:
        model = GameMessages
        fields = ['msg', 'gameId']


class tmpPIN(models.Model):
    email = models.CharField(max_length=150)
    pin = models.CharField(max_length=6)

    class Meta:
        unique_together = ('email', 'pin')


class tmpPINForm(ModelForm):
    class Meta:
        model = tmpPIN
        fields = ['email', 'pin']
