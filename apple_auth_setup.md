# 🍎 Apple OAuth Access Token Setup Guide  
**Purpose:** Enable Apple Login in your Django backend using REST API (for iOS, web, or React frontend).

---

## 📘 Overview

This guide shows how to:
- Create an Apple Developer account setup  
- Configure a **Sign in with Apple** service  
- Get your **client secret** and **access token**  
- Use it with your Django backend endpoint `/auth/social/apple/`

---

## ⚙️ Prerequisites

✅ You must have:
- An **Apple Developer Account** (https://developer.apple.com/)
- Django backend with an Apple login endpoint, for example:
  ```
  POST http://localhost:8000/auth/social/apple/
  ```
- Installed dependencies:
  ```bash
  pip install pyjwt cryptography requests
  ```

---

## 🪜 Step 1: Create an App ID

1. Go to [Apple Developer](https://developer.apple.com/account/resources/identifiers/list)
2. Click ➕ **Register an App ID**
3. Choose **App IDs → Continue**
4. Select **App → Continue**
5. Fill in the details:
   - Description: `Django Auth App`
   - Bundle ID: `com.yourcompany.djangoauth`
6. Click **Continue → Register**

---

## 🪜 Step 2: Create a Service ID (Web or Backend Auth)

1. Go to **Identifiers → Service IDs**
2. Click ➕ to create a new Service ID
3. Enter:
   - Description: `Django Apple Login`
   - Identifier: `com.yourcompany.djangoauth.web`
4. Click **Continue → Register**

5. Now select the new Service ID → **Edit**  
   - Enable ✅ **Sign in with Apple**
   - Click **Configure**
   - Under **Web Domain**, enter:
     ```
     localhost
     ```
   - Under **Return URLs**, enter:
     ```
     https://localhost:8000/
     http://127.0.0.1:8000/
     ```
   - Click **Next → Done → Save**

---

## 🪜 Step 3: Create a Key for Apple Login

1. Go to **Keys → +** (top right corner)
2. Name it: `Apple Login Key`
3. Enable ✅ **Sign in with Apple**
4. Under **Primary App ID**, select the App ID you created earlier.
5. Click **Continue → Register → Download**

⚠️ Important: You will only be able to download the `.p8` key **once**.  
Rename it and save it securely, e.g.:
```
AuthKey_ABC123XYZ.p8
```

---

## 🪜 Step 4: Get Required Details

You’ll now have these values (needed in Django backend):

| Variable | Description |
|-----------|-------------|
| `KEY_ID` | The ID of the `.p8` key you just downloaded |
| `TEAM_ID` | Found in your [Apple Developer Account → Membership] |
| `CLIENT_ID` | Your Service ID (e.g. `com.yourcompany.djangoauth.web`) |
| `PRIVATE_KEY` | Contents of the `.p8` file |

---

## 🪜 Step 5: Generate Client Secret (JWT)

Create a Python script (e.g., `generate_apple_secret.py`):

```python
import jwt, time

TEAM_ID = "YOUR_TEAM_ID"
CLIENT_ID = "com.yourcompany.djangoauth.web"
KEY_ID = "YOUR_KEY_ID"

with open("AuthKey_ABC123XYZ.p8", "r") as f:
    PRIVATE_KEY = f.read()

headers = {
    "kid": KEY_ID,
    "alg": "ES256"
}

claims = {
    "iss": TEAM_ID,
    "iat": int(time.time()),
    "exp": int(time.time()) + 3600 * 6,  # 6 hours expiration
    "aud": "https://appleid.apple.com",
    "sub": CLIENT_ID,
}

client_secret = jwt.encode(claims, PRIVATE_KEY, algorithm="ES256", headers=headers)
print(client_secret)
```

This `client_secret` will be used by Django to exchange the authorization code for tokens.

---

## 🪜 Step 6: Get Access Token from Apple (for Testing)

You can manually test by running this `curl` command:

```bash
curl -X POST https://appleid.apple.com/auth/token -d 'client_id=com.yourcompany.djangoauth.web' -d 'client_secret=YOUR_CLIENT_SECRET' -d 'code=AUTHORIZATION_CODE_FROM_APPLE' -d 'grant_type=authorization_code'
```

✅ It will return JSON like this:

```json
{
  "access_token": "ACCESS_TOKEN_VALUE",
  "expires_in": 3600,
  "id_token": "ID_TOKEN_VALUE",
  "refresh_token": "REFRESH_TOKEN_VALUE",
  "token_type": "Bearer"
}
```

---

## 🪜 Step 7: Send Token to Django Backend

Use this token to log in via your Django API:

```http
POST http://localhost:8000/auth/social/apple/
Content-Type: application/json

{
  "id_token": "ID_TOKEN_VALUE",
  "access_token": "ACCESS_TOKEN_VALUE"
}
```

Your Django backend should:
- Validate the `id_token` using Apple’s public keys  
- Decode and extract email, name, etc.  
- Create/login the user automatically 🎉

---

## 🧩 Example Apple Login Django Flow

Backend verifies ID token with Apple:

```python
import requests, jwt

APPLE_PUBLIC_KEYS_URL = "https://appleid.apple.com/auth/keys"

def verify_apple_token(id_token):
    res = requests.get(APPLE_PUBLIC_KEYS_URL)
    public_keys = res.json()['keys']
    header = jwt.get_unverified_header(id_token)
    key = next(k for k in public_keys if k['kid'] == header['kid'])
    return jwt.decode(id_token, key, algorithms=['RS256'], audience='com.yourcompany.djangoauth.web')
```

---

## 📋 References

- [Apple Developer Documentation](https://developer.apple.com/documentation/sign_in_with_apple)
- [Apple OAuth 2.0 Flow](https://developer.apple.com/sign-in-with-apple/)
- [Apple Public Keys Endpoint](https://appleid.apple.com/auth/keys)
- [JWT for Apple Authentication](https://developer.apple.com/documentation/sign_in_with_apple/generate_and_validate_tokens)

---

✅ After setup, you can fully integrate **Apple Login** in Django REST Framework, the same as Google login!
