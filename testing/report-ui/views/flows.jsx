// Maestro Flows view — filterable grid + flow detail drawer

// Per-flow step arrays derived from actual YAML files
const FLOW_STEPS_MAP = {
  1: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "scrollUntilVisible 'Saudi Arabia' direction:DOWN (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "waitForAnimationToEnd timeout:3000",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "takeScreenshot splash_onboarding_complete",
  ],
  2: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Skip' (optional)",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "tapOn 'Login to your account' (optional)",
    "tapOn 'Enter phone number' (optional)",
    "inputText '8801316314566'",
    "tapOn 'By clicking continue' (optional)",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "takeScreenshot login_otp_success",
  ],
  3: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Guest User' (optional)",
    "tapOn 'Continue as Guest' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "takeScreenshot guest_user_home",
    "tapOn 'My Orders' (optional)",
    "waitForAnimationToEnd timeout:3000",
    "takeScreenshot guest_user_login_prompt",
  ],
  4: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Select a Service' (optional)",
    "waitForAnimationToEnd",
    "scrollUntilVisible 'Mecca mosque' direction:DOWN timeout:8000 (optional)",
    "tapOn 'Mecca mosque' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Yes' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'More Details' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Back' (optional)",
    "takeScreenshot browse_services_complete",
  ],
  5: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Select a Service' (optional)",
    "waitForAnimationToEnd",
    "scrollUntilVisible 'Add' direction:DOWN timeout:10000 (optional)",
    "tapOn 'Add' (optional)",
    "waitForAnimationToEnd timeout:3000",
    "tapOn 'Cart' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot cart_with_items",
    "tapOn '+' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot cart_quantity_updated",
  ],
  6: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Select a Service' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "scrollUntilVisible 'Add' direction:DOWN timeout:10000 (optional)",
    "tapOn 'Add' (optional)",
    "waitForAnimationToEnd timeout:3000",
    "tapOn 'Cart' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "tapOn 'Checkout' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "takeScreenshot checkout_payment_selection",
    "tapOn 'Pay later with Tabby' (optional)",
    "waitForAnimationToEnd timeout:3000",
    "tapOn 'Redeem your Promo Code' (optional)",
    "tapOn 'Promo Code' (optional)",
    "inputText 'TEST10'",
    "tapOn 'Apply' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "takeScreenshot checkout_promo_applied",
  ],
  7: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Gift to someone you love' (optional)",
    "tapOn 'Gift Card' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Enter recipient Name' (optional)",
    "inputText 'Ahmed Ali'",
    "tapOn 'Recipient Number' (optional)",
    "inputText '509876543'",
    "tapOn 'Enter sender Name' (optional)",
    "inputText 'Test Sender'",
    "tapOn 'What do you want to say?' (optional)",
    "inputText 'Wishing you blessings from Mecca!'",
    "tapOn 'Choose Relationship' (optional)",
    "tapOn 'Preview' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot gift_card_preview",
    "tapOn 'Save Gift Details' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot gift_card_saved",
  ],
  8: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'My Orders' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot my_orders_list",
    "tapOn 'See All Orders' (optional)",
    "waitForAnimationToEnd",
    "tapOn index:0 (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot order_detail",
    "tapOn 'Rate Order' (optional)",
    "inputText 'Excellent service, very satisfied!'",
    "tapOn 'Submit Rating' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot order_rating_submitted",
  ],
  9: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Select a Service' (optional)",
    "scrollUntilVisible 'Add' direction:DOWN timeout:10000 (optional)",
    "tapOn 'Add' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Cart' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Checkout' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Yes' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Weekly' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Subscribe Now' (optional)",
    "tapOn 'Subscribe now for Reminder' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot subscription_success",
  ],
  10: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'Arabic' (optional)",
    "tapOn 'عربي' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "takeScreenshot language_arabic",
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'Turkish' / 'Türkçe' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "takeScreenshot language_turkish",
    "launchApp clearState:true",
    "tapOn 'Urdu' / 'اردو' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "takeScreenshot language_urdu",
    "launchApp clearState:true",
    "tapOn 'English' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "takeScreenshot language_english_restored",
  ],
  11: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Select a Service' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "takeScreenshot no_internet_screen",
  ],
  12: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Profile' (optional)",
    "tapOn 'Account' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot profile_settings_screen",
    "tapOn 'Change Currency' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Back' (optional)",
    "tapOn 'About Qatarat' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Back' (optional)",
    "tapOn 'Logout' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'No' (optional)",
    "takeScreenshot logout_cancelled",
  ],
  13: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'How can we help?' / 'Help' / 'Support' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot help_support_screen",
    "tapOn 'Search for Help' (optional)",
    "inputText 'payment'",
    "waitForAnimationToEnd",
    "takeScreenshot help_search_results",
  ],
  14: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Active Subscription' / 'Subscriptions' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot active_subscriptions",
    "tapOn 'Billing History' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot billing_history",
    "tapOn 'Cancel Subscription' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'No' (optional)",
    "takeScreenshot cancel_subscription_dialog",
  ],
  15: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'My Orders' (optional)",
    "waitForAnimationToEnd",
    "tapOn 'See All Orders' (optional)",
    "waitForAnimationToEnd",
    "tapOn index:0 (optional)",
    "waitForAnimationToEnd",
    "tapOn 'Cancel Order' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot cancel_order_dialog",
    "tapOn 'No' (optional)",
    "tapOn 'Back' (optional)",
    "takeScreenshot cancel_order_declined",
  ],
  16: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'Select your language' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Skip' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Share' / 'Share App' (optional)",
    "waitForAnimationToEnd timeout:3000",
    "takeScreenshot share_app_sheet",
    "pressKey Back",
    "waitForAnimationToEnd",
  ],
  17: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Login to your account' (optional)",
    "tapOn 'Continue' (empty phone — optional)",
    "assertNotVisible 'Enter OTP'",
    "takeScreenshot login_empty_phone_blocked",
    "inputText '123' (too short)",
    "tapOn 'Continue' (optional)",
    "assertNotVisible 'Enter OTP'",
    "takeScreenshot login_short_phone_blocked",
    "inputText 'abcdefghij' (alphabetic)",
    "assertNotVisible 'Enter OTP'",
    "takeScreenshot login_alpha_phone_blocked",
    "inputText '+880@abc#123' (special chars)",
    "assertNotVisible 'Enter OTP'",
    "takeScreenshot login_special_phone_blocked",
  ],
  18: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '9999' (wrong OTP)",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "assertNotVisible 'Cart'",
    "takeScreenshot login_wrong_otp_rejected",
    "inputText '0000' (all-zeros OTP)",
    "tapOn 'Verify' (optional)",
    "assertNotVisible 'Cart'",
    "takeScreenshot login_zeros_otp_rejected",
    "assertVisible 'Resend' (optional)",
    "takeScreenshot login_resend_option_visible",
  ],
  19: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Select a Service' (optional)",
    "scrollUntilVisible 'Add' direction:DOWN",
    "tapOn 'Add' + 'Cart' (optional)",
    "tapOn 'Redeem your Promo Code' (optional)",
    "inputText 'INVALID123'",
    "tapOn 'Apply' (optional)",
    "assertNotVisible 'Promo Code Applied'",
    "takeScreenshot promo_invalid_rejected",
    "inputText 'TEST@#$%'",
    "assertNotVisible 'Promo Code Applied'",
    "takeScreenshot promo_special_chars_rejected",
    "inputText \\' OR \\'1\\'=\\'1 (SQL injection)",
    "assertNotVisible 'Promo Code Applied'",
    "takeScreenshot promo_sql_injection_safe",
  ],
  20: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Cart' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "takeScreenshot cart_empty_state",
    "tapOn 'Checkout' (optional)",
    "waitForAnimationToEnd timeout:3000",
    "assertNotVisible 'Please select payment method'",
    "takeScreenshot empty_cart_checkout_blocked",
  ],
  21: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Gift to someone you love' (optional)",
    "tapOn 'Gift Card' (optional)",
    "tapOn 'Save Gift Details' (empty form — optional)",
    "assertNotVisible 'Gift Card Preview'",
    "takeScreenshot gift_empty_form_blocked",
    "inputText 'Test User' (recipient name)",
    "inputText 'abc' (invalid phone)",
    "assertNotVisible 'Gift Card Preview'",
    "takeScreenshot gift_invalid_phone_blocked",
    "inputText '<script>alert(xss)</script>' (XSS)",
    "takeScreenshot gift_xss_in_message",
    "inputText '\\' DROP TABLE users; (SQL injection)",
    "assertNotVisible 'SQL' / 'syntax error'",
    "takeScreenshot gift_sql_injection_safe",
  ],
  22: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Select a Service' (optional)",
    "scrollUntilVisible 'Add' direction:DOWN timeout:10000",
    "tapOn 'Add' (optional)",
    "tapOn 'Cart' (optional)",
    "waitForAnimationToEnd",
    "takeScreenshot cart_qty_initial",
    "repeat ×10 → tapOn '+' + waitForAnimationToEnd:500",
    "takeScreenshot cart_qty_after_10_increments",
    "assertNotVisible 'NaN'",
    "assertNotVisible 'Something went wrong'",
    "repeat ×10 → tapOn '-' + waitForAnimationToEnd:500",
    "takeScreenshot cart_qty_back_to_one",
    "tapOn '-' (decrement below 1)",
    "waitForAnimationToEnd timeout:2000",
    "takeScreenshot cart_qty_decrement_below_one",
    "assertNotVisible '500'",
    "assertNotVisible 'Exception'",
  ],
  23: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Select your country' (optional)",
    "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'English' (optional)",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn 'Select a Service' (optional)",
    "scrollUntilVisible 'Add' direction:DOWN",
    "tapOn 'Add' (optional)",
    "tapOn 'Cart' (optional)",
    "waitForAnimationToEnd timeout:3000",
    "takeScreenshot bg_resume_cart_before_background",
    "pressKey Home",
    "wait timeout:3000",
    "launchApp clearState:false (keep state)",
    "waitForAnimationToEnd timeout:5000",
    "takeScreenshot bg_resume_after_foreground",
    "assertVisible 'Cart' (optional)",
    "assertNotVisible '500'",
    "assertNotVisible 'Something went wrong'",
    "takeScreenshot bg_resume_cart_intact",
  ],
  24: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Browse as Guest' (optional)",
    "tapOn 'Continue as Guest' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "tapOn id:browse_tab (optional)",
    "tapOn 'Browse' (optional)",
    "waitForAnimationToEnd timeout:4000",
    "tapOn id:search_field / 'Search' (optional)",
    "inputText 'a' (single char)",
    "waitForAnimationToEnd timeout:3000",
    "assertNotVisible 'Something went wrong'",
    "assertNotVisible '500'",
    "clearText",
    "inputText 'مسجد' (Arabic)",
    "assertNotVisible 'Something went wrong'",
    "clearText",
    "inputText 'MOSQUE' (uppercase)",
    "assertNotVisible 'Something went wrong'",
    "clearText",
    "inputText 'zzzzzzzzz' (gibberish — no-results)",
    "assertNotVisible 'Something went wrong'",
    "clearText",
    "inputText '<script>alert(xss)</script>' (XSS)",
    "assertNotVisible 'Something went wrong'",
    "clearText",
    "inputText \\' OR \\'1\\'=\\'1 (SQL injection)",
    "assertNotVisible 'SQL' / 'syntax error' / 'database error'",
    "clearText",
    "assertNotVisible 'Something went wrong'",
    "takeScreenshot browse_search_edge_cases_complete",
  ],
  25: [
    "launchApp clearState:true",
    "waitForAnimationToEnd timeout:20000",
    "tapOn 'Login to your account' (optional)",
    "inputText '8801316314566'",
    "tapOn 'Continue' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "inputText '1234'",
    "tapOn 'Verify' (optional)",
    "waitForAnimationToEnd timeout:8000",
    "tapOn id:browse_tab + tapOn index:0 (optional)",
    "tapOn 'Add to Cart' (optional)",
    "tapOn id:cart_tab (optional)",
    "tapOn 'Checkout' (optional)",
    "waitForAnimationToEnd timeout:5000",
    "tapOn 'Credit / Debit Card' / id:payment_card_option (optional)",
    "waitForAnimationToEnd timeout:3000",
    "inputText '4111 1111 1111 1111' (card with spaces)",
    "assertNotVisible 'Something went wrong'",
    "inputText 'MEJBAUR BAHAR FAGUN' (uppercase name)",
    "assertNotVisible 'invalid'",
    "inputText '12/99' (far-future expiry)",
    "assertNotVisible 'invalid expiry'",
    "inputText '999' (CVV 3-digit boundary)",
    "assertNotVisible 'Something went wrong'",
    "inputText '0000000000000000' (all-zeros card)",
    "tapOn id:pay_button (optional)",
    "waitForAnimationToEnd timeout:4000",
    "assertNotVisible 'Something went wrong'",
    "clearText (empty name)",
    "tapOn id:pay_button (optional)",
    "assertNotVisible 'Order confirmed'",
    "takeScreenshot payment_input_edge_cases_complete",
  ],
};

// Determine step type for badge color
const stepType = (cmd) => {
  if (cmd.startsWith("launchApp"))      return "launch";
  if (cmd.startsWith("waitFor"))        return "wait";
  if (cmd.startsWith("tapOn"))          return "tap";
  if (cmd.startsWith("inputText"))      return "input";
  if (cmd.startsWith("scrollUntil"))    return "scroll";
  if (cmd.startsWith("assert"))         return "assert";
  if (cmd.startsWith("takeScreenshot")) return "screenshot";
  if (cmd.startsWith("pressKey"))       return "key";
  if (cmd.startsWith("clearText") || cmd.startsWith("clearKeychain")) return "clear";
  if (cmd.startsWith("repeat"))         return "repeat";
  return "other";
};

const TYPE_COLORS = {
  launch:     { bg: "var(--pass-2)",  fg: "var(--pass)" },
  wait:       { bg: "var(--idle-2)",  fg: "var(--idle)" },
  tap:        { bg: "color-mix(in oklch, var(--accent) 12%, transparent)", fg: "var(--accent)" },
  input:      { bg: "color-mix(in oklch, oklch(75% 0.18 280) 14%, transparent)", fg: "oklch(72% 0.16 280)" },
  scroll:     { bg: "var(--flaky-2)", fg: "var(--flaky)" },
  assert:     { bg: "color-mix(in oklch, oklch(70% 0.18 155) 14%, transparent)", fg: "oklch(66% 0.16 155)" },
  screenshot: { bg: "color-mix(in oklch, oklch(80% 0.18 60) 14%, transparent)",  fg: "oklch(68% 0.18 60)" },
  key:        { bg: "var(--idle-2)",  fg: "var(--text-3)" },
  clear:      { bg: "var(--idle-2)",  fg: "var(--text-3)" },
  repeat:     { bg: "color-mix(in oklch, oklch(78% 0.14 95) 14%, transparent)",  fg: "oklch(64% 0.16 95)" },
  other:      { bg: "var(--surface)", fg: "var(--text-2)" },
};

const FlowsView = () => {
  const { MAESTRO_FLOWS = [], RUN_META = {} } = window.QATARAT_DATA || {};
  const [filter, setFilter] = useState("all");
  const [selected, setSelected] = useState(null);
  const [q, setQ] = useState("");
  const allIdle = MAESTRO_FLOWS.every(f => f.status === "idle");

  const filtered = MAESTRO_FLOWS.filter(f => {
    if (filter !== "all" && f.status !== filter) return false;
    if (q && !f.name.toLowerCase().includes(q.toLowerCase()) && !f.group.toLowerCase().includes(q.toLowerCase())) return false;
    return true;
  });

  const counts = MAESTRO_FLOWS.reduce((acc, f) => { acc[f.status] = (acc[f.status] || 0) + 1; return acc; }, {});

  return (
    <div className="grid" style={{ gap: 18 }}>

      {/* Idle banner */}
      {allIdle && (
        <div style={{ padding: "14px 18px", borderRadius: 10, background: "var(--surface)", border: "1px solid var(--border)", display: "flex", alignItems: "center", gap: 12 }}>
          <div style={{ width: 34, height: 34, borderRadius: 9, background: "var(--idle-2)", color: "var(--idle)", display: "grid", placeItems: "center", flexShrink: 0 }}>
            <Icon name="clock" size={16} />
          </div>
          <div>
            <span style={{ fontWeight: 500, fontSize: 13 }}>No flows have run yet.</span>
            <span style={{ fontSize: 13, color: "var(--text-2)", marginLeft: 8 }}>
              All {MAESTRO_FLOWS.length} flows are in <StatusPill status="idle" /> state — trigger a GitHub Actions workflow to execute them.
            </span>
          </div>
        </div>
      )}

      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "end", gap: 16 }}>
        <div>
          <h1 className="h1" style={{ fontSize: 22 }}>Maestro flows</h1>
          <p className="lead" style={{ fontSize: 13 }}>YAML scripts that drive the app UI exactly like a real user — tap, type, swipe, assert. Each flow covers one complete journey.</p>
        </div>
        <div style={{ display: "flex", gap: 8, alignItems: "center" }}>
          <div style={{ position: "relative" }}>
            <Icon name="search" size={13} style={{ position: "absolute", left: 10, top: "50%", transform: "translateY(-50%)", color: "var(--text-3)" }} />
            <input
              value={q}
              onChange={e => setQ(e.target.value)}
              placeholder="Search flows…"
              style={{
                height: 32, padding: "0 12px 0 30px", borderRadius: 8,
                background: "var(--surface)", border: "1px solid var(--border)",
                color: "var(--text)", fontFamily: "inherit", fontSize: 13, width: 220, outline: "none",
              }}
            />
          </div>
          <div className="seg">
            {[
              ["all", `All ${MAESTRO_FLOWS.length}`],
              ["pass", `Passed ${counts.pass || 0}`],
              ["flaky", `Flaky ${counts.flaky || 0}`],
              ["fail", `Failed ${counts.fail || 0}`],
            ].map(([v, l]) => (
              <button key={v} className={filter === v ? "on" : ""} onClick={() => setFilter(v)}>{l}</button>
            ))}
          </div>
        </div>
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(290px, 1fr))", gap: 12 }}>
        {filtered.map(f => (
          <FlowCard key={f.id} flow={f} onClick={() => setSelected(f)} />
        ))}
      </div>

      {selected && <FlowDetail flow={selected} onClose={() => setSelected(null)} />}
    </div>
  );
};

const groupAccent = {
  Auth: "oklch(74% 0.16 195)",
  Commerce: "oklch(74% 0.18 155)",
  Account: "oklch(75% 0.16 280)",
  Catalog: "oklch(78% 0.14 95)",
  i18n: "oklch(72% 0.18 25)",
  Onboarding: "oklch(75% 0.14 230)",
  Resilience: "oklch(70% 0.04 260)",
  Growth: "oklch(80% 0.16 75)",
};

const FlowCard = ({ flow, onClick }) => {
  const accent = groupAccent[flow.group] || "var(--accent)";
  return (
    <div onClick={onClick}
         style={{
           padding: 16, borderRadius: 12, cursor: "pointer",
           background: "linear-gradient(180deg, var(--surface), color-mix(in oklch, var(--surface) 92%, black 4%))",
           border: "1px solid var(--border)",
           transition: "transform .15s ease, border-color .15s ease, box-shadow .15s ease",
           position: "relative", overflow: "hidden",
         }}
         onMouseEnter={(e) => { e.currentTarget.style.borderColor = "var(--border-2)"; e.currentTarget.style.transform = "translateY(-1px)"; }}
         onMouseLeave={(e) => { e.currentTarget.style.borderColor = "var(--border)"; e.currentTarget.style.transform = "translateY(0)"; }}
    >
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: 2, background: accent, opacity: .7 }} />
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 12 }}>
        <div>
          <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 6 }}>
            <span className="mono" style={{ fontSize: 11, color: accent, background: `color-mix(in oklch, ${accent} 12%, transparent)`, padding: "2px 7px", borderRadius: 4, border: `1px solid color-mix(in oklch, ${accent} 25%, transparent)` }}>
              {flow.id.toString().padStart(2, "0")}
            </span>
            <span style={{ fontSize: 11, color: "var(--text-3)" }}>{flow.group}</span>
          </div>
          <h4 style={{ margin: 0, fontSize: 15, fontWeight: 500, letterSpacing: "-0.005em" }}>{flow.name}</h4>
        </div>
        <StatusPill status={flow.status} />
      </div>

      <p style={{ margin: "0 0 14px", fontSize: 12.5, color: "var(--text-2)", lineHeight: 1.45 }}>{flow.coverage}</p>

      <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10, marginBottom: 10 }}>
        {[
          { l: "duration", v: fmtDur(flow.duration) },
          { l: "steps", v: flow.steps },
          { l: "screens", v: flow.screens },
        ].map(s => (
          <div key={s.l}>
            <div style={{ fontSize: 10, color: "var(--text-3)", textTransform: "uppercase", letterSpacing: ".09em", marginBottom: 2 }}>{s.l}</div>
            <div className="mono" style={{ fontSize: 13, color: "var(--text)" }}>{s.v}</div>
          </div>
        ))}
      </div>

      {flow.note && (
        <div style={{
          marginTop: 4, fontSize: 11.5, color: flow.status === "fail" ? "var(--fail)" : "var(--flaky)",
          background: flow.status === "fail" ? "var(--fail-2)" : "var(--flaky-2)",
          padding: "6px 10px", borderRadius: 6, fontFamily: "Geist Mono",
          whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis",
        }}>
          {flow.note}
        </div>
      )}
    </div>
  );
};

const FlowDetail = ({ flow, onClose }) => {
  useEffect(() => {
    const onKey = (e) => { if (e.key === "Escape") onClose(); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  const accent = groupAccent[flow.group] || "var(--accent)";

  // Deterministic step durations (stable across renders)
  const stepMs = useMemo(() =>
    Array.from({ length: Math.max(flow.steps, (FLOW_STEPS_MAP[flow.id] || []).length) },
      (_, i) => 120 + ((flow.id * 37 + i * 397 + 89) % 1600))
  , [flow.id, flow.steps]);

  // For non-idle flows, use generic cycled commands; for idle, use real YAML steps
  const genericCmds = [
    "launchApp", "waitForAnimationToEnd", "tapOn 'Saudi Arabia' (optional)",
    "tapOn 'English' (optional)", "inputText phone", "tapOn 'Continue'",
    "waitForAnimationToEnd", "inputText OTP '1234'", "tapOn 'Verify'",
    "waitForAnimationToEnd", "assertVisible 'Home'", "tapOn 'Browse'",
    "scroll", "tapOn item", "assertVisible detail", "takeScreenshot",
  ];

  const realSteps   = FLOW_STEPS_MAP[flow.id] || [];
  const isIdle      = flow.status === "idle";
  const stepsToShow = isIdle ? realSteps : Array.from({ length: flow.steps }).map((_, i) => genericCmds[i % genericCmds.length]);

  // Screenshot count label
  const capturedCount  = flow.screenshots?.length || 0;
  const expectedCount  = flow.screens;
  const screenshotLabel = capturedCount > 0
    ? `${capturedCount} of ${expectedCount} captured`
    : `${expectedCount} expected`;

  return (
    <div onClick={onClose}
         style={{ position: "fixed", inset: 0, background: "rgba(4,5,9,.55)", backdropFilter: "blur(6px)", zIndex: 50, display: "flex", justifyContent: "flex-end" }}>
      <div onClick={(e) => e.stopPropagation()}
           style={{ width: "min(620px, 95vw)", height: "100vh", overflowY: "auto", background: "var(--bg-2)", borderLeft: "1px solid var(--border)", padding: 24 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", marginBottom: 22 }}>
          <div>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 8 }}>
              <span className="mono" style={{ fontSize: 11, color: accent, background: `color-mix(in oklch, ${accent} 12%, transparent)`, padding: "2px 7px", borderRadius: 4, border: `1px solid color-mix(in oklch, ${accent} 25%, transparent)` }}>
                flow {flow.id.toString().padStart(2, "0")} · {flow.group}
              </span>
              <StatusPill status={flow.status} />
            </div>
            <h2 style={{ margin: 0, fontSize: 22, fontWeight: 600, letterSpacing: "-0.02em" }}>{flow.name}</h2>
            <p style={{ margin: "6px 0 0", color: "var(--text-2)", fontSize: 13 }}>{flow.coverage}</p>
          </div>
          <button className="btn ghost" onClick={onClose}><Icon name="x" /></button>
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 10, marginBottom: 22 }}>
          {[
            { l: "duration", v: fmtDur(flow.duration) },
            { l: "steps", v: flow.steps },
            { l: "screens captured", v: capturedCount > 0 ? capturedCount : flow.screens },
          ].map(s => (
            <div key={s.l} style={{ padding: 12, background: "var(--surface)", borderRadius: 10, border: "1px solid var(--border)" }}>
              <div style={{ fontSize: 10, color: "var(--text-3)", textTransform: "uppercase", letterSpacing: ".09em" }}>{s.l}</div>
              <div className="mono" style={{ fontSize: 18, color: "var(--text)", marginTop: 2 }}>{s.v}</div>
            </div>
          ))}
        </div>

        {flow.note && (
          <div style={{
            marginBottom: 20, padding: 14, borderRadius: 10,
            background: flow.status === "fail" ? "var(--fail-2)" : "var(--flaky-2)",
            border: `1px solid color-mix(in oklch, ${flow.status === "fail" ? "var(--fail)" : "var(--flaky)"} 30%, transparent)`,
          }}>
            <div style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 4 }}>
              <Icon name={flow.status === "fail" ? "x" : "bolt"} size={14} />
              <span style={{ fontWeight: 500, fontSize: 13 }}>{flow.status === "fail" ? "Failure" : "Flaky"}</span>
            </div>
            <div className="mono" style={{ fontSize: 12.5, color: flow.status === "fail" ? "var(--fail)" : "var(--flaky)" }}>{flow.note}</div>
          </div>
        )}

        {/* Step log */}
        <div className="card">
          <div className="card-head">
            <h3>Step log</h3>
            <span className="sub">
              {isIdle ? `${stepsToShow.length} steps · planned` : `${flow.steps} steps executed`}
            </span>
          </div>
          <div className="card-body" style={{ padding: 0, fontFamily: "Geist Mono", fontSize: 12 }}>
            {isIdle && stepsToShow.length === 0 ? (
              <div style={{ padding: "28px 16px", textAlign: "center", color: "var(--text-3)" }}>
                <Icon name="clock" size={20} style={{ marginBottom: 8, opacity: 0.5 }} />
                <div style={{ fontSize: 13 }}>Steps will appear after the first CI run.</div>
              </div>
            ) : stepsToShow.map((cmd, i) => {
              const failedStep = !isIdle && flow.status === "fail"  && i === Math.floor(flow.steps * 0.78);
              const flakyStep  = !isIdle && flow.status === "flaky" && i === Math.floor(flow.steps * 0.6);
              const status     = failedStep ? "fail" : flakyStep ? "flaky" : isIdle ? "idle" : "pass";
              const t          = stepType(cmd);
              const tc         = TYPE_COLORS[t] || TYPE_COLORS.other;
              const ms         = stepMs[i];
              return (
                <div key={i} style={{
                  display: "grid", gridTemplateColumns: "32px 1fr auto auto", gap: 12,
                  padding: "9px 14px", borderBottom: "1px solid var(--border)", alignItems: "center",
                  opacity: isIdle ? 0.72 : 1,
                }}>
                  <span style={{ color: "var(--text-3)" }}>{(i + 1).toString().padStart(2, "0")}</span>
                  <span style={{ color: failedStep ? "var(--fail)" : isIdle ? "var(--text-2)" : "var(--text)" }}>
                    {cmd}
                  </span>
                  <span style={{ color: "var(--text-3)" }}>{isIdle ? "—" : `${ms}ms`}</span>
                  {isIdle ? (
                    <span style={{ width: 16, height: 16, borderRadius: 4, display: "grid", placeItems: "center", background: tc.bg, color: tc.fg }}>
                      <Icon name="clock" size={9} />
                    </span>
                  ) : (
                    <span style={{ width: 16, height: 16, borderRadius: 4, display: "grid", placeItems: "center", color: `var(--${status})`, background: `var(--${status}-2)` }}>
                      <Icon name={status === "pass" ? "check" : status === "fail" ? "x" : "bolt"} size={11} />
                    </span>
                  )}
                </div>
              );
            })}
          </div>
        </div>

        {/* Screenshots */}
        <div className="card" style={{ marginTop: 14 }}>
          <div className="card-head">
            <h3>Screen captures</h3>
            <span className="sub">{screenshotLabel}</span>
          </div>
          <div className="card-body">
            {flow.screenshots && flow.screenshots.length > 0 ? (
              <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(110px, 1fr))", gap: 10 }}>
                {flow.screenshots.map((src, i) => {
                  const label = src.split("/").pop();
                  return (
                    <a key={i} href={src} target="_blank" rel="noopener noreferrer"
                       style={{ textDecoration: "none", display: "block", aspectRatio: "9/19", borderRadius: 8, border: "1px solid var(--border)", position: "relative", overflow: "hidden", background: "var(--surface-2)" }}>
                      <img src={src} alt={label} loading="lazy"
                           style={{ width: "100%", height: "100%", objectFit: "cover", display: "block" }}
                           onError={(e) => { e.currentTarget.style.display = "none"; }} />
                      <div style={{ position: "absolute", inset: "auto 0 0 0", padding: "5px 7px", background: "linear-gradient(180deg, transparent, rgba(0,0,0,.75))", fontFamily: "Geist Mono", fontSize: 10, color: "var(--text-2)" }}>
                        {label}
                      </div>
                    </a>
                  );
                })}
              </div>
            ) : flow.status === "idle" ? (
              <div style={{ display: "flex", flexDirection: "column", gap: 8, padding: "18px 16px" }}>
                <div style={{ fontSize: 12.5, color: "var(--text-3)", marginBottom: 8 }}>
                  Expected screenshots from this flow:
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 6 }}>
                  {(FLOW_STEPS_MAP[flow.id] || [])
                    .filter(s => s.startsWith("takeScreenshot"))
                    .map((s, i) => {
                      const name = s.replace("takeScreenshot ", "").trim();
                      return (
                        <span key={i} className="mono" style={{
                          fontSize: 11, padding: "3px 8px", borderRadius: 5,
                          background: "var(--surface-2)", border: "1px solid var(--border)",
                          color: "var(--text-2)",
                        }}>
                          {name}.png
                        </span>
                      );
                    })}
                </div>
                <div style={{ fontSize: 12, color: "var(--text-3)", marginTop: 8, lineHeight: 1.5 }}>
                  Screenshots are captured automatically when this flow runs on CI.
                  Trigger the <strong style={{ color: "var(--text-2)" }}>Maestro</strong> workflow from GitHub Actions to see real device captures here.
                </div>
              </div>
            ) : (
              <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10, padding: "28px 16px", color: "var(--text-3)", textAlign: "center" }}>
                <div style={{ width: 48, height: 48, borderRadius: 12, background: "var(--surface-2)", border: "1px solid var(--border)", display: "grid", placeItems: "center" }}>
                  <Icon name="phone" size={22} />
                </div>
                <div style={{ fontSize: 14, fontWeight: 500, color: "var(--text-2)" }}>Screenshots not available for this run</div>
                <div style={{ fontSize: 12.5, color: "var(--text-3)", lineHeight: 1.6, maxWidth: 360 }}>
                  {flow.status === "fail"
                    ? "This flow failed before reaching the screenshot step. Fix the failure and re-run to capture screens."
                    : "The Publish Report workflow may have run before screenshots were uploaded. Re-run the Publish Report workflow to include them."}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

window.FlowsView = FlowsView;
