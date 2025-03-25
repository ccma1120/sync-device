import os
import json
import re
import subprocess
from pathlib import Path

def get_pin_configure_parts():
    # Clone repo if needed
    repo_url = 'https://github.com/OpenNuvoton/NuTool-PinConfigure.git'
    repo_path = Path(__file__).parent / 'NuTool-PinConfigure'
    
    if not repo_path.exists():
        print('Cloning PinConfigure repo...')
        subprocess.run(['git', 'clone', repo_url, str(repo_path)], check=True)

    # Parse JS files
    js_path = repo_path / 'src'
    parts = set()
    
    for file in js_path.glob('*.js'):
        content = file.read_text(encoding='utf-8')
        # Look for part numbers in name fields
        matches = re.finditer(r'name:\s*"([^"]+)"', content)
        for match in matches:
            part = match.group(1).strip()
            if part:  # Skip empty strings
                parts.add(part)
    
    return sorted(parts)

def get_partnum_id_parts():
    filepath = Path(__file__).parent.parent / 'PartNumID.cpp'
    print(f"Looking for PartNumID.cpp at: {filepath.absolute()}")

    try:
        print(f'Reading from: {filepath}')
        content = filepath.read_text(encoding='utf-8')
        
        parts = set()
        # Skip lines with specific comments and extract part numbers from valid entries
        for line in content.splitlines():
            # Skip comment-only lines and specific comments
            if line.strip().startswith('//') or any(x in line for x in ['//old chip', '//not release', '//unknown']):
                continue
                
            # Match part numbers in format: {"PARTNUM", 0xXXXXXXXX, PROJ_XXX},
            match = re.search(r'{\s*"([^"]+)".*?}', line)
            if match:
                parts.add(match.group(1))
        
        if not parts:
            raise ValueError("No part numbers found in the file!")
            
        print(f"Found {len(parts)} parts")
        return sorted(parts)
        
    except Exception as e:
        print(f"Error processing file: {e}")
        raise

def main():
    try:
        pin_parts = get_pin_configure_parts()
        id_parts = get_partnum_id_parts()
        
        print(f'Parts in PinConfigure: {len(pin_parts)}')
        print(f'Parts in PartNumID: {len(id_parts)}')
        
        missing = sorted(set(pin_parts) - set(id_parts))
        extra = sorted(set(id_parts) - set(pin_parts))
        
        print('\nMissing from PartNumID.cpp:', missing)
        print('\nExtra in PartNumID.cpp:', extra)
        
        report = {
            'pinParts': pin_parts,
            'idParts': id_parts,
            'missing': missing,
            'extra': extra
        }
        
        with open('pin-parts-report.json', 'w') as f:
            json.dump(report, f, indent=2)
    
    except Exception as e:
        print(f"Error occurred: {e}")
        raise

if __name__ == '__main__':
    main()
