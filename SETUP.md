# Set up your GitHub profile

This package is designed for **mallesh002/mallesh002**. All display assets are included; the initial design needs no external image service or secret. The existing public profile repository was verified on **9 September 2026**. Nothing has been pushed to GitHub.

## 1. Add the files

Keep `README.md` and `assets/` together at the repository root. Upload the **contents** of this package, not an extra enclosing `mallesh002-profile` folder. GitHub shows a profile README when the repository is public, has the same name as the account, and contains a nonempty root `README.md`.

The easiest route for the visual profile is **Add file → Upload files** in [your repository](https://github.com/mallesh002/mallesh002). Add `README.md` and the entire `assets/` folder, then commit to the default branch. Use `main` for this existing repository. The profile is then visible at [github.com/mallesh002](https://github.com/mallesh002).

For the complete package, copy these items into an existing clone and commit normally:

| Item | Purpose |
| --- | --- |
| `README.md` | Your public profile content |
| `assets/` | All banners, icons, the animation, and the initial GitHub snapshot |
| `scripts/` | Asset regeneration and public snapshot updates |
| `.github/workflows/profile-stats.yml` | Optional automatic snapshot refresh |
| `ATTRIBUTIONS.md` and `docs/simple-icons-LICENSE.md` | Icon source and license |
| `SETUP.md` and `preview.html` | These instructions and an offline visual preview |

If using an existing clone, copy only the package files you want to adopt, review the diff, and commit. Git history retains your prior README. There is no need to create another repository or delete the existing one.

Suggested repository description:

> Full stack developer focused on backend systems, MySQL performance, and practical AI integrations.

## 2. Add your public links

Project descriptions are based on your confirmed engineering work and use generic titles. They do not claim that company code is public. Missing URLs are deliberately kept in HTML comments so the profile renders cleanly without broken links. Replace the placeholder, then remove its surrounding comment wrapper to show the link.

| Placeholder in `README.md` | Replace with |
| --- | --- |
| `REPLACE_JOB_DISCOVERY_URL` | Public job-discovery repository or a shareable case study |
| `REPLACE_DATABASE_CASE_STUDY_URL` | Public database-performance repository or case study |
| `REPLACE_CAREER_WORKFLOWS_URL` | Public resume/interview project or case study |
| `REPLACE_LINKEDIN_URL` | Your complete LinkedIn profile URL |
| `REPLACE_PORTFOLIO_URL` | Your complete personal website URL |
| `REPLACE_PUBLIC_EMAIL` | The email address you choose to publish |

Keep any unknown entry commented out, or remove it. No experience totals, performance numbers, or unconfirmed contact details have been invented.

## 3. Optional: refresh the public GitHub snapshot

The README contains a collapsible snapshot with **real public repository data** collected on 9 September 2026. It is a local image, so it continues to display if an update fails. The snapshot counts owned public repositories, including forks, and groups them by GitHub's primary language metadata. Repositories with no primary language are labeled **Unclassified**. These figures exclude private work and are not a proficiency score or contribution graph.

To enable refreshes:

1. Commit `scripts/update_github_stats.py` and `.github/workflows/profile-stats.yml` on the repository's default branch.
2. Open **Actions → Refresh profile snapshot → Run workflow**. Select the default branch.
3. The workflow subsequently requests a refresh on Mondays at **04:23 UTC / 09:53 IST**. Scheduled runs may be delayed by GitHub and run only from the default branch.

The workflow uses GitHub's built-in `GITHUB_TOKEN` and declares `contents: write` to commit generated files. No personal access token, external hosting, or secret setup is required. Repository or organization policies can still restrict Actions or branch writes. If direct bot commits are blocked, refresh locally and commit through your normal PR process; this package does not bypass branch rules.

GitHub can disable scheduled workflows in public repositories after 60 days without repository activity. Re-enable the workflow from Actions if that occurs. A failed API request stops the workflow before its commit step; the previously committed snapshot remains visible. GitHub image caching can delay when a new image appears.

Manual refresh with **Python 3.10 or newer**, from the repository root:

```bash
python scripts/update_github_stats.py --username mallesh002
```

The script uses only Python's standard library. On systems where Python is named `python3`, substitute that command. Unauthenticated local requests are subject to GitHub API rate limits; an optional `GITHUB_TOKEN` environment variable is supported. Never paste a token into a file or commit it.

To keep the snapshot static, omit the workflow. To remove it entirely, delete the `details` block under **Public code** in the README. The rest of the design works independently.

## 4. Visual behavior and compatibility

| Element | Implementation and fallback |
| --- | --- |
| Hero | Original vector monogram and layered geometry, with desktop/mobile and light/dark SVGs |
| Introduction | Repository-hosted GIF; runs once in about 3.5 seconds and rests on the complete sentence |
| Reduced motion | `picture` selects `intro-static.svg` when the browser requests reduced motion; the GIF's first frame also contains the full sentence |
| Tech stack | Eight local Simple Icons-based tiles; wrap naturally and have light/dark variants |
| Snapshot | Locally generated SVGs plus readable JSON, refreshed only when the optional script/workflow runs |
| Theme fallback | Every `picture` includes a readable light-theme `img` fallback; the terminal has its own dark background |
| Narrow screens | Mobile artwork switches at a 600px viewport; body text and stack tiles use normal Markdown/HTML flow |

GitHub sanitizes README HTML, removing scripts, inline styles, and arbitrary classes. This README relies on Markdown and supported image/HTML markup. It does not use JavaScript, external CSS, iframes, inline SVG markup, or SVG scripts in the public README. SVGs are separate files referenced as images.

GitHub documents `picture` and `prefers-color-scheme` for theme-aware images. During creation, GitHub's Markdown API preserved the combined viewport/theme media queries and the reduced-motion source in a generic markup test. The finished profile was checked locally; it has not been rendered on a live GitHub profile. Media handling can vary in other Markdown viewers; the fallback images and alt text keep the content understandable. Theme and motion preferences ultimately depend on the viewer.

Open `preview.html` from the extracted package to inspect the layout in a browser. This is a local preview, not a published website; GitHub's exact fonts, spacing, image cache, and account appearance settings can differ. The preview stylesheet does not form part of your README.

## 5. Customize the artwork

SVG files remain editable as text. The main artwork and tech tiles can also be regenerated:

```bash
python -m pip install Pillow
python scripts/generate_assets.py --font /path/to/monospace-font.ttf
```

On Windows, a suitable example is:

```powershell
py -m pip install Pillow
py scripts/generate_assets.py --font "C:\Windows\Fonts\consola.ttf"
```

On Linux, the script defaults to DejaVu Sans Mono if installed. A font file is used only to rasterize the GIF; fonts are not downloaded at profile-view time. Regenerating static artwork does not update the GitHub snapshot.

Edit `PALETTES`, `hero()`, or the intro sentence in `scripts/generate_assets.py` to change the visual direction. Keep text in the same general length range, then preview at desktop and phone widths. `scripts/update_github_stats.py` has a matching independent palette for snapshot colors.

## Dependencies and sources

| Dependency | Used for | Runtime dependency for profile visitors? |
| --- | --- | --- |
| GitHub repository image hosting | All local profile images | Yes, the same host as the profile |
| GitHub REST API | Public snapshot refresh | No; only when generating a new snapshot |
| GitHub Actions | Optional weekly refresh | No |
| `actions/checkout` v7.0.1 | Workflow checkout, pinned to its verified commit | No |
| Simple Icons | Vendored technology symbols | No external requests; files and license included |
| Pillow and a local monospace font | Rebuilding the GIF | No; not needed for setup or weekly updates |

Compatibility references checked on **9 September 2026**:

- [GitHub profile README requirements](https://docs.github.com/en/account-and-profile/how-tos/profile-customization/managing-your-profile-readme)
- [GitHub Markup: sanitization pipeline](https://github.com/github/markup)
- [GitHub: theme-aware images with picture](https://github.blog/developer-skills/github/how-to-make-your-images-in-markdown-on-github-adjust-for-dark-mode-and-light-mode/)
- [GitHub attachment image formats, including GIF and SVG](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/attaching-files)
- [GitHub REST: public user repositories](https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user)
- [Scheduled workflows and limitations](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule)
- [Workflow disabling and enabling](https://docs.github.com/actions/managing-workflow-runs/disabling-and-enabling-a-workflow)
- [Pinned checkout release](https://github.com/actions/checkout/releases/tag/v7.0.1)
