import os
from pathlib import Path

# 설정: 백업할 확장자와 무시할 폴더
TARGET_EXTENSIONS = {'.py', '.yaml', '.yml', '.css', '.js', '.md'}
IGNORE_DIRS = {'venv', '.git', '__pycache__', '.idea', '.vscode', 'node_modules', 'posts', 'assets', 'output', 'site'}
IGNORE_FILES = {'poetry.lock', 'package-lock.json', 'backup_code.py', 'project_backup.txt', '.DS_Store'}

def create_backup():
    root_dir = Path('.')
    output_file = Path('project_backup.txt')
    
    with open(output_file, 'w', encoding='utf-8') as outfile:
        outfile.write("=== PROJECT STRUCTURE ===\n")
        # 구조 먼저 기록
        for path in sorted(root_dir.rglob('*')):
            if any(part in IGNORE_DIRS for part in path.parts):
                continue
            depth = len(path.relative_to(root_dir).parts)
            if path.is_dir():
                outfile.write(f"{'  ' * (depth-1)}📂 {path.name}/\n")
            else:
                outfile.write(f"{'  ' * (depth-1)}📄 {path.name}\n")
        
        outfile.write("\n\n" + "="*50 + "\n\n")

        # 파일 내용 기록
        for path in sorted(root_dir.rglob('*')):
            if path.is_dir(): continue
            if any(part in IGNORE_DIRS for part in path.parts): continue
            if path.name in IGNORE_FILES: continue
            if path.suffix not in TARGET_EXTENSIONS: continue

            try:
                content = path.read_text(encoding='utf-8')
                outfile.write(f"### FILE: {path}\n")
                outfile.write("-" * 50 + "\n")
                outfile.write(content)
                outfile.write("\n" + "=" * 50 + "\n\n")
                print(f"✅ Backup: {path}")
            except Exception as e:
                print(f"❌ Skip {path}: {e}")

    print(f"\n🎉 완료! 'project_backup.txt' 파일이 생성되었습니다.")

if __name__ == '__main__':
    create_backup()
