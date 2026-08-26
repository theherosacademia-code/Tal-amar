# Claude Code toolkit

הכל נטען אוטומטית בכל סשן שנפתח על הרפו הזה. אין מה להתקין ידנית.

## סקילים — `.claude/skills/`

מקור: [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) + `find-skills` מ־[vercel-labs/skills](https://github.com/vercel-labs/skills).

| סקיל | מה זה עושה |
|---|---|
| `design-taste-frontend` | עיצוב פרונטאנד anti-slop (v2, ברירת המחדל) |
| `design-taste-frontend-v1` | הגרסה הקודמת, לתאימות אחורה |
| `high-end-visual-design` | ליטוש ויזואלי ברמת אייג'נסי |
| `minimalist-ui` | ממשק מינימליסטי עריכותי |
| `industrial-brutalist-ui` | טיפוגרפיה שוויצרית, ניגודיות גבוהה |
| `stitch-design-taste` | חוקי מערכת עיצוב ל־Google Stitch |
| `gpt-taste` | אותו כיוון, מכוון ל־GPT/Codex |
| `brandkit` | לוחות מיתוג, מערכות לוגו, חבילות זהות |
| `redesign-existing-projects` | מבקר UI קיים ואז מתקן בלי לשבור |
| `image-to-code` | מייצר תמונות ייחוס ואז מממש לפיהן |
| `imagegen-frontend-web` | ייצור תמונות ייחוס לוובסייט (בלי קוד) |
| `imagegen-frontend-mobile` | ייצור תמונות ייחוס למובייל (בלי קוד) |
| `full-output-enforcement` | מונע פלט קוד קטוע |
| `find-skills` | מאתר ומציע סקילים נוספים להתקנה |

## פלאגינים — `.claude/settings.json`

מותקנים אוטומטית מהמרקטפלייס בתחילת כל סשן.

| פלאגין | מקור | מה זה עושה |
|---|---|---|
| `superpowers` | `obra/superpowers-marketplace` | אוכף תכנון, בדיקות וביקורת עצמית לפני שמשימה נחשבת גמורה |
| `ralph-skills` | `snarktank/ralph` | מכריח בדיקה חוזרת בלולאה עד שהעבודה באמת הושלמה |

## שרתי MCP — `.mcp.json`

| שרת | מה זה עושה | מפתח API? |
|---|---|---|
| `playwright` | מפעיל דפדפן אמיתי — לחיצות, טפסים, בדיקות end-to-end | לא |
| `context7` | מושך תיעוד ספריות עדכני במקום לנחש | לא (אופציונלי להעלאת מכסה) |
| `firecrawl` | גירוד, סריקה וחיפוש בדפי אינטרנט חיים | לא (מכסה חינמית) |

## איך להרחיב לכל הרפוזיטוריז

הקבצים כאן חלים על הרפו הזה בלבד. כדי שהערכה תהיה זמינה בכל סשן ענן ובכל רפו,
מדביקים את `setup.sh` (בשורש הרפו) לשדה **Setup script** בהגדרות הסביבה
ב־[claude.ai/code](https://claude.ai/code). הוא רץ פעם אחת ואז נשמר במטמון.
