from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app = FastAPI(title="AlphaFold Cookbook")


PAGE = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>AlphaFold Cookbook</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, system-ui, sans-serif; }
    body { margin: 0; min-height: 100vh; display: grid; place-items: center;
      background: radial-gradient(circle at top, #233876, #080b18 58%); color: #f7f8ff; }
    main { width: min(760px, calc(100% - 40px)); padding: 48px 0; }
    .label { color: #8ee7cf; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
    h1 { margin: 14px 0; font-size: clamp(2.5rem, 8vw, 5.5rem); line-height: .95; }
    p { max-width: 620px; color: #c9cee7; font-size: 1.15rem; line-height: 1.7; }
    .card { margin-top: 32px; padding: 22px; border: 1px solid #ffffff24; border-radius: 18px;
      background: #ffffff0d; backdrop-filter: blur(12px); }
    a { color: #8ee7cf; }
  </style>
</head>
<body>
  <main>
    <div class="label">AI2Learn · Cookbook #01</div>
    <h1>AlphaFold<br>Cookbook</h1>
    <p>You are the chef. AI is your sous-chef. Together, you will choose a verified protein sequence, explore its predicted shape, and plate it as a rotating 3D story.</p>
    <div class="card">
      <strong>The kitchen is warming up.</strong>
      <p>The complete step-by-step recipe is currently in development.</p>
      <a href="https://t.me/AlphaFoldCookbookBot">Meet the Telegram cookbook bot</a>
    </div>
  </main>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
@app.get("/alphafold-cookbook", response_class=HTMLResponse)
@app.get("/alphafold-cookbook/", response_class=HTMLResponse)
async def home() -> str:
    return PAGE


@app.get("/health")
@app.get("/alphafold-cookbook/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
