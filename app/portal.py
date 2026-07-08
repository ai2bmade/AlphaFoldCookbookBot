from html import escape


SECTIONS = [
    (
        "01",
        "Generative AI for Work",
        "Build practical AI workflows one clear step at a time.",
        [
            (1, "Custom GPTs", "Create focused ChatGPT assistants for repeatable work."),
            (2, "Gemini Gems", "Build reusable Gemini experts around your own instructions."),
            (3, "Claude Projects", "Organize context, files, and conversations for long-running work."),
            (4, "Claude Artifacts", "Turn ideas into interactive documents, tools, and prototypes."),
            (5, "Build Web Services with Claude Code", "Move from a small idea to a deployed web service."),
            (6, "Claude Cowork", "Collaborate with Claude across documents and everyday tasks."),
            (7, "Gemini Advanced & NotebookLM", "Connect Workspace tools and compare large collections of sources."),
            (8, "Business Research with Perplexity", "Create source-backed research briefs for real decisions."),
            (9, "Presentation Design with Claude", "Turn a text outline into a clean presentation structure."),
            (10, "Codex + VPS", "Build, deploy, and maintain a service on your own server."),
            (11, "OpenClaw", "Explore an open AI workflow through a guided practical build."),
            (12, "Hermes AI", "Learn a practical Hermes AI workflow from setup to result."),
            (13, "Build a Slack Bot", "Create a useful team bot and connect it to a real workspace."),
            (14, "Build a Discord Bot", "Create, run, and improve a community assistant."),
            (15, "Google Sheets + Gemini Dashboard", "Turn spreadsheet data into an AI-assisted dashboard."),
        ],
    ),
    (
        "02",
        "Design & UI/UX",
        "Create clearer interfaces and visual assets with modern design tools.",
        [
            (16, "Figma", "Design a polished interface from frame to clickable prototype."),
            (17, "Photoshop Generative Fill", "Remove backgrounds, extend scenes, and composite objects faster."),
            (18, "Illustrator: Logos & Brand Graphics", "Build clean vector icons, logos, and print-ready graphics."),
            (19, "Ideogram AI Masterclass", "Generate typography-led logos and brand mockups with readable text."),
            (20, "Premiere Pro Practical Editing", "Edit, mix, and color a complete promotional video."),
            (21, "Data-Driven UX", "Use evidence and user behavior to improve an interface."),
        ],
    ),
    (
        "03",
        "Languages",
        "Practice small, repeatable language skills with immediate feedback.",
        [
            (22, "English Dictation", "Train listening accuracy with short, progressive dictation sessions."),
            (23, "English Vocabulary", "Build a personal vocabulary system that supports real recall."),
            (24, "Spanish", "Complete your first practical Spanish conversation step by step."),
            (25, "Arabic", "Learn the foundations needed for a first guided Arabic exchange."),
            (26, "Russian", "Build a small but usable foundation in Russian."),
        ],
    ),
    (
        "04",
        "Data Literacy & Marketing Tech",
        "Turn data into answers, dashboards, and measurable growth workflows.",
        [
            (27, "Python", "Use Python to automate one practical data task from start to finish."),
            (28, "SQL Fundamentals", "Write your own PostgreSQL and MySQL queries for business metrics."),
            (29, "Google Analytics 4", "Trace acquisition, identify drop-off, and measure campaign results."),
            (30, "Google Looker Studio", "Connect messy source data to a clear live dashboard."),
            (31, "Tableau Fundamentals", "Design a decision-ready dashboard from raw data."),
            (32, "Google Tag Manager", "Configure tracking events without editing production code each time."),
            (33, "SEO, GEO & AEO", "Make content discoverable across search and AI answer engines."),
            (34, "n8n", "Build a reliable no-code automation across multiple services."),
            (35, "Notion", "Create a practical workspace for knowledge, projects, and repeatable systems."),
        ],
    ),
    (
        "05",
        "Foundations & Science",
        "Make difficult subjects approachable through small, observable results.",
        [
            (36, "AlphaFold", "Explore protein structure prediction and create a 3D protein story."),
            (37, "Calculus", "Build an intuitive foundation through one complete visual problem."),
            (38, "Basic Physics", "Connect a simple physical observation to a working model."),
            (39, "Basic Chemistry", "Complete a safe, visual introduction to chemical reasoning."),
            (40, "Basic Electricity", "Build and understand a first simple circuit."),
        ],
    ),
]


def render_course(number: int, title: str, description: str) -> str:
    active = number == 36
    tag = "Available" if active else "Planned"
    card_class = "course active" if active else "course"
    content = f"""
      <div class="course-top">
        <span class="course-status">{tag}</span>
      </div>
      <h3>{escape(title)}</h3>
      <p>{escape(description)}</p>
      <span class="course-action">{"Open cookbook →" if active else "Coming step by step"}</span>
    """
    if active:
        return f'<a class="{card_class}" href="/alphafold-cookbook">{content}</a>'
    return f'<article class="{card_class}">{content}</article>'


def render_portal() -> str:
    nav = "".join(
        f'<a href="#section-{number}">{number}</a>' for number, _, _, _ in SECTIONS
    )
    sections = "".join(
        f"""
        <section id="section-{number}" class="catalog-section">
          <div class="section-intro">
            <span>{number}</span>
            <div><h2>{escape(title)}</h2><p>{escape(description)}</p></div>
          </div>
          <div class="course-grid">
            {''.join(render_course(*course) for course in courses)}
          </div>
        </section>
        """
        for number, title, description, courses in SECTIONS
    )

    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="AI2Learn Cookbooks: practical, step-by-step foundations for learning with AI.">
  <title>AI2Learn Cookbooks</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; background: #05070b; color: #f5f7fb; }}
    a {{ color: inherit; }}
    .shell {{ width: min(1180px, calc(100% - 36px)); margin: 0 auto; }}
    .topbar {{ position: sticky; top: 0; z-index: 20; border-bottom: 1px solid #202a37;
      background: #05070be8; backdrop-filter: blur(18px); }}
    .topbar-inner {{ min-height: 68px; display: flex; align-items: center; justify-content: space-between; gap: 24px; }}
    .logo {{ font-weight: 900; letter-spacing: -.04em; text-decoration: none; font-size: 1.25rem; }}
    .logo span {{ color: #1ed7f2; }}
    nav {{ display: flex; gap: 8px; }}
    nav a {{ width: 34px; height: 34px; display: grid; place-items: center; border: 1px solid #263343;
      border-radius: 10px; color: #9bacc0; text-decoration: none; font-size: .78rem; }}
    nav a:hover {{ color: #fff; border-color: #1ed7f2; }}
    .hero {{ padding: clamp(72px, 12vw, 150px) 0 80px; border-bottom: 1px solid #18222f;
      background: radial-gradient(circle at 72% 20%, #103c596b, transparent 34%),
                  radial-gradient(circle at 18% 16%, #17295770, transparent 32%); }}
    .eyebrow {{ color: #1ed7f2; font-weight: 800; text-transform: uppercase; letter-spacing: .15em; font-size: .75rem; }}
    h1 {{ max-width: 920px; margin: 18px 0 26px; font-size: clamp(3rem, 8vw, 7.6rem);
      line-height: .91; letter-spacing: -.07em; }}
    .hero-copy {{ max-width: 720px; margin: 0; color: #aebdce; font-size: clamp(1.05rem, 2vw, 1.35rem); line-height: 1.65; }}
    .hero-meta {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 38px; }}
    .hero-meta span {{ padding: 9px 13px; border: 1px solid #28384a; border-radius: 999px; color: #b8c5d3; font-size: .84rem; }}
    .catalog {{ padding: 28px 0 100px; }}
    .catalog-section {{ scroll-margin-top: 92px; padding: 72px 0; border-bottom: 1px solid #18222f; }}
    .section-intro {{ display: grid; grid-template-columns: 70px 1fr; gap: 18px; margin-bottom: 30px; }}
    .section-intro > span {{ color: #1ed7f2; font: 800 1rem/1 ui-monospace, monospace; padding-top: 9px; }}
    h2 {{ margin: 0; font-size: clamp(2rem, 4vw, 3.7rem); letter-spacing: -.045em; }}
    .section-intro p {{ margin: 10px 0 0; color: #8496aa; font-size: 1rem; }}
    .course-grid {{ display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 14px; }}
    .course {{ min-height: 250px; display: flex; flex-direction: column; padding: 22px; border: 1px solid #1d2a39;
      border-radius: 17px; background: linear-gradient(145deg, #0b1119, #080c12); text-decoration: none;
      transition: transform .2s ease, border-color .2s ease, background .2s ease; }}
    .course.active {{ border-color: #1ed7f280; background: linear-gradient(145deg, #0c2029, #091018); }}
    .course.active:hover {{ transform: translateY(-4px); border-color: #1ed7f2; }}
    .course-top {{ display: flex; justify-content: flex-end; gap: 12px; }}
    .course-status {{ color: #65768a; font-size: .7rem; text-transform: uppercase; letter-spacing: .1em; }}
    .active .course-status {{ color: #51e7c2; }}
    .course h3 {{ margin: 40px 0 10px; font-size: 1.24rem; line-height: 1.2; letter-spacing: -.02em; }}
    .course p {{ margin: 0; color: #8293a7; line-height: 1.55; font-size: .91rem; }}
    .course-action {{ margin-top: auto; padding-top: 24px; color: #637488; font-size: .82rem; }}
    .active .course-action {{ color: #1ed7f2; font-weight: 750; }}
    footer {{ padding: 36px 0 56px; color: #718399; font-size: .88rem; }}
    @media (max-width: 900px) {{ .course-grid {{ grid-template-columns: repeat(2, 1fr); }} }}
    @media (max-width: 620px) {{
      .shell {{ width: min(100% - 24px, 1180px); }}
      .topbar-inner {{ min-height: 60px; }} nav {{ gap: 5px; }} nav a {{ width: 30px; height: 30px; }}
      .hero {{ padding: 70px 0 58px; }}
      .section-intro {{ grid-template-columns: 1fr; gap: 6px; }}
      .section-intro > span {{ padding: 0; }}
      .course-grid {{ grid-template-columns: 1fr; }}
      .course {{ min-height: 220px; }}
    }}
  </style>
</head>
<body>
  <header class="topbar"><div class="shell topbar-inner">
    <a class="logo" href="/">AI2<span>Learn</span></a><nav aria-label="Cookbook sections">{nav}</nav>
  </div></header>
  <main>
    <section class="hero"><div class="shell">
      <div class="eyebrow">AI2Learn Cookbook Portal</div>
      <h1>Start small.<br>Go further.</h1>
      <p class="hero-copy">Practical, step-by-step foundations designed to help complete beginners finish something real—and build the confidence to continue on their own.</p>
      <div class="hero-meta"><span>40 planned cookbooks</span><span>5 learning paths</span><span>1 available now</span></div>
    </div></section>
    <div class="shell catalog">{sections}</div>
  </main>
  <footer><div class="shell">AI2Learn Cookbook · Step-by-step foundations for going further on your own.</div></footer>
</body>
</html>"""
