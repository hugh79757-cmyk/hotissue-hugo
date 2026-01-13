#!/usr/bin/env python3
import os
import re

POSTS_DIR = "/Users/twinssn/Desktop/hotissue-hugo/content/posts"

def title_to_slug(title):
    slug = title.replace(' ', '-')
    slug = re.sub(r'[^\w가-힣-]', '', slug)
    slug = re.sub(r'-+', '-', slug)
    slug = slug.strip('-')
    return slug

def fix_aliases(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # title 추출
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', content, re.MULTILINE)
    if not title_match:
        return False, None
    
    title = title_match.group(1).strip('"\'')
    korean_slug = title_to_slug(title)
    korean_alias = f'/{korean_slug}/'
    
    # 이미 한글 aliases가 front matter 안에 있으면 스킵
    parts = content.split('---', 2)
    if len(parts) >= 3:
        front_matter = parts[1]
        body = parts[2]
        
        if korean_alias in front_matter:
            return False, korean_slug
        
        # aliases 섹션이 있으면 추가
        if 'aliases:' in front_matter:
            front_matter = re.sub(
                r'(aliases:\s*\n([ \t]*-\s*.+\n)*)',
                r'\g<1>  - ' + korean_alias + '\n',
                front_matter
            )
        else:
            # aliases 섹션 새로 추가
            front_matter = front_matter.rstrip() + f'\naliases:\n  - {korean_alias}\n'
        
        # body에서 잘못 추가된 aliases 라인 제거
        body = re.sub(r'^\s*-\s*/[^/]+/\s*\n', '', body)
        
        new_content = '---' + front_matter + '---' + body
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True, korean_slug
    
    return False, None

count = 0
for filename in os.listdir(POSTS_DIR):
    if filename.endswith('.md'):
        filepath = os.path.join(POSTS_DIR, filename)
        success, slug = fix_aliases(filepath)
        
        if success and slug:
            print(f"FIXED: {filename[:40]}... -> /{slug[:30]}.../")
            count += 1
        else:
            print(f"SKIP: {filename[:40]}...")

print(f"\nDone! {count} files updated")
