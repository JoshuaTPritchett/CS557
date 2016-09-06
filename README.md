#Git Setup
```
 $git clone repo_url_here
 $git checkout -b your_branch_name (creates a local branch for you to work on)
 $git status (will check which branch you are on)
```

#Basic Git Procedure to Upload Code
```
  $git checkout master
  $git pull origin master (pulls master resources)
  $git checkout your_branch_name
  ** DO YOUR WORK THEN ***
  $git status (red will be files you changed)
  $git add file1 file2 ... (add all of the files you changed by name)
  $git commit -m "your message here" (make the message descriptive)
  $git checkout master
  $git pull origin master
  $git merge --squash your_branch_name (make sure you did your changes)
  $git push origin master (when you are ready for Josh to check it)
```
Any additional advice would be helpful if this work flow does not work for you

