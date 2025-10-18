
import re
NAME_RE  = re.compile(r"^[^\W\d_][^\W\d_'\-]+(?:\s+[^\W\d_][^\W\d_'\-]+){1,2}$", re.UNICODE)
PHONE_RE = re.compile(r"^\+?\d[\d\s\-\(\)]{7,16}\d$")
