# views.py
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import subprocess

@csrf_exempt  # CSRF 검사 비활성화 (보안에 유의해야 함)
def git_pull(request):
    if request.method == 'POST':
        try:
            import os
            # Git pull 명령을 실행
            result = subprocess.run(
                ["git", "pull"],
                capture_output=True,
                text=True,
                cwd=os.getcwd()  # Git 저장소 경로 지정
            )
            if result.returncode == 0:
                # 성공한 경우
                return JsonResponse({"status": "success", "output": result.stdout})
            else:
                # 오류가 발생한 경우
                return JsonResponse({"status": "error", "output": result.stderr})
        except Exception as e:
            # 예외 처리
            return JsonResponse({"status": "error", "output": str(e)})
    return JsonResponse({"status": "invalid request"}, status=400)
