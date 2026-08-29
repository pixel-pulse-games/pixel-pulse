# gogit v0.0.7b — Release Notes

Open user registration, dark mode toggle support, guest landing experience, 
and UI styling updates.

## What's new in this release

- **Open Account Registration (`/register`)**
  - Added `GET /register` and `POST /register` route handlers allowing new 
    users to create accounts directly without requiring admin intervention.
  - Users are automatically logged in via secure HTTP cookies upon successful 
    registration.
  - *Note:* Since per-repo permissions are not yet implemented, any user who 
    registers can push to both public and private repositories.

- **Guest Landing & Navigation**
  - Added guest welcome banner on the repository index page guiding unauthenticated 
    visitors to sign in or register.
  - Updated top navigation bar with dynamic session status ("Sign In", "Register", 
    "+ Add user", and "Logout" actions depending on auth state).

- **Dark Mode Support**
  - Integrated theme toggle button in the navigation bar.
  - Dark mode state is persisted across page visits using browser `localStorage` 
    and pure CSS overrides in `/static/style.css`.

- **Existing Core Features Preserved**
  - Commit history viewer (`GET /{repo}/commits`).
  - Admin user creation interface (`GET /admin/users/new`).
  - Public/private repository visibility controls (`gogit.private true`).

  ## What's *not* in this release yet

- No per-repo permissions — any registered user can push to any repository.
- No password reset or account deletion.
- No rate limiting or lockout on failed login attempts.
- No syntax highlighting or README rendering on the repo page.

## How to run
 gogit.exe -repos .\data -init-repo myproject
 gogit.exe -repos .\data -init-repo secret -private
 gogit.exe -userfile .\users.txt -create-user alice -password yourpassword
 gogit.exe -addr :8080 -repos .\data -userfile .\users.txt

## How to verify this release

1. Visit `http://localhost:8080/` anonymously:
   - Verify only public repos are displayed alongside the guest welcome banner.
2. Click **Register** (or go to `http://localhost:8080/register`):
   - Register a new account (e.g. `bob:password123`).
   - Confirm automatic login and redirection to the home dashboard showing both public and private repos.
3. Verify git CLI access for the newly registered user:
  - git clone http://bob:password123@localhost:8080/secret.git

4. Test the **Theme Toggle** button in the top header to ensure dark mode toggles and persists upon refresh.

## Next up

 - Per-repo permissions (restricting who can push/read specific repositories).
 - Syntax highlighting and README file rendering.