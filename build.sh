set -e

pip install cython
pip install -e .

# During the build, this script runs several times, and only needs to download
# repositories on first time.
if [ -d vendor ] && [ `ls -1 vendor | wc -l` = `cat repos.txt | wc -l` ]; then
    echo "$0: Language repositories have been cloned already."
else
    mkdir vendor
    cd vendor

    # Find repositories and their commits from repos.txt
    # Use update-repos.sh if you want to update to latest available commits.
    cat ../repos.txt | while read -r url commit; do
        target_dir=`basename "$url"`
        echo ""
        echo "$0: Cloning: $url (commit $commit) --> $target_dir"
        echo ""

        # https://serverfault.com/a/713065
        mkdir "$target_dir"
        cd "$target_dir"
        git init
        git remote add origin "$url"
        git fetch --depth=1 origin "$commit"
        git checkout "$commit"
        cd ..
    done

    cd ..
fi

echo ""
echo "$0: Running build.py"
python build.py
