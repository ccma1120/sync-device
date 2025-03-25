import re

def extract_part_numbers(file_path):
    part_numbers = set()
    with open(file_path, 'r') as f:
        for line in f:
            # Skip commented lines
            if '//not release' in line or '//unknown' in line or '//old chip' in line:
                continue
            # Remove everything after // before looking for part numbers
            line = line.split('//')[0]
            # Look for part numbers in format like "M451HD2AE"
            matches = re.findall(r'[A-Z][0-9A-Z]{5,}(?=[\s,"])', line)
            part_numbers.update(matches)
    return part_numbers

def main():
    local_parts = extract_part_numbers('PartNumID.cpp')
    ref_parts = extract_part_numbers('reference_PartNumID.cpp')

    with open('part_cmp_isp.txt', 'w') as f:
        f.write("Comparison Results between local PartNumID.cpp and ISPTool reference:\n")
        f.write("===============================================================\n\n")
        
        f.write("Parts in local PartNumID.cpp but not in ISPTool:\n")
        f.write("-----------------------------------------\n")
        for part in sorted(local_parts - ref_parts):
            f.write(f"{part}\n")
        
        f.write("\nParts in ISPTool but not in local PartNumID.cpp:\n")
        f.write("-----------------------------------------\n")
        for part in sorted(ref_parts - local_parts):
            f.write(f"{part}\n")

if __name__ == "__main__":
    main()
