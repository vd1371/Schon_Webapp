from django.shortcuts import render
from django.views.generic import TemplateView

class ShareholdingInfoIndexView(TemplateView):
	template_name = 'index.html'