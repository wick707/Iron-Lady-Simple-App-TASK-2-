from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Course
from .forms import CourseForm
import os

# --- Helper function to update the knowledgebase.md file ---
def update_knowledge_base():
    """Fetches all courses and rewrites the knowledgebase.md file."""
    courses = Course.objects.all()
    
    # Define the path to the knowledgebase.md file in the root directory
    # IMPORTANT: Adjust this path if your Django project is in a subdirectory
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'knowledgebase.md')

    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("# Iron Lady Programs Knowledge Base\n\n")
            for course in courses:
                f.write(f"## {course.name}\n\n")
                f.write(f"### Overview and Purpose\n{course.overview}\n\n")
                f.write(f"### Key Attributes\n")
                f.write(f"* **Target Audience:** {course.target_audience}\n")
                f.write(f"* **Program Duration:** {course.duration}\n")
                f.write(f"* **Community Access:** {course.community_access}\n")
                f.write(f"* **Program Mode:** {course.mode}\n")
                f.write(f"* **Program Fee:** {course.fee}\n")
                f.write(f"* **Certificate:** {'Yes' if course.certificate else 'Not specified'}\n\n")
                f.write(f"### Key Outcomes and Modules\n{course.outcomes}\n\n")
                f.write(f"### Interests Aligned\n{course.interests}\n\n")
                f.write("---\n\n")
    except Exception as e:
        print(f"Error writing to knowledgebase.md: {e}")

# --- Updated CourseListView to include dashboard stats ---
class CourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'courses/dashboard.html'
    context_object_name = 'courses'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        total_courses = Course.objects.count()
        context['total_courses'] = total_courses
        # Add more stats here if needed, e.g., online vs hybrid
        context['online_courses'] = Course.objects.filter(mode__icontains='Online').count()
        context['hybrid_courses'] = Course.objects.filter(mode__icontains='Hybrid').count()
        return context

class CourseCreateView(LoginRequiredMixin, CreateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Course added successfully!')
        response = super().form_valid(form)
        update_knowledge_base()
        return response

class CourseUpdateView(LoginRequiredMixin, UpdateView):
    model = Course
    form_class = CourseForm
    template_name = 'courses/course_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Course updated successfully!')
        response = super().form_valid(form)
        update_knowledge_base()
        return response

class CourseDeleteView(LoginRequiredMixin, DeleteView):
    model = Course
    template_name = 'courses/course_confirm_delete.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        messages.success(self.request, 'Course deleted successfully!')
        response = super().form_valid(form)
        update_knowledge_base()
        return response

