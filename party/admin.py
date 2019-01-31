from django.contrib import admin

from party.models import Party, PartyUser, PartyCategory

admin.site.register(Party)
admin.site.register(PartyUser)
admin.site.register(PartyCategory)
