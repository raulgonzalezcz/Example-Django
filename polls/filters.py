from .models import Question, Choice
import django_filters

class QuestionFilter(django_filters.FilterSet):
    class Meta:
        model = Question
        fields = ['question_text', 'pub_date', ]