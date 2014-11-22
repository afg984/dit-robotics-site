chgrp http . -R
chgrp afg .git -R
find . -type f -exec chmod 664 {} \;
find . -type d -exec chmod 775 {} \;
chmod 755 manage.py 
