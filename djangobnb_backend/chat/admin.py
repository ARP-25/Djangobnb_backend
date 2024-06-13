from django.contrib import admin
from .models import Conversation, ConversationMessage

class ConversationMessageInline(admin.TabularInline):
    model = ConversationMessage
    extra = 1  # Number of extra empty forms to display
    readonly_fields = ('created_at',)

class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'modified_at', 'get_users')
    list_filter = ('created_at', 'modified_at')
    search_fields = ('id',)
    inlines = [ConversationMessageInline]
    
    def get_users(self, obj):
        return ", ".join([user.email for user in obj.users.all()])
    get_users.short_description = 'Users'

class ConversationMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'conversation', 'created_by', 'sent_to', 'created_at')
    list_filter = ('created_at', 'conversation')
    search_fields = ('body', 'created_by__email', 'sent_to__email')

admin.site.register(Conversation, ConversationAdmin)
admin.site.register(ConversationMessage, ConversationMessageAdmin)
