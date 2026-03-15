### Section 4: Development Workflow & Best Practices

---

### Lesson 008 --- How I Version Control with Git (Best Practices)

**File Path:** [Lesson_008_transcript.txt](Artful_Bytes_Transcript/8%20How%20I%20version%20control%20with%20git%20(Best%20Practices)%20%20Embedded%20System%20Project%20Series%20%238.txt)

**Objective:** Initializes the nsumo git repository, makes the first commit (project skeleton), adds the printf submodule, and establishes git best practices including commit conventions, commit message formatting, and a branching workflow that will be used throughout the series.

**Terminology & Key Concepts:**
- **Git**: A distributed version control system (created by Linus Torvalds) that tracks changes as commits, maintains a complete history, and enables collaboration. The de facto standard for software projects.
- **Commit**: A snapshot of changes with a unique SHA-1 hash, an author, a timestamp, and a message describing what changed. Commits are the building blocks of a project's history.
- **Conventional Commits**: A commit message convention that structures messages as: `type(scope): description` on the subject line, followed by a body explaining *why*, and an optional footer for metadata. Types include `feat`, `fix`, `build`, `docs`, etc.
- **Git Submodule**: A mechanism to embed one git repository inside another at a pinned commit. Used to include the external printf library while preserving its origin and version.
- **`.gitignore`**: A file listing patterns of files/directories that git should not track. For this project, the `build/` directory is gitignored because its contents are generated artifacts.
- **Repository Hosting (GitHub)**: A platform for hosting git repositories remotely, enabling backup, collaboration, pull requests, and CI/CD integration.
- **Agile Mindset / Incremental Development**: The philosophy of delivering small, well-defined, working increments rather than large monolithic changes. Aligns with small, frequent commits.

**Techniques & Methods:**
- ==**Commit Rules (Three Rules)**:==
  1. Each commit contains only one change (single feature, fix, or logical unit).
  2. Each commit must build successfully (and pass static analysis).
  3. Each commit has a good message explaining what and especially *why*.
- ==**Conventional Commit Message Format**:==
  ```
  type(scope, subject line): short description (max 50 chars, describe solution not problem)

  Body: explain WHY this change is needed,
  not just what it does. Motivate the change
  to a potential reviewer or future self.

  Footer: video number, issue number, etc., JIRA-123
  ```
- **Imperative Mood**: Write "Add feature" not "Added feature" or "Adding feature." Think of the commit as something to be applied.
- **Command-Line Git**: Using git exclusively from the terminal (`git init`, `git add`, `git commit`, `git push`, `git log`, `git config --local`). Editor plugins (Vim + fugitive) supplement but don't replace CLI usage.
- **Local Git Configuration**: Using `git config --local` to set username and email per-repository rather than relying on global configuration.
- **Feature-per-Video Workflow**: Each video covers one module or feature, resulting in one or more well-defined commits that map cleanly to the video series progression.

**Source Code Mapping:**
- First commit message example:
  ```
  build: set project structure and add initial files

  Fill the project directory with all the required directories
  to immediately clarify the project structure to be used
  throughout the project series. Some placeholder files added
  because otherwise git won't pick up the directories.

  Video: How I Version Control with Git (Best Practices)
  ```
- Second commit message example:
  ```
  feat(external): add stripped-down printf implementation

  The printf implementation part of the standard library is too
  large for a small microcontroller, so use an external stripped-down
  implementation. Added unchanged as a submodule for better tracking.

  Video: How I Version Control with Git (Best Practices)
  ```

**Demo / Example:**
- **Goal:** Initialize the repository, make the first two commits following best practices, and push to GitHub.
- **Why Important:** Establishes the version control workflow and commit conventions that will be followed for the entire project. Good git practices are a professional necessity and improve project traceability.
- **Demo Flow:**
  1. Verify the project builds with `make` before committing.
  2. `git init` to initialize the repository.
  3. `git config --local user.name` and `user.email` for per-repo config.
  4. `git add .` to stage all files (`.gitignore` excludes `build/`).
  5. `git commit` with a Conventional Commits message (type: `build`, no scope, body explains why).
  6. Add GitHub remote, push to GitHub. README images render nicely on GitHub.
  7. Second commit: `git submodule add` the printf library under `external/printf`. Commit with type `feat`, scope `external`, body explains why the standard printf is too large.
  8. `git push`, verify both commits appear in `git log`.

**New Tools Introduced:**
- **Git** --- distributed version control system (command-line usage)
- **GitHub** --- repository hosting platform for remote backup, collaboration, and CI

**Discussion Prompts:**
- **Q1: Why focus on commit message quality for a solo project?**
  - Even as a sole developer, good commit messages serve as documentation of your decision-making process. When revisiting code weeks or months later, a well-written commit message explains *why* a change was made, not just what changed. It also builds the habit needed for professional collaborative development.
- **Q2: Why prefer many small commits over few large ones?**
  - Small commits are easier to review (including self-review), easier to revert if something breaks, create a more granular history for `git bisect`, and align with an agile workflow of incremental progress. Large commits often mix unrelated changes, making them harder to understand and debug.
- **Q3: Why use git submodules for the printf library?**
  - Submodules preserve the connection to the upstream repository and pin to a specific commit. This makes it clear where the code came from, which version is in use, and avoids modifying third-party code. Alternatives (copy-paste, package managers) lose this traceability.

**commit tempalte**
● No, Vim doesn't enforce any structure — it's just a blank text editor. He can type whatever he wants.         
  The Conventional Commits format (subject line, blank line, body, footer) is a self-imposed discipline, not   something the tool enforces. Nothing stops him from writing "fixed stuff" and saving.                      
                                                                                                             
  However, there are ways to enforce structure:
  
  - Git hooks (commit-msg hook) — a script that rejects commit messages not matching a pattern
  - CI tools like commitlint — check commit messages in the pipeline
  - Editor templates — git config commit.template .gitmessage pre-fills a template when the editor opens

**Visual Diagrams (from video ~00:57–03:03):**

These three diagrams answer **"Why use git?"** in increasing order of importance:

*Diagram 1: Commits Build a History*

A commit packages your change with an ID and description. Each commit links to the next, forming a traversable history that doubles as project documentation.

```
                                          History
  Commit                      ┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐   ┌───┐
 ┌──────────────┐             │ C1├──>│ C2├──>│ C3├──>│ C4├──>│ C5├──>│ C6│
 │              │             │   │   │   │   │   │   │   │   │   │   │   │
 │  ID          │ ─────────>  └───┘   └───┘   └───┘   └───┘   └───┘   └───┘
 │  +           │
 │  Description │              Traverse  ◄── ◄── ◄── ◄──  (go back to any version)
 │              │
 └──────────────┘              Documentation  (quality depends on commit messages)
```

- Each box in the chain is one commit (ID + message + diff)
- Git stores only the **differences**, not full copies
- You can traverse backward to restore any earlier version
- The chain itself is documentation — but only as good as your commit messages

*Diagram 2: Side-benefit — Backup (Distributed Nature)*

Because git is distributed, every clone holds the **complete** repository history. If any site is lost, the others still have everything.

```
                        Side-benefit: Backup

         Comp 1              Comp 2              GitHub
        ┌──────┐            ┌──────┐           ┌────────┐
        │ ┌──┐ │            │ ┌──┐ │           │ Server │
        │ │  │ │            │ │  │ │           │ ┌────┐ │
        │ └──┘ │            │ └──┘ │           │ │    │ │
        │  /\  │            │  /\  │           │ ├────┤ │
        └──┘└──┘            └──┘└──┘           │ │    │ │
             \                  |              └───┬──┘─┘
              \                 |                 /
               \                |                /
                \               |               /
                 v              v              v
              ┌──────────────────────────────────┐
              │     One complete copy on each     │
              │     site (full history + code)    │
              └──────────────────────────────────┘
```

- Git is **distributed** — not client-server
- `git push` to GitHub = automatic off-site backup
- Working from multiple computers = multiple backups
- Each clone has the **entire** commit history, not just latest files

*Diagram 3: Collaboration — Branches, Merging, and Conflict Resolution*

Two developers work on separate branches. When merging back, changes to the same code create conflicts that must be resolved.

```
                        Collaboration!

                  o───o───o───o              ~ Branch 1 (Dev A)
                 /               \
        o───o───o                 o──>  (merged)
                 \               /
                  o───o───o──o          ~ Branch 2 (Dev B)


        When both branches modify the same code:

        ┌─────────┐         ┌─────────┐
        │ File v1 │         │ File v2 │
        │ (Dev A) │ ──────> │ (Dev B) │
        │  ~~~    │    \  / │  ~~~    │
        └─────────┘     \/  └─────────┘
                        /\
                       /  \
                    ┌────────┐
                    │CONFLICT│
                    │  ****  │
                    └───┬────┘
                        │
                        v
                   ┌──────────┐
                   │ Resolve  │
                   └──────────┘
```

- Branches let developers work on different parts of the code **in parallel**
- Merging combines the work back together
- **Conflicts** occur when both branches modify the same lines
- Git detects conflicts and helps you **resolve** them
- This is where git "truly shines" — code review, parallel work, conflict resolution
- The instructor notes he won't use this much since he's a solo developer on nsumo

| # | Diagram | Git Benefit | Transcript Timestamp |
|---|---------|-------------|---------------------|
| 1 | Commit chain | Track changes, traverse history, documentation | ~00:57–02:12 |
| 2 | Distributed backup | Automatic backup across machines and GitHub | ~02:18–02:32 |
| 3 | Collaboration | Branching, merging, code review, conflict resolution | ~02:36–03:03 |

---

### Lesson 009 --- Static Analysis for C/C++ with cppcheck (+Makefile)

**File Path:** [Lesson_009_transcript.txt](Artful_Bytes_Transcript/9%20Static%20Analysis%20for%20CC+%20with%20cppcheck%20(+Makefile)%20%20Embedded%20System%20Project%20Series%20%239.txt)

**Objective:** Introduces static analysis using cppcheck to catch bugs that the compiler misses, demonstrates running it from the command line and integrating it into the Makefile as a `make cppcheck` rule for convenient project-wide analysis.

**Terminology & Key Concepts:**
- **Static Analysis**: Analyzing source code without executing it to find potential bugs, code quality issues, and violations. Complements compiler warnings by catching deeper issues like out-of-bounds array access, unused functions, null pointer dereferences, etc.
- **cppcheck**: A free, open-source static analyzer for C and C++. Available in Ubuntu's standard repository via `sudo apt install cppcheck`. Catches errors the compiler does not, such as buffer overflows and unused code.
- **Error Exit Code (`--error-exitcode=1`)**: A cppcheck flag that makes the tool return a non-zero exit code when errors are found. Critical for CI integration --- the CI pipeline can fail if static analysis detects issues.
- **Inline Suppression**: A way to suppress specific cppcheck warnings directly in the source code using `// cppcheck-suppress unusedFunction` comments, combined with the `--inline-suppr` flag.
- **Command-Line Suppression (`--suppress`)**: Suppressing specific warnings via command-line flags, optionally scoped to a specific file and line number. E.g., `--suppress=unusedFunction:main.c:5`.
- **Enable All Checks (`--enable=all`)**: Enables all cppcheck analysis categories (style, performance, portability, etc.) beyond just errors. More comprehensive but may produce more warnings.

**Techniques & Methods:**
- **Running cppcheck on Individual Files**: `cppcheck --quiet --enable=all --error-exitcode=1 main.c` for quick single-file analysis.
- **Running cppcheck on Directories**: `cppcheck src/` to recursively analyze all files in a directory. Use `-I` flag to add include directories for header resolution.
- **Makefile Integration**: Adding a `cppcheck` phony target to the Makefile for one-command project-wide analysis.
  ```makefile
  cppcheck:
  	@$(CPPCHECK) $(CPPCHECK_FLAGS) $(SOURCES_FORMAT_CPPCHECK)
  ```
- **Suppression Strategies**: Three levels of suppression: (1) inline `// cppcheck-suppress` in source, (2) `--suppress=errorId:file:line` on command line, (3) `--suppress=errorId` globally. Use judiciously --- suppress only when the warning is a false positive or intentional.
- **Excluding External Code**: Using `-i` flag to exclude directories (like `external/printf/`) from analysis, since third-party code should not be modified.

**Source Code Mapping:**

==**Automate with Makefile**==
- `Makefile:116-130` --- cppcheck configuration in the production Makefile:
  ```makefile
  CPPCHECK_INCLUDES = ./src ./
  CPPCHECK_FLAGS = \
  	--quiet --enable=all --error-exitcode=1 \
  	--inline-suppr \
  	--suppress=missingIncludeSystem \
  	--suppress=unmatchedSuppression \
  	--suppress=unusedFunction \
  	$(addprefix -I,$(CPPCHECK_INCLUDES))
  ```
- `Makefile:160-161` --- The cppcheck phony target:
  ```makefile
  cppcheck:
  	@$(CPPCHECK) $(CPPCHECK_FLAGS) $(SOURCES_FORMAT_CPPCHECK)
  ```

==**To run it Manually**==
To run it manually on a single file:

cppcheck --quiet --enable=all --error-exitcode=1 src/drivers/io.c

Then you'd add flags one by one as you hit issues:
- --suppress=missingIncludeSystem — because cppcheck can't find system headers
- -I./src — so it can resolve your project headers
- -iexternal/printf — skip third-party code

**Demo / Example:**
- **Goal:** Install cppcheck, demonstrate it catching bugs the compiler misses, and integrate it into the Makefile.
- **Why Important:** Static analysis catches bugs earlier in the development cycle, before they become runtime errors. Integrating it into the Makefile (and later CI) makes it effortless to run and impossible to skip.
- **Demo Flow:**
  1. Install cppcheck: `sudo apt install cppcheck`.
  2. Create a C file with an intentional out-of-bounds array access. Run cppcheck --- it detects the error.
  3. Fix the array error, add an unused function. Run cppcheck with `--enable=all` --- it detects the unused function.
  4. Demonstrate suppression: `--suppress=unusedFunction:main.c` and inline `// cppcheck-suppress unusedFunction`.
  5. Add `cppcheck` phony target to the Makefile with all flags.
  6. Exclude `external/` directory with `-i external/` to avoid analyzing third-party code.
  7. Run `make cppcheck` --- clean output with no errors.
  8. Commit the Makefile changes.

**New Tools Introduced:**
- **cppcheck** --- free, open-source static analyzer for C/C++ that catches bugs the compiler misses

**Discussion Prompts:**
- **Q1: Why use static analysis in addition to compiler warnings?**
  - Compilers focus on language correctness (syntax, types, linking). Static analyzers perform deeper semantic analysis --- detecting buffer overflows, null dereferences, unused code, resource leaks, and logic errors that compile without warnings but cause runtime bugs.
- **Q2: Should you fix all cppcheck warnings or suppress some?**
  - Fix genuine issues. Suppress only false positives (e.g., unused functions that will be used in future commits, system header warnings). The `--suppress=unusedFunction` in this project is used because functions are added incrementally across videos --- they may appear unused in early commits but are used later.

---

### Lesson 010 --- Simple CI/CD with GitHub Actions and Docker (Compile + Analysis)

**File Path:** [Lesson_010_transcript.txt](Artful_Bytes_Transcript/10%20Simple%20CICD%20with%20GitHub%20Actions%20and%20Docker%20(Compile+Analysis)%20%20%20Embedded%20System%20Project%20Series%20%2310.txt)

**Objective:** Sets up a continuous integration (CI) pipeline using GitHub Actions and Docker to automatically build the project and run static analysis on every push, establishing a workflow where code must pass CI before merging to the main branch.

**Terminology & Key Concepts:**
- **Continuous Integration (CI)**: The practice of automatically building, analyzing, and testing code on every commit/push to catch integration errors early. Prevents broken code from reaching the main branch.
- **GitHub Actions**: GitHub's built-in CI/CD platform. Workflows are defined in YAML configuration files under `.github/workflows/`. Jobs run on GitHub's servers, triggered by events like pushes or pull requests.
- **Docker Container**: A lightweight, reproducible environment that packages an OS, tools, and dependencies. Used here to package the MSP430 GCC toolchain so the CI system has a consistent, reproducible build environment.
- **Docker Hub**: A hosting platform for Docker container images (analogous to GitHub for git repositories). The instructor pushes the custom MSP430 toolchain container to Docker Hub so GitHub Actions can pull it.
- **Dockerfile**: A script defining how to build a Docker image. Specifies the base OS (Ubuntu 22.04), installs tools (wget, unzip), and sets up the user environment.
- **Pull Request (PR)**: A GitHub feature for proposing changes. The developer pushes a branch, opens a PR, CI runs automatically, and the PR can only be merged if CI passes.
- **Branch Protection Rules**: GitHub settings that enforce policies on the main branch: require PRs before merging, require CI checks to pass, prevent direct pushes.
- **Environment Variable (`TOOLS_PATH`)**: A variable passed to the Makefile at build time to specify the path to the toolchain. Makes the Makefile portable across different environments (local machine vs. Docker container).
- **Rebase and Merge**: A merge strategy that replays commits on top of the main branch without creating a merge commit, resulting in a cleaner linear history.

**Techniques & Methods:**
- **Docker for Toolchain Encapsulation**: The MSP430 GCC cross-toolchain is not available in standard OS package repositories and is too large to commit to git. A Docker container solves both problems --- it encapsulates the toolchain in a reusable, shareable image.
- **CI Pipeline Design**: Three checks executed sequentially on every push: (1) format check, (2) static analysis, (3) build. If any step fails, the pipeline fails and the PR cannot be merged.
- **Branch-Based Development Workflow**:
  1. Create a local feature branch (`git checkout -b feature-name`).
  2. Make code changes, build, and test locally.
  3. Commit and push the branch to GitHub.
  4. Open a pull request.
  5. CI runs automatically; review the PR diff.
  6. If CI passes, merge (rebase and merge for clean history).
- **Environment Variable for Portability**: Using `TOOLS_PATH` environment variable instead of hardcoded paths in the Makefile, allowing the same Makefile to work on the developer's local machine and inside the Docker container.
- **Branch Protection**: Configuring GitHub to require CI checks to pass before allowing merges to main. Also disabling direct pushes to main --- all changes must go through PRs.
- **Self-Review via PR**: Even as a sole developer, reviewing your own PR diff in GitHub's interface helps catch issues you might miss in your editor.

**Source Code Mapping:**
- `.github/workflows/ci.yml` --- The CI configuration file:
  ```yaml
  on: [push]
  jobs:
    build_and_static_analysis:
      runs-on: ubuntu-latest
      container:
        image: artfulbytes/msp430-gcc-9.3.1.11:latest
      env:
        TOOLS_PATH: /home/ubuntu/dev/tools
      steps:
        - name: Checkout the repository
          uses: actions/checkout@v3
          with:
            submodules: "true"
        - run: make format && git diff --quiet
        - run: make cppcheck
        - run: make HW=NSUMO
        - run: make HW=LAUNCHPAD
        - run: make tests
  ```
- `Makefile:26` --- `TOOLS_DIR = ${TOOLS_PATH}` --- Reads the toolchain path from an environment variable instead of hardcoding it.
- `tools/dockerfile` --- Docker image definition (Ubuntu 22.04 base, wget, unzip, user setup).

**Demo / Example:**
- **Goal:** Create a Docker container with the MSP430 toolchain, configure GitHub Actions to run CI on every push, and set up branch protection rules.
- **Why Important:** CI prevents broken code from reaching the main branch. Even for a one-person project, it enforces discipline and catches errors automatically. The setup is reusable for any MSP430 project.
- **Demo Flow:**
  1. Install Docker, create Docker group for non-root access.
  2. Create Dockerfile under `tools/`: base Ubuntu 22.04, install wget/unzip.
  3. Build Docker image, log in, download MSP430 GCC toolchain and support files from TI's website using wget.
  4. Unpack and organize toolchain inside the container, commit the Docker image.
  5. Push the image to Docker Hub as `artfulbytes/msp430-gcc-9.3.1.11:latest`.
  6. Create `.github/workflows/ci.yml`: trigger on push, run in Docker container, checkout repo, run `make` and `make cppcheck`.
  7. Commit and push --- CI fails (indentation error in YAML). Fix and force-push.
  8. Set up branch protection rules on GitHub: require PR, require CI status checks, disallow bypass.
  9. Demonstrate that pushing directly to main is now blocked.
  10. Update Makefile to use `TOOLS_PATH` environment variable. Update CI config to set `TOOLS_PATH` for the Docker container.
  11. Create branch, commit, push, open PR --- CI passes --- merge with rebase.
- **What Changed:**
  - `Makefile`: `TOOLS_DIR` now reads from `${TOOLS_PATH}` environment variable.
  - `.github/workflows/ci.yml`: New CI configuration file.
  - `tools/dockerfile`: New Dockerfile for the MSP430 toolchain container.

**New Tools Introduced:**
- **GitHub Actions** --- CI/CD platform integrated with GitHub for automated build/test/analysis pipelines
- **Docker** --- containerization platform for creating reproducible build environments
- **Docker Hub** --- hosting platform for Docker container images

**Discussion Prompts:**
- **Q1: Why use Docker for CI instead of installing the toolchain directly in the GitHub Actions VM?**
  - (1) The toolchain download URL from TI may break when they update versions. (2) Downloading ~500MB+ on every CI run is wasteful. (3) A Docker container provides a consistent, reproducible environment that matches local development. (4) The container can be reused across multiple projects.
- **Q2: Is CI overkill for a one-person project?**
  - Yes, in terms of strict necessity. But it enforces discipline, catches mistakes automatically, and teaches professional practices. The instructor acknowledges this is "overkill" but justifies it as part of the series' goal to demonstrate professional development practices.
- **Q3: Why use rebase-and-merge instead of regular merge commits?**
  - Rebase-and-merge adds the PR's commits directly on top of the main branch, creating a clean linear history without merge commits. This makes `git log` easier to read and `git bisect` more effective. Regular merge commits add noise to the history for simple single-commit PRs.

---

### Lesson 011 --- Documentation and Clang Format (+2 Bugs)

**File Path:** [Lesson_011_transcript.txt](Artful_Bytes_Transcript/11%20Documentation%20and%20Clang%20format%20(+2%20bugs)%20%20%20Embedded%20System%20Project%20Series%20%2311.txt)

**Objective:** Covers four commits: adding project documentation (README, coding guidelines), integrating clang-format into the Makefile and CI pipeline, fixing a Makefile bug where header file changes were not triggering rebuilds, and fixing a cppcheck performance issue caused by the vendor header file.

**Terminology & Key Concepts:**
- **README.md**: The primary documentation file for the project. Contains a project introduction, directory structure description, setup instructions, build commands, and workflow description. Rendered by GitHub on the repository page.
- **Coding Guidelines (`docs/coding_guidelines.md`)**: A document describing the coding conventions followed in the project: snake_case naming, 4-space indentation, module-prefixed functions, fixed-width integers, typedef rules for enums (suffix `_e`, don't typedef structs, don't use `_t`), include order (local -> project -> system), always use `{}` for if/else, `void` in empty parameter lists, `static` for internal functions, const correctness.
- **Clang-format**: An auto-formatter for C/C++ built on LLVM/Clang. Enforces consistent code formatting (indentation, brace style, line width) based on a `.clang-format` configuration file. Version 12 is used.
- **`.clang-format` Configuration**: Defines the formatting rules. Based on WebKit style with customizations: 100-character column limit, Allman-style braces for functions/structs/classes, K&R-style for control statements, 4-space indent, no tab, pointer binds to variable not type.
- **Makefile Header Dependency Bug**: The original Makefile only listed `.c` files as prerequisites for the build target. Modifying a `.h` file did not trigger a rebuild because Make was unaware of the dependency. Fixed by adding header files to the dependency list.
- **cppcheck Slowness Bug**: cppcheck became extremely slow when analyzing `msp430.h`, which contains thousands of `#ifdef` branches. Fixed by excluding the vendor header from cppcheck's analysis scope.
- **`git diff --quiet`**: A command that returns non-zero if there are uncommitted changes. Used in CI to detect if `make format` produced any changes --- if so, the code was not properly formatted before committing.

**Techniques & Methods:**
- **Formatting as CI Gate**: Adding `make format && git diff --quiet` as the first CI step. If any file is unformatted, `make format` reformats it, `git diff --quiet` detects the change, and CI fails. This prevents unformatted code from being merged.
- **Makefile Format Rule**: Adding a `format` phony target that runs clang-format on all project source and header files in one command.
  ```makefile
  format:
  	@$(FORMAT) -i $(SOURCES_FORMAT_CPPCHECK) $(HEADERS_FORMAT)
  ```
- **Header File Dependency Fix**: Deriving the list of header files from the source file list using suffix replacement (`.c=.h`), then adding headers as prerequisites to the build rule.
  ```makefile
  HEADERS = $(SOURCES_WITH_HEADERS:.c=.h) src/common/defines.h
  $(TARGET): $(OBJECTS) $(HEADERS)
  ```
- **cppcheck Performance Fix**: Separating the include paths for cppcheck (`CPPCHECK_INCLUDES = ./src ./`) from the compiler's include paths (which include the vendor header directory). This prevents cppcheck from analyzing the massive `msp430.h` file.
- **Suppression for System Headers**: Adding `--suppress=missingIncludeSystem` to avoid warnings about system headers that cppcheck cannot find.
- **Docker Image Update**: Updating the Dockerfile to include `clang-format-12` and `git` so the CI container can run formatting checks.
- **Four-Commit Workflow**: Each of the four changes (docs, clang-format, header bug fix, cppcheck bug fix) is a separate commit with its own branch, PR, and CI run --- demonstrating the disciplined workflow from Lesson 10.

**Source Code Mapping:**
- `Makefile:163-164` --- Format rule:
  ```makefile
  format:
  	@$(FORMAT) -i $(SOURCES_FORMAT_CPPCHECK) $(HEADERS_FORMAT)
  ```
- `Makefile:98-101` --- Header derivation from sources:
  ```makefile
  HEADERS = \
  	$(SOURCES_WITH_HEADERS:.c=.h) \
  	src/common/defines.h \
  ```
- `Makefile:139` --- Build rule with header dependencies:
  ```makefile
  $(TARGET): $(OBJECTS) $(HEADERS)
  ```
- `.clang-format` --- Formatting configuration:
  ```yaml
  BasedOnStyle: WebKit
  Language: Cpp
  ColumnLimit: 100
  BreakBeforeBraces: Custom
  BraceWrapping:
      AfterFunction: true
      AfterControlStatement: false
  AllowShortFunctionsOnASingleLine: Empty
  SortIncludes: false
  ```
- `docs/coding_guidelines.md` --- Key guidelines:
  - snake_case for files, functions, variables; UPPER_CASE for defines
  - Prefix functions with module name: `uart_init()`, `i2c_read()`
  - One module = one `.c/.h` pair
  - 4-space indent, no tabs
  - Always use `{}` for if/else
  - `void` in empty parameter lists
  - Internal functions must be `static`
  - Fixed-width integers (`uint8_t`, `uint16_t`)
  - Typedef enums with `_e` suffix; do NOT typedef structs or use `_t`
  - Include order: local -> project -> system
- `.github/workflows/ci.yml:14` --- Format check in CI pipeline:
  ```yaml
  - run: make format && git diff --quiet
  ```

**Demo / Example:**
- **Goal:** Add documentation, integrate clang-format into the build and CI pipeline, and fix two build system bugs.
- **Why Important:** Documentation makes the project accessible to others. Automated formatting eliminates style debates and ensures consistency. The bug fixes demonstrate real-world Makefile debugging --- exactly the kind of issues developers encounter when building their own build systems.
- **Demo Flow:**
  **Commit 1 --- Documentation:**
  1. Create README.md with project intro, directory structure, setup instructions, workflow.
  2. Create `docs/coding_guidelines.md` with all naming, formatting, and coding conventions.
  3. Add `.compile_commands.json` and `.cache` to `.gitignore` (editor-generated files).
  4. Branch, commit (type: `docs`), push, PR, CI passes, merge.

  **Commit 2 --- Clang-format Integration:**
  1. Add `format` phony target to Makefile: `clang-format-12 -i` on all source and header files.
  2. Update Dockerfile to install `clang-format-12` and `git`.
  3. Add `make format && git diff --quiet` as first CI step.
  4. Demonstrate locally: modify a file, `git diff` returns error; run `make format`, `git diff` returns zero.
  5. Branch, commit, push, PR, CI passes, merge.

  **Commit 3 --- Header Dependency Bug Fix:**
  1. Problem: modifying a `.h` file and running `make` says "up to date" --- the bug is not detected until a clean rebuild.
  2. Root cause: header files were not listed as prerequisites in the Makefile.
  3. Fix: create `HEADERS` variable from `SOURCES_WITH_HEADERS` using `.c=.h` substitution, add to build rule dependencies.
  4. Verify: modify a header, run `make` --- rebuild triggered, compilation error detected.
  5. Branch, commit, push, PR, CI passes, merge.

  **Commit 4 --- cppcheck Performance Bug Fix:**
  1. Problem: `make cppcheck` takes minutes instead of seconds after adding code.
  2. Root cause: cppcheck was analyzing `msp430.h`, which has thousands of `#ifdef` branches.
  3. Fix: use separate include paths for cppcheck (`CPPCHECK_INCLUDES = ./src ./`) that exclude the vendor header directory.
  4. Add suppressions: `missingIncludeSystem`, `unmatchedSuppression`, `unusedFunction`.
  5. Also fix `make cppcheck` error on second run by adding `-p` flag to `mkdir`.
  6. Branch, commit, push, PR, CI passes, merge.
- **What Changed:**
  - `README.md`: Complete project documentation.
  - `docs/coding_guidelines.md`: New coding conventions document.
  - `Makefile`: Added `format` target, fixed header dependencies, fixed cppcheck include paths and suppressions.
  - `.github/workflows/ci.yml`: Added format check step.
  - `tools/dockerfile`: Added `clang-format-12` and `git` packages.
  - `.gitignore`: Added editor-generated files.

**New Tools Introduced:**
- **clang-format (v12)** --- auto-formatter for C/C++ that enforces consistent coding style based on a configuration file

**Discussion Prompts:**
- **Q1: Why automate code formatting instead of relying on developers to format manually?**
  - Manual formatting is inconsistent, error-prone, and leads to style debates during code reviews. An auto-formatter applied via CI ensures every file in the repository follows the same style. Developers never have to think about formatting --- just run `make format` before committing, or let CI catch it.
- **Q2: Why was the header dependency bug significant?**
  - Without header files in the Makefile's dependency list, modifying a struct definition, changing a constant in `defines.h`, or altering a function signature in a header would not trigger a rebuild. The developer would run `make`, see "up to date," and believe the code is correct --- but the binary would contain the old definitions. This could cause subtle, hard-to-debug runtime errors. Only a `make clean && make` would catch it, which defeats Make's purpose.
- **Q3: Why did cppcheck become slow on the vendor header file?**
  - The `msp430.h` header contains hundreds of `#ifdef` blocks (one for each MSP430 variant). cppcheck attempts to analyze all possible preprocessing paths, leading to combinatorial explosion. Since the vendor header is trusted and unmodifiable, excluding it from analysis is the correct approach.
