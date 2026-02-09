# Food Items API - Restaurant Offers Integration

**Date:** January 4, 2026  
**Update:** Added restaurant offers to food item details API

---

## What Changed

### Backend Update
**File:** `app/api/routes/food_items.py`

✅ **Added restaurant offers** to the food item details endpoint (`GET /food-items/{id}`)

Now when you fetch a food item with `include_restaurant=true`, the response automatically includes:
- Restaurant details
- **Active restaurant offers** (NEW!)

---

## Updated API Response

### Before (Without Offers)
```json
{
  "restaurant": {
    "restaurant_id": "...",
    "name": "Dhaba Express",
    "rating": 4.4,
    ...
  }
}
```

### After (With Offers) ✅
```json
{
  "restaurant": {
    "restaurant_id": "...",
    "name": "Dhaba Express",
    "rating": 4.4,
    ...,
    "offers": [
      {
        "offer_id": "uuid",
        "title": "20% off on orders above ₹500",
        "description": "Special weekend offer",
        "discount_type": "percentage",
        "discount_value": 20.0,
        "min_order_amount": 500.0,
        "max_discount_amount": 150.0,
        "valid_from": "2026-01-01T00:00:00Z",
        "valid_until": "2026-01-31T23:59:59Z",
        "is_active": true
      }
    ]
  }
}
```

---

## Offer Filtering Logic

The API automatically filters offers to show only:
✅ Active offers (`is_active = true`)  
✅ Currently valid (between `valid_from` and `valid_until`)  
✅ Not expired

---

## Usage in User App

### Automatic - No Changes Needed!

When you fetch a food item, offers are now automatically included:

```typescript
// Existing code - no changes needed
const response = await foodAPI.getFoodItemById(foodItemId);

// Offers are now available
const offers = response.data.restaurant?.offers || [];

console.log('Available offers:', offers);
```

### Display Offers in UI

```typescript
import { OffersList } from '../components/OfferCard';

function FoodItemDetailsScreen({ foodItemId }) {
  const [foodItem, setFoodItem] = useState(null);
  
  useEffect(() => {
    const fetchData = async () => {
      const response = await foodAPI.getFoodItemById(foodItemId);
      setFoodItem(response.data);
    };
    fetchData();
  }, [foodItemId]);

  return (
    <ScrollView>
      {/* Food Item Details */}
      <Text>{foodItem?.name}</Text>
      <Image source={{ uri: foodItem?.image }} />
      <Text>₹{foodItem?.price}</Text>
      
      {/* Restaurant Offers - Now Available! */}
      {foodItem?.restaurant?.offers?.length > 0 && (
        <View style={{ marginVertical: 16 }}>
          <OffersList 
            offers={foodItem.restaurant.offers} 
            title={`Offers from ${foodItem.restaurant.name}`}
          />
        </View>
      )}
      
      {/* Add to Cart */}
      <Button title="Add to Cart" />
    </ScrollView>
  );
}
```

---

## TypeScript Types (Optional Update)

If you want type safety, update your food item interface:

```typescript
// types/api.ts or wherever you define types

interface RestaurantOffer {
  offer_id: string;
  title: string;
  description?: string;
  discount_type: 'percentage' | 'fixed_amount' | 'free_delivery';
  discount_value: number;
  min_order_amount?: number;
  max_discount_amount?: number;
  valid_from: string;
  valid_until: string;
  is_active: boolean;
}

interface Restaurant {
  restaurant_id: string;
  name: string;
  description?: string;
  cuisine_type?: string;
  image?: string;
  rating: number;
  total_ratings: number;
  avg_delivery_time?: number;
  delivery_fee: number;
  min_order_amount: number;
  is_open: boolean;
  is_veg: boolean;
  is_pure_veg: boolean;
  phone?: string;
  email?: string;
  address_line1?: string;
  address_line2?: string;
  city?: string;
  state?: string;
  postal_code?: string;
  latitude: number;
  longitude: number;
  offers?: RestaurantOffer[];  // NEW!
}

interface FoodItem {
  food_item_id: string;
  name: string;
  description?: string;
  price: number;
  discount_price?: number;
  image?: string;
  is_veg: boolean;
  rating: number;
  total_ratings: number;
  restaurant?: Restaurant;  // Now includes offers!
  category?: Category;
  customizations?: Customizations;
  // ... other fields
}
```

---

## Testing

### Test the Updated API

```bash
# Get food item details
curl http://localhost:8001/api/v1/food-items/{food_item_id}?include_restaurant=true

# Response will now include offers in restaurant object
```

### Expected Response Structure

```json
{
  "code": 200,
  "message": "Food item details retrieved successfully",
  "message_id": "FOOD_ITEM_DETAILS_SUCCESS",
  "data": {
    "food_item_id": "...",
    "name": "Tandoori Chicken",
    "price": 380,
    "restaurant": {
      "restaurant_id": "...",
      "name": "Dhaba Express",
      "offers": [
        {
          "offer_id": "...",
          "title": "20% off",
          "discount_type": "percentage",
          "discount_value": 20,
          "min_order_amount": 500
        }
      ]
    }
  }
}
```

---

## Benefits

✅ **No Extra API Calls** - Offers come with food item details  
✅ **Always Up-to-Date** - Only shows currently valid offers  
✅ **Better UX** - Users see offers immediately on food item page  
✅ **Consistent** - Same offer format as other endpoints  

---

## Performance

- **Minimal Impact** - Single additional query per food item request
- **Filtered** - Only active, valid offers are fetched
- **Cached** - Can be cached on frontend if needed

---

## Migration Notes

### For Existing Code

**No breaking changes!** 

- If you were fetching offers separately, you can continue to do so
- If you want to use the new integrated offers, they're available in `restaurant.offers`
- The offers field is optional, so old code won't break

### Recommended Approach

Use the integrated offers for:
- Food item detail pages
- Quick offer display

Use separate coupon API for:
- Checkout page (all available coupons)
- Coupon browsing page
- Coupon validation

---

## Summary

✅ **Backend Updated** - Food items API now includes restaurant offers  
✅ **Automatic** - No changes needed in existing API calls  
✅ **Type-Safe** - TypeScript types provided  
✅ **Tested** - Works with existing data  

**Next:** Test the updated API and display offers in your food item screens!
