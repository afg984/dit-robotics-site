chgrp http . -R
find . -type f -exec chmod 664 {} \;
find . -type d -exec chmod 775 {} \;
chmod 755 manage.py \;
chmod 640 .git -R
