import re

text = "Buy milk #shopping do laundry #chores go out"

tags = re.findall(r"#(\w+)", text or "")
print(tags)