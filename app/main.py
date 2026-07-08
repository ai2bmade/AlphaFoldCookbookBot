from pathlib import Path

import markdown
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles


BASE_DIR = Path(__file__).resolve().parent.parent
CONTENT_FILE = BASE_DIR / "content" / "section-01-introduction.md"

app = FastAPI(title="AlphaFold Cookbook")
app.mount("/assets", StaticFiles(directory=BASE_DIR / "assets"), name="assets")
app.mount(
    "/alphafold-cookbook/assets",
    StaticFiles(directory=BASE_DIR / "assets"),
    name="cookbook-assets",
)


def render_page() -> str:
    source = CONTENT_FILE.read_text(encoding="utf-8")
    body = markdown.markdown(
        source,
        extensions=["fenced_code", "sane_lists"],
        output_format="html5",
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="An AI-assisted beginner's cookbook for exploring AlphaFold and protein structure prediction.">
  <title>AlphaFold Cookbook · Section 1</title>
  <style>
    :root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{ margin: 0; background: #070b12; color: #eef3f9; line-height: 1.75; }}
    .topbar {{ position: sticky; top: 0; z-index: 10; display: flex; align-items: center;
      justify-content: space-between; gap: 20px; padding: 14px max(20px, calc((100vw - 1040px) / 2));
      border-bottom: 1px solid #263344; background: #070b12e8; backdrop-filter: blur(16px); }}
    .brand {{ color: #fff; font-weight: 850; letter-spacing: -.02em; text-decoration: none; }}
    .brand span {{ color: #13c9ed; }}
    .status {{ color: #8da0b5; font-size: .86rem; }}
    main {{ width: min(100% - 32px, 1040px); margin: 0 auto; padding: 34px 0 96px; }}
    article {{ width: min(100%, 840px); margin: 0 auto; }}
    article > p:first-child {{ width: min(100vw - 32px, 1120px); margin: 0 50% 52px;
      transform: translateX(-50%); }}
    article > p:first-child img {{ aspect-ratio: 16 / 9; object-fit: cover; border: 1px solid #233244; }}
    h1 {{ margin: 0 0 28px; font-size: clamp(2rem, 5vw, 4rem); line-height: 1.08; letter-spacing: -.045em; }}
    h3 {{ margin: 56px 0 18px; color: #fff; font-size: clamp(1.35rem, 3vw, 2rem); line-height: 1.25; }}
    p {{ color: #bdc9d6; font-size: clamp(1rem, 1.8vw, 1.13rem); }}
    strong {{ color: #fff; }}
    em {{ color: #8feafa; }}
    hr {{ margin: 44px 0; border: 0; border-top: 1px solid #263344; }}
    img {{ display: block; width: 100%; height: auto; margin: 30px 0 42px; border-radius: 16px;
      box-shadow: 0 18px 55px #0009; }}
    pre {{ overflow-x: auto; margin: 24px 0 30px; padding: 22px; border: 1px solid #24384c;
      border-radius: 14px; background: #0d1621; color: #9de8f3; line-height: 1.55; }}
    code {{ font-family: "Cascadia Code", "SFMono-Regular", Consolas, monospace; }}
    .footer {{ margin-top: 64px; padding-top: 22px; border-top: 1px solid #263344;
      color: #74879a; font-size: .9rem; }}
    @media (max-width: 640px) {{
      .status {{ display: none; }}
      main {{ width: min(100% - 24px, 1040px); padding-top: 18px; }}
      article > p:first-child {{ width: calc(100vw - 24px); margin-bottom: 34px; }}
      img {{ border-radius: 10px; margin-block: 22px 32px; }}
      pre {{ padding: 16px; font-size: .78rem; }}
    }}
  </style>
</head>
<body>
  <header class="topbar">
    <a class="brand" href="/alphafold-cookbook">AlphaFold <span>Cookbook</span></a>
    <div class="status">Cookbook #01 · Section 1</div>
  </header>
  <main>
    <article>{body}</article>
    <div class="footer">AI2Learn Cookbook · Learn by cooking with AI.</div>
  </main>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
@app.get("/alphafold-cookbook", response_class=HTMLResponse)
@app.get("/alphafold-cookbook/", response_class=HTMLResponse)
async def home() -> str:
    return render_page()


@app.get("/health")
@app.get("/alphafold-cookbook/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
