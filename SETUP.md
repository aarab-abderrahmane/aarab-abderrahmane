# Setup (5 steps)

## 1. Fill in your info
Open `generate_svg.py` and edit the lines marked `# TODO` (placeholders / guesses):
`OS`, `IDE`, `Languages.Real`, `Hobbies.Hardware`, `Discord`. Delete any line you don't want.

Open `today.py` and set your real birth date:
```python
BIRTHDAY = datetime.datetime(2000, 1, 1)   # <- PLACEHOLDER
```

## 2. Generate your card (once)
```bash
pip install pillow
python generate_svg.py me.png --cols 50     # me.png = photo with background removed (remove.bg)
```
No photo yet? Run `python generate_svg.py` for a placeholder silhouette.
Re-run any time you change the text or photo (this resets the numbers; the Action refills them).

## 3. Create a GitHub token
GitHub -> Settings -> Developer settings -> Personal access tokens -> **Fine-grained token**
- Repository access: **All repositories**
- Account permissions: Followers (read), Starring (read), Watching (read)
- Repository permissions: Commit statuses, Contents, Issues, Metadata, Pull requests (all read)

## 4. Add repo secrets
In the repo `aarab-abderrahmane/aarab-abderrahmane`: Settings -> Secrets and variables -> Actions
- `ACCESS_TOKEN` = the token from step 3
- `USER_NAME` = `aarab-abderrahmane`

## 5. Push and run
Upload everything in this folder to the repo's `main` branch, then Actions -> "README build" -> Run workflow.
The first run is slow (it counts lines of code in every repo and writes `cache/<hash>.txt`). After that it runs daily at 04:00 UTC.

Notes
- If the snake section shows a broken image, remove it or set up the Platane/snk Action.
- If text looks misaligned on your device, GitHub is using a different monospace font; this is normal for SVGs.
