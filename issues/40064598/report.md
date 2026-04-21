# intent:// restrictions bypassed via firebase dynamic links

| Field | Value |
|-------|-------|
| **Issue ID** | [40064598](https://issues.chromium.org/issues/40064598) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy, Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | nd...@protonmail.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2023-05-16 |
| **Bounty** | $3,000.00 |

## Description

**Steps to reproduce the problem:**  

Use the following on Android:

<a href="https://ndevtk.page.link/PZXe">Click me</a> make sure the Samsung browser is installed.

Put in a top-level sandbox this bypass allow-popups and allow-popups-to-escape-sandbox  

<a href='//null.app.goo.gl/vuln'>Click me</a>

**Problem Description:**  

Firebase dynamic links can open the Samsung, Firefox, Chrome browser to attacker controlled URL on Android.  

This bypasses <https://bugs.chromium.org/p/chromium/issues/detail?id=1345630> (prompt for opening other browsers) and <https://bugs.chromium.org/p/chromium/issues/detail?id=1365100> (bypass iframe sandbox on allow-popups-to-escape-sandbox and allow-popups)

**Additional Comments:**

\*\*Chrome version: \*\* 113.0.0.0 \*\*Channel: \*\* Stable

**OS:** Android

## Attachments

- [test-2023-06-02_18.53.34.mp4](attachments/test-2023-06-02_18.53.34.mp4) (video/mp4, 356.7 KB)

## Timeline

### [Deleted User] (2023-05-16)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-05-16)

Sandbox escape:
intent://null.app.goo.gl/vuln#Intent;package=com.google.android.gms;scheme=https;S.browser_fallback_url=https://websecblog.com/vulns/bypassing-firebase-authorization-to-create-custom-goo-gl-subdomains/;end;

Redirect user to diffrent browser:
intent://ndevtk.page.link/PZXe#Intent;package=com.google.android.gms;action=com.google.firebase.dynamiclinks.VIEW_DYNAMIC_LINK;scheme=https;S.browser_fallback_url=https://play.google.com/store/apps/details%3Fid%3Dcom.sec.android.app.sbrowser&pcampaignid%3Dfdl_short&url%3Dhttps://terjanq.me/xss.php%3Fheaders;end;

### ke...@chromium.org (2023-05-18)

Thanks for the report.

I've verified this behaviour. I suspect the root of the issue is that while we restrict external protocol navigations in sandboxed iframes (https://chromestatus.com/feature/5680742077038592), we appear to not apply the same restrictions in a sandboxed main frame. Assigning to arthursonzogni@ for thoughts.

Setting severity to low since it is (potentially) a very limited CSP bypass.

[Monorail components: Blink>SecurityFeature>ContentSecurityPolicy Mobile>Intents]

### [Deleted User] (2023-05-18)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-05-18)

That's not the bug I'm trying to report.
The bypass to https://crbug.com/chromium/1345630 and https://crbug.com/chromium/1365100 via dynamic links.

### nd...@protonmail.com (2023-05-18)

This also affects iframes with allow-popups (bypasses allow-popups-to-escape-sandbox)
So I guess I tried to put 3 bugs in one report and it failed :/

### nd...@protonmail.com (2023-05-18)

If main frames should enforce the external protocols sandbox maybe a valid bug but not what I want to report maybe still worth checking to see if its by design. 
Will explain the bypass for the bug that got high below not sure if I should have split the bugs into separate reports look to be the same owner mthiesse@chromium.org

VULNERABILITY DETAILS
A goo.gl Firebase Dynamic link [0] can be used to redirect users to other browsers without a confirmation prompt.
https://crbug.com/chromium/1345630 reports an intent redirect vulnerability that allowed to redirect Chromium users to a browser running an older version of Chromium without their confirmation, making them vulnerable to patched n-days.
This was fixed by checking for extra parameters in the intent link, however, this is still reproducible if a Firebase Dynamic link is used instead.

REPRODUCTION CASE
1. Install Samsung Browser
2. Open this page in Chrome
\`\`\`
<a href="https://test.app.goo.gl/samsung">Click here</a>
\`\`\`
3. Click the link

Expected behavior: A confirmation dialog gets shown, prompting the user whether they want to open Samsung Browser.

Actual behavior: The user gets immediately redirected to the Samsung Browser where the attacker's webpage gets opened (and potentially delivering an n-day exploit).

[0]: https://firebase.google.com/docs/dynamic-links

### ad...@google.com (2023-05-18)

(I am a bot: this is an auto-cc on a security bug)

### ar...@chromium.org (2023-06-02)

I am not sure to understand what this bug is about. I created a reproducer based on https://crbug.com/chromium/1445988#c7:
https://chrome-android-intent-firebase-redirect.glitch.me/

I observe the intent causes the samsung browser to open.
I am really not knowledgeable about how Chrome on Android should handle intents.
@mthiesse, could you tell if this is unexpected?

### ar...@chromium.org (2023-06-02)

I forgot the video:

### nd...@protonmail.com (2023-06-02)

I think its meant to prompt the user before opening a URL in a different browser. https://chromium-review.googlesource.com/c/chromium/src/+/3820605
Works by using Firebase Dynamic Links as a proxy.

The sandbox escape bypasses the fix in https://chromium-review.googlesource.com/c/chromium/src/+/4174394 although not sure what happens if a sandboxed main frame makes an intent navigation.

### mt...@chromium.org (2023-06-05)

I think the bug is probably not with Chrome, but with Firebase.

I don't think Chrome can/should block all navigations to firebase deep links (eg. intent://ndevtk.page.link/PZXe#Intent;package=com.google.android.gms;action=com.google.firebase.dynamiclinks.VIEW_DYNAMIC_LINK;scheme=https;S.browser_fallback_url=https://play.google.com/store/apps/details%3Fid%3Dcom.sec.android.app.sbrowser&pcampaignid%3Dfdl_short&url%3Dhttps://terjanq.me/xss.php%3Fheaders;end;)

The problem appears to be that GMS, through firebase dynamic links, is acting as an arbitrary redirection app and can be used to bypass our restrictions on which apps can be launched. There may be other vulnerabilities in addition to launching other browsers, I'll have to investigate.

### mt...@chromium.org (2023-06-05)

cc maddiestone who filed https://crbug.com/chromium/1249962

### mt...@chromium.org (2023-06-05)

Sorry, realized there are two issues here which should probably be separate bugs, though probably neither are Chrome bugs.

I think we should definitely treat the FDL bug to launch other browsers as a Firebase bug, they allow you to set the target package for a deep link, and don't restrict that at all. They should probably prevent FDLs from launching browsers. I just set up https://mthiessetest.page.link/6SuK to redirect to samsung browser and I didn't even need to create an app, it took like a minute to set up.



### mt...@chromium.org (2023-06-05)

As for the sandbox escape, this is a known issue - as soon as you've allowed external apps to be launched, the sandbox has been escaped as Android apps aren't subject to the same sandboxing. 

I don't know if we have a bug already capturing this, but we don't have any way of knowing if the launch of Chrome was because of a redirection through a third party app, or from eg. the user clicking a link. I can't think of a way to fix this without breaking a lot of benign usage as fallback URLs are a very common pattern in Firebase Dynamic Links.

### nd...@protonmail.com (2023-06-06)

Maybe add some people from the Firebase Team.
Having restrictions at the firebase level would also affect other apps seems like both teams would need to agree on a fix.
Maybe inject some restrictions that get sent as part of intent somehow.

### mt...@chromium.org (2023-06-06)

I don't think restrictions on not launching specific browser packages will affect other non-malicious apps (FDLs should respect the user's browser choice when launching a browser).

For the browser launch bug I think the best course of action would be for you to file a bug against Firebase here, as I don't think there's anything needed from Chrome: https://www.google.com/appserve/security-bugs/m2/new

Please reference this bug and request that they cc mthiesse@google.com so I can provide additional context (I don't get insight into bugs filed through Google vulnerability reports).

### nd...@protonmail.com (2023-06-06)

Thanks I created the report its https://crbug.com/chromium/286112048 :)

### mt...@chromium.org (2023-06-07)

Thank you! 

As for the sandbox escape issue, I don't have any good ideas for how to fix it. Attempting to pass sandbox flags through another app is fraught, and I'm not sure we'd want to expose the ability to launch URLs with arbitrary sandbox flags to any app.

I'd be inclined to WontFix this issue, and say that as soon as you've allowed popups to escape the sandbox you shouldn't expect the sandbox not to be escaped by popups :)

Let's get a second opinion from rsesek though.

### nd...@protonmail.com (2023-06-07)

I think sandboxed main frames should be included in the intent:// restriction.
This would mean in order to use any intent you would need to have allow-popups-to-escape-sandbox.

### mt...@chromium.org (2023-06-07)

I don't think I follow what you're saying. Why are sandboxed main frames relevant? Did you find that sandboxed main frames could send intents despite not having the  allow-popups-to-escape-sandbox flag?

### nd...@protonmail.com (2023-06-07)

yes that's the bug.

### mt...@chromium.org (2023-06-08)

Can you please clarify what your steps to reproduce that are? In your report you say:

"Put in a top-level sandbox this bypass allow-popups and allow-popups-to-escape-sandbox
<a href='//null.app.goo.gl/vuln'>Click me</a>"

I don't see where you're creating a sandboxed main frame and escaping it.

### nd...@protonmail.com (2023-06-08)

[Comment Deleted]

### nd...@protonmail.com (2023-06-08)

Full POC goes to intent without allow-popups-to-escape sandbox:
https://terjanq.me/xss.php?html=%3Ciframe%20sandbox=%22allow-popups%22%20src=%22https%3A%2F%2Fterjanq.me%2Fxss.php%3Fhtml%3D%253Ca%2520href%3D%2527%2F%2Fnull.app.goo.gl%2Fvuln%2527%253EClick%2520me%253C%2Fa%253E%22%3E

### mt...@chromium.org (2023-06-08)

That's an example of a sandboxed iframe, and by design allow-popups also allows external intents (see https://groups.google.com/a/chromium.org/g/blink-dev/c/-t-f7I6VvOI/m/Hu4J1brbDQAJ), so there's no bug there.

### nd...@protonmail.com (2023-06-08)

"by design allow-popups also allows external intents" right and that escapes the sandbox without allow-popups-to-escape-sandbox via Firebase.
A popup is a main frame and escaping it without allow-popups-to-escape-sandbox is a bug intent or otherwise.

### nd...@protonmail.com (2023-06-08)

Intents are equal to a sandbox escape so should be marked correctly.

### mt...@chromium.org (2023-06-08)

arthursonzogni@ can probably comment on why we chose to have allow-popups support external intents (I suspect backwards compatibility as historically this was always allowed in sandboxed frames), but this is not a bug.

### nd...@protonmail.com (2023-06-08)

You said "as soon as you've allowed popups to escape the sandbox you shouldn't expect the sandbox not to be escaped by popups :)"
As shown I did not allow popups to escape the sandbox by using allow-popups-escape-sandbox that's why I provided a PoC.

It may just be a problem with firebase dynamic links allow the self redirection which should have been fixed in
https://bugs.chromium.org/p/chromium/issues/detail?id=1365100


### nd...@protonmail.com (2023-06-08)

I meant allow-popups-to-escape-sandbox :)

### mt...@chromium.org (2023-06-08)

> You said "as soon as you've allowed popups to escape the sandbox you shouldn't expect the sandbox not to be escaped by popups :)"

My apologies, I had forgotten that "allow-popups" also intentionally allowed intents which are definitionally sandbox escapes. It would be nice if apps that redirected back to Chrome somehow maintained the sandbox that was applied to the site that sent the intent, but that's impossible to do in general, and I see no good way to do it in the specific case of FDLs.

Firebase Dynamic Links will be deprecated soon (https://firebase.google.com/support/dynamic-links-faq), so this specific source of redirects back to Chrome will go away eventually.

### nd...@protonmail.com (2023-06-08)

Agree killing FDLs is a very effective way to fix this type of sandbox escape!
Allowing intents from sandboxed main frames such as popups may create other issues but it may not be easy to fix in a non-breaking way.

### nd...@protonmail.com (2023-06-09)

Probably keep this bug open until FDLs go away that seems to be the main attack.

When was https://firebase.google.com/support/dynamic-links-faq first created?
Trying to figure out if I created this report when it got deprecated :)

### mt...@chromium.org (2023-06-09)

I don't know when the faq was created, but I believe the team was unaware of this issue until you filed b/286112048 two days ago.

### ad...@google.com (2023-06-29)

mthiesse@

FDL feel that this is not a vulnerability in their service and don't seem inclined to make changes. We probably can't wait for FDLs to go away. In any case, presumably other apps and packages could also offer the same intent redirection properties as FDL does.

Supposing we had to take action in Chrome to close this vulnerability, what would we do? Would we have to start to maintain a blocklist of intent patterns which have this arbitrary intent redirection property? Or, would we start to maintain an allowlist of known-OK intent patterns, or would we finally bite the bullet and prompt on all intent URIs?

(Bumping this up to severity medium, conservatively, based on the prior related bugs. It's definitely not Low and might be High.)

### nd...@protonmail.com (2023-06-29)

"prompt on all intent URIs" would reduce the attack surface significantly for Android I don't think there's any reason it should not be treated like any other custom protocols https://html.spec.whatwg.org/multipage/browsers.html#sandboxed-custom-protocols-navigation-browsing-context-flag

### mt...@chromium.org (2023-06-29)

I don't love prompting on all intent URIs, I'd be worried about notification fatigue and users not really understanding what this means (the vast majority of the time it's totally safe and something the user wants).

The real problem is that this wouldn't solve the security bug as FDLs have a verified app link, so you don't need to use intent URIs to exploit them.

I think ideally we push on firebase to solve this as it's really far worse than any other app having this vulnerability given they're default installed on basically all Android phones. Alternatively, the blocklist of apps that are exploitable in this way would probably be reasonable.

### nd...@protonmail.com (2023-06-29)

A blacklist for all FDLs or for all known web browsers?
If its "just" opening an app with no parameter's it probably does not need a prompt.

Like I don't think attackers could exploit just "calculator://" other then being annoying that they can anyway.


### am...@chromium.org (2023-06-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-06-30)

rsesek: Uh oh! This issue still open and hasn't been updated in the last 45 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2023-07-04)

> A blacklist for all FDLs or for all known web browsers?
>If its "just" opening an app with no parameter's it probably does not need a prompt.
>
>Like I don't think attackers could exploit just "calculator://" other then being annoying that they can anyway.

No, I'm only talking about FDLs, not blocking all intent URIs. And it wouldn't be a block so much as a prompt to warn the user they're leaving a secure context or something.

### nd...@protonmail.com (2023-07-04)

Prompt on FDL (or proxy apps like it) seems like a good fix. :)

### [Deleted User] (2023-07-10)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2023-07-11)

I agree with Ade’s c#36 that waiting for FDLs to go away is probably not viable, given that the deprecation timeline will be announced Q3 2023 and will provide a minimum of 12 months before full deprecation.

However, I don’t know how to mitigate this at all given mthiesse’s note about the DAL situation:

> The real problem is that this wouldn't solve the security bug as FDLs have a verified app link, so you don't need to use intent URIs to exploit them.

If we resolved the intent, we could see if it’s an FDL. But I don’t know how we can check, within Chrome, if the dynamic link will resolve to another browser app launch.

> Alternatively, the blocklist of apps that are exploitable in this way would probably be reasonable.

Presumably this could be heuristic-based as done in https://crbug.com/chromium/1249962?


Ade: I can’t see b/286112048. Do you know if we have more levers to pull with FDL server-side? 

### am...@chromium.org (2023-07-11)

The internal issue that this is being worked through with the Firebase team is b/286180144, you should have access to that. 

[Monorail blocked-on: b/286180144]

### ad...@google.com (2023-07-12)

Yep, I also can't see b/286112048.

### [Deleted User] (2023-07-19)

mthiesse: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2023-07-19)

[Empty comment from Monorail migration]

### nd...@protonmail.com (2023-07-19)

Did firebase agree to fix it?
This would be good for protecting other apps.

### mt...@chromium.org (2023-07-19)

Yes, Firebase is working on a fix.

### [Deleted User] (2023-07-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-21)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-08-31)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-11)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-09-21)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-02)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-12)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-24)

This issue hasn't been updated in the last 30 days - please update it or consider lowering its priority.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2023-10-24)

Just noting that the Firebase fix has landed and is in the process of rolling out.

### nd...@protonmail.com (2023-11-08)

https://crbug.com/chromium/286112048 has been marked as fixed.
"This issue will also be assessed by the Chrome VRP for reward consideration (to our understanding, you have also an issue filed directly with Chrome VRP)."

### am...@chromium.org (2023-11-08)

I don't have access to b/286112048 so thank you for sharing that comment!
I'm going to go ahead and close this as fixed then. This will allow us the bug to get picked up for a forthcoming Chrome VRP panel session. 

### [Deleted User] (2023-11-09)

[Empty comment from Monorail migration]

### am...@google.com (2023-11-16)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-11-16)

Congratulations NDevTK! The Chrome VRP Panel has decided to award you $3,000 for this report. Thank you for your efforts and reporting this issue to us! 

### nd...@protonmail.com (2023-11-16)

Thanks

### am...@google.com (2023-11-18)

[Empty comment from Monorail migration]

### is...@google.com (2023-11-18)

This issue was migrated from crbug.com/chromium/1445988?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>ContentSecurityPolicy, Mobile>Intents]
[Monorail blocked-on: b/286180144]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-02-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40064598)*
