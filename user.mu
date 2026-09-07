#!/usr/bin/python
print("#!c=0")

import os
import re
from utils import sanitize

id_hash = os.environ.get("var_id")
passed_name = os.environ.get("var_name", "")

if not id_hash:
  print("No identity provided.")
else:
  display_name = sanitize(passed_name) if passed_name else "Unknown"

  print("Name: " + display_name)
  print("Id: " + id_hash)

print("")
print("`_`[Back to chat`:/page/index.mu]`_")
