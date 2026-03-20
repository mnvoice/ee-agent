#!/usr/bin/env python3
"""Temporary script to analyze answer key extraction results."""
import json
import re

import anthropic

batch_ids = json.load(open("data/batch_repair/batch_ids.json"))
mapping = json.load(open("data/batch_repair/page_mapping.json"))


def parse_resp(raw_text):
    text = raw_text.strip()
    text = re.sub(r'```(?:json)?\s*', '', text).strip()
    text = text.replace('\\\\', '\x00D\x00')
    text = re.sub(r'\\(?!["\\/bfnrtu])', r'\\\\', text)
    text = text.replace('\x00D\x00', '\\\\')
    try:
        return json.loads(text)
    except Exception:
        return None


client = anthropic.Anthropic()
type_counts = {}
ak_files = {}
ak_total_answers = 0

# Sample first 3 batches (300 pages)
for entry in batch_ids[:3]:
    for result in client.messages.batches.results(entry["batch_id"]):
        raw = "".join(
            b.text for b in result.result.message.content if b.type == "text"
        )
        parsed = parse_resp(raw)
        ptype = parsed.get("type", "?") if parsed else "parse_fail"
        type_counts[ptype] = type_counts.get(ptype, 0) + 1
        if ptype == "answer_key":
            jf = mapping.get(result.custom_id, {}).get("json_file", "")
            answers = parsed.get("answers", {})
            ak_files[jf] = len(answers)
            ak_total_answers += len(answers)

print("Page types (first 300 pages):")
for k, v in sorted(type_counts.items(), key=lambda x: -x[1]):
    print(f"  {k}: {v}")
print(f"\nAnswer keys: {len(ak_files)} files, {ak_total_answers} total answers")
for f, n in sorted(ak_files.items())[:10]:
    print(f"  {f}: {n} answers")
