from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy

from .models import Course

# Create your views here.

class OwnerMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(owner=self.request.user)

class OwnerEditMixin(OwnerMixin, LoginRequiredMixin, PermissionRequiredMixin):
    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class OwnerCourseMixin:
    model = Course
    fields = ['subject', 'title', 'slug', 'overview']
    success_url = reverse_lazy('manage_course_list')

class OwnerCourseEditMixin(OwnerCourseMixin, OwnerEditMixin):
    template_name = 'courses/form.html'

class ManageCourseListView(OwnerCourseMixin, ListView):
    template_name = 'courses/list.html'
    permission_required = 'courses.view_course'

class CourseCreateView(OwnerCourseMixin, CreateView):
    template_name = 'courses/'
    permission_required = 'courses.add_course'

class CourseUpdateView(OwnerCourseMixin, UpdateView):
    permission_required = 'courses.change_course'

class CourseDeleteView(OwnerCourseMixin, DeleteView):
    template_name = 'courses/list.html'
    permission_required = 'courses.delete_course'


