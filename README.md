# ONE — AI Research Agent

**Tagline:** One Idea. A Complete Research Paper.  
**Built with:** Python, Streamlit, configurable AI API, DOCX/PDF/LaTeX exports.

ONE is a light-themed research-workspace starter app. Enter one idea to create an editable structured draft, save projects locally, ask the contextual assistant for help, and export DOCX, PDF, LaTeX, or a ZIP package.

## Important scope note

This repository is a working starter/MVP, not a guarantee of publication readiness. Demo Mode produces an explicitly labelled illustrative draft and does not conduct live scholarly searches. API Mode drafts from the configured model but does not automatically make its citations or claims true. The current reference verifier is intentionally conservative; verify sources and research claims independently before academic use. The app does not fabricate empirical results by design.

## Run locally

Python 3.10+ recommended.

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
streamlit run app.py
```

## Configure API mode

Create `.streamlit/secrets.toml` locally (never commit it):

```toml
OPENAI_API_KEY = "replace-with-your-key"
OPENAI_MODEL = "gpt-4.1-mini"
OPENAI_BASE_URL = "https://api.openai.com/v1"
```

Use a model available to your account. API Mode uses the OpenAI-compatible chat completions endpoint. The key is read server-side. Do not paste secrets into chat, manuscript text, or public repositories.

For Streamlit Community Cloud, add the same values in **App → Settings → Secrets**. The included `.streamlit/secrets.toml.example` is a template only.

## Features

- Premium white, ivory, navy, and sea-green light theme.
- One-idea manuscript generation flow.
- Demo Mode and configurable API Mode.
- Local SQLite project saving.
- Editable Markdown manuscript.
- Contextual chatbot popup.
- DOCX, PDF, LaTeX, and ZIP exports.
- Source notes and a human review checklist.

## Current limitations

- Scholarly web discovery and source metadata verification are not yet integrated; add an authorized scholarly API layer before claiming sources are verified.
- PDF export uses a basic text-oriented renderer. Complex equations, figures, and tables may need LaTeX compilation or a more advanced document conversion pipeline.
- The chatbot is a contextual helper, not an autonomous agent that can safely perform every research task.
- Authentication is not included. Do not deploy confidential multi-user research without adding authentication, authorization, and appropriate storage.
- SQLite is suitable for a starter/single-instance deployment; production multi-user deployments should use managed persistent storage.
- LaTeX is exported as source; compilation is not run on the server.

## Deployment

1. Push the project to a GitHub repository.
2. In Streamlit Community Cloud, create an app from that repository.
3. Set the main file to `app.py`.
4. Add secrets in the deployment settings.
5. Deploy and test generation and each export.

## Academic integrity

Always review the manuscript. Verify references, claims, methods, permissions, and applicable ethics requirements. Never represent illustrative content as experimental findings. ONE does not guarantee plagiarism-free output, journal acceptance, or compliance with every publisher.

## License

See [LICENSE](LICENSE). This project uses the MIT License.
