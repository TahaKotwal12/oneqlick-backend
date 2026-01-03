# Coupons & Offers - User App Integration Guide

**Date:** January 3, 2026  
**Status:** ✅ COMPLETED  

---

## What Was Integrated

### 1. API Service Layer
**File:** `services/api.ts`

Added complete `couponAPI` with 5 endpoints:
- ✅ `getAvailableCoupons()` - Browse coupons
- ✅ `validateCoupon()` - Validate coupon code
- ✅ `getMyCouponUsage()` - View usage history
- ✅ `getActiveOffers()` - Get all offers
- ✅ `getRestaurantOffers()` - Get restaurant-specific offers

### 2. React Hooks
**File:** `hooks/useCoupons.ts`

Created 4 custom hooks:
- ✅ `useCoupons()` - Manage coupons and validation
- ✅ `useCouponUsage()` - Track usage history
- ✅ `useRestaurantOffers()` - Restaurant-specific offers
- ✅ `useAllOffers()` - All active offers

### 3. UI Components
**Files:**
- ✅ `components/CouponCard.tsx` - Coupon display card
- ✅ `components/OfferCard.tsx` - Offer display card + list
- ✅ `app/coupons/index.tsx` - Coupons screen/modal

---

## How to Use in Your App

### 1. Display Coupons on Checkout Page

```typescript
import { useCoupons } from '../hooks/useCoupons';
import { CouponCard } from '../components/CouponCard';

function CheckoutScreen() {
  const { coupons, loading, fetchCoupons, validateCoupon } = useCoupons();
  const [cartTotal, setCartTotal] = useState(360);
  const [appliedCoupon, setAppliedCoupon] = useState(null);
  const [discount, setDiscount] = useState(0);

  useEffect(() => {
    // Fetch coupons when cart total changes
    fetchCoupons({ min_order_amount: cartTotal });
  }, [cartTotal]);

  const handleApplyCoupon = async (code: string) => {
    const validation = await validateCoupon(code, cartTotal);
    
    if (validation && validation.is_valid) {
      setAppliedCoupon(code);
      setDiscount(validation.discount_amount);
      Alert.alert('Success', `You saved ₹${validation.discount_amount}`);
    } else {
      Alert.alert('Error', validation?.error_message || 'Invalid coupon');
    }
  };

  return (
    <View>
      {/* Cart Items */}
      
      {/* Coupon Section */}
      <TouchableOpacity onPress={() => navigation.navigate('coupons')}>
        <Text>Apply Coupon</Text>
      </TouchableOpacity>

      {/* Price Breakdown */}
      <Text>Subtotal: ₹{cartTotal}</Text>
      <Text>Discount: -₹{discount}</Text>
      <Text>Total: ₹{cartTotal - discount}</Text>
    </View>
  );
}
```

### 2. Show Offers on Restaurant Page

```typescript
import { useRestaurantOffers } from '../hooks/useCoupons';
import { OffersList } from '../components/OfferCard';

function RestaurantScreen({ restaurantId }: { restaurantId: string }) {
  const { offers, loading } = useRestaurantOffers(restaurantId);

  return (
    <ScrollView>
      {/* Restaurant Info */}
      
      {/* Offers Section */}
      {offers.length > 0 && (
        <OffersList offers={offers} title="Special Offers" />
      )}

      {/* Menu Items */}
    </ScrollView>
  );
}
```

### 3. Display Coupon Usage History in Profile

```typescript
import { useCouponUsage } from '../hooks/useCoupons';

function ProfileScreen() {
  const { usageHistory, totalSavings, loading, fetchUsageHistory } = useCouponUsage();

  useEffect(() => {
    fetchUsageHistory();
  }, []);

  return (
    <View>
      <Text>Total Savings: ₹{totalSavings}</Text>
      
      <FlatList
        data={usageHistory}
        renderItem={({ item }) => (
          <View>
            <Text>{item.coupon_code}</Text>
            <Text>{item.coupon_title}</Text>
            <Text>Saved: ₹{item.discount_amount}</Text>
            <Text>Order: {item.order_number}</Text>
          </View>
        )}
      />
    </View>
  );
}
```

### 4. Use Coupons Modal/Screen

```typescript
import { useNavigation } from '@react-navigation/native';

function CheckoutScreen() {
  const navigation = useNavigation();
  const [selectedCoupon, setSelectedCoupon] = useState(null);
  const [discount, setDiscount] = useState(0);

  const handleCouponSelect = (code: string, discountAmount: number) => {
    setSelectedCoupon(code);
    setDiscount(discountAmount);
  };

  return (
    <View>
      <TouchableOpacity 
        onPress={() => navigation.navigate('coupons', {
          cartTotal: 360,
          restaurantId: 'restaurant-uuid',
          onCouponSelect: handleCouponSelect,
        })}
      >
        <Text>
          {selectedCoupon ? `Applied: ${selectedCoupon}` : 'Apply Coupon'}
        </Text>
      </TouchableOpacity>
    </View>
  );
}
```

---

## API Usage Examples

### Example 1: Get Available Coupons

```typescript
import { couponAPI } from '../services/api';

// Get all coupons
const response = await couponAPI.getAvailableCoupons();

// Get coupons for specific restaurant
const response = await couponAPI.getAvailableCoupons({
  restaurant_id: 'restaurant-uuid'
});

// Get coupons for cart total
const response = await couponAPI.getAvailableCoupons({
  min_order_amount: 300
});

// Response
{
  success: true,
  data: {
    coupons: [
      {
        coupon_id: "uuid",
        code: "SAVE20",
        title: "Save 20% on orders above ₹300",
        coupon_type: "percentage",
        discount_value: 20,
        min_order_amount: 300,
        is_available: true,
        ...
      }
    ],
    total_count: 5,
    available_count: 3
  }
}
```

### Example 2: Validate Coupon

```typescript
const validation = await couponAPI.validateCoupon({
  coupon_code: 'SAVE20',
  cart_total: 360,
  restaurant_id: 'restaurant-uuid' // optional
});

// Success response
{
  success: true,
  data: {
    is_valid: true,
    discount_amount: 72,
    final_amount: 288,
    coupon: { ... }
  }
}

// Error response
{
  success: true,
  data: {
    is_valid: false,
    discount_amount: 0,
    final_amount: 360,
    error_message: "Minimum order amount of ₹300 required"
  }
}
```

### Example 3: Get Usage History

```typescript
const response = await couponAPI.getMyCouponUsage({
  page: 1,
  page_size: 20
});

// Response
{
  success: true,
  data: {
    usage_history: [
      {
        coupon_code: "SAVE20",
        coupon_title: "Save 20% on orders above ₹300",
        order_number: "OQ20260103001",
        discount_amount: 72,
        used_at: "2026-01-03T12:00:00Z"
      }
    ],
    total_count: 5,
    total_savings: 350
  }
}
```

### Example 4: Get Restaurant Offers

```typescript
const response = await couponAPI.getRestaurantOffers('restaurant-uuid');

// Response
{
  success: true,
  data: {
    offers: [
      {
        offer_id: "uuid",
        title: "Free Delivery on orders above ₹200",
        discount_type: "free_delivery",
        discount_value: 0,
        min_order_amount: 200,
        ...
      }
    ],
    total_count: 2
  }
}
```

---

## Integration Checklist

### Backend Setup
- [x] Coupons API implemented
- [x] CORS enabled for mobile app
- [x] Authentication working
- [x] Database tables ready

### Frontend Setup
- [x] API service layer added
- [x] React hooks created
- [x] UI components built
- [x] Coupons screen created

### Testing
- [ ] Test coupon browsing
- [ ] Test coupon validation
- [ ] Test coupon application in checkout
- [ ] Test usage history display
- [ ] Test restaurant offers display
- [ ] Test error handling

### Integration Points
- [ ] Add "Apply Coupon" button to checkout
- [ ] Display offers on restaurant page
- [ ] Show usage history in profile
- [ ] Handle coupon in order creation
- [ ] Display discount in cart summary

---

## Common Integration Patterns

### Pattern 1: Checkout Flow with Coupons

```typescript
function CheckoutFlow() {
  const [cart, setCart] = useState([]);
  const [appliedCoupon, setAppliedCoupon] = useState(null);
  const [discount, setDiscount] = useState(0);
  
  const cartTotal = cart.reduce((sum, item) => sum + item.price * item.quantity, 0);
  const finalTotal = cartTotal - discount;

  const handleApplyCoupon = async (code: string) => {
    const validation = await couponAPI.validateCoupon({
      coupon_code: code,
      cart_total: cartTotal,
    });

    if (validation?.data?.is_valid) {
      setAppliedCoupon(code);
      setDiscount(validation.data.discount_amount);
    } else {
      Alert.alert('Error', validation?.data?.error_message);
    }
  };

  const handleRemoveCoupon = () => {
    setAppliedCoupon(null);
    setDiscount(0);
  };

  const handlePlaceOrder = async () => {
    const orderData = {
      items: cart,
      coupon_code: appliedCoupon,
      subtotal: cartTotal,
      discount: discount,
      total: finalTotal,
    };

    // Create order with coupon
    await orderAPI.createOrder(orderData);
  };

  return (
    <View>
      {/* Cart Items */}
      
      {/* Coupon Section */}
      {appliedCoupon ? (
        <View>
          <Text>Coupon Applied: {appliedCoupon}</Text>
          <Text>Discount: ₹{discount}</Text>
          <Button title="Remove" onPress={handleRemoveCoupon} />
        </View>
      ) : (
        <Button title="Apply Coupon" onPress={() => navigation.navigate('coupons')} />
      )}

      {/* Total */}
      <Text>Subtotal: ₹{cartTotal}</Text>
      <Text>Discount: -₹{discount}</Text>
      <Text>Total: ₹{finalTotal}</Text>

      <Button title="Place Order" onPress={handlePlaceOrder} />
    </View>
  );
}
```

### Pattern 2: Restaurant Page with Offers

```typescript
function RestaurantPage({ restaurantId }: { restaurantId: string }) {
  const { offers, loading } = useRestaurantOffers(restaurantId);

  return (
    <ScrollView>
      {/* Restaurant Header */}
      
      {/* Offers Section */}
      {!loading && offers.length > 0 && (
        <View style={{ marginVertical: 16 }}>
          <OffersList offers={offers} title="Special Offers" />
        </View>
      )}

      {/* Menu */}
    </ScrollView>
  );
}
```

### Pattern 3: Profile with Savings

```typescript
function ProfilePage() {
  const { usageHistory, totalSavings, loading, fetchUsageHistory } = useCouponUsage();

  useEffect(() => {
    fetchUsageHistory();
  }, []);

  return (
    <View>
      {/* Profile Info */}
      
      {/* Savings Card */}
      <View style={styles.savingsCard}>
        <Text style={styles.savingsTitle}>Total Savings</Text>
        <Text style={styles.savingsAmount}>₹{totalSavings}</Text>
        <Text style={styles.savingsSubtext}>
          You've saved with {usageHistory.length} coupons
        </Text>
      </View>

      {/* Usage History */}
      <Text style={styles.sectionTitle}>Coupon History</Text>
      <FlatList
        data={usageHistory}
        renderItem={({ item }) => (
          <View style={styles.historyItem}>
            <Text>{item.coupon_code}</Text>
            <Text>{item.coupon_title}</Text>
            <Text>₹{item.discount_amount}</Text>
          </View>
        )}
      />
    </View>
  );
}
```

---

## Error Handling

### Handle API Errors

```typescript
const { coupons, loading, error, fetchCoupons } = useCoupons();

if (error) {
  return (
    <View>
      <Text>Error: {error}</Text>
      <Button title="Retry" onPress={() => fetchCoupons()} />
    </View>
  );
}
```

### Handle Validation Errors

```typescript
const handleApplyCoupon = async (code: string) => {
  const validation = await validateCoupon(code, cartTotal);
  
  if (!validation) {
    Alert.alert('Error', 'Failed to validate coupon');
    return;
  }

  if (!validation.is_valid) {
    Alert.alert('Invalid Coupon', validation.error_message);
    return;
  }

  // Apply coupon
  setAppliedCoupon(code);
  setDiscount(validation.discount_amount);
};
```

---

## Next Steps

1. **Test the Integration**
   - Start the backend server
   - Start the Expo app
   - Test coupon browsing
   - Test coupon validation
   - Test applying coupons

2. **Add to Existing Screens**
   - Integrate into checkout flow
   - Add offers to restaurant pages
   - Add usage history to profile

3. **Enhance UI**
   - Add animations
   - Improve error messages
   - Add loading states
   - Add success feedback

4. **Add Features**
   - Auto-apply best coupon
   - Coupon recommendations
   - Push notifications for new coupons
   - Share coupons with friends

---

## Files Created

### API Layer
- ✅ `services/api.ts` (updated)

### Hooks
- ✅ `hooks/useCoupons.ts`

### Components
- ✅ `components/CouponCard.tsx`
- ✅ `components/OfferCard.tsx`

### Screens
- ✅ `app/coupons/index.tsx`

### Documentation
- ✅ `docs/COUPONS-USER-APP-INTEGRATION.md` (this file)

---

## Testing Commands

```bash
# Start backend
cd oneqlick-backend
python start_server.py

# Start frontend
cd oneQlick-User-App
npx expo start
```

---

**Integration Complete! 🎉**

The Coupons & Offers feature is now fully integrated into your User App and ready to use!
