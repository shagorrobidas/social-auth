# 🧾 Google OAuth Access Token Setup Guide  
**Purpose:** Use Google Login in your Django backend via REST API.

---

## 📘 Overview

This guide shows how to:
- Create a Google Cloud project  
- Configure OAuth 2.0 credentials  
- Use **Google OAuth Playground** to generate an access token  
- Test login with Django endpoint `/auth/social/google/`

---

## ⚙️ Prerequisites

✅ You must have:
- A **Google Account**
- A Django backend with a Google auth endpoint, for example:
  ```
  POST http://localhost:8000/auth/social/google/
  ```
- Installed packages (in Django):
  ```bash
  pip install google-auth google-auth-oauthlib google-auth-httplib2 requests
  ```

---

## 🪜 Step 1: Create a Google Cloud Project

1. Go to **Google Cloud Console**:  
   👉 [https://console.cloud.google.com/](https://console.cloud.google.com/)

2. Click the project dropdown → **New Project**

3. Enter:
   - Name: `Django Auth App`
   - Location: (any)

4. Click **Create**

---

## 🪜 Step 2: Configure OAuth Consent Screen

1. In the sidebar, go to  
   **APIs & Services → OAuth consent screen**

2. Choose **External** → Click **Create**

3. Fill in:
   - App name: e.g., *Django Google Auth*
   - User support email: your Gmail
   - Developer contact email: same Gmail

4. Click **Save and Continue**

5. Under **Scopes**, click **Add or Remove Scopes**  
   and select:
   ```
   https://www.googleapis.com/auth/userinfo.email
   https://www.googleapis.com/auth/userinfo.profile
   openid
   ```

6. Save → Continue → Add a **Test User** (your Gmail)

7. Click **Publish App**

---

## 🪜 Step 3: Create OAuth Client ID

1. Go to  
   **APIs & Services → Credentials**

2. Click **Create Credentials → OAuth Client ID**

3. Choose **Web application**

4. Name: `Django Auth Client`

5. Under **Authorized redirect URIs**, add:
   ```
   http://localhost:8000/
   http://127.0.0.1:8000/
   https://developers.google.com/oauthplayground
   ```

6. Click **Create**

7. Copy your:
   - **Client ID**
   - **Client Secret**

---

## 🪜 Step 4: Get Access Token from Google OAuth Playground

1. Go to 👉 [https://developers.google.com/oauthplayground](https://developers.google.com/oauthplayground)

2. Click the ⚙️ **Settings icon** (top-right corner)

3. Check ✅ **Use your own OAuth credentials**

4. Paste your:
   - Client ID
   - Client Secret  
   (from Step 3)

5. Click **Close**

6. In the left input box (“Input your own scopes”), paste:
   ```
   https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile openid
   ```

7. Click **Authorize APIs**

8. Log in with your Google account → Click **Allow**

9. Click **Exchange authorization code for tokens**

10. Copy your **access_token** from the results box.

---

## 🪜 Step 5: Test Token in Django

Use your access token in a POST request:

```http
POST http://localhost:8000/auth/social/google/
Content-Type: application/json

{
  "access_token": "PASTE_YOUR_ACCESS_TOKEN_HERE"
}
```

✅ If everything is correct:
- Django verifies the token with Google  
- Retrieves your email and profile info  
- Creates or logs in your user

---

## 🧠 Optional: Verify Token Before Sending

To confirm your token is valid:

```bash
curl "https://www.googleapis.com/oauth2/v3/tokeninfo?access_token=YOUR_ACCESS_TOKEN"
```

If valid, it returns your Google account details (email, etc.).

---

## 📋 Reference Docs

- [Google OAuth 2.0 Playground](https://developers.google.com/oauthplayground)
- [Google Identity Platform Documentation](https://developers.google.com/identity)
- [OAuth 2.0 for Web Server Applications](https://developers.google.com/identity/protocols/oauth2/web-server)
- [Google Tokeninfo Endpoint](https://www.googleapis.com/oauth2/v3/tokeninfo)
