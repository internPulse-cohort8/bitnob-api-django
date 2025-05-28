# Django Virtual Card - Team README

This document outlines the workflow and responsibilities for our Django team working on the virtual card creation service. We are a crucial part of a larger backend infrastructure, integrating with other services to provide a comprehensive financial platform.


## 1. Project Overview
Our team is responsible for developing and maintaining the Django-based backend service that handles virtual card creation and management through the Bitnob API. While other teams (e.g., Node.js for wallet creation, .NET for authentication) are building other core functionalities, our focus is specifically on the virtual card domain. We will interact with these other services via well-defined API endpoints.


## 2. Core Functionality & Our Responsibilities
The Django team's primary responsibilities include:

- **Bitnob API Integration:** Connecting our service to the Bitnob API to facilitate virtual card operations.

- **Virtual Card Creation:** Developing endpoints and logic to request and provision new virtual cards.

- **Virtual Card Management:** Implementing features for listing, funding, blocking, or unblocking virtual cards as needed.

- **Data Storage:** Managing the persistence of virtual card data within our Django application's database.

- **Internal API Endpoints:** Exposing secure API endpoints for other internal services to interact with our virtual card functionality.


## 3. Local Development Setup
To get started with local development, follow these steps:

- **Clone the Repository:**

```
git clone <your-repo-url>
cd <your-repo-name>
```

- **Create and Activate a Virtual Environment:**
It's crucial to use a virtual environment to manage project dependencies in isolation.

```
python -m venv venv
# On macOS/Linux:
source venv/bin/activate
# On Windows (Command Prompt):
venv\Scripts\activate.bat
# On Windows (PowerShell):
venv\Scripts\Activate.ps1
```

- **Install Dependencies:**
Ensure your virtual environment is activated, then install all required packages.

```
pip install -r requirements.txt
```

- **Set Up Environment Variables (`.env` file):**
Sensitive information and environment-specific settings are managed using `python-decouple` via a `.env` file.

Create a file named `.env` in the root directory of your project (the same directory as `manage.py`).

DO NOT commit this file to Git. It is already listed in .gitignore.

Populate your .env file with the necessary variables. Here's a sample. Replace placeholder values with actual credentials (for development only):

Example:
```
SECRET_KEY='actual-django-secret-key'
BITNOB_API_KEY='our_bitnob_api_key'
DEBUG=TRUE
BITNOB_BASE_URL=https://sandboxapi.bitnob.co/api/v1/
```
**Feel free to use the `.env.example` file provided, but ensure to change name to `.env`**

- **Run Migrations:**
Apply any database migrations to set up your local database.

```
python manage.py migrate
```

- **Run the Development Server:**

```
python manage.py runserver
```

Your Django application should now be running locally at http://127.0.0.1:8000/


## 4. Team Workflow: Branches and Pull Requests
We follow a simplified "GitHub Flow" to manage our code changes.

**4.1. The `main` Branch**
The `main` branch represents the stable, production-ready code.

Direct pushes to main are strictly forbidden. All changes must go through a Pull Request.

Always keep your local main branch updated.

**4.2. Feature Branching**
For every new task (feature, bug fix, improvement), you must create a new branch.

- **Start from `main`:**
Always ensure your local `main` is up-to-date before creating a new branch.

```
git checkout main
git pull origin main
```

- **Create your Feature Branch:**
Choose a descriptive name.

```
git checkout -b feature/your-task-name
# Examples:
# git checkout -b feature/implement-virtual-card-creation
# git checkout -b bugfix/fix-card-status-display
# git checkout -b chore/update-bitnob-sdk
```

- **4.3. Developing and Committing**
As you work on your task:

1. Make your code changes.

2. Stage your changes:

```
git add . # Or git add <specific_file>
```

3. Commit your changes:
Write clear and concise commit messages.

```
git commit -m "feat: Implement Bitnob virtual card creation endpoint"
# Example: "fix: Correct virtual card status mapping"
# Example: "chore: Update Django to latest patch version"
```

**Commit Message Best Practices:**
- Start with a type (feat, fix, chore, docs, style, refactor, test, build, ci).

- Followed by a colon and a space.

- Concise, imperative mood summary (e.g., "Add...", "Fix...", "Update...").

- (Optional) Leave a blank line, then add a more detailed explanation.

4. Push your branch to GitHub:
The first time you push a new branch:

```
git push -u origin feature/your-task-name
```

For subsequent pushes on the same branch:

```
git push
```

Push frequently! This serves as a backup and allows teammates to see your progress.

- **4.4. Keeping Your Branch Updated with `main`**
While you're working, others might merge their changes into `main`. To avoid large conflicts later, regularly pull `main` into your feature branch:

Ensure you are on your feature branch:

```
git checkout feature/your-task-name
```

Pull and merge `main` into your branch:

```
git pull origin main
```

- Resolve any merge conflicts: Git will guide you through this. After resolving, `git add` the conflicted files and `git commit` the merge.

- `git push` your updated feature branch.

- **4.5. Creating a Pull Request (PR)**
When your feature/bug fix is complete, tested, and ready for review:

1. Ensure your branch is pushed and up-to-date.

git push

2. Go to GitHub: Navigate to our repository. GitHub will usually prompt you to create a Pull Request for your recently pushed branch.

3. Configure the PR:

- Base branch: main (this is where your changes will eventually go).

- Compare branch (head): Your feature branch (e.g., feature/implement-virtual-card-creation).

4. Write a Clear PR Description:

Title: A concise summary of the PR's purpose.

Description:

What problem does this PR solve?

What changes were made?

How can reviewers test this functionality?

Any known limitations or future considerations.

Reference any related issues (e.g., "Closes #123", "Resolves #456").

Assign Reviewers: Request reviews from your teammates.


- **4.6. Code Review and Iteration**
1. Reviewers provide feedback: Your teammates will review your code on GitHub, leaving comments and suggestions.

2. Address feedback: Make necessary changes in your local feature branch, commit them, and git push them. These new commits will automatically appear in the open PR.

3. Discuss: Use the PR comments for discussion and clarification.


- **4.7. Merging and Cleaning Up**
Once the PR is approved and all discussions are resolved:

1. Merge the Pull Request: The designated team lead or an approved reviewer will merge the PR into the main branch on GitHub.

2. Delete the Feature Branch: After merging, GitHub usually offers a button to delete the feature branch. Do this to keep the repository clean.

3. Update your Local main and Delete Local Branch:

```
git checkout main
git pull origin main # Get the newly merged changes
git branch -d feature/your-task-name # Delete your local feature branch
```

(Use `git branch -D` if Git complains about unmerged changes, but try to avoid this by always merging main into your feature branch before the final PR merge).


## 5. Key Tools & Technologies
Python 3.x

- Django: Web framework

- Django REST Framework (DRF): For building our APIs

- `python-decouple`: For managing environment variables and settings

`requests`: For making HTTP requests to external APIs (like Bitnob)

Bitnob API: The primary external service we integrate with for virtual card functionality.

## 6. Communication & Collaboration
GitHub Issues: Use GitHub Issues to track tasks, bugs, and features. Assign issues to yourself when you start working on them. (N.B: We might not keep strictly to this only because we’re in a race against time)

Pull Request Comments: Use PR comments for specific code feedback and discussions.

Team Stand-ups/Check-ins: Regular (e.g., About 3 times daily when we select time) brief meetings to discuss progress, roadblocks, and next steps.

## 7. Contribution Guidelines
Always work on a new branch for each task.

Keep your commits focused and write clear messages.

Push your branch regularly.

Create Pull Requests for all changes to main.

Be proactive in reviewing teammates' PRs.

Communicate any challenges or roadblocks early.

Let's build the best feature together!

N.B: This wasn't edited to the best of abilites, and should be improved. It was just to get the team started.