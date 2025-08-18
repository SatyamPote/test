# resume_analyzer/views.py
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from gradio_client import Client, handle_file
import tempfile
import os
import json

# Page configurations remain the same
PAGE_CONFIG = {
    'analyzer': {
        'title': 'AI Resume Analyzer',
        'description': 'Get a comprehensive, section-by-section analysis of your resume against a job description. Includes a skills chart and detailed feedback.',
        'button_text': 'Analyze Full Resume'
    },
    'ats_checker': {
        'title': 'ATS Score Checker',
        'description': 'Quickly check your resume\'s compatibility with Applicant Tracking Systems. Get your score and actionable tips to pass the screening.',
        'button_text': 'Check My ATS Score'
    }
}

@csrf_exempt
def analyzer_view(request, page_type):
    context = PAGE_CONFIG[page_type].copy()
    template_name = f'resume_analyzer/{page_type}_page.html'

    if request.method == 'POST':
        temp_file_path = None # Initialize to None
        try:
            resume_file = request.FILES.get('resume')
            job_description = request.POST.get('jd')
            github_user = request.POST.get('github_user')

            if not all([resume_file, job_description, github_user]):
                raise ValueError("All fields are required. Please fill out the entire form.")

            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_f:
                for chunk in resume_file.chunks():
                    temp_f.write(chunk)
                temp_file_path = temp_f.name

            # This is the call to the external service
            client = Client("ahmedatk/resume-analyzer-template")
            result = client.predict(
                resume=handle_file(temp_file_path),
                jd=job_description,
                github_user=github_user,
                api_name="/predict"
            )
            
            # --- START: KEY FIX for the JSON error ---
            json_output = result[0]
            json_data = None
            
            # Intelligently handle if the API returns a string or a pre-parsed dictionary
            if isinstance(json_output, str):
                json_data = json.loads(json_output)
            elif isinstance(json_output, dict):
                json_data = json_output
            else:
                # If it's neither, we can't process it.
                raise TypeError("Received unexpected data type from API.")
            # --- END: KEY FIX ---

            context.update({
                'submitted': True,
                'json_result': json_data,
                'chart_html': result[1],
                'report_url': result[2]
            })

        except Exception as e:
            # This general 'except' block will now catch both our internal errors
            # and provide a better message for the upstream Gradio error.
            error_message = str(e)
            if "upstream Gradio app" in error_message:
                context['error'] = "The external AI service failed to process your request. This might be a temporary issue with the service or the content of your inputs. Please try again in a few moments."
            else:
                context['error'] = f'An error occurred: {error_message}'
        
        finally:
            # Ensure the temporary file is always deleted, even if an error occurs
            if temp_file_path and os.path.exists(temp_file_path):
                os.remove(temp_file_path)

    return render(request, template_name, context)