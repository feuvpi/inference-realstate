from django.shortcuts import render
import logging

logger = logging.getLogger(__name__)

def home(request):
    """Home page view"""
    logger.info("Home page accessed by %s", request.user)
    return render(request, 'base/home.html')
