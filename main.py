import requests
import json

# SETTINGS
USER = "MassimoSandre"
AVOID_FORKS = True

print("Getting repos info, it may take a while...")

gh_data = requests.get(f"https://api.github.com/users/{USER}/repos?page=1")
gh_data = gh_data.json()


repos_num = 0
repos = []
page = 2
while len(gh_data) > 0:
    for repo in gh_data:
        if not (AVOID_FORKS and repo["fork"]):
            repos.append(repo["name"])
            repos_num +=1
    gh_data = requests.get(f"https://api.github.com/users/{USER}/repos?page={page}")
    page+=1
    gh_data = gh_data.json()

print(f"Ready to download {repos_num} repositories")

output = []
i = 1
for repo_name in repos:
    if not (AVOID_FORKS and repo["fork"]):
        d = {"name": repo_name, "languages": None}
        loc_data = requests.get(f"https://api.codetabs.com/v1/loc?github={USER}/{repo_name}")
        d["languages"] = loc_data.json()
        output.append(d)
        
        file = open("repos.json","w")
        json.dump(output,file,indent=4)
        file.close()

        comp = (100*i)//repos_num
        print(f"{comp}% completed")
        i+=1

print("Generating stats...")

stats = {
    "repos_count": repos_num,
    "languages": []
    }


for repo in output:
    for lang in repo["languages"]:
        found = False
        for l in stats["languages"]:
            if l["language"] == lang["language"]:
                found = True

                l["files"] += lang["files"]
                l["lines"] += lang["lines"]
                l["blanks"] += lang["blanks"]
                l["comments"] += lang["comments"]
                l["linesOfCode"] += lang["linesOfCode"]
        
        if not found:
            new_lang = {
                "language": lang["language"],
                "files": lang["files"],
                "lines": lang["lines"],
                "blanks": lang["blanks"],
                "comments": lang["comments"],
                "linesOfCode": lang["linesOfCode"]
            }
            stats["languages"].append(new_lang)


file = open("stats.json","w")
json.dump(stats,file,indent=4)
file.close()

print("Generation completed")