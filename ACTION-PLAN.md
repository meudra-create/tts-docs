# SEO Action Plan — ndjonisango.com
**Generated:** 2026-05-21 | **Health Score:** 58/100 | **Target:** 75+/100

---

## 🔴 CRITICAL — Fix Immediately

### C1 · Fix Homepage Title Duplication
**Issue:** "…Centrafrique **Centrafrique**…" — the keyword appears twice, wasting characters and looking spammy to Google.  
**Fix:** In AIOSEO → Search Appearance → Homepage → Title, update to:
```
Ndjoni Sango — Actualités de Centrafrique | Presse RCA
```
**Effort:** 5 min | **Impact:** On-Page SEO, CTR

---

### C2 · Fix Category Sitemap lastmod Dates
**Issue:** 40 of 41 category pages in `category-sitemap.xml` show `1970-01-01` (Unix epoch zero), telling Google these pages have never been updated.  
**Fix:**
1. Update AIOSEO to latest version (this is a known bug)
2. If bug persists: AIOSEO → Sitemaps → Additional Pages → manually exclude categories with no value, or use the AIOSEO API to force-regenerate lastmod
3. Alternative: Use Yoast SEO's sitemap module if AIOSEO doesn't fix this

**Effort:** 30 min | **Impact:** Technical SEO, crawl budget

---

### C3 · Change Article Schema: BlogPosting → NewsArticle
**Issue:** Using `BlogPosting` instead of `NewsArticle` makes articles ineligible for Google News and Top Stories carousel.  
**Fix:** AIOSEO → Search Appearance → Content Types → Posts → Schema tab → change type to **News Article**  
**Effort:** 10 min | **Impact:** Schema, Google News eligibility, rich results

---

### C4 · Fix 45+ Empty Alt Text on Homepage Images
**Issue:** 45 images have `alt=""` on the homepage. This is an accessibility violation and prevents Google Image Search from indexing these images.  
**Fix:**
1. In WordPress Media Library, add descriptive French alt text to all article thumbnail images
2. In AIOSEO or theme settings, ensure article featured images inherit the image caption/description as alt text
3. Fix logo alt text in Appearance → Customize → Site Identity

**Effort:** 2–4 hours (bulk) | **Impact:** Images score, Google Images traffic, accessibility

---

### C5 · Remove Duplicate AdSense Script Loads
**Issue:** `adsbygoogle.js` is loaded 5 times on the homepage, causing significant performance drag.  
**Fix:** In your ad implementation code, load the AdSense library once in `<head>` via a single `<script async src="...adsbygoogle.js">` and configure all ad units without re-loading the script.  
**Effort:** 1–2 hours (developer) | **Impact:** Performance, LCP, INP

---

## 🟠 HIGH — Fix Within 1 Week

### H1 · Add Security Headers
**Fix:** Add to Apache `.htaccess`:
```apache
Header always set X-Content-Type-Options "nosniff"
Header always set X-Frame-Options "SAMEORIGIN"
Header always set Referrer-Policy "strict-origin-when-cross-origin"
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
```
**Effort:** 15 min | **Impact:** Technical SEO, security trust signals

---

### H2 · Exclude Stale WooCommerce Pages from Sitemap
**Issue:** `/panier/`, `/commande/`, `/boutique/`, `/mon-compte/`, `/sample-page/` are in the sitemap but unused since 2020. They dilute crawl budget.  
**Fix:** AIOSEO → Sitemaps → Additional Pages → exclude these URLs, or set them to `noindex` if they can't be removed  
**Effort:** 15 min | **Impact:** Crawl budget, thin content

---

### H3 · Fix Homepage og:type and Add og:image
**Issue:** Homepage uses `og:type = article` (should be `website`) and has no `og:image`.  
**Fix:** AIOSEO → Search Appearance → Social → Facebook → set homepage OG type to `website` and upload a default OG image (1200×630px)  
**Effort:** 20 min | **Impact:** Social sharing CTR

---

### H4 · Fix Duplicate BreadcrumbList Schema
**Issue:** Both AIOSEO and the Newspaper theme are emitting `BreadcrumbList` schema on article pages.  
**Fix:** In the Newspaper theme settings, disable structured data/schema output (AIOSEO should be the sole source)  
**Effort:** 15 min | **Impact:** Schema validation

---

### H5 · Rename Cyrillic Image Filenames
**Issue:** Images uploaded from Russian sources retain Cyrillic filenames (e.g., `СВЛ_СиБиЭс.jpg`). Google cannot read these as keyword signals.  
**Fix:** Before uploading images, rename to descriptive French slugs. For existing images: if the URLs are not widely linked, replace the files and update references. Use a regex in the database or the WordPress Media Library.  
**Effort:** Ongoing process | **Impact:** Image SEO, keyword signals

---

### H6 · Reduce JavaScript Load
**Fix:**
1. Remove `jquery-migrate.min.js` if no plugins require it (test first)
2. Defer non-critical Google Site Kit event provider scripts
3. Self-host Google Fonts or use `font-display: swap` + preconnect
4. Audit Google Site Kit — remove unused integrations (OptinMonster, WPForms if not in use)

**Effort:** 2–3 hours | **Impact:** LCP, INP, overall PageSpeed score

---

## 🟡 MEDIUM — Fix Within 1 Month

### M1 · Create Individual Author Profiles
**Issue:** All articles use generic "Ndjoni Sango" account, severely hurting E-E-A-T signals.  
**Fix:**
1. Create individual WordPress user accounts for each journalist
2. Add bio, photo, location, and social media links to author profiles
3. Link author profiles to their LinkedIn/Twitter with `rel="me"`
4. In AIOSEO author schema, add `sameAs` properties pointing to professional profiles

**Effort:** 4–8 hours | **Impact:** E-E-A-T, content quality scoring, author rich results

---

### M2 · Add NewsMediaOrganization Schema
**Fix:** Add a `NewsMediaOrganization` JSON-LD block to the homepage:
```json
{
  "@context": "https://schema.org",
  "@type": "NewsMediaOrganization",
  "name": "Ndjoni Sango",
  "url": "https://ndjonisango.com/",
  "logo": "https://ndjonisango.com/wp-content/uploads/2025/02/Logo-Ndjoni-Sango.png",
  "foundingDate": "2017",
  "areaServed": "CF",
  "publishingPrinciples": "https://ndjonisango.com/mentions-legales/",
  "sameAs": ["https://www.facebook.com/ndjonisango", "https://twitter.com/ndjonisango"]
}
```
**Effort:** 30 min | **Impact:** Google News trust, E-E-A-T

---

### M3 · Improve llms.txt for AI Citation
**Issue:** The current `llms.txt` is a basic auto-generated list of articles.  
**Fix:** Manually enhance `llms.txt` with:
- Editorial mission statement
- Coverage areas (RCA politics, security, development, Africa)
- Editorial team description
- Key recurring topics/series

**Effort:** 1 hour | **Impact:** AI Search Readiness, ChatGPT/Perplexity citations

---

### M4 · Audit and Noindex Low-Value Tag Pages
**Issue:** 9 tag sitemaps suggest hundreds of tag archive pages. Many may be thin with 1–3 articles.  
**Fix:** Audit tag pages by article count. Noindex tags with fewer than 5 articles using AIOSEO → Sitemaps → Taxonomies → Tags → Exclude thin ones  
**Effort:** 2 hours | **Impact:** Crawl budget, thin content, overall site quality

---

### M5 · Add About/Editorial Page
**Fix:** Create a `/equipe/` or `/a-propos/` page with:
- Newsroom history and mission
- Editorial team with photos and bios
- Contact information for press inquiries
- Editorial standards / code of ethics

**Effort:** 4 hours | **Impact:** E-E-A-T, trust signals, backlink acquisition

---

### M6 · Implement Image SEO Best Practices
**Fix:**
1. Always add descriptive French alt text in Media Library before inserting images
2. Use descriptive French/English filenames: `touadera-president-centrafrique-2026.jpg`
3. Add `width` and `height` attributes to all `<img>` tags to prevent CLS
4. Consider converting images to WebP format

**Effort:** Ongoing | **Impact:** Images, CLS, Google Images

---

## 🟢 LOW — Backlog

### L1 · Run PageSpeed Insights and Fix Core Web Vitals
Run https://pagespeed.web.dev/?url=https://ndjonisango.com/ and address LCP, INP, and CLS scores. Target: all three in the "Good" range.

### L2 · Build Backlinks from Regional Sources
- Submit to African media directories
- Register on AllAfrica.com, Africanews partner lists
- Reach out to French-language Wikipedia for citations
- Submit press releases to wire services that link back

### L3 · Create a Pillar Content Strategy
Consider creating long-form pillar articles for key topics (e.g., "Situation politique en RCA en 2026") that aggregate coverage and attract editorial links.

### L4 · Configure Google Search Console
Set up GSC to monitor indexation, Core Web Vitals field data, and search performance. This enables the `seo-google` subagent to provide real field data in future audits.

### L5 · Configure HREFLANG (if multilingual expansion planned)
If ndjonisango.com ever adds Sango-language or Lingala-language content, implement `hreflang` tags from the start.

### L6 · Implement IndexNow
With active daily publishing, implementing IndexNow would push new articles to Bing and other IndexNow-compatible search engines immediately upon publication. WordPress plugin available.

---

## Implementation Roadmap

| Week | Actions |
|------|---------|
| **Week 1** | C1, C2, C3, C4, C5, H1, H2, H3, H4 |
| **Week 2** | H5, H6, M1 (start author profiles) |
| **Week 3** | M2, M3, M4, M5 |
| **Week 4** | M6 (ongoing), L1 (PageSpeed review) |
| **Month 2+** | L2 (backlinks), L3 (pillar content), L4, L6 |

---

*Action plan generated by Claude SEO v1.9.0 | 2026-05-21*
