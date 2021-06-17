from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user']
    search_fields = ['user__username', 'user__email']

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Language)
admin.site.register(Course)


class LessonAdmin(admin.ModelAdmin):
    # inlines = ['like']
    list_display = ['__str__', 'user']
    search_fields = ['user__username', 'user__email']

    class Meta:
        model = Lesson


admin.site.register(Lesson, LessonAdmin)


admin.site.register(Word)
admin.site.register(WordTranslation)
admin.site.register(Phrase)
admin.site.register(PhraseTranslation)
admin.site.register(Example)
admin.site.register(Topic)

admin.site.register(LearningCourses)
admin.site.register(LearningCourse)
admin.site.register(LearningLesson)

admin.site.register(WordScore)
admin.site.register(PhraseScore)
