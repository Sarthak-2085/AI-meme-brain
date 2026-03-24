# AI Meme Brain

A lightweight Flask API that serves as the **AI brain** for the [AI Meme Automation Engine](https://www.linkedin.com/posts/daily-tech-updates-and-news_techpolicy-anthropic-retaliation-activity-7442161111635898368-kzFl?utm_source=share&utm_medium=member_desktop&rcm=ACoAAFJcNgEB2ZTMU03C76BgbRnU_sMsHVAHtYQ).

It receives a news headline, uses Groq AI to pick the best meme template, generates the meme via Imgflip, and returns everything to Make.com for posting.

---

## 🧠 What It Does

- Receives a tech news headline from Make.com via webhook
- Uses **Groq AI (LLaMA 3.3 70B)** to pick the most meme-worthy angle
- Dynamically selects the best template from **50+ meme templates**
- Calls **Imgflip API** to generate the meme image
- Returns `meme_url`, `caption`, `hashtags`, and `cta` back to Make.com

---

## 🏗️ Architecture

```
Make.com
  → Scheduler (daily trigger)
  → RSS Feed (TechCrunch)
  → HTTP POST → AI Meme Brain (this repo)
                  → Groq AI picks story + template
                  → Imgflip generates meme image
                  → returns meme_url + caption
  → Buffer → posts meme to LinkedIn
  → Gmail → sends backup email
```

---

## 🛠️ Tech Stack

| Tool | Purpose | Cost |
|---|---|---|
| Flask | Web framework | Free |
| Groq API | AI meme logic (LLaMA 3.3 70B) | Free |
| Imgflip API | Meme image generation | Free |
| Render | Hosting | Free |
| cron-job.org | Keep server warm | Free |
| Make.com | Orchestration + posting | Free |

**Total cost: $0/month** 💸

---

## 🔁 API Endpoints

### `POST /generate-meme`
Generates a meme from a news headline.

**Headers:**
```
Content-Type: application/json
X-Webhook-Secret: your-secret
```

**Body:**
```json
{
  "text": "OpenAI launches GPT-5 and it writes better code than most developers"
}
```

**Response:**
```json
{
  "status": "success",
  "meme_url": "https://i.imgflip.com/xxxxx.jpg",
  "linkedin_caption": "...",
  "hashtags": "#AI #Tech ...",
  "cta": "What do you think? Drop your thoughts below!",
  "template_used": "Surprised Pikachu",
  "chosen_headline": "...",
  "top_text": "...",
  "bottom_text": "..."
}
```

### `GET /health`
Returns service status.
```json
{"status": "ok", "service": "AI Meme Brain"}
```

---

## 🚀 Deployment (Render)

### 1. Fork this repo

### 2. Create a Render account
Go to [render.com](https://render.com) → sign up with GitHub → create a new Web Service → connect this repo.

### 3. Set environment variables in Render dashboard

| Variable | Value |
|---|---|
| `GROQ_API_KEY` | Get free at [console.groq.com](https://console.groq.com) |
| `IMGFLIP_USERNAME` | Your [imgflip.com](https://imgflip.com) username |
| `IMGFLIP_PASSWORD` | Your imgflip password |
| `WEBHOOK_SECRET` | Any random string e.g. `meme-secret-2025` |

### 4. Deploy
Render auto-deploys from GitHub. Every push to main triggers a redeploy.

### 5. Keep server warm (important!)
Render free tier spins down after 15 min inactivity. Use [cron-job.org](https://cron-job.org) to ping `/health` every 15 minutes for free.

---

## ⚙️ Make.com Setup

Your Make.com scenario should look like this:

```
[Scheduler] → [RSS - TechCrunch] → [HTTP - POST to /generate-meme] → [Buffer - LinkedIn] → [Gmail]
```

**HTTP Module config:**
- URL: `https://your-app.onrender.com/generate-meme`
- Method: POST
- Headers: `Content-Type: application/json`, `X-Webhook-Secret: your-secret`
- Body: `{"text": "{{2.title}}"}`
- Parse response: YES
- Timeout: 120 seconds

**Buffer Module:**
- Text: `{{HTTP.data.linkedin_caption}}` + hashtags
- Link to an image: `{{HTTP.data.meme_url}}`
- Thumbnail: `{{HTTP.data.meme_url}}`

---

## 🧠 How AI Picks Templates

The Groq AI receives the news headline alongside all 50+ template descriptions like:

```
id:155067746 | name:Surprised Pikachu | use_for:obvious outcome that still surprises people
id:55311130  | name:This Is Fine      | use_for:everything is on fire but acting calm
id:4087833   | name:Waiting Skeleton  | use_for:long wait, delays, slow releases
```

It then picks the template whose `use_for` best matches the news story — making every meme genuinely different and context-aware.

**Examples:**
- *"Apple delays product again"* → Waiting Skeleton
- *"Google fires engineers, replaces with AI"* → Crying Jordan / Disaster Girl  
- *"Every app adding AI features"* → X X Everywhere
- *"Dev uses AI to write code"* → Roll Safe

---

## 📸 Sample Output

> *"Online bot traffic will exceed human traffic by 2027"*
> 
> Template: **Woman Yelling at Cat**  
> Headline: Elizabeth Warren calls Pentagon’s decision to bar Anthropic ‘retaliation’
> <img width="510" height="328" alt="image" src="https://github.com/user-attachments/assets/1fd7d1d9-3f5f-4506-b56f-9bfeefe1d369" />


---

## 🔗 Related

- [AI Meme Automation Engine (Make.com)](https://github.com/Sarthak-2085/AI-Meme-Automation-Engine-LinkedIn-Growth-System-)
- [Auto Tech News Sender](https://github.com/Sarthak-2085/Automatic-Tech-News-Sender)
- [LinkedIn Page](https://www.linkedin.com/company/daily-tech-updates-and-news)

---

## 📬 Notes

Built as part of a broader journey into automation, AI workflows, and system design.  
100% free stack — no credit card, no paid APIs.

***This project is part of a broader journey into automation, AI workflows, and system design.  
More projects and improvements will be added over time.***
