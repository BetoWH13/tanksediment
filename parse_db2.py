import re
import json

with open(r"tanksediment-com-20260219-200502-wbvxd3yjtoj0\database.sql", "r", encoding="utf-8", errors="replace") as f:
    sql = f.read()

sql = sql.replace("SERVMASK_PREFIX_", "wp_")

# Each INSERT is one row: INSERT INTO `wp_posts` VALUES (col1,col2,...);
# We need to extract all of them
insert_pattern = re.compile(r"INSERT INTO `wp_posts` VALUES \((.+?)\);", re.DOTALL)

def split_sql_row(row):
    """Split a SQL VALUES row respecting quoted strings and escaped chars."""
    fields = []
    current = []
    in_string = False
    i = 0
    while i < len(row):
        c = row[i]
        if c == '\\' and in_string and i + 1 < len(row):
            current.append(c)
            current.append(row[i+1])
            i += 2
            continue
        if c == "'" and not in_string:
            in_string = True
            current.append(c)
        elif c == "'" and in_string:
            in_string = False
            current.append(c)
        elif c == ',' and not in_string:
            fields.append(''.join(current).strip())
            current = []
        else:
            current.append(c)
        i += 1
    if current:
        fields.append(''.join(current).strip())
    return fields

def unquote(val):
    val = val.strip()
    if val.upper() == 'NULL':
        return None
    if val.startswith("'") and val.endswith("'"):
        val = val[1:-1]
        val = val.replace("\\'", "'")
        val = val.replace("\\\\", "\\")
        val = val.replace("\\n", "\n")
        val = val.replace("\\r", "\r")
        val = val.replace('\\"', '"')
    return val

posts = []
errors = 0
for match in insert_pattern.finditer(sql):
    row_str = match.group(1)
    fields = split_sql_row(row_str)
    if len(fields) < 23:
        errors += 1
        continue
    try:
        post = {
            "ID":           unquote(fields[0]),
            "post_author":  unquote(fields[1]),
            "post_date":    unquote(fields[2]),
            "post_content": unquote(fields[4]),
            "post_title":   unquote(fields[5]),
            "post_excerpt": unquote(fields[6]),
            "post_status":  unquote(fields[7]),
            "post_name":    unquote(fields[11]),
            "post_type":    unquote(fields[20]),
            "post_parent":  unquote(fields[15]),
        }
        posts.append(post)
    except Exception as e:
        errors += 1

print(f"Total rows parsed: {len(posts)}  (errors: {errors})")

# Show all post_types and statuses
from collections import Counter
types = Counter((p["post_type"], p["post_status"]) for p in posts)
print("\nAll post_type + post_status combinations:")
for (t, s), c in sorted(types.items()):
    print(f"  {t:30s} {s:15s} {c}")

# Filter published pages and posts
published = [p for p in posts if p["post_status"] == "publish" and p["post_type"] in ("post", "page")]
print(f"\nPublished pages/posts: {len(published)}")
for p in published:
    print(f"  [{p['post_type']:5s}] ID={p['ID']:4s} slug={p['post_name'][:50]:50s} title={p['post_title'][:60]}")

with open("extracted_posts.json", "w", encoding="utf-8") as f:
    json.dump(published, f, ensure_ascii=False, indent=2)

print("\nSaved to extracted_posts.json")
