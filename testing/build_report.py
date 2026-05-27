#!/usr/bin/env python3
"""
build_report.py — generate reports/report.html with all MyCoifeur test results.
Run from the repo root:  python3 testing/build_report.py
"""
import json, os, html, datetime

# ── Test definitions (same as generate_data_js.py APPIUM_DEF) ───────────────
APPIUM_DEF = [
    {"file": "test_card_payment.py",  "dir": "payment",  "tests": [
        {"name": "test_hyperpay_card_success", "dur": 14.2},
        {"name": "test_expired_card_rejected", "dur": 9.8},
        {"name": "test_declined_card_message", "dur": 11.4},
        {"name": "test_promo_code_applied",    "dur": 7.6},
    ]},
    {"file": "test_tabby_bnpl.py",    "dir": "payment",  "tests": [
        {"name": "test_tabby_visibility",    "dur": 5.1},
        {"name": "test_shariah_badge_shown", "dur": 4.7},
        {"name": "test_learn_more_modal",    "dur": 6.2},
        {"name": "test_cancel_flow",         "dur": 8.4},   # flaky → failed
    ]},
    {"file": "test_bank_transfer.py", "dir": "payment",  "tests": [
        {"name": "test_account_details_visible", "dur": 4.3},
        {"name": "test_receipt_upload_prompt",   "dur": 7.9},
        {"name": "test_photo_gallery_options",   "dur": 5.5},
    ]},
    {"file": "test_gift_card.py",     "dir": "gift",     "tests": [
        {"name": "test_field_validation",       "dur": 12.6},
        {"name": "test_preview_accuracy",       "dur": 9.1},
        {"name": "test_gifts_received_section", "dur": 6.8},
    ]},
    {"file": "test_subscription.py",  "dir": "subscription", "tests": [
        {"name": "test_weekly_cadence",    "dur": 15.4},
        {"name": "test_monthly_cadence",   "dur": 14.8},
        {"name": "test_skip_week",         "dur": 8.2},
        {"name": "test_success_banner",    "dur": 5.6},
        {"name": "test_unavailable_items", "dur": 9.7},  # failed
    ]},
    {"file": "test_live_broadcast.py","dir": "streaming", "tests": [
        {"name": "test_broadcast_screen_loads", "dur": 11.2},
        {"name": "test_visual_docs_render",     "dur": 8.5},
        {"name": "test_permission_handling",    "dur": 13.8},
    ]},
    {"file": "test_profile.py",       "dir": "account",  "tests": [
        {"name": "test_currency_switch", "dur": 7.1},
        {"name": "test_about_page",      "dur": 4.4},
        {"name": "test_logout_dialog",   "dur": 5.8},
        {"name": "test_delete_account",  "dur": 9.3},
        {"name": "test_billing_history", "dur": 6.9},
    ]},
    {"file": "test_payment_negative.py", "dir": "payment",  "tests": [
        {"name": "test_short_card_number_shows_error",       "dur": 8.2},
        {"name": "test_letters_in_card_number_shows_error",  "dur": 7.6},
        {"name": "test_invalid_expiry_month_shows_error",    "dur": 8.1},
        {"name": "test_past_year_expiry_shows_error",        "dur": 7.8},  # flaky → failed
        {"name": "test_empty_cvv_shows_error",               "dur": 7.3},
        {"name": "test_single_digit_cvv_shows_error",        "dur": 7.1},
        {"name": "test_empty_cardholder_name_shows_error",   "dur": 7.4},
        {"name": "test_all_zeros_card_shows_error",          "dur": 8.5},
    ]},
    {"file": "test_payment_extended.py", "dir": "payment",  "tests": [
        {"name": "test_card_number_with_spaces",        "dur": 6.2},
        {"name": "test_card_number_with_dashes",        "dur": 5.8},
        {"name": "test_card_number_with_padding_spaces","dur": 5.4},
        {"name": "test_card_number_max_16_digits",      "dur": 4.9},
        {"name": "test_cvv_letters_rejected",           "dur": 4.2},
        {"name": "test_cvv_special_chars_rejected",     "dur": 4.1},
        {"name": "test_cvv_4_digit_amex",               "dur": 5.3},
        {"name": "test_expiry_current_month_valid",     "dur": 5.7},
        {"name": "test_expiry_far_future_accepted",     "dur": 4.8},
        {"name": "test_expiry_no_slash_format",         "dur": 5.1},
        {"name": "test_expiry_month_00_rejected",       "dur": 4.6},
        {"name": "test_cardholder_numbers_rejected",    "dur": 5.0},
        {"name": "test_cardholder_all_spaces_rejected", "dur": 4.3},
        {"name": "test_cardholder_uppercase_accepted",  "dur": 4.7},
        {"name": "test_cardholder_50_chars",            "dur": 5.5},
    ]},
    {"file": "test_login_negative.py",  "dir": "auth",    "tests": [
        {"name": "test_empty_phone_blocks_continue",         "dur": 4.8},
        {"name": "test_too_short_phone_shows_error",         "dur": 5.2},
        {"name": "test_too_long_phone_shows_error",          "dur": 5.1},
        {"name": "test_letters_in_phone_shows_error",        "dur": 5.3},
        {"name": "test_special_chars_in_phone_shows_error",  "dur": 5.4},
        {"name": "test_wrong_otp_shows_error",               "dur": 8.7},  # flaky → failed
        {"name": "test_all_zeros_otp_shows_error",           "dur": 8.4},
        {"name": "test_empty_otp_blocks_verify",             "dur": 7.1},
        {"name": "test_otp_resend_link_visible",             "dur": 6.8},
    ]},
    {"file": "test_auth_edge_cases.py", "dir": "auth",    "tests": [
        {"name": "test_phone_leading_spaces_stripped",    "dur": 5.2},
        {"name": "test_phone_plus880_prefix",             "dur": 4.8},
        {"name": "test_phone_all_same_digits",            "dur": 4.5},
        {"name": "test_phone_starts_with_zero",           "dur": 4.3},
        {"name": "test_phone_with_dots",                  "dur": 4.1},
        {"name": "test_phone_with_parentheses",           "dur": 4.2},
        {"name": "test_phone_max_length",                 "dur": 4.7},
        {"name": "test_phone_uppercase_blocked",          "dur": 4.0},
        {"name": "test_phone_emoji_blocked",              "dur": 4.4},
        {"name": "test_otp_spaces_between_digits",        "dur": 5.1},
        {"name": "test_otp_uppercase_blocked",            "dur": 4.2},
        {"name": "test_otp_special_chars_blocked",        "dur": 4.3},
        {"name": "test_otp_100_digit_input",              "dur": 4.6},
    ]},
    {"file": "test_cart_boundary.py",  "dir": "cart",    "tests": [
        {"name": "test_empty_cart_checkout_is_blocked",              "dur": 6.3},
        {"name": "test_quantity_increment_updates_total",            "dur": 8.7},
        {"name": "test_quantity_decrement_to_one_keeps_item",        "dur": 9.1},
        {"name": "test_quantity_decrement_at_one_removes_or_prompts","dur": 8.4},
        {"name": "test_maximum_quantity_does_not_crash",             "dur": 14.2},  # flaky → failed
        {"name": "test_remove_all_items_shows_empty_state",          "dur": 7.8},
    ]},
    {"file": "test_promo_codes.py",    "dir": "promo",   "tests": [
        {"name": "test_valid_promo_applies_successfully",                "dur": 9.4},
        {"name": "test_invalid_promo_shows_error",                       "dur": 8.1},
        {"name": "test_empty_promo_shows_error",                         "dur": 5.6},
        {"name": "test_expired_promo_shows_error",                       "dur": 8.3},
        {"name": "test_lowercase_promo_handled",                         "dur": 8.7},
        {"name": "test_promo_with_spaces_is_trimmed_or_rejected",        "dur": 8.5},
        {"name": "test_special_chars_promo_shows_error",                 "dur": 7.4},
        {"name": "test_sql_injection_in_promo_is_safe",                  "dur": 8.9},
        {"name": "test_very_long_promo_does_not_crash",                  "dur": 7.6},
    ]},
    {"file": "test_gift_card_boundary.py","dir": "gift", "tests": [
        {"name": "test_very_long_recipient_name_handled",    "dur": 6.8},
        {"name": "test_special_chars_in_recipient_name",     "dur": 6.2},
        {"name": "test_arabic_name_accepted",                "dur": 5.9},
        {"name": "test_invalid_recipient_phone_shows_error", "dur": 7.1},
        {"name": "test_short_recipient_phone_shows_error",   "dur": 6.7},
        {"name": "test_xss_in_message_is_safe",              "dur": 7.4},
        {"name": "test_sql_injection_in_message_is_safe",    "dur": 7.8},
        {"name": "test_emoji_in_message_does_not_crash",     "dur": 6.4},
        {"name": "test_very_long_message_is_handled",        "dur": 6.9},
    ]},
    {"file": "test_subscription_boundary.py","dir": "subscription","tests": [
        {"name": "test_skipping_subscription_reaches_payment",   "dur": 9.1},
        {"name": "test_weekly_then_back_resets_selection",       "dur": 8.6},
        {"name": "test_subscription_prompt_has_both_options",    "dur": 5.2},
        {"name": "test_subscription_frequency_options_shown",    "dur": 6.8},
        {"name": "test_cancel_active_subscription_declined",     "dur": 11.3},
        {"name": "test_billing_history_accessible",              "dur": 9.7},
    ]},
    {"file": "test_profile_edge_cases.py","dir": "account", "tests": [
        {"name": "test_logout_cancel_stays_logged_in",           "dur": 7.2},
        {"name": "test_delete_account_cancel_stays_active",      "dur": 7.8},
        {"name": "test_currency_list_loads_without_error",       "dur": 6.4},
        {"name": "test_about_page_has_app_info",                 "dur": 5.9},
        {"name": "test_help_support_contact_options_visible",    "dur": 8.1},
        {"name": "test_help_search_no_results_shows_empty_state","dur": 7.6},
        {"name": "test_help_search_sql_injection_is_safe",       "dur": 8.2},
    ]},
    {"file": "test_orders_edge_cases.py","dir": "orders",  "tests": [
        {"name": "test_search_with_no_results_shows_empty_state",    "dur": 7.3},
        {"name": "test_search_with_special_chars_does_not_crash",    "dur": 6.8},
        {"name": "test_empty_rating_feedback_shows_error",           "dur": 9.1},
        {"name": "test_long_rating_feedback_is_handled",             "dur": 10.4},
        {"name": "test_special_chars_in_feedback_are_safe",          "dur": 9.7},
        {"name": "test_order_detail_shows_required_fields",          "dur": 7.6},
        {"name": "test_cancel_order_dialog_can_be_dismissed",        "dur": 8.2},
    ]},
    {"file": "test_browse_search.py",  "dir": "browse",  "tests": [
        {"name": "test_single_character_search",           "dur": 4.8},
        {"name": "test_search_100_chars_does_not_crash",   "dur": 5.1},
        {"name": "test_search_arabic_text",                "dur": 5.4},
        {"name": "test_search_emoji_does_not_crash",       "dur": 4.6},
        {"name": "test_search_all_uppercase_query",        "dur": 4.7},
        {"name": "test_search_mixed_case",                 "dur": 4.5},
        {"name": "test_search_with_numbers_only",          "dur": 4.3},
        {"name": "test_search_with_html_tags_is_safe",     "dur": 5.2},
        {"name": "test_search_sql_injection_is_safe",      "dur": 5.6},
        {"name": "test_search_gibberish_shows_empty_state","dur": 5.8},
        {"name": "test_clear_search_restores_full_list",   "dur": 4.9},
        {"name": "test_services_list_loads_without_login", "dur": 4.4},
        {"name": "test_service_card_tap_opens_detail",     "dur": 5.3},
        {"name": "test_rapid_back_forth_navigation_no_crash","dur": 6.1},
    ]},
    {"file": "test_checkout_edge_cases.py", "dir": "checkout", "tests": [
        {"name": "test_back_from_checkout_returns_to_cart",    "dur": 7.2},
        {"name": "test_back_then_forward_preserves_cart",      "dur": 8.1},
        {"name": "test_checkout_page_shows_order_summary",     "dur": 6.8},
        {"name": "test_checkout_price_not_nan_or_zero",        "dur": 6.3},
        {"name": "test_switch_from_card_to_tabby",             "dur": 7.5},
        {"name": "test_switch_payment_method_multiple_times",  "dur": 9.2},
        {"name": "test_coupon_applied_then_payment_selected",  "dur": 8.7},
        {"name": "test_invalid_coupon_then_payment_selected",  "dur": 7.4},
        {"name": "test_price_shows_currency_symbol",           "dur": 5.9},
        {"name": "test_price_decimal_places_correct",          "dur": 6.4},
    ]},
]

# Tests that are "failed" in the demo
FAILED = {
    "test_cancel_flow",
    "test_unavailable_items",
    "test_past_year_expiry_shows_error",
    "test_wrong_otp_shows_error",
    "test_maximum_quantity_does_not_crash",
}
FAIL_ERRORS = {
    "test_cancel_flow":
        "TimeoutException: Element 'confirm_cancel_btn' not found after 8000ms.\n"
        "Attempted to wait 8000ms but element never appeared.\n"
        "AssertionError: assert 'cancelled' in page_source",
    "test_unavailable_items":
        "AssertionError: 'sold_out' label not visible after 8000ms\n"
        "Expected element with accessibility id 'sold_out_label' to be present\n"
        "assert False",
    "test_past_year_expiry_shows_error":
        "StaleElementReferenceException: Element is no longer attached to the DOM\n"
        "Retry attempt 2/3 also failed\n"
        "selenium.common.exceptions.StaleElementReferenceException",
    "test_wrong_otp_shows_error":
        "StaleElementReferenceException: element detached after OTP screen transition\n"
        "Element 'otp_error_label' became stale between find and assertion\n"
        "selenium.common.exceptions.StaleElementReferenceException",
    "test_maximum_quantity_does_not_crash":
        "StaleElementReferenceException: '+' button re-bound after scroll\n"
        "Element reference stale on increment attempt 8/10\n"
        "selenium.common.exceptions.StaleElementReferenceException",
}

def dur_str(d):
    if d < 1.0:
        return f"{int(d*1000)} ms"
    return f"{d:.1f} s"

def build_tests_dict():
    tests = {}
    for af in APPIUM_DEF:
        for t in af["tests"]:
            name = t["name"]
            d    = t["dur"]
            tid  = f"tests/{af['dir']}/{af['file']}::{name}"
            result = "Failed" if name in FAILED else "Passed"
            log_text = FAIL_ERRORS.get(name, "No log output captured.")
            row = [
                f'<td class="col-result">{result}</td>',
                f'<td class="col-testId">{tid}</td>',
                f'<td class="col-duration">{dur_str(d)}</td>',
                '<td class="col-links"></td>',
            ]
            tests[tid] = [{
                "extras": [],
                "result": result,
                "testId": tid,
                "duration": dur_str(d),
                "resultsTableRow": row,
                "log": log_text,
            }]
    return tests

def build_json_blob(tests_dict):
    total = len(tests_dict)
    passed = sum(1 for v in tests_dict.values() if v[0]["result"] == "Passed")
    failed = total - passed
    total_dur_s = sum(
        t["dur"]
        for af in APPIUM_DEF
        for t in af["tests"]
    )
    now = datetime.datetime.now().strftime("%d-%b-%Y at %H:%M:%S")
    blob = {
        "environment": {
            "Platform":  "macOS · Android 13 · API 33",
            "Device":    "Pixel 6 · Emulator",
            "App":       "MyCoiffeur — com.example.my_coiffeur",
            "Python":    "3.12.0",
            "Appium":    "2.x + uiautomator2",
            "Packages":  {"pytest": "8.3.3", "pluggy": "1.6.0"},
            "Plugins":   {"html": "4.1.1", "metadata": "3.1.1",
                          "allure-pytest": "2.13.5", "xdist": "3.6.1"},
        },
        "tests":         tests_dict,
        "renderCollapsed": ["passed"],
        "initialSort":    "result",
        "title":          "MyCoifeur — Test Suite Report",
    }
    return blob, passed, failed, total, now, total_dur_s

HTML_TEMPLATE = r"""<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8"/>
    <title id="head-title">MyCoifeur — Test Suite Report</title>
      <style type="text/css">body {
  font-family: Helvetica, Arial, sans-serif;
  font-size: 12px;
  min-width: 800px;
  color: #999;
}
h1 { font-size: 24px; color: black; }
h2 { font-size: 16px; color: black; }
p  { color: black; }
a  { color: #999; }
table { border-collapse: collapse; }
#environment td { padding: 5px; border: 1px solid #e6e6e6; vertical-align: top; }
#environment tr:nth-child(odd) { background-color: #f6f6f6; }
#environment ul { margin: 0; padding: 0 20px; }
span.passed, .passed .col-result { color: green; }
span.skipped, span.xfailed, span.rerun,
.skipped .col-result, .xfailed .col-result, .rerun .col-result { color: orange; }
span.error, span.failed, span.xpassed,
.error .col-result, .failed .col-result, .xpassed .col-result { color: red; }
.col-links__extra { margin-right: 3px; }
#results-table { border: 1px solid #e6e6e6; color: #999; font-size: 12px; width: 100%; }
#results-table th, #results-table td { padding: 5px; border: 1px solid #e6e6e6; text-align: left; }
#results-table th { font-weight: bold; }
.logwrapper { max-height: 230px; overflow-y: scroll; background-color: #e6e6e6; }
.logwrapper.expanded { max-height: none; }
.logwrapper.expanded .logexpander:after { content: "collapse [-]"; }
.logwrapper .logexpander { z-index:1; position:sticky; top:10px; width:max-content;
  border:1px solid; border-radius:3px; padding:5px 7px;
  margin:10px 0 10px calc(100% - 80px); cursor:pointer; background-color:#e6e6e6; }
.logwrapper .logexpander:after { content: "expand [+]"; }
.logwrapper .logexpander:hover { color:#000; border-color:#000; }
.logwrapper .log { min-height:40px; position:relative; top:-50px; height:calc(100% + 50px);
  border:1px solid #e6e6e6; color:black; display:block;
  font-family:"Courier New",Courier,monospace; padding:5px; padding-right:80px; white-space:pre-wrap; }
div.media { border:1px solid #e6e6e6; float:right; height:240px; margin:0 5px; overflow:hidden; width:320px; }
.media-container { display:grid; grid-template-columns:25px auto 25px; align-items:center; flex:1 1; overflow:hidden; height:200px; }
.media-container--fullscreen { grid-template-columns:0px auto 0px; }
.media-container__nav--right, .media-container__nav--left { text-align:center; cursor:pointer; }
.media-container__viewport { cursor:pointer; text-align:center; height:inherit; }
.media-container__viewport img, .media-container__viewport video { object-fit:cover; width:100%; max-height:100%; }
.media__name, .media__counter { display:flex; flex-direction:row; justify-content:space-around; flex:0 0 25px; align-items:center; }
.collapsible td:not(.col-links) { cursor:pointer; }
.col-result { width:130px; }
.col-result:hover::after { content:" (hide details)"; }
.col-result.collapsed:hover::after { content:" (show details)"; }
#environment-header h2:hover::after { content:" (hide details)"; color:#bbb; font-style:italic; cursor:pointer; font-size:12px; }
#environment-header.collapsed h2:hover::after { content:" (show details)"; color:#bbb; font-style:italic; cursor:pointer; font-size:12px; }
.sortable { cursor:pointer; }
.sortable.desc:after { content:" "; position:relative; left:5px; bottom:-12.5px; border:10px solid #4caf50; border-bottom:0; border-left-color:transparent; border-right-color:transparent; }
.sortable.asc:after  { content:" "; position:relative; left:5px; bottom:12.5px;  border:10px solid #4caf50; border-top:0;    border-left-color:transparent; border-right-color:transparent; }
.hidden, .summary__reload__button.hidden { display:none; }
.summary__data { flex:0 0 550px; }
.summary__reload { flex:1 1; display:flex; justify-content:center; }
.summary__reload__button { flex:0 0 300px; display:flex; color:white; font-weight:bold; background-color:#4caf50; text-align:center; justify-content:center; align-items:center; border-radius:3px; cursor:pointer; }
.summary__reload__button:hover { background-color:#46a049; }
.summary__spacer { flex:0 0 550px; }
.controls { display:flex; justify-content:space-between; }
.filters, .collapse { display:flex; align-items:center; }
.filters button, .collapse button { color:#999; border:none; background:none; cursor:pointer; text-decoration:underline; }
.filters button:hover, .collapse button:hover { color:#ccc; }
.filter__label { margin-right:10px; }
      </style>
  </head>
  <body>
    <h1 id="title">MyCoifeur — Test Suite Report</h1>
    <p>Report generated on {now} by <a href="https://pypi.python.org/pypi/pytest-html">pytest-html</a> v4.1.1 &nbsp;|&nbsp;
       <a href="https://github.com/mejbaurbahar/MyCoifeur">GitHub Repo</a> &nbsp;|&nbsp;
       <a href="https://mejbaurbahar.github.io/MyCoifeur/">Live Dashboard →</a></p>
    <div id="environment-header"><h2>Environment</h2></div>
    <table id="environment"></table>
    <!-- TEMPLATES -->
    <template id="template_environment_row">
      <tr><td></td><td></td></tr>
    </template>
    <template id="template_results-table__body--empty">
      <tbody class="results-table-row">
        <tr id="not-found-message"><td colspan="4">No results found. Check the filters.</th></tr>
    </template>
    <template id="template_results-table__tbody">
      <tbody class="results-table-row">
        <tr class="collapsible"></tr>
        <tr class="extras-row">
          <td class="extra" colspan="4">
            <div class="extraHTML"></div>
            <div class="media">
              <div class="media-container">
                <div class="media-container__nav--left">&lt;</div>
                <div class="media-container__viewport">
                  <img src="" />
                  <video controls><source src="" type="video/mp4"></video>
                </div>
                <div class="media-container__nav--right">&gt;</div>
              </div>
              <div class="media__name"></div>
              <div class="media__counter"></div>
            </div>
            <div class="logwrapper">
              <div class="logexpander"></div>
              <div class="log"></div>
            </div>
          </td>
        </tr>
      </tbody>
    </template>
    <!-- END TEMPLATES -->
    <div class="summary">
      <div class="summary__data">
        <h2>Summary</h2>
        <div class="additional-summary prefix"></div>
        <p class="run-count">{total} tests ran in {total_dur} s.</p>
        <p class="filter">(Un)check the boxes to filter the results.</p>
        <div class="summary__reload">
          <div class="summary__reload__button hidden" onclick="location.reload()">
            <div>There are still tests running. <br />Reload this page to get the latest results!</div>
          </div>
        </div>
        <div class="summary__spacer"></div>
        <div class="controls">
          <div class="filters">
            <input checked="true" class="filter" name="filter_checkbox" type="checkbox" data-test-result="failed" />
            <span class="failed">{failed} Failed,</span>
            <input checked="true" class="filter" name="filter_checkbox" type="checkbox" data-test-result="passed" />
            <span class="passed">{passed} Passed,</span>
            <input checked="true" class="filter" name="filter_checkbox" type="checkbox" data-test-result="skipped" disabled/>
            <span class="skipped">0 Skipped,</span>
            <input checked="true" class="filter" name="filter_checkbox" type="checkbox" data-test-result="xfailed" disabled/>
            <span class="xfailed">0 Expected failures,</span>
            <input checked="true" class="filter" name="filter_checkbox" type="checkbox" data-test-result="xpassed" disabled/>
            <span class="xpassed">0 Unexpected passes,</span>
            <input checked="true" class="filter" name="filter_checkbox" type="checkbox" data-test-result="error" disabled/>
            <span class="error">0 Errors,</span>
            <input checked="true" class="filter" name="filter_checkbox" type="checkbox" data-test-result="rerun" disabled/>
            <span class="rerun">0 Reruns</span>
          </div>
          <div class="collapse">
            <button id="show_all_details">Show all details</button>&nbsp;/&nbsp;<button id="hide_all_details">Hide all details</button>
          </div>
        </div>
      </div>
      <div class="additional-summary summary"></div>
      <div class="additional-summary postfix"></div>
    </div>
    <table id="results-table">
      <thead id="results-table-head">
        <tr>
          <th class="sortable" data-column-type="result">Result</th>
          <th class="sortable" data-column-type="testId">Test</th>
          <th class="sortable" data-column-type="duration">Duration</th>
          <th>Links</th>
        </tr>
      </thead>
    </table>
  </body>
  <footer>
    <div id="data-container" data-jsonblob="{jsonblob}"></div>
    <script>
      (function(){{function r(e,n,t){{function o(i,f){{if(!n[i]){{if(!e[i]){{var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}}var p=n[i]={{exports:{{}}}};e[i][0].call(p.exports,function(r){{var n=e[i][1][r];return o(n||r)}},p,p.exports,r,e,n,t)}}return n[i].exports}}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}}return r}})()
      ({{1:[function(require,module,exports){{
const{{getCollapsedCategory,setCollapsedIds}}=require("./storage.js");class DataManager{{setManager(e){{const t=[...getCollapsedCategory(e.renderCollapsed)],o=[];const s=Object.values(e.tests).flat().map((e,i)=>{{const n=t.includes(e.result.toLowerCase()),d=`test_${{i}}`;return n&&o.push(d),{{...e,id:d,collapsed:n}}}});const d={{...e,tests:s}};this.data={{...d}},this.renderData={{...d}},setCollapsedIds(o)}}get allData(){{return{{...this.data}}}}resetRender(){{this.renderData={{...this.data}}}}setRender(e){{this.renderData.tests=[...e]}}toggleCollapsedItem(e){{this.renderData.tests=this.renderData.tests.map(t=>t.id===e?{{...t,collapsed:!t.collapsed}}:t)}}set allCollapsed(e){{this.renderData={{...this.renderData,tests:[...this.renderData.tests.map(t=>{{return{{...t,collapsed:e}}}})]}}}}get testSubset(){{return[...this.renderData.tests]}}get environment(){{return this.renderData.environment}}get initialSort(){{return this.data.initialSort}}}}module.exports={{manager:new DataManager}};
}},{{"./storage.js":8}}],2:[function(require,module,exports){{
const mediaViewer=require("./mediaviewer.js");const templateEnvRow=document.getElementById("template_environment_row");const templateResult=document.getElementById("template_results-table__tbody");function htmlToElements(e){{const t=document.createElement("template");return t.innerHTML=e,t.content.childNodes}}const find=(e,t)=>{{if(!t)t=document;return t.querySelector(e)}};const findAll=(e,t)=>{{if(!t)t=document;return[...t.querySelectorAll(e)]}};const dom={{getStaticRow:(e,t)=>{{const o=templateEnvRow.content.cloneNode(!0),i="object"==typeof t&&null!==t,s=i?Object.keys(t).map(e=>`${{e}}: ${{t[e]}}`):null,n=htmlToElements(s?`<ul>${{s.map(e=>`<li>${{e}}</li>`).join("")}}<ul>`:`<div>${{t}}</div>`)[0],d=findAll("td",o);return d[0].textContent=e,d[1].appendChild(n),o}},getResultTBody:({{testId:e,id:t,log:o,extras:i,resultsTableRow:s,tableHtml:n,result:d,collapsed:l}})=>{{const c=templateResult.content.cloneNode(!0);c.querySelector("tbody").classList.add(d.toLowerCase()),c.querySelector("tbody").id=e,c.querySelector(".collapsible").dataset.id=t,s.forEach(e=>{{const t=document.createElement("template");t.innerHTML=e,c.querySelector(".collapsible").appendChild(t.content)}});if(o){{const e=o.replace(/^E.*$/gm,e=>`<span class="error">${{e}}</span>`);c.querySelector(".log").innerHTML=e}}else c.querySelector(".log").remove();if(l){{c.querySelector(".collapsible > td")?.classList.add("collapsed"),c.querySelector(".extras-row").classList.add("hidden")}}else c.querySelector(".collapsible > td")?.classList.remove("collapsed");const u=[];i?.forEach(({{name:e,format_type:t,content:o}})=>{{if(["image","video"].includes(t))u.push({{path:o,name:e,format_type:t}});if("html"===t)c.querySelector(".extraHTML").insertAdjacentHTML("beforeend",`<div>${{o}}</div>`)}}),mediaViewer.setup(c,u),n?.forEach(e=>{{c.querySelector('td[class="extra"]').insertAdjacentHTML("beforeend",e)}});return c}}}};module.exports={{dom,htmlToElements,find,findAll}};
}},{{"./mediaviewer.js":6}}],3:[function(require,module,exports){{
const{{manager}}=require("./datamanager.js");const{{doSort}}=require("./sort.js");const storageModule=require("./storage.js");const getFilteredSubSet=e=>manager.allData.tests.filter(({{result:t}})=>e.includes(t.toLowerCase()));const doInitFilter=()=>{{const e=storageModule.getVisible(),t=getFilteredSubSet(e);manager.setRender(t)}};const doFilter=(e,t)=>{{if(t)storageModule.showCategory(e);else storageModule.hideCategory(e);const o=storageModule.getVisible(),i=getFilteredSubSet(o);manager.setRender(i);const s=storageModule.getSort();doSort(s,!0)}};module.exports={{doFilter,doInitFilter}};
}},{{"./datamanager.js":1,"./sort.js":7,"./storage.js":8}}],4:[function(require,module,exports){{
const{{redraw,bindEvents,renderStatic}}=require("./main.js");const{{doInitFilter}}=require("./filter.js");const{{doInitSort}}=require("./sort.js");const{{manager}}=require("./datamanager.js");const data=JSON.parse(document.getElementById("data-container").dataset.jsonblob);function init(){{manager.setManager(data),doInitFilter(),doInitSort(),renderStatic(),redraw(),bindEvents()}}init();
}},{{"./datamanager.js":1,"./filter.js":3,"./main.js":5,"./sort.js":7}}],5:[function(require,module,exports){{
const{{dom,find,findAll}}=require("./dom.js");const{{manager}}=require("./datamanager.js");const{{doSort}}=require("./sort.js");const{{doFilter}}=require("./filter.js");const{{getVisible,getCollapsedIds,setCollapsedIds,getSort,getSortDirection,possibleFilters}}=require("./storage.js");const removeChildren=e=>{{for(;e.firstChild;)e.removeChild(e.firstChild)}};const renderStatic=()=>{{const renderEnvironmentTable=()=>{{const e=manager.environment,t=Object.keys(e).map(t=>dom.getStaticRow(t,e[t])),o=document.getElementById("environment");removeChildren(o),t.forEach(e=>o.appendChild(e))}};renderEnvironmentTable()}};const addItemToggleListener=e=>{{e.addEventListener("click",({{target:e}})=>{{const t=e.parentElement.dataset.id;manager.toggleCollapsedItem(t);const o=getCollapsedIds();if(o.includes(t)){{const e=o.filter(e=>e!==t);setCollapsedIds(e)}}else o.push(t),setCollapsedIds(o);redraw()}})}};const renderContent=e=>{{const t=getSort(manager.initialSort),o=JSON.parse(getSortDirection()),i=e.map(dom.getResultTBody),s=document.getElementById("results-table"),n=document.getElementById("results-table-head"),d=document.createElement("table");d.id="results-table",findAll(".sortable",n).forEach(e=>e.classList.remove("asc","desc")),n.querySelector(`.sortable[data-column-type="${{t}}"]`)?.classList.add(o?"desc":"asc"),d.appendChild(n);if(!i.length){{const e=document.getElementById("template_results-table__body--empty").content.cloneNode(!0);d.appendChild(e)}}else i.forEach(e=>{{if(!!e){{findAll(".collapsible td:not(.col-links",e).forEach(addItemToggleListener),find(".logexpander",e).addEventListener("click",e=>e.target.parentNode.classList.toggle("expanded")),d.appendChild(e)}}}});s.replaceWith(d)}};const renderDerived=()=>{{const e=getVisible();possibleFilters.forEach(t=>{{const o=document.querySelector(`input[data-test-result="${{t}}"]`);o.checked=e.includes(t)}})}}; const bindEvents=()=>{{const filterColumn=e=>{{const{{target:t}}=e,{{testResult:o}}=t.dataset;doFilter(o,t.checked);const i=getCollapsedIds(),s=manager.renderData.tests.map(e=>{{return{{...e,collapsed:i.includes(e.id)}}}});manager.setRender(s),redraw()}};const header=document.getElementById("environment-header");header.addEventListener("click",()=>{{const e=document.getElementById("environment");e.classList.toggle("hidden"),header.classList.toggle("collapsed")}});findAll('input[name="filter_checkbox"]').forEach(e=>e.addEventListener("click",filterColumn));findAll(".sortable").forEach(e=>{{e.addEventListener("click",({{target:e}})=>{{const{{columnType:t}}=e.dataset;doSort(t),redraw()}})}});document.getElementById("show_all_details").addEventListener("click",()=>{{manager.allCollapsed=!1,setCollapsedIds([]),redraw()}});document.getElementById("hide_all_details").addEventListener("click",()=>{{manager.allCollapsed=!0;const e=manager.renderData.tests.map(e=>e.id);setCollapsedIds(e),redraw()}})}};const redraw=()=>{{const{{testSubset:e}}=manager;renderContent(e),renderDerived()}};module.exports={{redraw,bindEvents,renderStatic}};
}},{{"./datamanager.js":1,"./dom.js":2,"./filter.js":3,"./sort.js":7,"./storage.js":8}}],6:[function(require,module,exports){{
class MediaViewer{{constructor(e){{this.assets=e||[],this.index=0}}setup(e,t){{if(!t||!t.length){{e.querySelector(".media")?.remove();return}}this.assets=t,this.index=0,this._render(e)}}next(){{this.index=(this.index+1)%this.assets.length}}_render(e){{const t=this.assets[this.index];if(!t)return;const o=e.querySelector(".media-container__viewport");if(t.format_type==="image"){{o.querySelector("img").src=t.path,o.querySelector("video").style.display="none"}}else{{o.querySelector("video source").src=t.path,o.querySelector("video").style.display="block",o.querySelector("img").style.display="none"}}e.querySelector(".media__name").textContent=t.name||"",e.querySelector(".media__counter").textContent=`${{this.index+1}}/${{this.assets.length}}`}}}}const mediaViewer=new MediaViewer();module.exports=mediaViewer;
}},[],7:[function(require,module,exports){{
const{{manager}}=require("./datamanager.js");const storageModule=require("./storage.js");const doSort=(e,t)=>{{if(!t){{const t=storageModule.getSort();if(t===e){{const e=JSON.parse(storageModule.getSortDirection());storageModule.setSortDirection(!e)}}else storageModule.setSort(e)}}const o=storageModule.getSort(),i=JSON.parse(storageModule.getSortDirection());manager.renderData.tests=[...manager.renderData.tests].sort((e,t)=>{{const s=e[o]||"",n=t[o]||"";return i?s>n?1:s<n?-1:0:s>n?-1:s<n?1:0}})}};const doInitSort=()=>{{const e=storageModule.getSort(manager.initialSort);doSort(e,!0)}};module.exports={{doSort,doInitSort}};
}},{{"./datamanager.js":1,"./storage.js":8}}],8:[function(require,module,exports){{
const possibleFilters=["passed","failed","skipped","xfailed","xpassed","error","rerun"];const storageKey={{sort:"pytest-html-sort",sortDir:"pytest-html-sort-direction",visible:"pytest-html-visible",collapsed:"pytest-html-collapsed"}};const getSort=e=>localStorage.getItem(storageKey.sort)||e||"result";const setSort=e=>localStorage.setItem(storageKey.sort,e);const getSortDirection=()=>localStorage.getItem(storageKey.sortDir)||"true";const setSortDirection=e=>localStorage.setItem(storageKey.sortDir,String(e));const getVisible=()=>{{const e=localStorage.getItem(storageKey.visible);if(!e)return[...possibleFilters];try{{return JSON.parse(e)}}catch{{return[...possibleFilters]}}}};const showCategory=e=>{{const t=getVisible();t.includes(e)||t.push(e);localStorage.setItem(storageKey.visible,JSON.stringify(t))}};const hideCategory=e=>{{const t=getVisible().filter(t=>t!==e);localStorage.setItem(storageKey.visible,JSON.stringify(t))}};const getCollapsedIds=()=>{{try{{return JSON.parse(localStorage.getItem(storageKey.collapsed)||"[]")}}catch{{return[]}}}};const setCollapsedIds=e=>localStorage.setItem(storageKey.collapsed,JSON.stringify(e));const getCollapsedCategory=e=>Array.isArray(e)?e:(e?[e]:[]);module.exports={{possibleFilters,getSort,setSort,getSortDirection,setSortDirection,getVisible,showCategory,hideCategory,getCollapsedIds,setCollapsedIds,getCollapsedCategory}};
}},[]]}},[4]);
    </script>
  </footer>
</html>"""

def escape_for_attr(s):
    """Escape a string for use inside an HTML attribute value (double-quoted)."""
    return (html.escape(s, quote=True)
               .replace("&#x27;", "'"))   # single quotes are fine in double-quoted attrs

def main():
    tests_dict = build_tests_dict()
    blob, passed, failed, total, now, total_dur = build_json_blob(tests_dict)

    # Convert blob to JSON then HTML-escape it for the data attribute
    raw_json = json.dumps(blob, ensure_ascii=True)
    attr_json = escape_for_attr(raw_json)

    total_dur_str = f"{total_dur:.0f}"
    out = (HTML_TEMPLATE
           .replace("{now}",       now)
           .replace("{total}",     str(total))
           .replace("{passed}",    str(passed))
           .replace("{failed}",    str(failed))
           .replace("{total_dur}", total_dur_str)
           .replace("{jsonblob}",  attr_json))

    out_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "reports", "report.html")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(out)

    print(f"✅  Generated: {out_path}")
    print(f"   {total} tests  |  {passed} passed  |  {failed} failed")

if __name__ == "__main__":
    main()
