from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.urls import reverse
from django.db.models import Count
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg')

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.image.path)
        if img.height > 320 or img.width > 320:
            output_size = (320, 320)
            img.thumbnail(output_size)
            img.save(self.image.path)

    @property
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = 'default.jpg'
        return url


class Language(models.Model):
    id = models.CharField(primary_key=True, max_length=3)
    language = models.CharField(max_length=50, unique=True)
    flag = models.ImageField(default='default.jpg')

    def __str__(self):
        return self.language


class Course(models.Model):
    learning_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="learning_language")
    speaking_language = models.ForeignKey(
        Language, on_delete=models.CASCADE, related_name="speaking_language")

    def __str__(self):
        return f'Learn {self.learning_language} form {self.speaking_language}'
    # get_learning_language_display()}

    def get_words(self):
        return Word.objects.filter(language=self.learning_language).count()

    def get_phrases(self):
        return Phrase.objects.filter(language=self.learning_language).count()

    def get_examples(self):
        return Example.objects.filter(course=self).count()

    def get_lessons(self):
        return Lesson.objects.filter(course=self).count()

    def get_learners(self):
        return LearningCourses.objects.filter(course=self).count()

    def enroll(self, user):
        if LearningCourses.objects.filter(user=user, course=self):
            return False
        return True


class LearningCourses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.__str__()


class LearningCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return self.course.__str__()


class Topic(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name


class Word(models.Model):
    word = models.CharField(max_length=200, unique=True)
    topic = models.ManyToManyField(Topic, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.word


class WordTranslation(models.Model):
    word = models.ForeignKey(Word, on_delete=models.CASCADE)

    part_of_speech_list = [
        ('noun', 'noun'),
        ('pronoun', 'pronoun'),
        ('adjective', 'adjective'),
        ('verb', 'verb'),
        ('adverb', 'adverb'),
        ('preposition', 'preposition'),
        ('conjunction', 'conjunction'),
        ('article', 'article'),
        ('exclamation', 'exclamation'),
        ('prefix', 'prefix'),
        ('abbreviation', 'abbreviation'),
    ]

    part_of_speech = models.CharField(
        max_length=12, choices=part_of_speech_list, null=True)
    ipa = models.CharField(max_length=200, null=True)
    meaning = models.CharField(max_length=200)
    definition = models.CharField(max_length=200, null=True, blank=True)
    node = models.CharField(max_length=200, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_liked = models.ManyToManyField(
        User, related_name="user_liked_word_trans", null=True, blank=True)

    def __str__(self):
        return self.word.__str__()

    def get_absolute_url(self):
        return reverse('word-detail', kwargs={'word_id': self.word.id})


class Phrase(models.Model):
    phrase = models.CharField(max_length=200, unique=True)
    topic = models.ManyToManyField(Topic, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    language = models.ForeignKey(
        Language, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.phrase.__str__()


class PhraseTranslation(models.Model):
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    ipa = models.CharField(max_length=200, null=True)
    meaning = models.CharField(max_length=200)
    definition = models.CharField(max_length=200, null=True, blank=True)
    node = models.CharField(max_length=200, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user_liked = models.ManyToManyField(
        User, related_name="user_liked_phrase_trans", null=True, blank=True)

    def __str__(self):
        return self.phrase.__str__()


class Example(models.Model):
    example = models.CharField(max_length=200, unique=True)
    translation = models.CharField(max_length=200)
    node = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    topic = models.ManyToManyField(Topic, null=True, blank=True)
    user_liked = models.ManyToManyField(
        User, related_name="user_liked_example", null=True, blank=True)

    def __str__(self):
        return self.example


class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    name = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now=True)

    topic = models.ManyToManyField(Topic, null=True, blank=True)
    word = models.ManyToManyField(Word, null=True, blank=True)
    phrase = models.ManyToManyField(Phrase, null=True, blank=True)
    example = models.ManyToManyField(Example, null=True, blank=True)
    user_liked = models.ManyToManyField(
        User, related_name="user_liked_lesson", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'course_id': self.course.id})


class LearningLesson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)

    def __str__(self):
        return self.lesson.name


class WordScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    last_practiced = models.DateTimeField(auto_now=True)
    listening = models.FloatField(default=0)
    speaking = models.FloatField(default=0)
    reading = models.FloatField(default=0)
    writing = models.FloatField(default=0)

    def get_total_point(self):
        return {self.listening + self.speaking + self.reading + self.writing}

    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     if not self.id:
    #         self.last_practiced = timezone.now()
    #     return super(WordScore, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} | word: {self.word} | total point: {self.listening + self.speaking + self.reading + self.writing}"


class PhraseScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phrase = models.ForeignKey(Phrase, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    last_practiced = models.DateTimeField(auto_now=True)
    listening = models.FloatField(default=0)
    speaking = models.FloatField(default=0)
    reading = models.FloatField(default=0)
    writing = models.FloatField(default=0)

    def get_total_point(self):
        return {self.listening + self.speaking + self.reading + self.writing}

    def __str__(self):
        return f"{self.user.username} | phrase: {self.phrase} | total point: {self.listening + self.speaking + self.reading + self.writing}"


class ExpTracker(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    daily_exp = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} | daily exp: {self.daily_exp}"

    def get_total_exp(self, user):
        return ExpTracker.objects.filter(user=user)

        # Book.objects.annotate(Count('authors'))


# class Follow(models.Model):
#     follower = models.ForeignKey(User, related_name='follower', on_delete=models.CASCADE)
#     following = models.ManyToManyField(User, related_name='following', on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now=True)
