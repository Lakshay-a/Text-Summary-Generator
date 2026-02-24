from fastapi import FastAPI
import uvicorn
import os
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from textSummaryGenerator.pipeline.prediction import PredictionPipeline

text:str = "What is Text Summarization?"

app = FastAPI()

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Text Summary Generator</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>

<body class="min-h-screen bg-slate-950 text-slate-100">
  <!-- Background glow -->
  <div class="pointer-events-none fixed inset-0 overflow-hidden">
    <div class="absolute -top-40 left-1/2 h-[520px] w-[520px] -translate-x-1/2 rounded-full bg-indigo-500/20 blur-3xl"></div>
    <div class="absolute -bottom-40 right-10 h-[520px] w-[520px] rounded-full bg-fuchsia-500/10 blur-3xl"></div>
  </div>

  <main class="relative mx-auto max-w-5xl px-4 py-10">
    <!-- Top bar -->
    <div class="flex items-center justify-between">
      <div class="flex items-center gap-3">
        <div class="grid h-10 w-10 place-items-center rounded-2xl bg-white/10 ring-1 ring-white/10">
          <span class="text-lg">✦</span>
        </div>
        <div>
          <div class="text-sm text-slate-300">Text Summary Generator</div>
        </div>
      </div>

    </div>

    <!-- Hero -->
    <section class="mt-10">
      <h1 class="text-4xl sm:text-5xl font-semibold tracking-tight">
        Summarize text in seconds.
      </h1>
      <p class="mt-3 max-w-2xl text-slate-300">
        Paste any paragraph, article, or notes — the model will generate a concise summary.
      </p>
    </section>

    <!-- Content -->
    <section class="mt-8 grid gap-6 lg:grid-cols-2">
      <!-- Input card -->
      <div class="rounded-3xl bg-white/5 ring-1 ring-white/10 p-6 shadow-xl">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold">Input</h2>
          <span id="counter" class="text-xs text-slate-400">0 chars</span>
        </div>

        <textarea id="inputText"
          class="mt-3 w-full min-h-[260px] rounded-2xl bg-slate-950/60 ring-1 ring-white/10 p-4
                 placeholder:text-slate-500 focus:outline-none focus:ring-2 focus:ring-indigo-400/60"
          placeholder="Paste text here… (e.g., a job description, article, or notes)"
        ></textarea>

        <div class="mt-4 flex flex-wrap gap-3">
          <button id="summarizeBtn" onclick="generateSummary()"
            class="inline-flex items-center justify-center gap-2 rounded-2xl bg-white px-5 py-3
                   text-sm font-semibold text-slate-900 hover:bg-slate-200 transition">
            <span>Generate Summary</span>
            <span class="text-base">→</span>
          </button>

          <button onclick="fillExample()"
            class="rounded-2xl bg-white/5 px-5 py-3 text-sm ring-1 ring-white/10 hover:bg-white/10 transition">
            Use example
          </button>

          <button onclick="clearAll()"
            class="rounded-2xl bg-white/5 px-5 py-3 text-sm ring-1 ring-white/10 hover:bg-white/10 transition">
            Clear
          </button>
        </div>

        <div id="errorBox"
             class="hidden mt-4 rounded-2xl border border-red-500/30 bg-red-500/10 p-3 text-sm text-red-200">
        </div>
      </div>

      <!-- Output card -->
      <div class="rounded-3xl bg-white/5 ring-1 ring-white/10 p-6 shadow-xl">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-semibold">Summary</h2>
          <div class="flex items-center gap-2">
            <button id="copyBtn" onclick="copySummary()"
              class="rounded-xl bg-white/5 px-3 py-2 text-xs ring-1 ring-white/10 hover:bg-white/10 transition">
              Copy
            </button>
          </div>
        </div>

        <div class="mt-3 rounded-2xl bg-slate-950/60 ring-1 ring-white/10 p-4 min-h-[260px]">
          <div id="statusRow" class="hidden mb-3 text-xs text-slate-400">
            <span class="inline-flex items-center gap-2">
              <span class="h-2 w-2 rounded-full bg-indigo-400 animate-pulse"></span>
              Generating summary…
            </span>
          </div>
          <p id="summaryBox" class="whitespace-pre-wrap text-slate-200">
            Your summary will appear here.
          </p>
        </div>

        
      </div>
    </section>

  </main>

  <script>
    const inputEl = document.getElementById("inputText");
    const counter = document.getElementById("counter");
    const statusRow = document.getElementById("statusRow");
    const summaryBox = document.getElementById("summaryBox");
    const errorBox = document.getElementById("errorBox");
    const summarizeBtn = document.getElementById("summarizeBtn");
    const copyBtn = document.getElementById("copyBtn");

    function setLoading(isLoading) {
      statusRow.classList.toggle("hidden", !isLoading);
      summarizeBtn.disabled = isLoading;
      summarizeBtn.classList.toggle("opacity-60", isLoading);
      summarizeBtn.classList.toggle("cursor-not-allowed", isLoading);
    }

    function showError(msg) {
      errorBox.textContent = msg;
      errorBox.classList.remove("hidden");
    }

    function clearError() {
      errorBox.classList.add("hidden");
      errorBox.textContent = "";
    }

    inputEl.addEventListener("input", () => {
      counter.textContent = `${inputEl.value.length} chars`;
      if (inputEl.value.trim().length > 0) clearError();
    });

    function fillExample() {
      inputEl.value =
`Eric: MACHINE!
Rob: That's so gr8!
Eric: I know! And shows how Americans see Russian ;)
Rob: And it's really funny!
Eric: I know! I especially like the train part!
Rob: Hahaha! No one talks to the machine like that!
Eric: Is this his only stand-up?
Rob: Idk. I'll check.
Eric: Sure.
Rob: Turns out no! There are some of his stand-ups on youtube.
Eric: Gr8! I'll watch them now!
Rob: Me too!
Eric: MACHINE!
Rob: MACHINE!
Eric: TTYL?
Rob: Sure :)`;
      counter.textContent = `${inputEl.value.length} chars`;
      clearError();
    }

    function clearAll() {
      inputEl.value = "";
      counter.textContent = "0 chars";
      summaryBox.textContent = "Your summary will appear here.";
      clearError();
    }

    async function generateSummary() {
      clearError();
      const text = inputEl.value.trim();
      if (!text) {
        showError("Please paste some text to summarize.");
        return;
      }

      setLoading(true);
      summaryBox.textContent = "";

      try {
        // Calling your existing endpoint: POST /predict?text=...
        const res = await fetch("/predict?text=" + encodeURIComponent(text), { method: "POST" });

        if (!res.ok) {
          const raw = await res.text();
          throw new Error(raw || `Request failed (${res.status})`);
        }

        const data = await res.json();
        summaryBox.textContent = data.summary ?? "No summary returned.";
      } catch (err) {
        showError("Error: " + (err?.message || err));
        summaryBox.textContent = "Your summary will appear here.";
      } finally {
        setLoading(false);
      }
    }

    async function copySummary() {
      const text = summaryBox.textContent || "";
      if (!text.trim() || text.includes("Your summary will appear")) return;

      try {
        await navigator.clipboard.writeText(text);
        copyBtn.textContent = "Copied!";
        setTimeout(() => copyBtn.textContent = "Copy", 900);
      } catch (e) {
        copyBtn.textContent = "Failed";
        setTimeout(() => copyBtn.textContent = "Copy", 900);
      }
    }
  </script>
</body>
</html>
    """

@app.get('/train')
async def training():
    try:
        os.system("python main.py")
        return Response("Training successful!!")
    except Exception as e:
        return Response(f"Error occurred during training: {str(e)}")
    
@app.post('/predict')
async def predict_route(text: str):
    try:
        obj = PredictionPipeline()
        summary = obj.predict(text)
        return {"summary": summary}
    except Exception as e:
        raise e
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
