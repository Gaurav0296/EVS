#!/usr/bin/env python3
"""Sends the 4 animated HTML birthday emails via SMTP (e.g. Gmail App Password).

Supports:
  - Stage 1 (Morning):   Sunrise & Floating Balloons
  - Stage 2 (Afternoon): Floating Hearts & Love Note
  - Stage 3 (Evening):   Birthday Cake & Make a Wish
  - Stage 4 (Midnight):  Fireworks & Starry Night Finale

Usage:
  # Send Stage 1 email via SMTP (reads credentials from env vars):
  python3 send_birthday_email.py --stage 1

  # Export all 4 HTML emails locally to preview in a browser:
  python3 send_birthday_email.py --export-previews ./previews
"""

import argparse
from datetime import datetime
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
import ssl
from zoneinfo import ZoneInfo

IST = ZoneInfo("Asia/Kolkata")

STAGES = {
    1: {
        "time_label": "Morning Surprise • Part 1 of 4",
        "subject": "☀️ Good Morning Birthday Girl! Let the celebration begin 🎈",
        "gif": "1_sunrise_balloons.gif",
        "bg_outer": "#fff5f2",
        "card_border": "#ffd8cc",
        "badge_bg": "#ffe5d9",
        "badge_text": "#d9480f",
        "accent": "#ff5a79",
        "button_bg": "linear-gradient(135deg, #ff5a79, #ff8fa3)",
        "button_solid": "#ff5a79",
        "heading": "Rise & Shine, Birthday Girl! 🎈",
        "subheading": "The sun came up today just to celebrate you.",
        "body_paragraphs": [
            "Happy Birthday! Today is all about celebrating the most wonderful, kind, and radiant person in my life.",
            "This is just the first of <strong>4 little birthday surprises</strong> heading to your inbox today. I hope your morning starts with the biggest smile, a warm cup of your favorite drink, and the feeling of how truly special and cherished you are.",
        ],
        "quote": "“Every sunrise is brighter because I get to share my days with you.”",
        "cta_text": "🎈 Pop Your Birthday Balloons (Interactive)",
        "footer_hint": "Keep an eye on your inbox this afternoon (2:00 PM IST) for Part 2 of 4... 💌",
    },
    2: {
        "time_label": "Afternoon Note • Part 2 of 4",
        "subject": "💌 A little afternoon birthday note just for you 💕",
        "gif": "2_floating_hearts.gif",
        "bg_outer": "#fff0f3",
        "card_border": "#ffccd5",
        "badge_bg": "#ffe5ec",
        "badge_text": "#c9184a",
        "accent": "#e01e5a",
        "button_bg": "linear-gradient(135deg, #e01e5a, #ff758f)",
        "button_solid": "#e01e5a",
        "heading": "Sending You a Million Smiles 💕",
        "subheading": "Just a midday reminder of how much you mean to me.",
        "body_paragraphs": [
            "I hope your birthday is unfolding beautifully so far! In the middle of your day, I wanted to pause and remind you of all the little things I adore about you—your laugh, your warmth, and the way you make ordinary moments feel magical.",
            "If I could attach a note for every reason I appreciate you, no inbox in the world would have enough storage.",
        ],
        "quote": "“In a room full of art, I would still stare at you.”",
        "cta_text": "💌 Open Your Interactive Birthday Note",
        "footer_hint": "Tonight (7:00 PM IST) brings cake & wishes in Part 3 of 4... 🎂",
    },
    3: {
        "time_label": "Evening Celebration • Part 3 of 4",
        "subject": "🎂 Close your eyes and make a birthday wish! ✨",
        "gif": "3_birthday_cake.gif",
        "bg_outer": "#f6f0ff",
        "card_border": "#e5d4ff",
        "badge_bg": "#ede0ff",
        "badge_text": "#6b21a8",
        "accent": "#7c3aed",
        "button_bg": "linear-gradient(135deg, #7c3aed, #c084fc)",
        "button_solid": "#7c3aed",
        "heading": "Time to Make a Birthday Wish! 🎂",
        "subheading": "The candles are lit and flickering just for you.",
        "body_paragraphs": [
            "Even if there’s a real cake waiting for you too, I baked a little digital one with flickering candles right here in your inbox!",
            "Take a deep breath, think of your biggest, happiest wish for this new year of your life, and click the button below to blow out the candles.",
        ],
        "quote": "“May every wish you make tonight come true—and may I always be by your side to cheer you on.”",
        "cta_text": "🕯️ Click to Blow Out Your Candles",
        "footer_hint": "One final midnight surprise awaits (11:30 PM IST) in Part 4 of 4... 🎆",
    },
    4: {
        "time_label": "Midnight Finale • Part 4 of 4",
        "subject": "🎆 Under the stars: Happy Birthday! ✨🌙",
        "gif": "4_starry_fireworks.gif",
        "bg_outer": "#eef2ff",
        "card_border": "#c7d2fe",
        "badge_bg": "#e0e7ff",
        "badge_text": "#3730a3",
        "accent": "#4f46e5",
        "button_bg": "linear-gradient(135deg, #4f46e5, #818cf8)",
        "button_solid": "#4f46e5",
        "heading": "A Sky Full of Fireworks for You 🎆",
        "subheading": "Ending your special day under a starry sky.",
        "body_paragraphs": [
            "As your birthday comes to a close tonight, I wanted to light up the night sky for you. Thank you for being my favorite person, my best friend, and my greatest adventure.",
            "Here’s to another incredible year of memories, laughter, late-night talks, and dreams coming true together. Happy Birthday!",
        ],
        "quote": "“To the moon, the stars, and all the fireworks in between—you shine brighter than them all.”",
        "cta_text": "🎆 Launch Your Midnight Fireworks Show",
        "footer_hint": "Yours ✨ • Happy Birthday!",
    },
}


def render_email_html(stage_num, her_name, sender_name, pages_url, img_src="cid:birthday_animation"):
  s = STAGES[stage_num]
  interactive_link = f"{pages_url.rstrip('/')}?stage={stage_num}"
  paragraphs_html = "\n".join(
      f'<p style="margin: 0 0 16px 0; font-size: 16px; line-height: 1.65; color: #334155;">{p}</p>'
      for p in s["body_paragraphs"]
  )

  return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{s["subject"]}</title>
</head>
<body style="margin: 0; padding: 0; background-color: {s["bg_outer"]}; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="background-color: {s["bg_outer"]}; padding: 32px 12px;">
    <tr>
      <td align="center">
        <table role="presentation" width="600" cellspacing="0" cellpadding="0" border="0" style="max-width: 600px; width: 100%; background-color: #ffffff; border-radius: 24px; border: 2px solid {s["card_border"]}; overflow: hidden; box-shadow: 0 12px 32px rgba(15, 23, 42, 0.08);">
          <!-- Top Stage Pill -->
          <tr>
            <td align="center" style="padding: 28px 24px 12px 24px;">
              <span style="display: inline-block; padding: 6px 16px; border-radius: 999px; background-color: {s["badge_bg"]}; color: {s["badge_text"]}; font-size: 12px; font-weight: 700; letter-spacing: 0.6px; text-transform: uppercase;">
                {s["time_label"]}
              </span>
            </td>
          </tr>

          <!-- Heading -->
          <tr>
            <td align="center" style="padding: 8px 32px 4px 32px;">
              <h1 style="margin: 0; font-size: 28px; line-height: 1.25; color: #0f172a; font-weight: 800;">
                {s["heading"]}
              </h1>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding: 4px 32px 20px 32px;">
              <p style="margin: 0; font-size: 15px; color: #64748b; font-weight: 500;">
                For <strong style="color: {s["accent"]};">{her_name}</strong> — {s["subheading"]}
              </p>
            </td>
          </tr>

          <!-- Animated GIF Hero -->
          <tr>
            <td align="center" style="padding: 0 24px 24px 24px;">
              <a href="{interactive_link}" target="_blank" style="text-decoration: none; display: block;">
                <img src="{img_src}" alt="{s["heading"]}" width="552" style="width: 100%; max-width: 552px; height: auto; border-radius: 16px; display: block; border: 1px solid {s["card_border"]};" />
              </a>
            </td>
          </tr>

          <!-- Personal Message Body -->
          <tr>
            <td style="padding: 4px 36px 8px 36px;">
              <p style="margin: 0 0 16px 0; font-size: 17px; font-weight: 600; color: #1e293b;">
                Dear {her_name},
              </p>
              {paragraphs_html}
            </td>
          </tr>

          <!-- Highlighted Quote Box -->
          <tr>
            <td style="padding: 4px 36px 24px 36px;">
              <div style="background-color: {s["bg_outer"]}; border-left: 4px solid {s["accent"]}; padding: 16px 20px; border-radius: 0 12px 12px 0; font-style: italic; color: #334155; font-size: 15px; line-height: 1.6;">
                {s["quote"]}
              </div>
            </td>
          </tr>

          <!-- Interactive GitHub Pages CTA Button -->
          <tr>
            <td align="center" style="padding: 4px 36px 28px 36px;">
              <a href="{interactive_link}" target="_blank" style="display: inline-block; background-color: {s["button_solid"]}; background-image: {s["button_bg"]}; color: #ffffff; text-decoration: none; font-size: 16px; font-weight: 700; padding: 14px 28px; border-radius: 999px; box-shadow: 0 6px 18px rgba(0, 0, 0, 0.12);">
                {s["cta_text"]}
              </a>
            </td>
          </tr>

          <!-- Sign-off -->
          <tr>
            <td style="padding: 0 36px 28px 36px; border-bottom: 1px solid #f1f5f9;">
              <p style="margin: 0; font-size: 16px; color: #334155;">
                Yours,<br/>
                <strong style="color: {s["accent"]}; font-size: 18px;">{sender_name}</strong> ✨
              </p>
            </td>
          </tr>

          <!-- Next Email Teaser Footer -->
          <tr>
            <td align="center" style="padding: 18px 24px; background-color: #f8fafc;">
              <p style="margin: 0; font-size: 13px; color: #64748b; font-weight: 500;">
                {s["footer_hint"]}
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def send_email(stage_num, smtp_email, smtp_password, recipient_emails, her_name, sender_name, pages_url, smtp_host="smtp.gmail.com", smtp_port=465):
  s = STAGES[stage_num]
  if isinstance(recipient_emails, str):
    recipients = [r.strip() for r in recipient_emails.split(",") if r.strip()]
  else:
    recipients = list(recipient_emails)

  gif_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", s["gif"])
  with open(gif_path, "rb") as f:
    gif_bytes = f.read()

  plain_text = (
      f"{s['heading']}\n\n"
      f"Dear {her_name},\n\n"
      + "\n\n".join(s["body_paragraphs"]).replace("<strong>", "").replace("</strong>", "")
      + f"\n\n{s['quote']}\n\n"
      f"Open your interactive animation: {pages_url.rstrip('/')}?stage={stage_num}\n\n"
      f"Yours,\n{sender_name}"
  )
  html_content = render_email_html(stage_num, her_name, sender_name, pages_url, img_src="cid:birthday_animation")

  context = ssl.create_default_context()
  with smtplib.SMTP_SSL(smtp_host, smtp_port, context=context) as server:
    server.login(smtp_email, smtp_password)

    # 1. Send the birthday email to each recipient address
    for recipient in recipients:
      msg = MIMEMultipart("related")
      msg["Subject"] = s["subject"]
      msg["From"] = f"{sender_name} <{smtp_email}>"
      msg["To"] = recipient

      alt = MIMEMultipart("alternative")
      msg.attach(alt)
      alt.attach(MIMEText(plain_text, "plain", "utf-8"))
      alt.attach(MIMEText(html_content, "html", "utf-8"))

      mime_img = MIMEImage(gif_bytes, _subtype="gif")
      mime_img.add_header("Content-ID", "<birthday_animation>")
      mime_img.add_header("Content-Disposition", "inline", filename=s["gif"])
      msg.attach(mime_img)

      server.sendmail(smtp_email, [recipient], msg.as_string())

    now_ist = datetime.now(IST).strftime("%d %b %Y, %I:%M:%S %p IST")
    print(f"[{now_ist}] Successfully sent Stage {stage_num} ({s['time_label']}) to: {', '.join(recipients)}")

    # 2. Send confirmation notification email to yourself (gaurav.shukla344@gmail.com)
    notify_to = os.environ.get("NOTIFY_EMAIL", "gaurav.shukla344@gmail.com")
    notify_msg = MIMEMultipart("alternative")
    notify_msg["Subject"] = f"✅ [Sent] Birthday Email Stage {stage_num}/4 delivered to {her_name}"
    notify_msg["From"] = f"Birthday Bot <{smtp_email}>"
    notify_msg["To"] = notify_to

    notify_body = (
        f"Hi {sender_name},\n\n"
        f"Your automated birthday email (Stage {stage_num} of 4) was just sent!\n\n"
        f"• Stage: {s['time_label']}\n"
        f"• Subject: {s['subject']}\n"
        f"• Sent To: {', '.join(recipients)}\n"
        f"• Time (IST): {now_ist}\n"
        f"• Interactive Link: {pages_url.rstrip('/')}?stage={stage_num}\n"
    )
    notify_msg.attach(MIMEText(notify_body, "plain", "utf-8"))
    server.sendmail(smtp_email, [notify_to], notify_msg.as_string())
    print(f"[{now_ist}] Sent delivery confirmation email to yourself ({notify_to}).")


def detect_stage_from_ist_time(now_ist=None):
  """Determines which of the 4 stages to send based on current Indian Standard Time (IST)."""
  if now_ist is None:
    now_ist = datetime.now(IST)
  hour = now_ist.hour
  if hour < 12:
    return 1  # Morning (09:00 AM IST)
  elif hour < 17:
    return 2  # Afternoon (02:00 PM IST)
  elif hour < 22:
    return 3  # Evening (07:00 PM IST)
  else:
    return 4  # Night / Midnight Finale (11:30 PM IST)


def main():
  parser = argparse.ArgumentParser(description="Send or preview the 4 animated birthday emails (Indian Standard Time - IST).")
  parser.add_argument("--stage", type=int, choices=[1, 2, 3, 4], help="Which of the 4 birthday emails to send (1-4).")
  parser.add_argument("--auto-ist", action="store_true", help="Automatically pick Stage 1-4 based on current Indian Standard Time (Asia/Kolkata).")
  parser.add_argument("--export-previews", type=str, help="Directory to export HTML email previews to.")
  args = parser.parse_args()

  now_ist = datetime.now(IST)
  print(f"Current Indian Standard Time: {now_ist.strftime('%d %b %Y, %I:%M:%S %p IST')}")

  her_name = os.environ.get("HER_NAME", "Shambhavi")
  sender_name = os.environ.get("SENDER_NAME", "Gaurav")
  pages_url = os.environ.get("PAGES_URL", "https://gaurav0296.github.io/EVS")

  if args.export_previews:
    os.makedirs(args.export_previews, exist_ok=True)
    for st in [1, 2, 3, 4]:
      gif_rel = f"../assets/{STAGES[st]['gif']}"
      html = render_email_html(st, her_name, sender_name, pages_url, img_src=gif_rel)
      out_file = os.path.join(args.export_previews, f"email_stage_{st}.html")
      with open(out_file, "w", encoding="utf-8") as f:
        f.write(html)
      print(f"Exported {out_file}")
    return

  stage = args.stage or (detect_stage_from_ist_time(now_ist) if args.auto_ist else None)
  if not stage:
    parser.error("Please specify --stage {1,2,3,4}, --auto-ist, or --export-previews <dir>.")

  smtp_email = os.environ.get("SMTP_EMAIL") or "gaurav.shukla344@gmail.com"
  smtp_password = os.environ.get("SMTP_PASSWORD")
  recipient_emails = os.environ.get(
      "RECIPIENT_EMAIL",
      "d.shambhavi02@gmail.com,d.shambhavi0210@gmail.com",
  )

  if not all([smtp_email, smtp_password]):
    raise SystemExit(
        "Missing required environment variables: SMTP_EMAIL, SMTP_PASSWORD.\n"
        "Set these in your GitHub Repository Secrets (Settings -> Secrets and variables -> Actions)."
    )

  send_email(
      stage_num=stage,
      smtp_email=smtp_email,
      smtp_password=smtp_password,
      recipient_emails=recipient_emails,
      her_name=her_name,
      sender_name=sender_name,
      pages_url=pages_url,
  )


if __name__ == "__main__":
  main()
