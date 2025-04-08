#!/bin/sh

git filter-branch -f --env-filter '
OLD_EMAIL_1="test@Tests-MBP.fritz.box"
OLD_EMAIL_2="test@tests-mbp.home"

CORRECT_NAME="ffers"
CORRECT_EMAIL="fferses@gmail.com"

if [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL_1" ] || \
   [ "$GIT_COMMITTER_EMAIL" = "$OLD_EMAIL_2" ]; then
    export GIT_COMMITTER_NAME="$CORRECT_NAME"
    export GIT_COMMITTER_EMAIL="$CORRECT_EMAIL"
fi

if [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL_1" ] || \
   [ "$GIT_AUTHOR_EMAIL" = "$OLD_EMAIL_2" ]; then
    export GIT_AUTHOR_NAME="$CORRECT_NAME"
    export GIT_AUTHOR_EMAIL="$CORRECT_EMAIL"
fi
' --tag-name-filter cat -- --all


