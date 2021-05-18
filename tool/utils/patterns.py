#!/usr/bin/env python3

comment_pattern = r'(^[\/]\*+|^[\/]{2}|^\* |\*+[\/]$)'
function_pattern = r'^(static)?\s*(unsigned|signed)?\s*(void|int|char|short|long|float|double)\s+(\w+)\s*\(.*(\))?'
func_name_pattern = r'\s*(\w+)\s*\(.*\)'
ext_pattern = r'(\w+)\.([a-zA-Z]{1,3})'
cve_pattern = r'CVE-(\d{4})-(\d{4,7})'
advisories_pattern = r'mfsa(\d{4})-(\d{2,3})'
