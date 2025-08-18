from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from gradio_client import Client, handle_file
import tempfile
import os
from .models import Company, Interview

# Page Views

def interview_list(request):
    """
    Displays a list of all available interviews, grouped by company.
    """
    companies = Company.objects.prefetch_related('interviews').all()
    context = {'companies': companies}
    return render(request, 'interviews/interview_list.html', context)


def interview_detail(request, slug):
    """
    Displays the main interview interface for a specific interview.
    """
    interview = get_object_or_404(Interview, slug=slug)
    context = {'interview': interview}
    return render(request, 'interviews/interview_detail.html', context)


# API Proxy Views

@csrf_exempt
@require_POST
def start_interview_api(request):
    """
    API endpoint to start the interview.
    It takes a resume file and job description, sends them to the Gradio API,
    and returns the initial response.
    """
    try:
        resume_file = request.FILES.get('resume')
        job_description = request.POST.get('job_description')

        if not resume_file or not job_description:
            return JsonResponse({'error': 'Missing resume file or job description.'}, status=400)

        # Save the uploaded file temporarily to pass its path to the client
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_f:
            for chunk in resume_file.chunks():
                temp_f.write(chunk)
            temp_file_path = temp_f.name

        client = Client("ahmedatk/ai_interviewer")
        result = client.predict(
            resume=handle_file(temp_file_path),
            job_desc=job_description,
            api_name="/gradio_start_interview"
        )
        os.remove(temp_file_path) # Clean up the temporary file

        response_data = {
            'conversation': result[0],
            'audio_url': result[1],
            'download_report_url': result[2]
        }
        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': f'An API error occurred: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def handle_response_api(request):
    """
    API endpoint to handle the user's response during the interview.
    """
    try:
        user_response = request.POST.get('response')
        if not user_response:
            return JsonResponse({'error': 'User response cannot be empty.'}, status=400)

        client = Client("ahmedatk/ai_interviewer")
        result = client.predict(
            response=user_response,
            api_name="/gradio_handle_response"
        )

        response_data = {
            'conversation': result[0],
            'audio_url': result[1],
            'download_report_url': result[2]
        }
        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': f'An API error occurred: {str(e)}'}, status=500)


@csrf_exempt
@require_POST
def end_interview_api(request):
    """
    API endpoint to end the interview and get the final report.
    """
    try:
        client = Client("ahmedatk/ai_interviewer")
        result = client.predict(api_name="/gradio_end_interview")

        response_data = {
            'conversation': result[0],
            'audio_url': result[1],
            'download_report_url': result[2]
        }
        return JsonResponse(response_data)

    except Exception as e:
        return JsonResponse({'error': f'An API error occurred: {str(e)}'}, status=500)