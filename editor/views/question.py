from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView
from editor.models import Question
import git

def save_content_to_file(request, form, **kwargs):
    try:
        repo = git.Repo(settings.GLOBAL_SETTINGS['REPO_PATH'])
        path_to_questionfile = settings.GLOBAL_SETTINGS['REPO_PATH'] + 'questions/' + form.cleaned_data["filename"]
        fh = open(path_to_questionfile, 'w')
        fh.write(form.cleaned_data["content"])
        fh.close()
        repo.index.add(['questions/' + form.cleaned_data["filename"]])
        repo.index.commit('Made some changes to question: %s' % form.cleaned_data["name"])
        question = form.save()
    except IOError:
        save_error = "Could not save question file."
        if 'question' in kwargs:
            return render(request, 'question/edit.html', {'form': form, 'save_error': save_error, 'question': kwargs['question']})
        else:
            return render(request, 'question/new.html', {'form': form, 'save_error': save_error})
    return HttpResponseRedirect(reverse('question_edit', args=(question.slug,)))


class QuestionCreateView(CreateView):
    model = Question
    template_name = 'question/new.html'
    
    def form_valid(self, form):
        return save_content_to_file(self.request, form)


class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'question/edit.html'
    
    def form_valid(self, form):
        return save_content_to_file(self.request, form, question=self.get_object())
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            questionfile = open(settings.GLOBAL_SETTINGS['REPO_PATH'] + 'questions/' + self.object.filename, 'r')
            self.object.content = questionfile.read()
            questionfile.close()
        except IOError:
            self.object.content = "Could not read from question file."
            
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(self.get_context_data(form=form))
        
    def get_success_url(self):
        return reverse('question_index')