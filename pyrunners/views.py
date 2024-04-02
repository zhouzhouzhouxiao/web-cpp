import os
import subprocess
from pathlib import Path
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def index(request):
    if request.method == 'POST':
        user_code = request.POST.get('code', None)
        file_code_dir = 'file_code'

        os.makedirs(file_code_dir,exist_ok=True)  # 这一行会确保文件夹已经存在，如果不存在会创建

        # 找到所有的.cpp文件
        all_cpp_files = [str(filepath) for filepath in Path(file_code_dir).glob('*.cpp')]

        compile_cmd = f'g++ {" ".join(all_cpp_files)} -o {file_code_dir}/main.exe'

        proc_compile = subprocess.run(compile_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if proc_compile.returncode != 0:
            error_message = proc_compile.stderr.decode('ISO-8859-1') if proc_compile.stderr else 'no error'
            return JsonResponse({'error': error_message})

        run_cmd = os.path.abspath(os.path.join(file_code_dir, 'main.exe'))

        proc_run = subprocess.Popen(run_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        output, error = proc_run.communicate()

        output_message = output.decode() if output else 'no output'

        error_message = error.decode() if error else 'no error'

        # 返回JSON响应
        return JsonResponse({'output': output_message, 'error': error_message})
    else:
        return render(request, 'pyrunners/yuanindex.html')

@csrf_exempt
def file_list(request):
    files = [f.name for f in Path('pyrunners/file_code').glob('*.cpp')]
    files += [f.name for f in Path('pyrunners/file_code').glob('*.h')]
    return JsonResponse(files, safe=False)

@csrf_exempt
def add_file(request):
    filename = request.POST.get('filename', None)
    with open(f'pyrunners/file_code/{filename}', 'w') as f:
        f.write('')
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def delete_file(request):
    filename = request.POST.get('filename', None)
    filepath = f"pyrunners/file_code/{filename}"
    if filename and os.path.exists(filepath):
        os.remove(filepath)
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def rename_file(request):
    old_filename = request.POST.get('old_filename', None)
    new_filename = request.POST.get('new_filename', None)
    old_filepath = f"pyrunners/file_code/{old_filename}"
    new_filepath = f"pyrunners/file_code/{new_filename}"
    if old_filename and new_filename and os.path.exists(old_filepath): os.rename(old_filepath, new_filepath)
    return JsonResponse({'status': 'ok'})


@csrf_exempt
def load_file(request):
    # 获取请求中的文件名
    filename = request.POST.get('filename', None)

    # 先确认文件是否存在
    filepath = f"pyrunners/file_code/{filename}"
    if not os.path.exists(filepath):
        return JsonResponse({'status': 'error', 'message': '文件不存在'})

    # 读取并返回文件内容
    with open(filepath, 'r') as file:
        file_content = file.read()

    # 返回一个包含文件内容JSON响应到前端
    return JsonResponse({'status': 'ok', 'fileContent': file_content})


@csrf_exempt
def save_file(request):
    if request.method == 'POST':
        filename = request.POST.get('filename', None)
        code = request.POST.get('code', None)
        filepath = f"pyrunners/file_code/{filename}"
        with open(filepath, 'w') as file:
            file.write(code)
        return JsonResponse({'status': 'ok'})