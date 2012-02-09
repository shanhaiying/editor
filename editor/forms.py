from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from editor.models import Exam, Question, ExamQuestion

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        
        
class ExamForm(ModelForm):
    class Meta:
        model = Exam
        
ExamQuestionFormSet = inlineformset_factory(Exam, ExamQuestion)