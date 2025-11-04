# Define coupon values in a dictionary
coupons = {
    "CuponOne": 100,
    "CouponTwo": 200,
    "CouponThree": 300
}

price = 1000
coupon = str(input("Enter your coupon code: "))

discount = coupons.get(coupon, 0)
final_price = price - discount
print(f"Coupon applied! You get a discount of {discount}. Final price is {final_price}." if discount > 0 else "Invalid coupon code.")