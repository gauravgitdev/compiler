import requests
import time
from django.shortcuts import render

language_map = {
    'python': {'filename': 'main.py', 'version': '3.10.0'},
    'cpp': {'filename': 'main.cpp', 'version': '10.2.0'},
    'c': {'filename': 'main.c', 'version': '10.2.0'},
    'java': {'filename': 'Main.java', 'version': '15.0.2'},
    'javascript': {'filename': 'main.js', 'version': '16.3.0'}
}

def editor_view(request):
    output = ''
    code = ''
    language = 'python'
    user_input = ''
    execution_time = None  # Initialize

    if request.method == 'POST':
        code = request.POST.get('code', '')
        language = request.POST.get('language', 'python')
        user_input = request.POST.get('user_input', '')

        lang_info = language_map.get(language, language_map['python'])

        payload = {
            "language": language,
            "version": lang_info['version'],
            "files": [{"name": lang_info['filename'], "content": code}],
            "stdin": user_input
        }

        try:
            start_time = time.time()
            response = requests.post(
                'https://emkc.org/api/v2/piston/execute',
                json=payload,
                headers={'Content-Type': 'application/json'}
            )
            end_time = time.time()
            execution_time = round(end_time - start_time, 3)  # seconds with ms precision

            if response.status_code == 200:
                result = response.json()
                output = result.get('run', {}).get('output', 'No output')
            else:
                output = f"Error: {response.status_code} - {response.text}"

        except Exception as e:
            output = f"Execution failed: {str(e)}"

    return render(request, 'editor.html', {
        'output': output,
        'code': code,
        'language': language,
        'user_input': user_input,
        'execution_time': execution_time
    })
