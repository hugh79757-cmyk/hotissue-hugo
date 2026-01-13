#!/usr/bin/env python3
import os
import re

POSTS_DIR = "/Users/twinssn/Desktop/hotissue-hugo/content/posts"

def extract_slug(filename):
    name = filename.replace('.md', '')
    match = re.match(r'^\d{4}-\d{2}-\d{2}-(.+)$', name)
    if match:
        return match.group(1)
    return name

def add_aliases(filepath, slug):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'aliases:' in content:
        return False
    
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            front_matter = parts[1]
            body = parts[2]
            
            new_front_matter = front_matter.rstrip() + f'\naliases:\n  - /{slug}/\n'
            new_content = '---' + new_front_matter + '---' + body
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            return True
    return False

count = 0
for filename in os.listdir(POSTS_DIR):
    if filename.endswith('.md'):
        filepath = os.path.join(POSTS_DIR, filename)
        slug = extract_slug(filename)
        
        if add_aliases(filepath, slug):
            print(f"ADDED: {filename} -> /{slug}/")
            count += 1
        else:
            print(f"SKIP: {filename}")

print(f"\nDone! {count} files updated")
