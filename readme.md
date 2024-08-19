## Quick-Start 🚀

Note: To begin, you'll need an API key from [Gemini](https://ai.google.dev/gemini-api/docs/api-key?hl=zh-tw).

### Development Mode

- Note: In Dev mode, the default config with backend is **SQLite**.

1. Clone Repo:

```
git clone https://github.com/timmy0123/GeogptProject-back.git
```

2.  Configure Virtual Environment (Recommended):
    <details>
      
       * Create Virtual Environment
       
         ```
         # macOS/Linux
         # You may need to run `sudo apt-get install python3-venv` first on Debian-based OSs
         python3 -m venv .venv
         
         # Windows
         # You can also use `py -3 -m venv .venv`
         python -m venv .venv
         ```

    - Activate the virtual environment:
      ``` # macOS/Linux
      source .venv/bin/activate
           # Windows
           .venv\Scripts\activate
           ```
      </details>


3.  Install Dependencies:

```
pip install -r requirements.txt
```

4. Update the .env file with

```
GOOGLE_API_KEY=<Your_API_KEY>
```

5. Run the application:

```
python -m backend.app.main --mode dev
# or
python -m backend.app.main
```
