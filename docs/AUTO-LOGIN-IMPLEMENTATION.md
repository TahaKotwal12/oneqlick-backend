# Remember Me / Auto-Login Implementation Guide

**Date:** January 4, 2026  
**Feature:** Automatic login when app reopens  

---

## ✅ What Was Implemented

### 1. AuthContext (`contexts/AuthContext.tsx`)
A React Context that manages authentication state across the entire app with:
- **Auto-login on app start**
- **Remember me functionality**
- **Token validation**
- **Offline support**

### 2. Root Layout Integration (`app/_layout.tsx`)
Wrapped the entire app with `AuthProvider` to enable global authentication state.

---

## 🔑 How It Works

### App Start Flow

```
1. App Opens
   ↓
2. AuthProvider mounts
   ↓
3. checkAuth() runs automatically
   ↓
4. Check "remember_me" preference
   ↓
5. If remember_me = true:
   - Get stored tokens
   - Get stored user data
   - Verify token by fetching profile
   - If valid: Auto-login ✅
   - If invalid: Clear session
   ↓
6. If remember_me = false:
   - Clear all data
   - Show login screen
```

---

## 📱 Usage in Your App

### 1. Update Login Screen

Add remember me checkbox and use the AuthContext:

```typescript
import { useAuth } from '../contexts/AuthContext';
import { useState } from 'react';

function LoginScreen() {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [rememberMe, setRememberMe] = useState(true); // Default to true
  
  const handleLogin = async () => {
    try {
      // Call your existing login API
      const response = await api.auth.login(email, password);
      
      if (response.success && response.data) {
        // Use AuthContext login with remember me preference
        await login(
          response.data.user,
          response.data.tokens.access_token,
          response.data.tokens.refresh_token,
          rememberMe  // Pass remember me preference
        );
        
        // Navigation will happen automatically via AuthContext
      }
    } catch (error) {
      Alert.alert('Error', 'Login failed');
    }
  };

  return (
    <View>
      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
      />
      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
      />
      
      {/* Remember Me Checkbox */}
      <View style={{ flexDirection: 'row', alignItems: 'center' }}>
        <Checkbox
          value={rememberMe}
          onValueChange={setRememberMe}
        />
        <Text>Remember Me</Text>
      </View>
      
      <Button title="Login" onPress={handleLogin} />
    </View>
  );
}
```

### 2. Protect Routes with Auth Check

```typescript
import { useAuth } from '../contexts/AuthContext';
import { useRouter } from 'expo-router';
import { useEffect } from 'react';

function ProtectedScreen() {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      // Redirect to login if not authenticated
      router.replace('/(auth)/login');
    }
  }, [isAuthenticated, isLoading]);

  if (isLoading) {
    return <LoadingScreen />;
  }

  if (!isAuthenticated) {
    return null; // Will redirect
  }

  return (
    <View>
      {/* Your protected content */}
    </View>
  );
}
```

### 3. Use Auth State Anywhere

```typescript
import { useAuth } from '../contexts/AuthContext';

function ProfileScreen() {
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    // User will be redirected to login automatically
  };

  return (
    <View>
      <Text>Welcome, {user?.name}!</Text>
      <Text>{user?.email}</Text>
      <Button title="Logout" onPress={handleLogout} />
    </View>
  );
}
```

### 4. Check Auth Status in Root Navigator

```typescript
// app/(tabs)/_layout.tsx or similar
import { useAuth } from '../../contexts/AuthContext';
import { Redirect } from 'expo-router';

export default function TabsLayout() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <SplashScreen />;
  }

  if (!isAuthenticated) {
    return <Redirect href="/(auth)/login" />;
  }

  return (
    <Tabs>
      {/* Your tabs */}
    </Tabs>
  );
}
```

---

## 🎯 Key Features

### ✅ Auto-Login
- User logs in once with "Remember Me" checked
- App closes
- User reopens app
- **Automatically logged in!** No need to enter credentials again

### ✅ Token Validation
- On app start, checks if token is still valid
- Fetches latest user profile to verify
- If token expired, clears session and shows login

### ✅ Offline Support
- If network is unavailable, uses cached user data
- User can still access the app with stored data
- Profile updates when network returns

### ✅ Remember Me Toggle
- Users can choose to be remembered or not
- If unchecked, session clears on app close
- If checked, stays logged in indefinitely

---

## 🔐 Security Considerations

### Current Implementation
- Tokens stored in AsyncStorage (encrypted on iOS, less secure on Android)
- Remember me enabled by default
- No automatic token refresh (yet)

### Recommended Improvements

1. **Add Biometric Authentication**
```typescript
import * as LocalAuthentication from 'expo-local-authentication';

const authenticateWithBiometrics = async () => {
  const hasHardware = await LocalAuthentication.hasHardwareAsync();
  const isEnrolled = await LocalAuthentication.isEnrolledAsync();
  
  if (hasHardware && isEnrolled) {
    const result = await LocalAuthentication.authenticateAsync({
      promptMessage: 'Authenticate to access your account',
    });
    return result.success;
  }
  return false;
};
```

2. **Add Token Refresh**
```typescript
// In AuthContext, add automatic token refresh
useEffect(() => {
  const refreshInterval = setInterval(async () => {
    if (isAuthenticated) {
      // Refresh token every 30 minutes
      await refreshAccessToken();
    }
  }, 30 * 60 * 1000);

  return () => clearInterval(refreshInterval);
}, [isAuthenticated]);
```

3. **Add Session Timeout**
```typescript
// Auto-logout after 30 days of inactivity
const SESSION_TIMEOUT = 30 * 24 * 60 * 60 * 1000; // 30 days

const checkSessionTimeout = async () => {
  const lastActivity = await AsyncStorage.getItem('last_activity');
  if (lastActivity) {
    const timeSinceLastActivity = Date.now() - parseInt(lastActivity);
    if (timeSinceLastActivity > SESSION_TIMEOUT) {
      await logout();
    }
  }
};
```

---

## 📝 Storage Keys

The following keys are used in AsyncStorage:

| Key | Description | Example Value |
|-----|-------------|---------------|
| `access_token` | JWT access token | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `refresh_token` | JWT refresh token | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` |
| `user_data` | Serialized user object | `{"user_id":"123","name":"John","email":"john@example.com"}` |
| `remember_me` | Remember me preference | `"true"` or `"false"` |

---

## 🧪 Testing

### Test Auto-Login

1. **Login with Remember Me**
   ```
   - Open app
   - Login with email/password
   - Check "Remember Me"
   - Close app completely
   - Reopen app
   - ✅ Should be automatically logged in
   ```

2. **Login without Remember Me**
   ```
   - Open app
   - Login with email/password
   - Uncheck "Remember Me"
   - Close app completely
   - Reopen app
   - ✅ Should show login screen
   ```

3. **Token Expiration**
   ```
   - Login with Remember Me
   - Wait for token to expire (or manually delete from backend)
   - Reopen app
   - ✅ Should show login screen
   ```

4. **Offline Access**
   ```
   - Login with Remember Me
   - Turn off network
   - Close and reopen app
   - ✅ Should still be logged in with cached data
   ```

---

## 🐛 Troubleshooting

### Issue: User not auto-logging in

**Check:**
1. Is `remember_me` set to `"true"` in AsyncStorage?
2. Are tokens present in AsyncStorage?
3. Is user data present in AsyncStorage?
4. Check console for errors in `checkAuth()`

**Debug:**
```typescript
// Add to AuthContext checkAuth()
console.log('Remember Me:', await AsyncStorage.getItem('remember_me'));
console.log('Access Token:', await tokenManager.getAccessToken());
console.log('User Data:', await AsyncStorage.getItem('user_data'));
```

### Issue: App stuck on loading screen

**Check:**
1. Is `isLoading` state being set to `false`?
2. Is there an error in `checkAuth()`?

**Fix:**
```typescript
// Ensure isLoading is always set to false
finally {
  setIsLoading(false);
}
```

### Issue: User logged out unexpectedly

**Check:**
1. Token might have expired
2. Backend might have invalidated the session
3. User might have logged out from another device

---

## 📚 API Reference

### useAuth Hook

```typescript
const {
  user,              // Current user object or null
  isAuthenticated,   // Boolean: is user logged in?
  isLoading,         // Boolean: is auth check in progress?
  login,             // Function: login user
  logout,            // Function: logout user
  updateUser,        // Function: update user data
  checkAuth,         // Function: manually check auth status
} = useAuth();
```

### login()

```typescript
await login(
  user: User,                    // User object from API
  accessToken: string,           // JWT access token
  refreshToken: string,          // JWT refresh token
  rememberMe: boolean = true     // Remember me preference
);
```

### logout()

```typescript
await logout();
// Clears all stored data and calls backend logout API
```

### updateUser()

```typescript
await updateUser(updatedUser: User);
// Updates stored user data
```

---

## 🎉 Summary

**What you get:**
✅ Auto-login when app reopens  
✅ Remember me toggle  
✅ Token validation  
✅ Offline support  
✅ Global auth state  
✅ Easy to use hooks  

**Next steps:**
1. Update your login screen to use `useAuth()`
2. Add remember me checkbox
3. Protect routes with auth checks
4. Test the auto-login flow

**Your users will love:**
- No need to login every time
- Seamless app experience
- Fast app startup
- Works offline

---

**Implementation Complete! 🚀**
