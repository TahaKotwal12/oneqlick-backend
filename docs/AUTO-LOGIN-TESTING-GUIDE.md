# 🧪 Testing Auto-Login Feature

## Quick Test Guide

### Step 1: Access the Debug Screen

Navigate to the debug screen in your app:
```
http://localhost:8081/auth-debug
```

Or add a button in your app to navigate there:
```typescript
import { useRouter } from 'expo-router';

const router = useRouter();
router.push('/auth-debug');
```

---

### Step 2: Login and Check Storage

1. **Go to Login Screen**
2. **Enter your credentials**
3. **Make sure "Remember Me" is CHECKED** ✅
4. **Click "Sign In"**
5. **Go to Debug Screen** (`/auth-debug`)
6. **Verify the following:**
   - ✅ "Remember Me" shows "✅ Enabled"
   - ✅ "Access Token" shows a token
   - ✅ "Refresh Token" shows a token
   - ✅ "User Data" shows "Present"
   - ✅ "Authenticated" shows "Yes ✅"

---

### Step 3: Test Auto-Login

1. **Close the app COMPLETELY**
   - On iOS: Swipe up from bottom and swipe away the app
   - On Android: Recent apps → Swipe away
   - **Don't just minimize it!**

2. **Reopen the app**

3. **Expected Result:**
   - ✅ You should be automatically logged in
   - ✅ You should see the home screen
   - ✅ NO login screen should appear

---

### Step 4: Test Without Remember Me

1. **Logout** (use the debug screen button)
2. **Login again**
3. **UNCHECK "Remember Me"** ❌
4. **Click "Sign In"**
5. **Go to Debug Screen**
6. **Verify:**
   - ❌ "Remember Me" shows "❌ Disabled"

7. **Close the app completely**
8. **Reopen the app**
9. **Expected Result:**
   - ❌ You should see the LOGIN screen
   - ❌ NOT automatically logged in

---

## Troubleshooting

### Issue: Always shows login screen

**Check on Debug Screen:**
1. Is "Remember Me" showing "✅ Enabled"?
   - If NO: You need to check "Remember Me" when logging in
   
2. Are tokens present?
   - If NO: Login might have failed or tokens weren't saved

3. Is "Authenticated" showing "Yes"?
   - If NO: Check console for errors in AuthContext

**Console Debugging:**
Add this to your AuthContext `checkAuth()` function:
```typescript
console.log('=== AUTH CHECK DEBUG ===');
console.log('Remember Me:', rememberMe);
console.log('Access Token:', accessToken ? 'Present' : 'Missing');
console.log('Refresh Token:', refreshToken ? 'Present' : 'Missing');
console.log('User Data:', storedUser ? 'Present' : 'Missing');
```

### Issue: App stuck on loading

**Check:**
1. Is `isLoading` stuck on `true`?
2. Check console for errors in `checkAuth()`

**Fix:**
The `finally` block should always set `isLoading` to `false`. Check if there's an error preventing this.

### Issue: Tokens present but not logging in

**Check:**
1. Token might be expired
2. Backend might have invalidated the session
3. Profile fetch might be failing

**Debug:**
```typescript
// In AuthContext checkAuth()
try {
  const profileResponse = await api.user.getProfile();
  console.log('Profile Response:', profileResponse);
} catch (error) {
  console.error('Profile Fetch Error:', error);
}
```

---

## Expected Console Output

When app starts with Remember Me enabled:

```
=== AUTH CHECK DEBUG ===
Remember Me: true
Access Token: Present
Refresh Token: Present
User Data: Present
Fetching profile...
Profile Response: { success: true, data: { user: {...} } }
✅ Auto-login successful!
```

When app starts without Remember Me:

```
=== AUTH CHECK DEBUG ===
Remember Me: false
Clearing session...
❌ Not remembered, showing login
```

---

## Quick Commands

### Check AsyncStorage (React Native Debugger)
```javascript
AsyncStorage.getAllKeys().then(keys => {
  AsyncStorage.multiGet(keys).then(data => {
    console.log('All Storage:', data);
  });
});
```

### Manually Set Remember Me
```javascript
AsyncStorage.setItem('remember_me', 'true');
```

### Clear All Storage
```javascript
AsyncStorage.clear();
```

---

## Success Criteria

✅ **Auto-Login Works:**
- Login with Remember Me checked
- Close app completely
- Reopen app
- Automatically logged in to home screen

✅ **Remember Me Toggle Works:**
- Login without Remember Me
- Close app
- Reopen app
- Shows login screen

✅ **Debug Screen Shows Correct Data:**
- Remember Me status matches checkbox
- Tokens are present when logged in
- User data is present when logged in

---

## Next Steps After Testing

Once auto-login is working:

1. **Remove the debug screen** (or hide it in production)
2. **Add biometric authentication** (optional)
3. **Add session timeout** (optional)
4. **Add token refresh** (recommended)

---

**Happy Testing! 🚀**
