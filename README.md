# 🎂 4-Part Animated Birthday Email Automation (Oct 2 IST • GitHub Actions + GitHub Pages)

Pre-configured to send **4 animated HTML birthday emails** on **October 2nd in Indian Standard Time (`Asia/Kolkata`, IST)** to:
- `d.shambhavi02@gmail.com`
- `d.shambhavi0210@gmail.com`
- **Plus an automatic delivery confirmation email to your own address (`SMTP_EMAIL`)** every time a stage is sent!

## 🕒 October 2nd IST Schedule (`Asia/Kolkata`)

| Stage | Date & Time (IST) | GitHub Cron (UTC) | Theme & Inline GIF |
| :---: | :---: | :---: | :--- |
| **1** | **Oct 2, 09:00 AM IST** | `30 3 2 10 *` | ☀️ **Morning Sunrise & Balloons** (`assets/1_sunrise_balloons.gif`) |
| **2** | **Oct 2, 02:00 PM IST** | `30 8 2 10 *` | 💌 **Afternoon Floating Hearts** (`assets/2_floating_hearts.gif`) |
| **3** | **Oct 2, 07:00 PM IST** | `30 13 2 10 *` | 🎂 **Evening Birthday Cake & Wish** (`assets/3_birthday_cake.gif`) |
| **4** | **Oct 2, 11:30 PM IST** | `0 18 2 10 *` | 🎆 **Midnight Starry Fireworks Finale** (`assets/4_starry_fireworks.gif`) |

---

## 🚀 Step-by-Step GitHub Setup

### Step 1: Push This Project to `github.com/Gaurav0296/EVS`
Notice your repository's default branch is **`master`** (GitHub Actions schedules only run on the default branch):
```bash
cd /usr/local/google/home/shugaurav/.gemini/jetski/brain/b3c8d07b-3be9-4d24-9118-5d962cb44c74/scratch/birthday-email-automation
git push -u origin master --force
```

### Step 2: Confirm Your Secrets in `github.com/Gaurav0296/EVS`
In **[github.com/Gaurav0296/EVS/settings/secrets/actions](https://github.com/Gaurav0296/EVS/settings/secrets/actions)**, make sure your Gmail address and 16-character Gmail App Password are saved (the workflow automatically supports `SMTP_EMAIL` / `EMAIL_USER` / `GMAIL_USER` / `SENDER_EMAIL` / `EMAIL` and `SMTP_PASSWORD` / `EMAIL_PASS` / `EMAIL_PASSWORD` / `GMAIL_APP_PASSWORD` / `APP_PASSWORD`):

| Secret Name | Value |
| :--- | :--- |
| `SMTP_EMAIL` | Your Gmail address — sends the emails **and** receives your "✅ [Sent]" confirmation emails |
| `SMTP_PASSWORD` | Your 16-character Gmail App Password ([myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords)) |

### Step 3: Enable GitHub Pages on `/docs`
1. Go to **[github.com/Gaurav0296/EVS/settings/pages](https://github.com/Gaurav0296/EVS/settings/pages)**.
2. Under **Build and deployment → Source**, select **Deploy from a branch**.
3. Select branch **`master`** and folder **`/docs`**, then click **Save**.
   - Live URL: `https://gaurav0296.github.io/EVS/?stage=1`

### Step 4: Test or Trigger Manually Anytime
1. Go to **[github.com/Gaurav0296/EVS/actions](https://github.com/Gaurav0296/EVS/actions)**.
2. Click **Send 4 Animated Birthday Emails 🎉 (Oct 2 IST)** on the left.
3. Click **Run workflow** (if you want to trigger Stage 1, 2, 3, or 4 manually right away), or let the scheduled cron automatically run at **9:00 AM IST**, **2:00 PM IST**, **7:00 PM IST**, and **11:30 PM IST** today!
