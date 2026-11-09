# yattayo-social-assets

Card tipografiche generate automaticamente per i post social di Yattayo AI (yattayo.ai).

- `yattayo_card.py` — generatore (Pillow), formato 1080x1350 JPEG, temi `violet`, `light`, `orange`
- `fonts/` — Sora e DM Sans (SIL Open Font License, vedi file OFL)
- `cards/AAAA/MM/` — card pubblicate, servite via raw.githubusercontent.com

Esempio:
```
python3 yattayo_card.py --fonts fonts --out cards/2026/11/2026-11-10.jpg \
  --theme violet --kicker "Per PMI" --title "..." --subtitle "..." --cta "Prova gratis su yattayo.ai"
```
