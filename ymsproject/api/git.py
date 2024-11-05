# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess, os

@csrf_exempt
def git_pull(request):
    if request.method == 'POST':
        try:
            # 현재 경로 확인 (Git 저장소 경로)
            repo_path = os.getcwd()
            
            # git fetch 실행
            fetch_result = subprocess.run(
                ["git", "fetch"],
                capture_output=True,
                text=True,
                cwd=repo_path
            )
            
            if fetch_result.returncode != 0:
                return JsonResponse({"status": "error", "output": fetch_result.stderr})

            # git pull 실행
            pull_result = subprocess.run(
                ["git", "pull"],
                capture_output=True,
                text=True,
                cwd=repo_path
            )
            
            if pull_result.returncode == 0:
                # 성공적으로 fetch와 pull을 완료한 경우
                return JsonResponse({"status": "success", "output": pull_result.stdout})
            else:
                # pull 명령어에서 오류가 발생한 경우
                return JsonResponse({"status": "error", "output": pull_result.stderr})
                
        except Exception as e:
            # 예외 처리
            return JsonResponse({"status": "error", "output": str(e)})
            
    # 잘못된 요청일 경우
    return JsonResponse({"status": "invalid request"}, status=400)