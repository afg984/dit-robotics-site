chgrp http . -R
chgrp afg .git -R
find . -type f -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;
chmod 755 manage.py
chmod 775 .
chmod 664 db.sqlite3
