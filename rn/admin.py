from django.contrib import admin
from rn.models import UserDetails,Player,UserProfile,activePlayer, Bidder, Team
from rn.models import UserDetails,Player,UserProfile,activePlayer, Bidder,UserPurse,active
# Register your models here.

class UserDetailsAdmin(admin.ModelAdmin):
    exclude=[]

# class pBidModelAdmin(admin.ModelAdmin):
# 	exclude=["posted"]
    
class PlayerAdmin(admin.ModelAdmin):
    exclude=[]
    
class UserProfileAdmin(admin.ModelAdmin):
    exclue=[]
    


class BidAdmin(admin.ModelAdmin):
    exclude=[]

class activePlayerAdmin(admin.ModelAdmin):
	exclude=[]

class BidderAdmin(admin.ModelAdmin):
    exclude = []
class TeamAdmin(admin.ModelAdmin):
    exclude = []

class UserPurseAdmin(admin.ModelAdmin):
	exclude=[]

class activeAdmin(admin.ModelAdmin):
	exclude=[]

admin.site.register(active,activeAdmin)
admin.site.register(UserDetails,UserDetailsAdmin)
admin.site.register(Player,PlayerAdmin)
admin.site.register(UserProfile,UserProfileAdmin)

# admin.site.register(pBidModel,pBidModelAdmin)
admin.site.register(activePlayer,activePlayerAdmin)
admin.site.register(Bidder, BidderAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(UserPurse,UserPurseAdmin)
