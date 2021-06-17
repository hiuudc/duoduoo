from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, UsernameField

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from .forms import *
from .models import *
from .decorators import *
from django.views.generic import *

import json
from datetime import datetime, date
from django.utils import timezone
from django.db.models import F, Q


def register(request):
    if request.user.is_anonymous:
        return render(request, 'base/register.html')
    else:
        return redirect('learn')


def registero(request, language_id):
    return render(request, 'base/register.html', {'language_id': language_id})


def course_register(request, language_id, course_id):
    if request.user.is_anonymous:
        course = Course.objects.get(id=course_id)
        if request.method == 'POST':
            formRegister = UserRegisterForm(request.POST)
            if formRegister.is_valid():
                user = formRegister.save()

                learningcourses = LearningCourses.objects.create(
                    user=user, course=course)
                learningcourses.save()

                learningcourse = LearningCourse.objects.create(
                    user=user, course=course)
                learningcourse.save()

                username = formRegister.cleaned_data.get('username')
                email = formRegister.cleaned_data.get('email')
                messages.success(
                    request, f"Your account has been created with username: {username} and email: {email}.")
                return redirect('login')
        else:
            formRegister = UserRegisterForm()
        context = {'formRegister': formRegister, 'course': course}
        return render(request, 'base/course/course_register.html', context)
    else:
        return redirect('learn')


def logoutUser(request):
    logout(request)
    return redirect('login')

# @allowed_user(allowed_roll=['admin'])


def profile(request, username):
    try:
        user = User.objects.get(username=username)
        learning_courses = LearningCourses.objects.filter(user=user.id)
        if request.method == 'POST' and request.user.id == user.id:
            form = ProfileUpdateForm(request.POST, request.FILES,
                                     instance=request.user.profile)
            if form.is_valid():
                form.save()
                messages.success(
                    request, f"Your profile has been updated!")
                return redirect('profile', username=username)
        else:
            form = ProfileUpdateForm(instance=request.user.profile)

        context = {'user': user,
                   'learning_courses': learning_courses, 'form': form}
    except:
        context = {'user': None,
                   'learning_courses': None, 'form': None}
    return render(request, 'base/profile.html', context)


@login_required()
def settingsProfile(request):
    user = User.objects.get(user=request.user)

    context = {'user': user, }

    return render(request, 'base/settings/profile.html', context)
# !done


@login_required()
def settingsAccount(request):

    context = {}

    return render(request, 'base/settings/account.html', context)
# !done


@login_required()
def settingsPassword(request):
    context = {}
    return render(request, 'base/settings/password.html', context)
# !done

# Entry.objects.filter(id=10).update(comments_on=False)


def home(request, *args, **kwargs):
    if request.user.is_anonymous:
        context = {}
        return render(request, 'base/home.html', context)
    else:
        return redirect('learn')


@login_required()
def learn(request):
    learning_course = LearningCourse.objects.get(user=request.user)
    learning_courses = LearningCourses.objects.filter(
        user=request.user).exclude(course=learning_course.course.id)

    lessons_learning = LearningLesson.objects.filter(
        user=request.user, course=learning_course.course.id)
    words = WordScore.objects.filter(
        user=request.user, course=learning_course.course.id, last_practiced__date=timezone.now().date()).count()
    phrases = PhraseScore.objects.filter(
        user=request.user, course=learning_course.course.id, last_practiced__date=timezone.now().date()).count()
    context = {'lessons_learning': lessons_learning, 'learning_courses': learning_courses,
               'learning_course': learning_course, 'learning_language': learning_course.course.learning_language,
               'words': words, 'phrases': phrases}
    return render(request, 'base/learn.html', context)


@login_required()
def wordsLearned(request):
    learning_course = LearningCourse.objects.get(user=request.user)
    try:
        words = request.user.wordscore_set.all().filter(course=learning_course.course.id)
        context = {'words': words, 'learning_language': learning_course.course.learning_language,
                   'learning_course': learning_course}
        return render(request, 'base/word/words_learned.html', context)
    except:
        context = {'words': None, 'learning_language': learning_course.course.learning_language,
                   'learning_course': learning_course}
        return render(request, 'base/word/words_learned.html', context)


@login_required()
def phrasesLearned(request):
    learning_course = LearningCourse.objects.get(user=request.user)
    try:
        phrases = request.user.phrasescore_set.all().filter(
            course=learning_course.course.id)
        context = {'phrases': phrases, 'learning_language': learning_course.course.learning_language,
                   'learning_course': learning_course}
        return render(request, 'base/phrase/phrases_learned.html', context)
    except:
        context = {'phrases': None, 'learning_language': learning_course.course.learning_language,
                   'learning_course': learning_course}
        return render(request, 'base/phrase/phrases_learned.html', context)


@login_required()
def lessonLearning(request):
    learning_course = LearningCourse.objects.get(user=request.user)

    learning_lessons = LearningLesson.objects.filter(
        user=request.user, course=learning_course.course)

    context = {'learning_lessons': learning_lessons, 'learning_language': learning_course.course.learning_language,
               'learning_course': learning_course}
    return render(request, 'base/lesson/lessons_learning.html', context)


@login_required()
def words(request, course_id):
    course = Course.objects.get(id=course_id)
    words = Word.objects.filter(language=course.learning_language)

    context = {'words': words, 'course': course}
    return render(request, 'base/word/words.html', context)


@login_required()
def word(request, course_id, word_id):
    course = Course.objects.get(id=course_id)
    word = Word.objects.get(language=course.learning_language, id=word_id)
    translations = word.wordtranslation_set.all()

    context = {'word': word, 'course': course,
               'translations': translations}
    return render(request, 'base/word/word_detail.html', context)


class WordCreateView(LoginRequiredMixin, CreateView):
    model = Word
    fields = ['word', 'topic']
    success_url = reverse_lazy('course-words')

    def form_valid(self, form):
        form.instance.user = self.request.user
        learningCourse = LearningCourse.objects.get(user=self.request.user)
        form.instance.course = Course.objects.get(id=learningCourse.id)
        return super().form_valid(form)


@login_required()
def addWord(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = WordForm(request.POST)
        if form.is_valid():
            word = form.cleaned_data.get('word')
            new_word = Word.objects.create(
                user=request.user,
                word=word,
                language=course.learning_language
            )
            new_word.save()
            topics = form.cleaned_data.get('topic')
            for topic in topics:
                new_word.topic.add(topic)

            messages.success(
                request, f"Added {word} to this course.")
            return redirect('course-words', course_id=course_id)
    else:
        form = WordForm()
    context = {'form': form, 'course': course, }
    return render(request, 'base/word/word_form.html', context)


class WordTransCreateView(LoginRequiredMixin, CreateView):
    model = WordTranslation
    fields = ['word', 'part_of_speech', 'ipa', 'meaning', 'definition']

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.word = self.kwargs['word_id']
        learningCourse = LearningCourse.objects.get(user=self.request.user)
        form.instance.course = Course.objects.get(id=learningCourse.id)
        return super().form_valid(form)


@login_required()
def addWordTrans(request, course_id, word_id):
    course = Course.objects.get(id=course_id)
    word = Word.objects.get(id=word_id, language=course.learning_language)

    if request.method == 'POST':
        form = WordTransForm(request.POST, initial={
            'user': request.user, 'word': word})
        if form.is_valid():
            if WordTranslation.objects.filter(word=word, user=request.user, course=course).exists():
                word_trans = WordTranslation.objects.filter(
                    word=word, user=request.user, course=course)
                for word_tran in word_trans:
                    if form.cleaned_data.get('part_of_speech') == word_tran.part_of_speech:
                        messages.info(
                            request, f"You already have a translation of {word} with part of speech: {word_tran.part_of_speech}.")
                        return render(request, 'base/word/word_trans_form.html', {'form': form, 'course': course, 'word': word, 'action': 'Add'})
            else:
                new_word_trans = WordTranslation.objects.create(user=request.user, word=word, course=course,
                                                                part_of_speech=form.cleaned_data.get('part_of_speech'), ipa=form.cleaned_data.get('ipa'),
                                                                meaning=form.cleaned_data.get('meaning'), definition=form.cleaned_data.get('definition'),
                                                                node=form.cleaned_data.get('node'),)
                new_word_trans.save()
                messages.success(
                    request, f"Added your translation for {word}.")

                return redirect('word-detail', course_id=course_id, word_id=word_id)
    else:
        form = WordTransForm(initial={
            'user': request.user, 'word': word})
    context = {'form': form, 'course': course, 'word': word, 'action': 'Add'}
    return render(request, 'base/word/word_trans_form.html', context)


class WordTransUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = WordTranslation
    fields = ['part_of_speech', 'ipa', 'meaning', 'definition']

    # def form_valid(self, form):
    #     form.instance.user = self.request.user
    #     learningCourse = LearningCourse.objects.get(user=self.request.user)
    #     form.instance.course = Course.objects.get(id=learningCourse.id)
    #     return super().form_valid(form)

    def test_func(self):
        word_trans = self.get_object()
        if self.request.user == word_trans.user:
            return True
        return False


@login_required()
def editWordTrans(request, course_id, word_id, word_translation_id):
    course = Course.objects.get(id=course_id)
    word = Word.objects.get(id=word_id, language=course.learning_language)
    word_trans = WordTranslation.objects.get(
        id=word_translation_id, user=request.user, course=course_id)

    if request.method == 'POST' and request.user.id == word_trans.user.id:
        form = WordTransForm(request.POST, instance=word_trans, initial={
                             'user': request.user, 'word': word_trans.word})
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Edited your translation for {word}.")
            return redirect('word-detail', course_id=course_id, word_id=word_id)
    else:
        form = WordTransForm(instance=word_trans)

    context = {'form': form, 'course': course,
               'word': word, 'word_trans': word_trans, 'action': 'Edit'}
    return render(request, 'base/word/word_trans_form.html', context)


class WordTransDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = WordTranslation

    def test_func(self):
        word_trans = self.get_object()
        if self.request.user == word_trans.user:
            return True
        return False


@login_required()
def removeWordTrans(request, course_id, word_id, word_translation_id):
    course = Course.objects.get(id=course_id)
    word = Word.objects.get(id=word_id, language=course.learning_language)
    word_trans = WordTranslation.objects.get(
        id=word_translation_id, user=request.user, course=course_id)

    if request.method == 'POST' and request.user.id == word_trans.user.id:
        if request.user == word_trans.user:
            word_trans.delete()
            messages.success(
                request, f"Removed your translation for {word}.")
        return redirect('word-detail', course_id=course_id, word_id=word_id)
    else:
        form = WordTransForm(instance=word_trans)

    context = {'form': form, 'course': course,
               'word': word, 'action': 'Remove'}
    return render(request, 'base/word/word_trans_form.html', context)


@login_required()
def phrases(request, course_id):
    course = Course.objects.get(id=course_id)
    phrases = Phrase.objects.filter(language=course.learning_language)

    context = {'phrases': phrases, 'course': course}
    return render(request, 'base/phrase/phrases.html', context)


@login_required()
def phrase(request, course_id, phrase_id):
    course = Course.objects.get(id=course_id)
    phrase = Phrase.objects.get(
        id=phrase_id, language=course.learning_language)
    translations = phrase.phrasetranslation_set.all()

    context = {'phrase': phrase, 'course': course,
               'translations': translations}
    return render(request, 'base/phrase/phrase_detail.html', context)


@login_required()
def addPhrase(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = PhraseForm(request.POST)
        if form.is_valid():
            phrase = form.cleaned_data.get('phrase')
            new_phrase = Phrase.objects.create(
                user=request.user,
                phrase=phrase,
                language=course.learning_language
            )
            new_phrase.save()
            topics = form.cleaned_data.get('topic')
            for topic in topics:
                new_phrase.topic.add(topic)

            messages.success(
                request, f"Added new phrase: \"{phrase}\" to this course.")
            return redirect('course-phrases', course_id=course_id)
    else:
        form = PhraseForm()
    context = {'form': form, 'course': course, }
    return render(request, 'base/phrase/phrase_form.html', context)


@login_required()
def addPhraseTranslation(request, course_id, phrase_id):
    course = Course.objects.get(id=course_id)
    phrase = Phrase.objects.get(
        id=phrase_id, language=course.learning_language)

    if request.method == 'POST':
        form = PhraseTransForm(request.POST, initial={
            'user': request.user, 'phrase': phrase})

        if PhraseTranslation.objects.filter(user=request.user, course=course, phrase=phrase,).exists():
            messages.info(
                request, f"You already have a translation of '{phrase}'.")
            return render(request, 'base/phrase/phrase_trans_form.html', {'form': form, 'course': course,
                                                                          'phrase': phrase, 'action': 'Add'})
        else:
            if form.is_valid():
                new_phrase_trans = PhraseTranslation.objects.create(
                    user=request.user,
                    course=course,
                    phrase=phrase,
                    ipa=form.cleaned_data.get('ipa'),
                    meaning=form.cleaned_data.get('meaning'),
                    definition=form.cleaned_data.get('definition')
                )
                new_phrase_trans.save()
                messages.success(
                    request, f"Added your translation of '{phrase}'.")

                return redirect('phrase-detail', course_id=course_id, phrase_id=phrase_id)
    else:
        form = PhraseTransForm(initial={
            'user': request.user, 'phrase': phrase})
    context = {'form': form, 'course': course,
               'phrase': phrase, 'action': 'Add'}
    return render(request, 'base/phrase/phrase_trans_form.html', context)


@login_required()
def editPhraseTranslation(request, course_id, phrase_id, phrase_translation_id):
    course = Course.objects.get(id=course_id)
    phrase = Phrase.objects.get(
        id=phrase_id, language=course.learning_language)
    phrase_trans = PhraseTranslation.objects.get(
        id=phrase_translation_id, user=request.user, course=course_id)

    if request.method == 'POST' and request.user.id == phrase_trans.user.id:
        form = PhraseTransForm(request.POST, instance=phrase_trans, initial={
            'user': request.user, 'phrase': phrase_trans.phrase})
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Edited your translation for {phrase}.")
            return redirect('phrase-detail', course_id=course_id, phrase_id=phrase_id)
    else:
        form = PhraseTransForm(instance=phrase_trans)

    context = {'form': form, 'course': course,
               'phrase': phrase, 'action': 'Edit'}
    return render(request, 'base/phrase/phrase_trans_form.html', context)


@login_required()
def removePhraseTranslation(request, course_id, phrase_id, phrase_translation_id):
    course = Course.objects.get(id=course_id)
    phrase = Phrase.objects.get(
        id=phrase_id, language=course.learning_language)
    phrase_trans = PhraseTranslation.objects.get(
        id=phrase_translation_id, user=request.user, course=course_id)

    if request.method == 'POST' and request.user.id == phrase_trans.user.id:
        if request.user == phrase_trans.user:
            phrase_trans.delete()
            messages.success(
                request, f"Removed your translation for {phrase}.")
            return redirect('phrase-detail', course_id=course_id, phrase_id=phrase_id)
    else:
        form = PhraseTransForm(instance=phrase_trans, initial={
            'user': phrase_trans.user, 'phrase': phrase_trans.phrase})

    context = {'form': form, 'course': course,
               'phrase': phrase, 'action': 'Remove'}
    return render(request, 'base/phrase/phrase_trans_form.html', context)


@login_required()
def examples(request, course_id):
    course = Course.objects.get(id=course_id)
    examples = Example.objects.filter(course=course_id)

    context = {'examples': examples, 'course': course}
    return render(request, 'base/example/examples.html', context)


@login_required()
def example(request, course_id, example_id):
    course = Course.objects.get(id=course_id)
    example = Example.objects.get(id=example_id, course=course_id)

    context = {'course': course, 'example': example}
    return render(request, 'base/example/example_detail.html', context)


@login_required()
def addExample(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            example = form.cleaned_data.get('example')
            new_example = Example.objects.create(
                user=request.user,
                example=example,
                course=course
            )
            new_example.save()
            topics = form.cleaned_data.get('topic')
            for topic in topics:
                new_example.topic.add(topic)

            messages.success(
                request, f"Added \"{example}\" to this course.")
            return redirect('course-examples', course_id=course_id)
    else:
        form = ExampleForm()
    context = {'form': form, 'course': course, 'action': 'Add'}
    return render(request, 'base/example/example_form.html', context)


@login_required()
def editExample(request, course_id, example_id):
    course = Course.objects.get(id=course_id)
    example = Example.objects.get(
        id=example_id, course=course_id, user=request.user)

    if request.method == 'POST' and request.user.id == example.user.id:
        form = ExampleForm(request.POST, instance=example, initial={
            'user': request.user, 'example': example.example})
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Edited your \"{example}\".")
            return redirect('example-detail', course_id=course_id, example_id=example_id)
    else:
        form = ExampleForm(instance=example)

    context = {'form': form, 'course': course,
               'example': example, 'action': 'Edit'}
    return render(request, 'base/example/example_form.html', context)


@login_required()
def removeExample(request, course_id, example_id):
    course = Course.objects.get(id=course_id)
    example = Example.objects.get(
        id=example_id, course=course_id, user=request.user)

    if request.method == 'POST' and request.user.id == example.user.id:
        if request.user == example.user:
            example.delete()
            messages.success(
                request, f"Removed your \"{example}\".")
            return redirect('example-detail', course_id=course_id, example_id=example_id)
    else:
        form = ExampleForm(instance=example, initial={
            'user': example.user, 'example': example.example})

    context = {'form': form, 'course': course,
               'example': example, 'action': 'Remove'}
    return render(request, 'base/example/example_form.html', context)


@login_required()
def courses(request):
    return render(request, 'base/course/courses.html')


@login_required()
def courseso(request, language_id):
    return render(request, 'base/course/courses.html', {'language_id': language_id})


def get_json_languages_data(request):
    obj_languages = list(Language.objects.all().values())
    return JsonResponse({'data': obj_languages})


def get_json_courses_data(request, *args, **kwargs):
    selected_language_id = kwargs.get('language_id')
    data = []
    if request.user.is_anonymous:
        if selected_language_id == "all":
            courses = Course.objects.all()
            [data.append({"id": x.id, "name_course": str(x), "learners": x.get_learners(), "enroll": False})
                for x in courses]
        else:
            courses = Course.objects.filter(
                speaking_language=selected_language_id)
            [data.append({"id": x.id, "name_course": str(x), "learners": x.get_learners(), "enroll": False})
                for x in courses]
    else:
        if selected_language_id == "all":
            courses = Course.objects.all()
            [data.append({"id": x.id, "name_course": str(x), "learners": x.get_learners(), "enroll": x.enroll(request.user)})
                for x in courses]
        else:
            courses = Course.objects.filter(
                speaking_language=selected_language_id)
            [data.append({"id": x.id, "name_course": str(x), "learners": x.get_learners(), "enroll": x.enroll(request.user)})
                for x in courses]
    return JsonResponse({'data': data})


@login_required()
def course_enroll(request, course_id):
    course = Course.objects.get(id=course_id)
    if request.is_ajax and request.method == "POST":
        if LearningCourses.objects.filter(course=course, user=request.user):
            try:
                if LearningCourse.objects.get(user=request.user):
                    edit2learningc = LearningCourse.objects.get(
                        user=request.user)
                    edit2learningc.course = course
                    edit2learningc.save()
            except:
                add2learningc = LearningCourse.objects.create(
                    course=course, user=request.user)
                add2learningc.save()
        else:
            add2learningcourses = LearningCourses.objects.create(
                course=course, user=request.user)
            add2learningcourses.save()
            try:
                if LearningCourse.objects.get(user=request.user):
                    edit2learningc = LearningCourse.objects.get(
                        user=request.user)
                    edit2learningc.course = course
                    edit2learningc.save()
            except:
                add2learningc = LearningCourse.objects.create(
                    course=course, user=request.user)
                add2learningc.save()

        return JsonResponse("Successfully...", safe=False)

    context = {'course': course, 'learners': course.get_learners(), 'words': course.get_words(),
               'phrases': course.get_phrases(), 'examples': course.get_examples(), 'lessons': course.get_lessons()}
    return render(request, 'base/course/course_enroll.html', context)


@login_required()
def course(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course_id)

    context = {'lessons': lessons, 'course': course}
    return render(request, 'base/course/course_detail.html', context)


@login_required()
def lessons(request, course_id):
    course = Course.objects.get(id=course_id)
    lessons = Lesson.objects.filter(course=course_id)

    context = {'lessons': lessons, 'course': course}
    return render(request, 'base/course/course_detail.html', context)


@login_required()
def lesson(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id)

    if request.is_ajax and request.method == "POST":
        # words = request.POST.get("words")
        data = json.loads(request.body)
        words = data['words']
        phrases = data['phrases']

        for wrd in words:
            # word_update = WordScore.objects.filter(
            #     course=course, user=request.user, word=wrd["word_id"]).update(
            #         listening=wrd["listening"], speaking=wrd["speaking"],
            #         reading=wrd["reading"], writing=wrd["writing"])

            wordS = WordScore.objects.get(
                course=course, user=request.user, word=wrd["word_id"])
            wordS.listening = wrd["listening"]
            wordS.speaking = wrd["speaking"]
            wordS.reading = wrd["reading"]
            wordS.writing = wrd["writing"]
            wordS.save()

        for phr in phrases:
            phraseS = PhraseScore.objects.get(
                course=course, user=request.user, phrase=phr["phrase_id"])
            phraseS.listening = wrd["listening"]
            phraseS.speaking = wrd["speaking"]
            phraseS.reading = wrd["reading"]
            phraseS.writing = wrd["writing"]
            phraseS.save()

        return JsonResponse("Successfully...", safe=False)
    else:
        lesson = Lesson.objects.get(id=lesson_id, course=course_id)
        remove = False
        if request.user.id == lesson.user.id:
            remove = True
        admin = User.objects.get(username="admin")

        # Words
        words_in_lesson = lesson.word.all()
        word_trans = WordTranslation.objects.filter(Q(user=admin) | Q(user=request.user),
                                                    course=course_id, word__id__in=words_in_lesson)
        words_learning_list = list(words_in_lesson)
        words_list = []

        for word in words_learning_list:
            word_tran = None
            edit = False
            if word_trans.filter(user=request.user, word=word.id).exists():
                word_tran = word_trans.filter(
                    word=word.id, user=request.user)
                edit = True
            elif word_trans.filter(user=admin, word=word.id).exists():
                word_tran = word_trans.filter(
                    word=word.id, user=admin)

            if word_tran is not None:
                for wort in word_tran.values():
                    words_list.append({"word_id": word.id, "word": str(word.word), "part_of_speech": wort["part_of_speech"], "ipa": wort["ipa"],
                                       "meaning": wort["meaning"], "definition": wort["definition"], "translation_id": wort["id"],
                                       "edit": edit, "remove": remove, "missing_translation": False, })
            else:
                words_list.append(
                    {"word_id": word.id, "word": word.word, "missing_translation": True, "edit": edit, "remove": remove, })
        # Phrases
        phrases_in_lesson = lesson.phrase.all()
        phrase_trans = PhraseTranslation.objects.filter(Q(user=admin) | Q(user=request.user),
                                                        course=course_id, phrase__id__in=phrases_in_lesson)
        phrases_learning_list = list(phrases_in_lesson)
        phrases_list = []

        for phrase in phrases_learning_list:
            phrase_tran = None
            edit = False
            if phrase_trans.filter(phrase=phrase.id, user=request.user).exists():
                phrase_tran = phrase_trans.filter(
                    phrase=phrase.id, user=request.user)
                edit = True
            elif phrase_trans.filter(phrase=phrase.id, user=admin).exists():
                word_tran = phrase_trans.filter(
                    phrase=phrase.id, user=admin)

            if phrase_tran is not None:
                [phrases_list.append({"phrase_id": x.phrase.id, "phrase": str(x.phrase), "ipa": x.ipa,
                                      "meaning": x.meaning, "definition": x.definition, 'translation_id': x.id,
                                      "edit": edit, "remove": remove, "missing_translation": False, }) for x in phrase_tran]
            else:
                phrases_list.append(
                    {"phrase_id": phrase.id, "phrase": phrase.phrase, "missing_translation": True, "edit": edit, "remove": remove, })

        # Examples
        examples_in_lesson = lesson.example.all()
        examples_list = []
        for example in examples_in_lesson:
            missing_translation = True
            if example.translation is not None:
                missing_translation = False
            examples_list.append({"id": example.id, "example": str(example.example),
                                  "translation": example.translation, "node": example.node, "edit": remove, "remove": remove, "missing_translation": missing_translation})

        context = {'course': course, 'lesson': lesson,
                   'words_list': json.dumps(words_list),
                   'phrases_list': json.dumps(phrases_list),
                   'examples_list': json.dumps(examples_list),
                   }
        return render(request, 'base/lesson/lesson_detail.html', context)

# relative_words = Word.objects.filter(topic__id__in=word.topic.all())
# word__in = ?
# filter(Q(name__icontains=query) | Q(state__icontains=query))
# .exclude(word__in=lesson.word.all())


@login_required()
def lesson_search_word(request, course_id, lesson_id, word_qr):
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)

    if request.is_ajax and request.method == "GET":
        specific_word = False
        if Word.objects.filter(language=course.learning_language.id, word=str(word_qr)).exists():
            specific_word = True
        wordResults = Word.objects.filter(language=course.learning_language.id,
                                          word__contains=str(word_qr))
        dataSendBack = []
        for word in wordResults:
            learning = False
            if word in lesson.word.all():
                learning = True
                dataSendBack.append(
                    {'id': word.id, 'word': word.word, 'user_id': word.user_id, 'language_id': word.language_id, 'learning': learning})
            else:
                dataSendBack.append(
                    {'id': word.id, 'word': word.word, 'user_id': word.user_id, 'language_id': word.language_id, 'learning': learning})
        return JsonResponse({'data': dataSendBack, 'specific_word': specific_word}, safe=False)


@login_required()
def lesson_add_word(request, course_id, lesson_id, word_id):
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)
    if request.is_ajax and request.method == "POST":
        if request.user.id == lesson.user.id:
            course = Course.objects.get(id=course_id)
            word = Word.objects.get(
                id=word_id, language=course.learning_language)
            lesson.word.add(word)
            add_word_score, created = WordScore.objects.get_or_create(
                user=request.user, course=course, word=word)

            admin = User.objects.get(username="admin")
            word_tran = None
            edit = False
            if WordTranslation.objects.filter(user=request.user, word=word.id).exists():
                word_tran = WordTranslation.objects.filter(
                    word=word.id, user=request.user)
                edit = True
            elif WordTranslation.objects.filter(user=admin, word=word.id).exists():
                word_tran = WordTranslation.objects.filter(
                    word=word.id, user=admin)

            word_tran_sendback = []
            if word_tran is not None:
                for wort in word_tran.values():
                    word_tran_sendback.append({"word_id": word.id, "word": str(word.word), "part_of_speech": wort["part_of_speech"], "ipa": wort["ipa"],
                                               "meaning": wort["meaning"], "definition": wort["definition"], "translation_id": wort["id"],
                                               "edit": edit, "remove": True, "missing_translation": False, })
            else:
                word_tran_sendback.append(
                    {"word_id": word.id, "word": word.word, "missing_translation": True, "edit": edit, "remove": True, })
            return JsonResponse({'data': word_tran_sendback}, safe=False)
        return JsonResponse(f"You aren't the author.", safe=False)


@login_required()
def lesson_add_unknow_word(request, course_id, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)
    if request.is_ajax and request.method == "POST":
        if request.user.id == lesson.user.id:
            course = Course.objects.get(id=course_id)

            data = json.loads(request.body)
            word = data['unknow_word']
            part_of_speech = data['part_of_speech']
            ipa = data['ipa']
            meaning = data['meaning']
            definition = data['definition']
            node = data['node']

            if Word.objects.filter(word=word, language=course.learning_language).exists():
                return JsonResponse(f"{word} is already exist.", safe=False)
            else:
                new_word = Word.objects.create(
                    word=word, language=course.learning_language, user=request.user)
                new_word.save()

                new_word_tran = WordTranslation.objects.create(word=new_word, user=request.user, course=course,
                                                               part_of_speech=part_of_speech, ipa=ipa, meaning=meaning, definition=definition, node=node)
                new_word_tran.save()
                lesson.word.add(new_word)
                add_word_score, created = WordScore.objects.get_or_create(
                    user=request.user, course=course, word=new_word)

                return JsonResponse(f"Added {word} and its translation.", safe=False)
        return JsonResponse(f"You aren't the author.", safe=False)


@login_required()
def lesson_remove_word(request, course_id, lesson_id, word_id):
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)
    if request.is_ajax and request.method == "POST":
        if request.user.id == lesson.user.id:
            course = Course.objects.get(id=course_id)
            word = Word.objects.get(
                id=word_id, language=course.learning_language)
            lesson.word.remove(word)
            return JsonResponse(f"Removed {word} successfully...", safe=False)
        return JsonResponse(f"You aren't the author.", safe=False)


@login_required()
def lesson_search_phrase(request, course_id, lesson_id, phrase_qr):
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)

    if request.is_ajax and request.method == "GET":
        specific_phrase = False
        if Phrase.objects.filter(language=course.learning_language.id, phrase=str(phrase_qr)).exists():
            specific_phrase = True
        phraseResults = Phrase.objects.filter(language=course.learning_language.id,
                                              phrase__contains=str(phrase_qr))
        dataSendBack = []
        for phrase in phraseResults:
            learning = False
            if phrase in lesson.phrase.all():
                learning = True
                dataSendBack.append(
                    {'id': phrase.id, 'phrase': phrase.phrase, 'user_id': phrase.user_id, 'learning': learning})
            else:
                dataSendBack.append(
                    {'id': phrase.id, 'phrase': phrase.phrase, 'user_id': phrase.user_id, 'learning': learning})
        return JsonResponse({'data': dataSendBack, 'specific_phrase': specific_phrase}, safe=False)


@login_required()
def lesson_add_phrase(request, course_id, lesson_id, phrase_id):
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)
    if request.is_ajax and request.method == "POST":
        if request.user.id == lesson.user.id:
            course = Course.objects.get(id=course_id)
            phrase = Phrase.objects.get(
                id=phrase_id, language=course.learning_language)
            lesson.phrase.add(phrase)
            add_phrase_score, created = PhraseScore.objects.get_or_create(
                user=request.user, course=course, phrase=phrase)

            admin = User.objects.get(username="admin")
            phrase_tran = None
            edit = False
            if PhraseTranslation.objects.filter(user=request.user, phrase=phrase.id).exists():
                phrase_tran = PhraseTranslation.objects.filter(
                    phrase=phrase.id, user=request.user)
                edit = True
            elif PhraseTranslation.objects.filter(user=admin, phrase=phrase.id).exists():
                phrase_tran = PhraseTranslation.objects.filter(
                    phrase=phrase.id, user=admin)

            phrase_tran_sendback = []
            if phrase_tran is not None:
                [phrase_tran_sendback.append({"phrase_id": x.phrase.id, "phrase": str(x.phrase), "ipa": x.ipa,
                                              "meaning": x.meaning, "definition": x.definition, "translation_id": x.id,
                                              "edit": edit, "remove": True, "missing_translation": False, }) for x in phrase_tran]
            else:
                phrase_tran_sendback.append(
                    {"phrase_id": phrase.id, "phrase": phrase.phrase, "edit": edit, "remove": True,
                     "missing_translation": True, })
            return JsonResponse({'data': phrase_tran_sendback}, safe=False)
        return JsonResponse(f"You aren't the author.", safe=False)


@login_required()
def lesson_add_unknow_phrase(request, course_id, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)
    if request.is_ajax and request.method == "POST":
        if request.user.id == lesson.user.id:
            course = Course.objects.get(id=course_id)

            data = json.loads(request.body)
            phrase = data['unknow_phrase']
            ipa = data['ipa']
            meaning = data['meaning']
            definition = data['definition']
            node = data['node']

            if Phrase.objects.filter(phrase=phrase, language=course.learning_language).exists():
                return JsonResponse(f"{phrase} is already exist.", safe=False)
            else:
                new_phrase = Phrase.objects.create(
                    phrase=phrase, language=course.learning_language, user=request.user)
                new_phrase.save()

                new_phrase_tran = PhraseTranslation.objects.create(phrase=new_phrase, user=request.user, course=course,
                                                                   ipa=ipa, meaning=meaning, definition=definition, node=node)
                new_phrase_tran.save()
                lesson.phrase.add(new_phrase)
                add_phrase_score, created = PhraseScore.objects.get_or_create(
                    user=request.user, course=course, phrase=new_phrase)

                return JsonResponse(f"Added {phrase} and its translation.", safe=False)
        return JsonResponse(f"You aren't the author.", safe=False)


@login_required()
def lesson_remove_phrase(request, course_id, lesson_id, phrase_id):
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)
    if request.is_ajax and request.method == "POST":
        if request.user.id == lesson.user.id:
            course = Course.objects.get(id=course_id)
            phrase = Phrase.objects.get(
                id=phrase_id, language=course.learning_language)
            lesson.phrase.remove(phrase)
            return JsonResponse(f"Removed {phrase} successfully...", safe=False)
        return JsonResponse(f"You aren't the author.", safe=False)


@login_required()
def lesson_search_example(request, course_id, lesson_id, example_qr):
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)

    if request.is_ajax and request.method == "GET":
        exampleResults = Example.objects.filter(
            course=course, example__contains=str(example_qr))
        dataSendBack = []
        for example in exampleResults:
            learning = False
            if example in lesson.example.all():
                learning = True
                dataSendBack.append(
                    {'id': example.id, 'example': example.example, 'user_id': example.user_id, 'learning': learning})
            else:
                dataSendBack.append(
                    {'id': example.id, 'example': example.example, 'user_id': example.user_id, 'learning': learning})
        return JsonResponse({'data': dataSendBack, }, safe=False)


@login_required()
def lesson_add_example(request, course_id, lesson_id, example_id):
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)
    if request.is_ajax and request.method == "POST":
        if request.user.id == lesson.user.id:
            course = Course.objects.get(id=course_id)
            example = Example.objects.get(id=example_id, course=course)
            lesson.example.add(example)

            example_tran_sendback = []
            if example.translation is not None:
                example_tran_sendback.append({"id": example.id, "example": str(example.example), "translation": example.translation,
                                              "missing_translation": False, })
            else:
                example_tran_sendback.append(
                    {"id": example.id, "example": example.example, "missing_translation": True, })
            return JsonResponse({'data': example_tran_sendback}, safe=False)
        return JsonResponse(f"You aren't the author.", safe=False)


@login_required()
def lesson_add_unknow_example(request, course_id, lesson_id):
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)
    if request.is_ajax and request.method == "POST":
        if request.user.id == lesson.user.id:
            course = Course.objects.get(id=course_id)

            data = json.loads(request.body)
            example = data['unknow_example']
            translation = data['translation']
            node = data['node']

            if Example.objects.filter(example=example, user=request.user, course=course).exists():
                return JsonResponse(f"{example} is already exist.", safe=False)
            else:
                new_example = Example.objects.create(
                    example=example, course=course, user=request.user, translation=translation, node=node)
                new_example.save()

                lesson.example.add(new_example)
                return JsonResponse(f"Added {example} and its translation.", safe=False)
        return JsonResponse(f"You aren't the author.", safe=False)


@login_required()
def lesson_remove_example(request, course_id, lesson_id, example_id):
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)
    if request.is_ajax and request.method == "POST":
        if request.user.id == lesson.user.id:
            course = Course.objects.get(id=course_id)
            example = Example.objects.get(
                id=example_id, course=course, user=request.user)
            lesson.example.remove(example)
            return JsonResponse(f"Removed {example} successfully...", safe=False)
        return JsonResponse(f"You aren't the author.", safe=False)


# ~ add to learning lessons too
@login_required()
def lessonLearn(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)

    words_lesson = lesson.word.all()
    phrases_lesson = lesson.phrase.all()

    if request.is_ajax and request.method == "POST":
        if LearningLesson.objects.filter(
                course=course, user=request.user, lesson=lesson).exists():
            return JsonResponse('You are learning this lesson.', safe=False)
        else:
            new_learning_lesson, created = LearningLesson.objects.get_or_create(
                course=course, user=request.user, lesson=lesson)
            for word in words_lesson:
                new_word_score, created = WordScore.objects.get_or_create(
                    course=course, user=request.user, word=word)
            for phrase in phrases_lesson:
                new_phrase_score, created = PhraseScore.objects.get_or_create(
                    course=course, user=request.user, phrase=phrase)
            return JsonResponse('Add to your learning lessons.', safe=False)

    # Words
    word_trans = WordTranslation.objects.filter(
        course=course_id, word__id__in=words_lesson)

    # words_learning = request.user.wordscore_set.all().filter(
    #     course=course_id).order_by('point')[:3]

    words_learning = WordScore.objects.filter(
        user=request.user, course=course_id, word__id__in=words_lesson)
    # annotate or extra
    # .extra(select = {'fieldsum': 'material_cost + labor_cost'}, order_by = ('fieldsum'))
    words_learning.annotate(
        total_point=F('listening') + F('speaking') + F('reading') + F('writing')).order_by('total_point')[:3]
    words_learning_list = list(words_learning)

    word_dict = {"words": []}

    admin = User.objects.get(username="admin")
    for word in words_learning_list:
        word_tran = None
        if word_trans.filter(word=word.word, user=request.user).exists():
            word_tran = word_trans.filter(
                word=word.word, user=request.user)
        elif word_trans.filter(word=word.word, user=admin).exists():
            word_tran = word_trans.filter(word=word.word, user=admin)

        if word_tran is not None:
            for wort in word_tran.values():
                word_dict["words"].append(
                    {"word_id": word.word.id, "word": word.word.word, "part_of_speech": wort["part_of_speech"], "ipa": wort["ipa"],
                     "meaning": wort["meaning"], "definition": wort["definition"], "missing_translation": False, })
        else:
            word_dict["words"].append(
                {"word_id": word.word.id, "word": word.word.word, "missing_translation": True})

    # words = words_inlesson | words_learning  # merge querysets
    # words = words_learning.union(words_inlesson)

    # Phrases
    phrases_learning = PhraseScore.objects.filter(
        user=request.user, course=course_id, phrase__id__in=phrases_lesson)
    phrases_learning.annotate(
        total_point=F('listening') + F('speaking') + F('reading') + F('writing')).order_by('total_point')[:3]
    phrases_learning_list = list(phrases_learning)

    phrase_trans = PhraseTranslation.objects.filter(
        course=course_id, phrase__id__in=phrases_lesson)

    phrase_dict = {"phrases": []}

    for phrase in phrases_learning_list:
        phrase_tran = None
        missing_translation = True
        if phrase_trans.filter(phrase=phrase.phrase, user=request.user).exists():
            phrase_tran = phrase_trans.filter(
                phrase=phrase.phrase, user=request.user)
        elif phrase_trans.filter(phrase=phrase.phrase, user=admin):
            phrase_tran = phrase_trans.filter(
                phrase=phrase.phrase, user=admin)

        if phrase_tran is not None:
            missing_translation = False
            [phrase_dict["phrases"].append(
                {"phrase_id": x.phrase.id, "phrase": x.phrase.phrase, "ipa": x.ipa,
                 "meaning": x.meaning, "definition": x.definition,
                 "words_in_phrase": [], "missing_translation": missing_translation}) for x in phrase_tran]
        else:
            phrase_dict["phrases"].append(
                {"phrase_id": phrase.phrase.id, "phrase": phrase.phrase.phrase, "missing_translation": missing_translation})

        if missing_translation:
            continue
        else:
            # get word trans in phrase
            phr = str(phrase.phrase)
            char = None
            for word in phr.split():
                word_lower = word.lower()
                for c in ['.', ',', '!', '?']:
                    if c in word:
                        word_lower = word.replace(c, '').lower()
                        char = c
                        break

                word_in_phrase_tran = None
                if Word.objects.filter(language=course.learning_language.id, word=word_lower).exists():
                    word_obj = Word.objects.get(
                        language=course.learning_language.id, word=word_lower)

                    if WordTranslation.objects.filter(course=course_id, word=word_obj, user=request.user).exists():
                        word_in_phrase_tran = WordTranslation.objects.filter(
                            course=course_id, word=word_obj, user=request.user)
                    elif WordTranslation.objects.filter(course=course_id, word=word_obj, user=admin).exists():
                        word_in_phrase_tran = WordTranslation.objects.filter(
                            course=course_id, word=word_obj, user=admin)

                    # f"{str(word_obj.word)}{char}"
                    for key in phrase_dict["phrases"]:
                        if key["phrase"] == phr:
                            if word_in_phrase_tran is not None:
                                for wort in word_in_phrase_tran.values():
                                    key["words_in_phrase"].append(
                                        {"word_id": word_obj.id, "word": f"{str(word_obj.word)}{char}", "part_of_speech": wort["part_of_speech"],
                                         "ipa": wort["ipa"], "meaning": wort["meaning"], "definition": wort["definition"], "missing_translation": False})
                            else:
                                key["words_in_phrase"].append(
                                    {"word_id": word_obj.id, "word": f"{str(word_obj.word)}{char}", "missing_translation": True})
                            break
                else:
                    for key in phrase_dict["phrases"]:
                        if key["phrase"] == phr:
                            key["words_in_phrase"].append(
                                {"word": f"{word}{char}", "missing_translation": True})
                            break

    # Examples
    examples_lesson = lesson.example.all()
    examples_learning = Example.objects.filter(
        user=request.user, course=course_id, id__in=examples_lesson)
    examples_learning_list = list(examples_learning)

    example_list = []
    example_dict = {"examples": []}
    if examples_learning.count() > 5:
        for word in words_learning_list:
            example_match = examples_learning.filter(
                course=course, example__contains=str(word.word))[:2]
            for example in example_match:
                if(example.id in example_list):
                    continue
                else:
                    example_list.append(example.id)
                    example_dict["examples"].append(
                        {"example_id": example.id, "example": example.example, "translation": example.translation,
                         "node": example.node, "words_in_example": []})

    else:
        for example in examples_learning:
            example_dict["examples"].append(
                {"example_id": example.id, "example": example.example, "translation": example.translation,
                 "node": example.node, "words_in_example": []})

    # get word trans in example
    for example in examples_learning_list:
        exmp = str(example.example)
        for word in exmp.split():
            word_in_example_tran = None

            word_lower = word.lower()
            for c in ['.', ',', '!', '?']:
                if c in word:
                    word_lower = word.replace(c, '').lower()
                    char = c
                    break

            if Word.objects.filter(language=course.learning_language.id, word=word_lower).exists():
                word_obj = Word.objects.get(
                    language=course.learning_language.id, word=word_lower)

                if WordTranslation.objects.filter(course=course_id, word=word_obj, user=request.user).exists():
                    word_in_example_tran = WordTranslation.objects.filter(
                        course=course_id, word=word_obj, user=request.user)
                elif WordTranslation.objects.filter(course=course_id, word=word_obj, user=admin).exists():
                    word_in_example_tran = WordTranslation.objects.filter(
                        course=course_id, word=word_obj, user=admin)

                for key in example_dict["examples"]:
                    if key["example"] == exmp:
                        if word_in_example_tran is not None:
                            for wort in word_in_example_tran.values():
                                key["words_in_example"].append({"word_id": word_obj.id, "word": f"{str(word_obj.word)}{char}", "part_of_speech": wort["part_of_speech"],
                                                                "ipa": wort["ipa"], "meaning": wort["meaning"], "definition": wort["definition"], "missing_translation": False})
                        else:
                            key["words_in_example"].append(
                                {"word_id": word_obj.id, "word": f"{str(word_obj.word)}{char}", "missing_translation": True})
                        break
            else:
                for key in example_dict["examples"]:
                    if key["example"] == exmp:
                        key["words_in_example"].append(
                            {"word": f"{word}{char}", "missing_translation": True})
                        break

    context = {'lesson': lesson, 'course': course,
               'learning_language': course.learning_language,
               'speaking_language': course.speaking_language,
               'word_dict': json.dumps(word_dict),
               'phrase_dict': json.dumps(phrase_dict),
               'example_dict': json.dumps(example_dict),
               }

    return render(request, 'base/lesson/lesson_learn.html', context)


@ login_required()
def addLesson(request, course_id):
    course = Course.objects.get(id=course_id)

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            new_lesson = Lesson.objects.create(
                user=request.user,
                course=course,
                name=name
            )
            new_lesson.save()
            words = form.cleaned_data.get('word')
            for word in words:
                new_lesson.word.add(word)

                if WordScore.objects.filter(
                        user=request.user, course=course, word=word).exists() == False:
                    WordScore.objects.create(
                        user=request.user, course=course, word=word
                    )

            phrases = form.cleaned_data.get('phrase')
            for phrase in phrases:
                new_lesson.phrase.add(phrase)
                PhraseScore.objects.create(
                    user=request.user,
                    course=course,
                    phrase=phrase
                )

            examples = form.cleaned_data.get('example')
            for example in examples:
                new_lesson.example.add(example)

            topics = form.cleaned_data.get('topic')
            for topic in topics:
                new_lesson.topic.add(topic)

            messages.success(
                request, f"Added your new lesson name: \"{name}\" to this course.")

            LearningLesson.objects.create(
                user=request.user,
                course=course,
                lesson=new_lesson
            )

            return redirect('course-lessons', course_id=course_id)
    else:
        form = LessonForm()
    context = {'form': form, 'course': course, 'action': "Add"}
    return render(request, 'base/lesson/lesson_form.html', context)


@login_required()
def editLesson(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id)

    if request.method == 'POST':
        form = LessonForm(request.POST, instance=lesson, initial={
            'user': lesson.user, 'course': lesson.course})
        if form.is_valid():
            name = form.cleaned_data.get('name')
            words = form.cleaned_data.get('word')
            for word in words:
                if WordScore.objects.filter(user=request.user,
                                            course=course,
                                            word=word).exists() == False:
                    WordScore.objects.create(
                        user=request.user,
                        course=course,
                        word=word
                    )

            form.save()
            messages.success(
                request, f"Edited your lesson name: \"{name}\".")
            return redirect('lesson-detail', course_id=course_id, lesson_id=lesson_id)
    else:
        form = LessonForm(instance=lesson, initial={
            'user': lesson.user, 'course': lesson.course})
    context = {'form': form, 'course': course, 'action': "Edit"}
    return render(request, 'base/lesson/lesson_form.html', context)


@login_required()
def removeLesson(request, course_id, lesson_id):
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id, course=course_id)

    if request.method == 'POST':
        if request.user == lesson.user:
            LearningLesson.objects.get(
                user=request.user,
                course=course,
                lesson=lesson
            ).delete()

            lesson.delete()
            messages.success(
                request, f"Removed your lesson name: \"{lesson.name}\" from this course.")
            return redirect('course-lessons', course_id=course_id)
    else:
        form = LessonForm(instance=lesson, initial={
            'user': lesson.user, 'course': lesson.course})
    context = {'form': form, 'course': course, 'action': "Remove"}
    return render(request, 'base/lesson/lesson_form.html', context)


# def lessonLikeToggle(request, course_id, lesson_id):
#     course = Course.objects.get(id=course_id)
#     lesson = Lesson.objects.get(id=lesson_id, course=course_id)

#     if not course.exist() or lesson.exist():
#         return Response(status=404)
#     users_liked_lesson = Lesson.like.all()
#     if request.user in users_liked_lesson:
#         lesson.like.remove(request.user)
#     else:
#         lesson.like.add(request.user)
