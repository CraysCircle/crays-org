# crays-org

Local working copy for `www.crays.org`.

This project is a static mirror/worktree of the current Vercel project `crays-org`.

- Vercel project: `prj_5paxPwt5pgAe7cyvTn85lUx1wwV6`
- Vercel team: `team_hBEkypVxg4SGGaxkUdHo6e4y`
- Production domains: `www.crays.org`, `crays.org`
- Latest recovered local source: `C:\Users\34669\Documents\Codex\2026-05-13\bitte-ziehe-dr-die-daten-von`
- Important yesterday edits: 14.05.2026, especially `public\finance\index.html` at 21:52
- Stock image source: `C:\Users\34669\OneDrive - Crays Europe SE\Dokumente\Crays\Bilder\Stock Images`

## Local Development

```powershell
npm start
```

The local server opens the `public` directory and serves routes like `/finance/`, `/association/`, and `/tech/`.

## Refresh From Live

```powershell
npm run mirror:live
```

This mirrors same-origin pages and assets from `https://crays.org` into `public`.

## Deployment Note

The `.vercel/project.json` file is kept locally and ignored by Git. It links this folder to the existing Vercel project when using the Vercel CLI on this machine.
