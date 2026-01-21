# Artful Bytes Hugo Site - Codebase Architecture

## 1. Project Overview

| Property | Value |
|----------|-------|
| **Project Name** | Artful Bytes Hugo Site |
| **Base URL** | https://artfulbytes.com/ |
| **Platform** | Hugo v0.131.0 |
| **Theme** | PaperMod (Git submodule) |
| **Deployment** | Netlify |
| **Purpose** | Educational content platform about embedded systems engineering |

---

## 2. Root Directory Structure

```
hugosite-main/
├── config.yaml              # Main Hugo configuration
├── netlify.toml             # Netlify deployment configuration
├── README.md                # Project documentation
├── .gitignore               # Git ignore rules
├── .gitmodules              # Git submodule definitions (PaperMod theme)
├── .hugo_build.lock         # Hugo build lock file
│
├── content/                 # Website content (Markdown)
├── layouts/                 # Custom HTML templates
├── assets/                  # CSS and compiled assets
├── static/                  # Static files (images, videos)
├── archetypes/              # Content templates
├── public/                  # Generated output (build artifacts)
└── themes/                  # Hugo themes (PaperMod submodule)
```

---

## 3. Layer Architecture

### 3.1 Content Layer (`content/`)

```
content/
├── _index.md          # Home page content + video series data (28 videos)
├── guide.md           # Embedded systems learning guide (/embedded-guide)
└── thanks.md          # Email signup confirmation page (/email-thanks)
```

**Purpose:** Markdown files containing all website content with YAML/TOML frontmatter for metadata.

**Key Content:**
- `_index.md`: Contains `videoseries` array with 28 embedded systems tutorial videos
- `guide.md`: Comprehensive learning guide for embedded development
- `thanks.md`: Newsletter signup confirmation page

---

### 3.2 Template Layer (`layouts/`)

```
layouts/
├── index.html                    # Custom home page layout
└── partials/                     # Reusable template components
    ├── header.html               # Navigation header with theme toggle
    ├── footer.html               # Footer with links and scripts
    ├── contact-form.html         # Netlify contact form
    ├── convertkit-form.html      # Newsletter signup form
    ├── video-slider.html         # Video carousel component
    └── extend_head.html          # Head tag extensions
```

**Purpose:** Go HTML templates that override or extend PaperMod theme defaults.

**Key Templates:**
| Template | Purpose |
|----------|---------|
| `index.html` | Home page with hero, video grid, carousel, about, and contact sections |
| `header.html` | Navigation with logo, social links, and dark/light theme toggle |
| `footer.html` | Full-width footer with newsletter form, links, and scroll-to-top |
| `video-slider.html` | Horizontal scrolling video carousel |
| `convertkit-form.html` | Email newsletter subscription (ConvertKit ID: 7935190) |
| `contact-form.html` | Contact form with Netlify Forms + honeypot spam protection |

---

### 3.3 Styling Layer (`assets/css/`)

```
assets/
└── css/
    └── extended/
        ├── custom.css              # Main custom styles
        └── theme-vars-override.css # Theme color variables
```

**Purpose:** CSS files that extend and customize the PaperMod theme.

**custom.css Features:**
- Typography: Roboto Condensed (body), Londrina Solid (logo)
- Layout: 960px max-width, centered
- Components: Video grid, carousel, forms, sections
- Responsive breakpoints: 768px (mobile/desktop)

**theme-vars-override.css:**
```css
/* Light Theme */
--theme: #ffffff
--header-bg: #f1f1f1

/* Dark Theme (.dark) */
--theme: #1b1b1b
--header-bg: #242424
```

---

### 3.4 Static Assets Layer (`static/`)

```
static/
└── images/
    ├── niklas.png    # Profile photo
    └── niklas.webm   # Profile video (hero section)
```

**Purpose:** Static files served directly without Hugo processing.

---

### 3.5 Theme Layer (`themes/PaperMod/`)

```
themes/
└── PaperMod/              # Git submodule
    ├── layouts/           # Base templates
    ├── assets/css/        # Theme CSS
    ├── assets/js/         # Theme JavaScript
    ├── i18n/              # Internationalization
    └── go.mod             # Hugo modules definition
```

**Purpose:** PaperMod theme providing base templates, styles, and functionality.

**Source:** https://github.com/adityatelange/hugo-PaperMod

---

### 3.6 Build Output Layer (`public/`)

```
public/                    # Generated static site
├── index.html            # Home page
├── embedded-guide/       # Guide page
├── email-thanks/         # Thanks page
├── categories/           # Category pages
├── tags/                 # Tag pages
├── images/               # Static images
├── assets/css/           # Bundled CSS
├── 404.html              # Error page
├── index.xml             # RSS feed
└── sitemap.xml           # XML sitemap
```

**Purpose:** Hugo-generated static files ready for deployment.

---

## 4. Configuration Files

### 4.1 config.yaml
```yaml
baseURL: https://artfulbytes.com/
languageCode: en-us
title: Artful Bytes
theme: ["PaperMod"]

params:
  defaultTheme: dark
  assets:
    css:
      - css/custom.css
  footer:
    hideCopyright: true
```

### 4.2 netlify.toml
```toml
[build]
  command = "hugo"
  publish = "public"

[context.production.environment]
  HUGO_VERSION = "0.131.0"

# URL redirects for legacy blog posts
[[redirects]]
  from = "/bots2d-blogpost"
  to = "https://github.com/artfulbytes/website/..."
  status = 301
```

### 4.3 .gitmodules
```
[submodule "themes/PaperMod"]
    path = themes/PaperMod
    url = https://github.com/adityatelange/hugo-PaperMod
```

---

## 5. URL Routes

| URL | Source | Template |
|-----|--------|----------|
| `/` (home) | `_index.md` | `layouts/index.html` |
| `/embedded-guide` | `guide.md` | PaperMod default |
| `/email-thanks` | `thanks.md` | PaperMod default |
| `/categories` | Auto-generated | PaperMod |
| `/tags` | Auto-generated | PaperMod |
| `/sitemap.xml` | Auto-generated | Hugo |
| `/index.xml` | Auto-generated | RSS feed |

---

## 6. External Integrations

| Service | Purpose | Integration Point |
|---------|---------|-------------------|
| **ConvertKit** | Email newsletter | `convertkit-form.html` (Form ID: 7935190) |
| **Netlify Forms** | Contact form processing | `contact-form.html` |
| **YouTube** | Video embeds | `video-slider.html`, `index.html` |
| **GitHub** | Source repository | Header social links |

---

## 7. Data Flow Diagrams

### 7.1 Content Rendering Flow
```
config.yaml ─────────┐
                     │
content/*.md ────────┼──→ Hugo Build ──→ public/ ──→ Netlify CDN ──→ Browser
                     │
layouts/*.html ──────┤
                     │
themes/PaperMod/ ────┤
                     │
assets/css/*.css ────┘
```

### 7.2 Video Series Data Flow
```
content/_index.md
    └── frontmatter.videoseries[] (28 videos)
            ↓
    layouts/index.html
            ↓
    layouts/partials/video-slider.html
            ↓
    YouTube thumbnails (i.ytimg.com)
            ↓
    User clicks → YouTube video
```

### 7.3 Form Submission Flow
```
Newsletter Form:
    User → convertkit-form.html → ConvertKit API → /email-thanks

Contact Form:
    User → contact-form.html → Netlify Forms → Email notification
```

---

## 8. Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Browser                             │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                      Netlify CDN (Hosting)                       │
│  ┌─────────────────────────────────────────────────────────┐    │
│  │                    public/ (Static Files)                │    │
│  │  HTML │ CSS │ Images │ XML Feeds                        │    │
│  └─────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────┘
                                ↑
                          Hugo Build
                                ↑
┌─────────────────────────────────────────────────────────────────┐
│                      Source Files                                │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  content/    │  │  layouts/    │  │  assets/     │          │
│  │  (Markdown)  │  │  (Templates) │  │  (CSS)       │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│         ↑                 ↑                 ↑                   │
│         └────────────────┬┴─────────────────┘                   │
│                          ↓                                       │
│              ┌───────────────────────┐                          │
│              │  themes/PaperMod/     │                          │
│              │  (Base Theme)         │                          │
│              └───────────────────────┘                          │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐                             │
│  │ config.yaml  │  │ netlify.toml │                             │
│  │ (Hugo conf)  │  │ (Deploy conf)│                             │
│  └──────────────┘  └──────────────┘                             │
└─────────────────────────────────────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    External Services                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐                │
│  │ ConvertKit │  │  YouTube   │  │   GitHub   │                │
│  │ (Newsletter)│  │  (Videos)  │  │  (Source)  │                │
│  └────────────┘  └────────────┘  └────────────┘                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. File Count Summary

| Category | Count | Location |
|----------|-------|----------|
| Configuration | 3 | Root directory |
| Content | 3 | `content/` |
| Archetypes | 1 | `archetypes/` |
| Templates | 7 | `layouts/` |
| Stylesheets | 2 | `assets/css/` |
| Static assets | 2 | `static/images/` |
| **Total Source** | **~18 files** | |

---

## 10. Development Workflow

### Local Development
```bash
# Clone with submodules
git clone --recurse-submodules <repo>

# Run development server
hugo server

# View at http://localhost:1313
```

### Build Process
```bash
# Build static site
hugo

# Output in public/ directory
```

### Deployment (Netlify)
1. Push to Git repository
2. Netlify auto-triggers build
3. Runs `hugo` command
4. Publishes `public/` directory
5. Live at https://artfulbytes.com/

---

## 11. Key Design Patterns

### 11.1 Template Override Pattern
Custom templates in `layouts/` override PaperMod theme defaults while inheriting base functionality.

### 11.2 Partial Component Pattern
Reusable components in `layouts/partials/` enable modular template design.

### 11.3 CSS Extension Pattern
Files in `assets/css/extended/` automatically extend PaperMod's stylesheets.

### 11.4 Content-Data Hybrid
`_index.md` combines content with structured data (videoseries array) for dynamic rendering.

---

## 12. Technology Stack

| Layer | Technology |
|-------|------------|
| Static Site Generator | Hugo v0.131.0 |
| Theme | PaperMod |
| Templates | Go HTML Templates |
| Content | Markdown (YAML/TOML frontmatter) |
| Styling | CSS3 (custom + theme variables) |
| Forms | Netlify Forms, ConvertKit |
| Hosting | Netlify CDN |
| Version Control | Git (with submodules) |

---

## 13. Accessibility Features

- Keyboard shortcuts (Alt+H, Alt+T, Alt+G)
- Dark/light theme toggle with localStorage persistence
- Semantic HTML structure
- ARIA labels on interactive elements
- Respects `prefers-reduced-motion`

---

## 14. Performance Optimizations

- Hugo asset bundling and minification
- CSS fingerprinting for cache control
- Lazy-loading YouTube thumbnails
- CSS scroll-snap for smooth carousel
- Static site = no server rendering overhead
