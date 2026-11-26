# Housekeeping: deleting merged brief branches

Agents leave `brief/*` branches on the remote after a brief is merged. Only the author deletes them. Check first what is still in flight: the branches of briefs listed as `under` in `project/lane-plan.html` must stay.

PowerShell (no bash needed):

    git pull
    Get-Content project/housekeeping/delete_brief_branches.sh | Where-Object { $_ -like 'git push origin --delete *' } | ForEach-Object { Invoke-Expression $_ }
    git fetch --prune

Git Bash or Linux: `bash project/housekeeping/delete_brief_branches.sh`, then `git fetch --prune`.

Count what is left: PowerShell `git ls-remote --heads origin 'brief/*' | Measure-Object -Line`; bash `git ls-remote --heads origin 'brief/*' | wc -l`.

The list in the script is a snapshot; the guru regenerates it after each wave of merges. A "Deletion of directory '.git/objects/xx' failed" prompt from Git for Windows is harmless: answer n (a program such as an editor or OneDrive has the folder open).
