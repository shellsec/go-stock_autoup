@echo off
echo ===== go-stock �Զ����¹��� =====
echo.

REM ���Python�Ƿ��Ѱ�װ
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo [����] δ��⵽Python��װ���밲װPython 3.6����߰汾��
    echo �����Դ� https://www.python.org/downloads/ ����Python��
    echo.
    pause
    exit /b 1
)

echo [��Ϣ] ��⵽Python��װ��
echo.

REM ��װ�����������
echo [��Ϣ] ���ڰ�װ�����������...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo [����] ��װ������ʧ�ܡ�
    pause
    exit /b 1
)
echo [��Ϣ] �����װ�ɹ���
echo.

REM ���и��½ű�
echo [��Ϣ] ��ʼ�����Զ����½ű�...
python auto_update.py
if %errorlevel% neq 0 (
    echo [����] ���¹���ʧ�ܡ���鿴update_log.txt��ȡ��ϸ��Ϣ��
    pause
    exit /b 1
)

echo.
echo [��Ϣ] ���¹�������ɡ�
pause
exit /b 0