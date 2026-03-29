"""
AI Meme Brain — Render Flask App
Does: Groq AI picks story + template → Imgflip generates meme → returns to Make.com
Does NOT: LinkedIn posting, Gmail (Make.com handles those)
"""

from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

GROQ_API_KEY     = os.environ.get("GROQ_API_KEY")
IMGFLIP_USERNAME = os.environ.get("IMGFLIP_USERNAME")
IMGFLIP_PASSWORD = os.environ.get("IMGFLIP_PASSWORD")
WEBHOOK_SECRET   = os.environ.get("WEBHOOK_SECRET", "meme-secret-123")

MEME_TEMPLATES = [
    {"id": "101470",    "name": "Ancient Aliens",                "use_for": "conspiracy or unexplained tech"},
    {"id": "61579",     "name": "One Does Not Simply",           "use_for": "something harder than it looks"},
    {"id": "131087935", "name": "Running Away Balloon",          "use_for": "label-based comparison or distraction"},
    {"id": "4087833",   "name": "Waiting Skeleton",              "use_for": "long wait, delays, slow releases"},
    {"id": "100777631", "name": "Bernie Once Again Asking",      "use_for": "repeated request or recurring problem"},
    {"id": "93895088",  "name": "Expanding Brain",               "use_for": "escalating levels of intelligence or ideas"},
    {"id": "129242436", "name": "Change My Mind",                "use_for": "strong controversial opinion"},
    {"id": "155067746", "name": "Surprised Pikachu",             "use_for": "obvious outcome that still surprises people"},
    {"id": "14371066",  "name": "Conspiracy Keanu",              "use_for": "mind-blowing tech realization"},
    {"id": "563423",    "name": "That Would Be Great",           "use_for": "passive aggressive feature request"},
    {"id": "89370399",  "name": "Roll Safe",                     "use_for": "flawed but confident logic or workaround"},
    {"id": "217743513", "name": "UNO Draw 25",                   "use_for": "refusing to do the obvious thing"},
    {"id": "124822590", "name": "Left Exit 12 Off Ramp",         "use_for": "sudden change of direction or preference"},
    {"id": "247375501", "name": "Boardroom Meeting Suggestion",  "use_for": "corporate or startup absurdity"},
    {"id": "135256802", "name": "Epic Handshake",                "use_for": "two unlikely things agreeing"},
    {"id": "61532",     "name": "The Most Interesting Man",      "use_for": "I don't always... but when I do"},
    {"id": "134797956", "name": "Baby Yoda",                     "use_for": "cute or wholesome tech moment"},
    {"id": "1035805",   "name": "Philosoraptor",                 "use_for": "philosophical tech question"},
    {"id": "55311130",  "name": "This Is Fine",                  "use_for": "everything is on fire but acting calm"},
    {"id": "102156234", "name": "Mocking SpongeBob",             "use_for": "mocking a bad argument or claim"},
    {"id": "91538330",  "name": "Bike Fall",                     "use_for": "self-sabotage or own goal"},
    {"id": "195389578", "name": "Monkey Puppet",                 "use_for": "awkward side-eye or uncomfortable moment"},
    {"id": "178591752", "name": "Tuxedo Winnie the Pooh",        "use_for": "fancy vs basic version of same thing"},
    {"id": "226297822", "name": "Panik Kalm Panik",              "use_for": "panic then calm then panic again"},
    {"id": "161865971", "name": "Grus Plan",                     "use_for": "plan that unexpectedly backfires"},
    {"id": "196652226", "name": "Ight Imma Head Out",            "use_for": "leaving a bad or chaotic situation"},
    {"id": "252600902", "name": "Always Has Been",               "use_for": "plot twist or sudden realization"},
    {"id": "438680",    "name": "Batman Slapping Robin",         "use_for": "correcting someone firmly"},
    {"id": "114585149", "name": "Inhaling Seagull",              "use_for": "trend spreading everywhere fast"},
    {"id": "482641",    "name": "The Rock Driving",              "use_for": "double take or sudden realization"},
    {"id": "28034594",  "name": "Oprah You Get A",               "use_for": "giving something to absolutely everyone"},
    {"id": "259237855", "name": "Sleeping Shaq",                 "use_for": "ignoring something critically important"},
    {"id": "370867422", "name": "Disaster Girl",                 "use_for": "watching chaos unfold with satisfaction"},
    {"id": "142009471", "name": "Clown Applying Makeup",         "use_for": "self-deception or being delusional"},
    {"id": "445799",    "name": "Success Kid",                   "use_for": "small but satisfying unexpected win"},
    {"id": "91545132",  "name": "X X Everywhere",                "use_for": "something appearing absolutely everywhere"},
    {"id": "20007896",  "name": "I Should Buy A Boat",           "use_for": "sudden realization about wealth or success"},
    {"id": "1509839",   "name": "Captain Picard Facepalm",       "use_for": "embarrassing tech failure or bad decision"},
    {"id": "16464531",  "name": "Crying Jordan",                 "use_for": "loss defeat or disappointment in tech"},
    {"id": "80707627",  "name": "Yo Dawg",                       "use_for": "recursion or something inside something"},
    {"id": "47345944",  "name": "Imagination SpongeBob",         "use_for": "big possibilities or rainbow thinking"},
    {"id": "110163934", "name": "I Guarantee It",                "use_for": "overconfident guarantee or bold claim"},
    {"id": "3218037",   "name": "All The Things",                "use_for": "doing or automating all the things"},
    {"id": "8072508",   "name": "Overly Attached Girlfriend",    "use_for": "overdependence on a tool or platform"},
]


def ai_generate_meme_plan(articles):
    templates_str = "\n".join(
        f'id:{t["id"]} | name:{t["name"]} | use_for:{t["use_for"]}'
        for t in MEME_TEMPLATES
    )
    news_str = "\n".join(f"- {a}" for a in articles[:10])

    prompt = f"""You are a viral tech meme creator for LinkedIn.

NEWS HEADLINES:
{news_str}

AVAILABLE MEME TEMPLATES:
{templates_str}

YOUR JOB:
1. Pick the single most meme-worthy headline
2. Choose the BEST matching template id from the list above
3. Write punchy top_text and bottom_text (each max 80 characters, make it funny)
4. Write a short LinkedIn caption (2-3 lines, witty but professional, end with 3-5 hashtags)

IMPORTANT: Pick different templates based on context. Do not always pick Drake or Two Buttons.

Respond ONLY with valid JSON, no markdown, no explanation:
{{
  "chosen_headline": "...",
  "template_id": "...",
  "template_name": "...",
  "top_text": "...",
  "bottom_text": "...",
  "linkedin_caption": "..."
}}"""

    resp = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.9,
            "max_tokens": 500,
        },
        timeout=30,
    )
    resp.raise_for_status()
    raw = resp.json()["choices"][0]["message"]["content"].strip()
    if "```" in raw:
        parts = raw.split("```")
        raw = parts[1] if len(parts) > 1 else raw
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def generate_meme_image(template_id, top_text, bottom_text):
    resp = requests.post(
        "https://api.imgflip.com/caption_image",
        data={
            "template_id": template_id,
            "username": IMGFLIP_USERNAME,
            "password": IMGFLIP_PASSWORD,
            "text0": top_text,
            "text1": bottom_text,
            "font": "impact",
            "max_font_size": "50",
        },
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    if not data.get("success"):
        raise Exception(f"Imgflip failed: {data.get('error_message', 'unknown')}")
    return data["data"]["url"]


@app.route("/generate-meme", methods=["POST"])
def generate_meme():
    if request.headers.get("X-Webhook-Secret") != WEBHOOK_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    # Handle both plain text and JSON body from Make.com
    raw_body = request.get_data(as_text=True)

    try:
        body = json.loads(raw_body)
        articles_input = body.get("articles", body.get("text", ""))
    except Exception:
        articles_input = raw_body

    # Convert to list regardless of format
    if isinstance(articles_input, list):
        articles = [str(a).strip() for a in articles_input if str(a).strip()]
    else:
        text = str(articles_input).strip()
        # Split by common separators Make.com uses
        for sep in ["\n", " ||| ", "|||", " | "]:
            if sep in text:
                articles = [a.strip() for a in text.split(sep) if a.strip()]
                break
        else:
            articles = [text] if text else []

    if not articles:
        return jsonify({"error": "No articles provided"}), 400

    try:
        plan     = ai_generate_meme_plan(articles)
        meme_url = generate_meme_image(plan["template_id"], plan["top_text"], plan["bottom_text"])

        return jsonify({
            "status": "success",
            "meme_url": meme_url,
            "linkedin_caption": plan["linkedin_caption"],
            "template_used": plan["template_name"],
            "chosen_headline": plan["chosen_headline"],
            "top_text": plan["top_text"],
            "bottom_text": plan["bottom_text"],
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "AI Meme Brain"}), 200


if __name__ == "__main__":
    app.run(debug=False)
