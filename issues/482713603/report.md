# Sandbox escape from extensions due to insufficent checks in chrome.devtools.inspectedWindow.reload and chrome://policy

| Field | Value |
|-------|-------|
| **Issue ID** | [482713603](https://issues.chromium.org/issues/482713603) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>DevTools |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | ad...@gmail.com |
| **Assignee** | yd...@google.com |
| **Created** | 2026-02-08 |
| **Bounty** | $20,000.00 |

## Description

---

### Report description

WebUI restart message applies local test policies when the policy test page should be disabled

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

<https://chromium.googlesource.com/chromium/src/>

---

### The problem

#### Please describe the technical details of the vulnerability

#### 1. technical details

Chromium exposes a policy inspection WebUI at `chrome://policy`, and a separate test page at `chrome://policy/test` that is only intended to be available when policy testing is explicitly enabled.

The test page availability is guarded by `PolicyUI::ShouldLoadTestPage`, which checks both a testing preference and whether the profile is cloud managed:

This behavior represents a regression of the intended restrictions that were previously addressed in <https://issues.chromium.org/issues/338248595>.

```
// chrome/browser/ui/webui/policy/policy_ui.cc
// static
bool PolicyUI::ShouldLoadTestPage(Profile* profile) {
  // Test page should only load if testing is enabled.
  if (!policy::utils::IsPolicyTestingEnabled(profile->GetPrefs(),
                                             chrome::GetChannel())) {
    return false;
  }
  // The test page is not allowed if the profile is cloud managed unless
  // we are already using the test policies.
  if (policy::ManagementServiceFactory::GetForProfile(profile)
          ->HasManagementAuthority(
              policy::EnterpriseManagementAuthority::CLOUD) &&
      !profile->GetProfilePolicyConnector()->IsUsingLocalTestPolicyProvider()) {
    return false;
  }
  return true;
}

```

At startup, `ChromeBrowserPolicyConnector::MaybeApplyLocalTestPolicies` reads a JSON string from a local pref and, if present, activates the local test policy provider and loads that JSON as policies:

```
// chrome/browser/policy/chrome_browser_policy_connector.cc
void ChromeBrowserPolicyConnector::MaybeApplyLocalTestPolicies(
    PrefService* local_state) {
  // Early return if the policy test page is disabled by any policy. This is
  // done because that policy is a profile level policy and we have not yet
  // loaded any profile to access its prefs.
  const auto& chrome_policies =
      GetPolicyService()->GetPolicies(policy::PolicyNamespace(
          policy::PolicyDomain::POLICY_DOMAIN_CHROME, std::string()));
  if (auto* policy_test_page_enabled = chrome_policies.GetValue(
          policy::key::kPolicyTestPageEnabled, base::Value::Type::BOOLEAN);
      policy_test_page_enabled && !policy_test_page_enabled->GetBool()) {
    return;
  }

  std::string policies_to_apply =
      local_state->GetString(policy_prefs::kLocalTestPoliciesForNextStartup);
  if (policies_to_apply.empty()) {
    return;
  }

  LocalTestPolicyProvider* test_provider =
      local_test_provider_for_testing_ ? static_cast<LocalTestPolicyProvider*>(
                                             local_test_provider_for_testing_)
                                       : local_test_provider_.get();
  test_provider->set_active(true);
  GetPolicyService()->UseLocalTestPolicyProvider(test_provider);
  test_provider->LoadJsonPolicies(policies_to_apply);
  local_state->ClearPref(policy_prefs::kLocalTestPoliciesForNextStartup);
}

```

The local test provider itself is created on supported channels (for example, Dev/Canary and debug builds) without consulting per‑profile management state:

```
// components/policy/core/common/local_test_policy_provider.cc
// static
std::unique_ptr<LocalTestPolicyProvider>
LocalTestPolicyProvider::CreateIfAllowed(version_info::Channel channel) {
  if (utils::IsPolicyTestingEnabled(/*pref_service=*/nullptr, channel)) {
    return base::WrapUnique(new LocalTestPolicyProvider());
  }

  return nullptr;
}

```

On the WebUI side, both `chrome://policy` and `chrome://policy/test` share the same `PolicyUIHandler`. Among other messages, this handler exposes a `"restartBrowser"` message that accepts a JSON string and stores it into the pref inspected at startup:

```
// chrome/browser/ui/webui/policy/policy_ui_handler.cc
void PolicyUIHandler::HandleRestartBrowser(const base::ListValue& args) {
  CHECK(args.size() == 2);
  const std::string& policies = args[1].GetString();

  // Set policies to preference
  PrefService* prefs = g_browser_process->local_state();
  prefs->SetString(policy::policy_prefs::kLocalTestPoliciesForNextStartup,
                   policies);

  // Restart browser
  chrome::AttemptRestart();
}

```

Unlike the `setLocalTestPolicies` and `revertLocalTestPolicies` handlers, `HandleRestartBrowser` does not check `PolicyUI::ShouldLoadTestPage` before accepting the JSON payload. As a result:

- In builds where the local test policy provider exists (for example, Dev/Canary or debug builds), and
- In profiles where `PolicyUI::ShouldLoadTestPage(profile)` would return `false` (for example, cloud‑managed profiles that are not already using local test policies),

any JavaScript running in the `chrome://policy` WebUI can call the `"restartBrowser"` message and cause arbitrary JSON to be written into `kLocalTestPoliciesForNextStartup`. On the next startup, that JSON is loaded via `MaybeApplyLocalTestPolicies` and applied as active policies through the local test provider, even though the test page itself should not be available.

#### 2. vulnerability reproduction

The attached JavaScript helper under `web/policy_js_bypass/policy_restart_test.js` demonstrates the behavior in a realistic way using a Dev‑channel Chrome build:

- The script is designed to be pasted into the DevTools console on `chrome://policy`.
- It optionally loads a JSON payload from a remote URL or uses an inline JSON array of policy entries (for example, setting `CloudReportingEnabled` to `false`).
- It validates that the payload is parseable as JSON and then calls:
  - `chrome.send('restartBrowser', [callbackId, jsonText]);`

Conceptual reproduction steps using a Dev build:

1. Start a Dev‑channel Chrome build where local test policy provider support is compiled in.
2. Open `chrome://policy` and then open DevTools (Console tab).
3. Copy the contents of `web/policy_js_bypass/policy_restart_test.js` into the console, optionally adjusting the JSON payload if needed, and execute it.
4. Observe console logging indicating that a payload is chosen and the `"restartBrowser"` message is being sent.
5. The browser process exits and restarts automatically.
6. After restart, open `chrome://policy` again and search for `CloudReportingEnabled` (or other values from the JSON payload). The policy is now present with the value defined in the JSON, sourced from the local test provider.

In a profile configuration where `PolicyUI::ShouldLoadTestPage(profile)` would return `false` (for example, a cloud‑managed profile that does not already use local test policies), the same `"restartBrowser"` path would still accept and store the JSON payload from `chrome://policy`. On restart, `MaybeApplyLocalTestPolicies` applies those values as active policies, even though the test page is not supposed to be usable for injecting local test policies.

#### Impact analysis

- **Who can exploit it:** Any local user or script that can execute JavaScript in the `chrome://policy` WebUI of a build where the local test policy provider is enabled (for example, Dev/Canary or debug builds). This includes users manually pasting code into the DevTools console or higher‑privileged browser automation running in the same profile.
- **What they gain:** In environments where the policy test page is intended to be unavailable (for example, certain cloud‑managed profiles), the user can still inject a JSON payload through the `"restartBrowser"` WebUI message and cause those values to be applied as local test policies on the next startup. This allows local policy values (such as `CloudReportingEnabled` or other supported keys) to be overridden through a test‑only mechanism even when the test page should be disabled, affecting how the browser interprets and enforces policies for that profile.
- **Security significance:** The issue does not provide remote code execution or cross‑user compromise, and it does not bypass sandboxing. Its significance lies in weakening the separation between normal policy evaluation and test‑only policy mechanisms: policy values can be altered via a test helper path from `chrome://policy` even when the environment is configured so that the policy test page should not be usable. This can change how certain enterprise policy checks behave for that local profile, depending on which policies are supplied in the JSON payload.

---

### The cause

#### What version of Chrome have you found the security issue in?

146.0.7666.1/stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Permissions Bypass

#### How would you like to be publicly acknowledged for your report?

Povcfe of Tencent Security Xuanwu Lab

## Attachments

- [policy_js_bypass.mp4](attachments/policy_js_bypass.mp4) (video/mp4, 1.5 MB)
- [policy_restart_test.js](attachments/policy_restart_test.js) (text/javascript, 2.4 KB)

## Timeline

### po...@gmail.com (2026-02-08)

#### patch

```
diff --git a/chrome/browser/ui/webui/policy/policy_ui_handler.cc b/chrome/browser/ui/webui/policy/policy_ui_handler.cc
--- a/chrome/browser/ui/webui/policy/policy_ui_handler.cc
+++ b/chrome/browser/ui/webui/policy/policy_ui_handler.cc
@@ -406,7 +406,12 @@ void PolicyUIHandler::HandleRevertLocalTestPolicies(
   Profile::FromWebUI(web_ui())
       ->GetProfilePolicyConnector()
       ->RevertUseLocalTestPolicyProvider();
 }
 
 void PolicyUIHandler::HandleRestartBrowser(const base::ListValue& args) {
-  CHECK(args.size() == 2);
+  if (!PolicyUI::ShouldLoadTestPage(Profile::FromWebUI(web_ui()))) {
+    return;
+  }
+
+  CHECK(args.size() == 2);
   const std::string& policies = args[1].GetString();
 
   // Set policies to preference

```

### ts...@google.com (2026-02-09)

Precondtion of running JS in chrome://policy WebUI is a pretty high bar, setting sev accordingly. It seems that this doesn't provide protection for users who are in the test group, so making this check doesn't really solve the problem for them.  Not sure if this is working as intended in that webui is powerful.

### ts...@google.com (2026-02-09)

Assigning to author of PolicyUIHandler::HandleRestartBrowser, setting found-in based on age of code to extended-stable.

### po...@gmail.com (2026-02-09)

This behavior represents a regression of the intended restrictions that were previously addressed in <https://issues.chromium.org/issues/338248595>.

### dx...@google.com (2026-04-16)

Project: chromium/src  

Branch:  main  

Author:  Dzmitry Radchuk [radchuk@google.com](mailto:radchuk@google.com)  

Link:    <https://chromium-review.googlesource.com/7764606>

Ensure chrome://policy restartBrowser message ignored when not supported

---


Expand for full commit details
```
     
    It was possible to go to chrome://policy and in the dev tools send 
    the restartBrowser message to set test policies even if the policy test 
    page was disabled and/or unavailable because both pages share the same 
    handler. 
     
    Bug: 482713603 
    Change-Id: I5a5a777be4c5e5083f9a12f1c8240b5cbb0ccca8 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7764606 
    Reviewed-by: Yann Dago <ydago@chromium.org> 
    Auto-Submit: Dzmitry Radchuk <radchuk@google.com> 
    Reviewed-by: Gauthier Ambard <gambard@chromium.org> 
    Commit-Queue: Gauthier Ambard <gambard@chromium.org> 
    Reviewed-by: Owen Min <zmin@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1615744}

```

---

Files:

- M `chrome/browser/ui/webui/policy/policy_test_ui_browsertest.cc`
- M `chrome/browser/ui/webui/policy/policy_ui_handler.cc`
- M `ios/chrome/browser/webui/ui_bundled/policy/policy_ui_handler.mm`

---

Hash: [7b6ba28a2a8ea3abd1cbe60ccea6f964f0cdb142](https://chromiumdash.appspot.com/commit/7b6ba28a2a8ea3abd1cbe60ccea6f964f0cdb142)  

Date: Thu Apr 16 11:22:48 2026


---

### sp...@google.com (2026-05-26)

*NOTE: This is an automatically generated email*

Hello,

Chrome Vulnerability Rewards Program (VRP) Panel has decided that the security impact of this
issue does not meet the criteria to qualify for a reward.

Rationale for this decision:

No harm demonstrated

Note that the fact that this issue is not being rewarded does not mean
that the product team won't fix the issue. We have filed a bug with the product
team and they will review your report and decide if a fix is required. We'll
let you know if the issue was fixed.

Regards,   

Google Security Bot

*How did we do? Please fill out a [short anonymous survey](https://goo.gl/IR3KRH).*

### ch...@google.com (2026-07-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/482713603)*
