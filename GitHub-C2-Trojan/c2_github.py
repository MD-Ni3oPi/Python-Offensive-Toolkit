import github3

# ---------------------------------------------------
# CONFIGURATION - CHANGE THESE THREE
# ---------------------------------------------------
# Your secret token (github_pat_...)
TOKEN = "YOUR TOKEN"

# Your GitHub Username
USER = "USERNAME"

# The name of your private repo
REPO_NAME = "REPO NAME"


def test_connection():
    try:
        # 1. Start the login process
        print(f"[*] Attempting to connect as {USER}...")
        gh = github3.login(token=TOKEN)

        # 2. Try to grab the repository
        repository = gh.repository(USER, REPO_NAME)

        # 3. Check if it actually found the repo
        if repository:
            print(f"[+] SUCCESS! Connected to repository: {repository.name}")
            print(f"[*] Description: {repository.description}")
        else:
            print("[!] FAILED: Repository not found. Check the name.")

    except Exception as e:
        print(f"[!] ERROR: {e}")


if __name__ == "__main__":
    test_connection()
