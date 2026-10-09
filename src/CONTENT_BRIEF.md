# CONTENT BRIEF — Sarasota Sewer Specialists (sewerlinerepairsarasotafl.com)

You are writing page content as JSON files. Do NOT browse the web — use only the facts in this brief.
Do NOT invent facts, numbers, names, or credentials. When unsure, write generally ("many homes", "often").

## Business constants
- Business name: **Sarasota Sewer Specialists**
- Domain (canonical): https://sewerlinerepairsarasotafl.com
- Phone: **(941) 555-0100** — PLACEHOLDER. Use exactly this string everywhere; tel links as `tel:+19415550100`.
- Address: **"Sarasota, FL" city-only**. NEVER invent a street address.

## Output
Write one JSON file per assigned page to the directory named in your task message,
e.g. `~/workspace/sarasota-site/content/services/trenchless-sewer-repair.json`.
Filenames must be exactly `<slug>.json`. Validate: every file must be parseable JSON.

## JSON schema (exact keys)
```json
{
  "slug": "trenchless-sewer-repair",
  "kind": "service",
  "url_path": "/services/trenchless-sewer-repair/",
  "title": "Trenchless Sewer Repair in Sarasota, FL | Sarasota Sewer Specialists",
  "meta": "Trenchless sewer repair in Sarasota, FL with minimal digging. Camera diagnosis, bursting & lining. Call (941) 555-0100.",
  "h1": "Trenchless Sewer Repair in Sarasota, FL",
  "eyebrow": "Sarasota, FL · No-Dig Sewer Repair",
  "hero_sub": "One or two sentences under the H1. Factual, no hype.",
  "sections": [
    {"h2": "Section Heading in Title Case", "html": "<p>Paragraph.</p><h3>Subsection in Title Case</h3><p>Paragraph.</p>"}
  ],
  "faqs": [
    {"q": "Sentence case question ending with ? for faq items only", "a": "<p>Answer, 40-80 words.</p>"}
  ],
  "zips": ["34236"],
  "area_label": "Downtown Sarasota",
  "date": "2026-10-09"
}
```
- `kind`: one of `service`, `location`, `blog`, `core`.
- `zips` / `area_label`: locations only (omit or null elsewhere). `date`: blog only.
- `sections[].html`: only `<p>`, `<h3>`, `<ul>`, `<ol>`, `<li>`, `<strong>`, `<a>` tags.
  Never put h1/h2 inside html. Blog bodies may include contextual links as
  `<a href="/services/trenchless-sewer-repair/">anchor text</a>` using paths from the URL map below.
- `title`: Title Case, include city + FL, keep under ~60 characters.
- `meta`: max **155 characters** (hard limit — count carefully), unique per page.
  Services, locations, and core (except blog hub/posts): include the phone number.
  Blog posts and blog hub: NO phone in meta.

## Heading rules
- h1, h2, h3, and `<title>`: **Title Case** — capitalize every major word;
  lowercase a/an/the/in/of/to/and/or/for/on/with unless first or last word.
- FAQ questions: **sentence case** ("How long does trenchless sewer repair take?").

## HARD RULES — violations fail the build
1. **Zero fabrication.** No license numbers, no certifications, no reviews/testimonials,
   no star ratings, no "years in business", no invented statistics (no percentages,
   no "500+ jobs completed" style counts). Use the verified Sarasota facts below only.
2. **No pricing anywhere.** Never mention dollars, costs, price ranges, or "free estimates".
3. **No contact forms.** The site is call-focused. Never mention filling out a form.
4. **No competitor names.** Do not name any local plumbing/sewer company.
5. **Do not claim Orangeburg pipe exists in Sarasota** (unverified). Do not cite
   species-specific root-intrusion studies. "Mature live oaks and ficus trees" phrasing is fine.
6. **No duplication.** Your pages must not repeat each other's sentences. Each location page
   needs distinct substance: different housing era, pipe materials, soil/water exposure,
   landmarks, and weather angle (see per-page angles in your task message).
7. No lorem ipsum, no `{{placeholders}}`, no "TBD"/"TODO".

## Word counts (body = hero_sub + sections text; FAQs do NOT count)
- Services: **≥1250 words** body. 6–8 FAQs.
- Locations: **≥950 words** body. 6–8 FAQs.
- Blog posts: **≥1350 words** body. 4–6 FAQs. Include 3–5 contextual internal links in body.
- Core pages: **≥650 words** body (homepage ≥800). 4–6 FAQs where natural
  (home, about, contact, services hub, locations hub); privacy/terms: no FAQs.
Aim 10–15% above minimums to be safe. Write 5–8 sections per page; use h3
subsections inside longer sections for depth.

## Sarasota facts (verified — weave in freely, do not contradict)
- Rainy season **June–September**; ~60% of 49–53 in annual rain falls then; August wettest (9.11 in).
- **Seasonally high water table 0–3.5 ft** across much of Sarasota County.
- **Myakka fine sand** (Florida's state soil) + EauGallie fine sand (poorly drained).
- Mechanism: saturated sandy soil loses support → **pipe bellies/sagging**; settling stresses
  joints → **joint separation**; high groundwater **infiltrates cracked laterals**.
- Housing eras → pipe materials:
  - 1920s–40s historic core (Laurel Park; Burns Court 1924–25 Mediterranean Revival bungalows;
    Rosemary District; Gillespie Park): clay tile + early cast-iron laterals.
  - 1950s–60s tracts (North Tamiami Trail corridor 34234; Southgate): cast-iron DWV, clay laterals; slab-on-grade begins.
  - **1960s–80s slab subdivisions (Gulf Gate, Bee Ridge): cast-iron DWV under slab + clay/cast-iron laterals = prime failure cohort.**
  - 1990s+ (Palmer Ranch, east of I-75): transitional to PVC/ABS.
  - 2000s+ (Lakewood Ranch): PVC, low failure risk.
- Failure modes: cast-iron corrosion and internal scale under slab, bellies, root intrusion
  from mature live oaks/ficus, joint separation after saturation.
- Landmarks: Siesta Key Beach (quartz sand), St. Armands Circle, Ringling Museum / Ca' d'Zan,
  Marie Selby Botanical Gardens, Myakka River State Park, Legacy Trail (18.5 mi),
  Sarasota Bay, Phillippi Creek, Whitaker Bayou, Sarasota National Cemetery (34241),
  Pinecraft Park (Amish enclave around Bahia Vista St; seasonal Dec–Mar),
  Historic Spanish Point (Osprey), Warm Mineral Springs (south county).
- Sarasota County septic-to-sewer program: Bee Ridge plant 12→18 MGD advanced treatment upgrade;
  Venice Gardens expansion slipped to ~2029; Florida 2030 septic deadline; North Port phase 1
  residential conversions by 2031; ~12,000+ Englewood-area homes on AIRVAC vacuum sewers
  (vacuum mains cannot be cut into like gravity mains — technical nuance).
- Storms: Irma (2017), Ian (2022), Debby (Aug 2024 — inland flooding incl. Bee Ridge),
  Helene & Milton (2024). Barrier islands (Siesta Key, Longboat Key) flood repeatedly.

## URL map (use these exact paths for contextual links)
Services: /services/trenchless-sewer-repair/ /services/pipe-bursting/
  /services/cipp-pipe-lining/ /services/sewer-camera-inspection/
  /services/sewer-line-replacement/ /services/tree-root-removal/
  /services/hydro-jetting/ /services/sewer-odor-detection/
  /services/emergency-sewer-repair/ /services/commercial-sewer-services/
  /services/septic-to-sewer-conversion/
Locations: /locations/downtown-sarasota-34236/ /locations/st-armands-lido-key/
  /locations/siesta-key-34242/ /locations/longboat-key-34228/
  /locations/gulf-gate-34231/ /locations/bee-ridge-34233/
  /locations/southgate-pinecraft-34239/ /locations/north-sarasota-34234/
  /locations/palmer-ranch-34238/ /locations/fruitville-34232/
  /locations/bradenton/ /locations/venice/ /locations/north-port/
  /locations/osprey-nokomis/
Blog: /blog/cast-iron-sewer-pipe-sarasota-slab-homes/
  /blog/rainy-season-sewer-backups-sarasota/
  /blog/trenchless-vs-traditional-sewer-repair/
  /blog/tree-roots-sewer-lines-sarasota/
  /blog/sewer-camera-inspection-what-to-expect/
  /blog/signs-sewer-line-failure/
  /blog/septic-to-sewer-conversion-sarasota-county/
  /blog/pipe-bursting-vs-pipe-lining/
  /blog/siesta-key-barrier-island-sewer-challenges/
  /blog/hydro-jetting-vs-snaking/
Core: / /services/ /locations/ /blog/ /about/ /contact/
  /privacy-policy/ /terms-of-service/

## Tone
Direct, expert, local. Short paragraphs. Teach the homeowner something real about
their pipes and their neighborhood on every page. No hype words ("best", "cheapest",
"#1"). Calls to action are simple: "Call (941) 555-0100".
