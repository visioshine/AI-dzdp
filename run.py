import sys
import os
import site
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Add user site-packages to path
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.append(user_site)

# Also add the scripts directory
scripts_dir = os.path.join(os.path.dirname(user_site), 'Scripts')
if scripts_dir not in sys.path:
    sys.path.append(scripts_dir)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")
