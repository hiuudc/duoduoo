from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from .views import *

urlpatterns = [
    path('', views.home, name="home"),
    path('learn/', views.learn, name="learn"),

    path('register/', views.register, name="register"),
    path('courses/<str:language_id>/register/',
         views.registero, name="registero"),
    path('courses/<str:language_id>/register/<int:course_id>',
         views.course_register, name="course-register"),

    path('login/', auth_views.LoginView.as_view(
        template_name='base/login.html'), name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('profile/<str:username>/', views.profile, name="profile"),
    path('settings/profile/', views.settingsProfile, name="settings-profile"),
    path('settings/account/', views.settingsAccount, name="settings-account"),
    path('settings/password/', views.settingsPassword, name="settings-password"),

    path('words_learned/', views.wordsLearned, name="words-learned"),
    path('phrases_learned/', views.phrasesLearned, name="phrases-learned"),
    path('lessons_learning/', views.lessonLearning, name="lessons-learning"),

    path('courses/<int:course_id>/words/',
         views.words, name="course-words"),
    path('courses/<int:course_id>/words/<int:word_id>/translations/',
         views.word, name="word-detail"),
    path('courses/<int:course_id>/words/add/',
         views.addWord, name="word-add"),

    path('courses/<int:course_id>/words/<int:word_id>/translations/add/',
         views.addWordTrans, name="word-translation-add"),
    path('courses/<int:course_id>/words/<int:word_id>/translations/<int:word_translation_id>/edit/',
         views.editWordTrans, name="word-translation-edit"),
    path('courses/<int:course_id>/words/<int:word_id>/translations/<int:word_translation_id>/remove/',
         views.removeWordTrans, name="word-translation-remove"),


    path('courses/<int:course_id>/phrases/',
         views.phrases, name="course-phrases"),
    path('courses/<int:course_id>/phrases/<int:phrase_id>/translations/',
         views.phrase, name="phrase-detail"),
    path('courses/<int:course_id>/phrases/add/',
         views.addPhrase, name="phrase-add"),

    path('courses/<int:course_id>/phrases/<int:phrase_id>/translations/add/',
         views.addPhraseTranslation, name="phrase-translation-add"),
    path('courses/<int:course_id>/phrases/<int:phrase_id>/translations/<int:phrase_translation_id>/edit/',
         views.editPhraseTranslation, name="phrase-translation-edit"),
    path('courses/<int:course_id>/phrases/<int:phrase_id>/translations/<int:phrase_translation_id>/remove/',
         views.removePhraseTranslation, name="phrase-translation-remove"),

    path('languages-json/',
         views.get_json_languages_data, name="languages-json"),
    path('courses-json/<str:language_id>/',
         views.get_json_courses_data, name="courses-json"),


    path('courses/', views.courses, name="courses"),
    path('courses/<str:language_id>/', views.courseso, name="courseso"),
    path('courses/enroll/<int:course_id>/',
         views.course_enroll, name="course-enroll"),

    path('courses/<int:course_id>/', views.course, name="course-detail"),
    path('courses/<int:course_id>/lessons/',
         views.lessons, name="course-lessons"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/',
         views.lesson, name="lesson-detail"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/learn/',
         views.lessonLearn, name="lesson-learn"),

    path('courses/<int:course_id>/lessons/<int:lesson_id>/search_word/<str:word_qr>/',
         views.lesson_search_word, name="lesson-search-word"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/add_word/<int:word_id>/',
         views.lesson_add_word, name="lesson-add-word"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/unknow_word/add/',
         views.lesson_add_unknow_word, name="lesson-add-unknow-word"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/remove_word/<int:word_id>/',
         views.lesson_remove_word, name="lesson-remove-word"),

    path('courses/<int:course_id>/lessons/<int:lesson_id>/search_phrase/<str:phrase_qr>/',
         views.lesson_search_phrase, name="lesson-search-phrase"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/add_phrase/<int:phrase_id>/',
         views.lesson_add_phrase, name="lesson-add-phrase"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/unknow_phrase/add/',
         views.lesson_add_unknow_phrase, name="lesson-add-unknow-phrase"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/remove_phrase/<int:phrase_id>/',
         views.lesson_remove_phrase, name="lesson-remove-phrase"),

    path('courses/<int:course_id>/lessons/<int:lesson_id>/search_example/<str:example_qr>/',
         views.lesson_search_example, name="lesson-search-example"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/add_example/<int:example_id>/',
         views.lesson_add_example, name="lesson-add-example"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/unknow_example/add/',
         views.lesson_add_unknow_example, name="lesson-add-unknow-example"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/remove_example/<int:example_id>/',
         views.lesson_remove_example, name="lesson-remove-example"),

    path('courses/<int:course_id>/lesson_add/',
         views.addLesson, name="lesson-add"),

    # ~ remove soon
    path('courses/<int:course_id>/lessons/<int:lesson_id>/lesson_edit/',
         views.editLesson, name="lesson-edit"),
    path('courses/<int:course_id>/lessons/<int:lesson_id>/lesson_remove/',
         views.removeLesson, name="lesson-remove"),

    path('courses/<int:course_id>/examples/',
         views.examples, name="course-examples"),
    path('courses/<int:course_id>/examples/<int:example_id>/',
         views.example, name="example-detail"),

    path('courses/<int:course_id>/example_add/',
         views.addExample, name="example-add"),
    path('courses/<int:course_id>/examples/<int:example_id>/example_edit/',
         views.editExample, name="example-edit"),
    path('courses/<int:course_id>/examples/<int:example_id>/example_remove/',
         views.removeExample, name="example-remove"),






    path('reset_password/',
         auth_views.PasswordResetView.as_view(
             template_name="base/password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(
             template_name="base/password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name="base/password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name="base/password_reset_done.html"),
         name="password_reset_complete"),
]
