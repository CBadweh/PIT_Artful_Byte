# Episode 10 – CI/CD Top Level

## 1. High-level workflow (lifecycle)

```mermaid
flowchart LR
    subgraph Local["Local (your machine)"]
        B[New branch]
        C[Edit code]
        D[make + make cppcheck]
        E[Commit]
        F[Push branch]
        B --> C --> D --> E --> F
    end

    subgraph GitHub["GitHub"]
        PR[Open Pull Request]
        CI[GitHub Actions: build + cppcheck]
        Merge[Merge to main]
        PR --> CI --> Merge
    end

    F --> PR
    CI -->|fail| Fix[Fix & push again]
    Fix --> PR
```

## 2. Where things run (containers & repo)

```mermaid
flowchart TB
    subgraph Local["Your PC"]
        A[Code + Dockerfile] --> B[Build image]
        B --> C[Push image]
        A --> D[Commit & push code]
    end

    C --> DH[(Docker Hub)]
    D --> GH[GitHub repo]

    GH --> Trigger[Push / PR]
    Trigger --> Action[GitHub Action]
    Action --> VM[Linux VM]
    VM --> Pull[Pull image]
    DH --> Pull
    Pull --> Container[Container]
    GH --> Checkout[Checkout code]
    Checkout --> Container
    Container --> Make[make + make cppcheck]
    Make --> Result{Pass?}
    Result -->|Yes| Merge[Merge allowed]
    Result -->|No| Fix[Fix and re-push]
```

## 3. CI job steps (sequence)

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant GH as GitHub
    participant VM as GitHub runner (Ubuntu VM)
    participant DH as Docker Hub
    participant Box as Container (MSP430 toolchain)

    Dev->>GH: Push branch / open PR
    GH->>VM: Start workflow
    VM->>DH: docker pull artful-bytes-msp430
    DH-->>VM: Image
    VM->>Box: Start container
    VM->>GH: Checkout repo into container
    GH-->>Box: Source code
    Box->>Box: make (TOOLS_PATH=/dev/tools)
    Box->>Box: make cppcheck
    alt All pass
        Box-->>VM: Success
        VM-->>GH: Status: pass → merge allowed
    else Build or cppcheck fails
        Box-->>VM: Failure
        VM-->>GH: Status: fail → merge blocked
        GH-->>Dev: Fix and re-push
    end
```

## 4. Main branch protection (rules)

```mermaid
flowchart LR
    subgraph Rules["Branch protection: main"]
        R1[Require PR]
        R2[Require CI status check]
        R3[Require up-to-date branch]
        R4[No bypass]
    end

    PR[Pull request] --> R1
    R1 --> R2
    R2 --> R3
    R3 --> R4
    R4 --> Merge[Merge allowed]
```