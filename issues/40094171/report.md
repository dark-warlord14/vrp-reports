# Security: CORS issue with Chrome Extensions

| Field | Value |
|-------|-------|
| **Issue ID** | [40094171](https://issues.chromium.org/issues/40094171) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>SecurityFeature>CORS, Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | gr...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2019-02-28 |
| **Bounty** | $500.00 |

## Description

**VULNERABILITY DETAILS**  

Hello, I found that Chrome Extensions are NOT properly enforcing CORS. Specifically, an extension can successfully fetch a url on a different port than the user is visiting. This is denied by other Browsers such as FireFox. Furthermore, if you are to run the same code on a web server and browse the site through chrome, the fetch request IS properly denied for the alternate port.

**VERSION**  

Chrome Version: [72.0.3626.119] + [stable] (likely others)  

Operating System: [Windows 10 Enterprise]

**REPRODUCTION CASE**  

I have attached two files. Together these represent a Chrome Extension. There is a standard manifest.json and a main.js file which does the work. Simply add these files to a folder and load these as an unpacked extension in Chrome. Upon loading the URL defined in the manifest.json you will see that the browser console ALLOWS the request on an alternate port.

If you run the same main.js file on a web server (and modify the domain name) you will see that anything that does NOT match the port you are visiting will properly fail.

Note that I chose dgrindle.com in the main.js and mainifest.json files, but this can be modified to any URL/server that is listening on multiple ports.

**CREDIT INFORMATION**  

Reporter credit: [Devin Grindle]

## Attachments

- [main.js](attachments/main.js) (text/plain, 234 B)
- [manifest.json](attachments/manifest.json) (text/plain, 229 B)
- [manifest.json](attachments/manifest_53072923.json) (text/plain, 233 B)

## Timeline

### rs...@chromium.org (2019-02-28)

[Empty comment from Monorail migration]

[Monorail components: Blink>SecurityFeature>CORS Platform>Extensions]

### sh...@chromium.org (2019-03-01)

[Empty comment from Monorail migration]

### rd...@chromium.org (2019-03-01)

AFAIK, this is working as intended.  The match patterns we use for permissions in extensions apply to all ports if the port is not explicitly specified.  We also properly inform the user that the extension can read and modify all data on that pattern.

I don't think this is really a security bug (or a bug at all).  Is there a particular attack that you were thinking of?

### gr...@gmail.com (2019-03-04)

Specifying a port within the match pattern does NOT properly block an extension from accessing a different port on the same domain name. I have attached another manifest.json which ONLY allows port 443, however the extension can still successfully reach port 8443.

With the manifest provided, users are shown that the extension only has permission to access https://dgrindle.com:443/* while the extension can clearly access other ports.

This is a security issue since users are lead to believe an extension only has access to a single port while in reality, the extension can potentially access information from another service/port.

w3 standards for Same-Origin clearly defines "An origin is defined by the scheme, host, and port of a URL" - https://www.w3.org/Security/wiki/Same_Origin_Policy. As such, an extension should be held to this same standard.

An example of how this could be abused: An extension could grab a set of credentials as they are logging into a specific URL. Those credentials could then be used by an extension to query/probe another port on the server. Some APIs run on different ports which could then give the extension direct access to the API. All of this could be done behind the scenes using fetch or ajax. If the extension only had permission to the port specified it would likely be more difficult to achieve the same level of access.

Please let me know if you have any questions.

### to...@chromium.org (2019-03-04)

The URL match pattern for the manifest does not support specifying the port, I think.
I cannot find a document that says it supports, and AFAIK internal implementation doesn't handle port match.

So I agreed that this is expected behavior.

Also some well-known ports that have a risk to be attacked by crafted http requests are still blocked by the network stack regardless of cors and manifest.

### gr...@gmail.com (2019-03-04)

The extension it's self does NOT run when directly navigating to https://dgrindle.com:8443 but does run on https://dgrindle.com:443. That said, it DOES appear that the match pattern is attempting to honor the port specified by the manifest, but not enforcing it.

Looking at the source for this, the comments clearly defines a port: https://src.chromium.org/viewvc/chrome/trunk/src/extensions/common/url_pattern.h

For the sake of security, content scripts should be held to the same restrictions as the context of web pages that user is visiting unless explicitly defined by the manifests permissions section. For example, with a Firefox add-on, permissions for that entire domain need to be granted in order to fetch a different port number.

### rd...@chromium.org (2019-03-04)

> The URL match pattern for the manifest does not support specifying the port, I think.

It is supported, just not well documented.

> Specifying a port within the match pattern does NOT properly block an extension from accessing a different port on the same domain name. I have attached another manifest.json which ONLY allows port 443, however the extension can still successfully reach port 8443.

Ah, that's interesting.  If the match pattern specifies a port, it should be restricted to that port.  (If the port is omitted as was the case in the original example, it defaults to '*', so it's expected that it have access.)

> With the manifest provided, users are shown that the extension only has permission to access https://dgrindle.com:443/* while the extension can clearly access other ports.

Note that in the installation prompt, we just say "dgrindle.com", rather than "dgrindle.com:443".  But in the chrome://extensions page, we do list the port.

----

URLPatterns have support for this, and it looks like we're properly applying the restrictions for content scripts and for extension API permissions (e.g., using chrome.tabs.executeScript).  I think we should do the same for CORS.  toyoshim@, what would it take to add support for (conditionally) restricting to a port in CorsOriginPattern?

### to...@chromium.org (2019-03-05)

Ah, OK.
I think it isn't so difficult to support port match in CorsOriginPattern and related code.

I'm not sure if I can work on this before the next branch-cut, but I can make a patch to support it once my works for the OOR-CORS beta trial is done.

May I change this bug type from Bug-Security to Feature?
If people still think this is a security bug that should be fixed ASAP, I will take this first.

### to...@chromium.org (2019-03-05)

tentatively set to M-75.

### rd...@chromium.org (2019-03-06)

> May I change this bug type from Bug-Security to Feature?
If people still think this is a security bug that should be fixed ASAP, I will take this first.

Thanks for taking a look!

I think this is a low-priority/severity security bug, but still mostly a security bug.  Technically, this is a violation of the security model - however, the surface is very slim, and from a permissions perspective, the user is already prompted for access to the full site (independent of port).  I think M75 is probably fine.

meacer@ may also have thoughts.

### to...@chromium.org (2019-03-06)

[Empty comment from Monorail migration]

### to...@chromium.org (2019-05-08)

Sorry, this work was suspended. Let me update the milestone.

### gr...@gmail.com (2019-05-08)

Thanks for the update. Looking forward to M-75. As a quick side note on this, I've noticed that if an extension is active on a site via it's IP, CORB DOES properly block connections to alternate ports. However, when visiting a site by its domain name, the extension is allowed to connect to alternative ports.

### to...@chromium.org (2019-05-09)

I have a prototype now, but launch will be postponed to be in m76.

https://crbug.com/chromium/936900#c13
Thank you for more information.
Let me add lukasza to CC for CORB behaviors, he leads the CORB feature.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-17)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/ea2d90b8198ef3112b272ce84df1dcad04632381

commit ea2d90b8198ef3112b272ce84df1dcad04632381
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Fri May 17 09:54:20 2019

OOR-CORS: Add port match support in network::cors::OriginAccessEntry

To support port matching in allow/block lists, now OriginAccessEntry
takes the port, and MatchesOrigin takes the port matching count in.

Blink callers updates, and mojom interface/callers updates will follow.

Bug: 936900
Change-Id: I2e616c4d71964407b07292679d57301fce4b7917
Tbr: tsepez@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1616708
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#660782}

[modify] https://crrev.com/ea2d90b8198ef3112b272ce84df1dcad04632381/services/network/public/cpp/cors/origin_access_entry.cc
[modify] https://crrev.com/ea2d90b8198ef3112b272ce84df1dcad04632381/services/network/public/cpp/cors/origin_access_entry.h
[modify] https://crrev.com/ea2d90b8198ef3112b272ce84df1dcad04632381/services/network/public/cpp/cors/origin_access_entry_unittest.cc
[modify] https://crrev.com/ea2d90b8198ef3112b272ce84df1dcad04632381/services/network/public/cpp/cors/origin_access_list.cc
[modify] https://crrev.com/ea2d90b8198ef3112b272ce84df1dcad04632381/third_party/blink/renderer/platform/weborigin/origin_access_entry.cc
[modify] https://crrev.com/ea2d90b8198ef3112b272ce84df1dcad04632381/third_party/blink/renderer/platform/weborigin/origin_access_entry.h


### to...@chromium.org (2019-05-20)

Now all CLs are ready for reviews.
3 more changes will be submitted to finish this work.

### to...@chromium.org (2019-05-20)

cc: reviewers

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6c44900c006b7c7dab5221c2817c233d380ab746

commit 6c44900c006b7c7dab5221c2817c233d380ab746
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Wed May 22 11:07:08 2019

OOR-CORS: Update blink::OriginAccessEntry to use the port

network::cors::OriginAccessEntry was updated to support port number.
This patches also update corresponding blink::OriginAccessEntry
so that it takes const SecurityOrigin& or const KURL& in ctors
in order to obtain the effective port. The port number is passed
to the network::cors::OriginAccessEntry to support the port match
in Blink.

Bug: 936900
Change-Id: I72d534280a4bd9a8296fe383385cd90e346f2b6c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1617049
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#662128}

[modify] https://crrev.com/6c44900c006b7c7dab5221c2817c233d380ab746/services/network/public/cpp/cors/origin_access_entry.h
[modify] https://crrev.com/6c44900c006b7c7dab5221c2817c233d380ab746/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/6c44900c006b7c7dab5221c2817c233d380ab746/third_party/blink/renderer/modules/credentialmanager/credentials_container.cc
[modify] https://crrev.com/6c44900c006b7c7dab5221c2817c233d380ab746/third_party/blink/renderer/platform/weborigin/origin_access_entry.cc
[modify] https://crrev.com/6c44900c006b7c7dab5221c2817c233d380ab746/third_party/blink/renderer/platform/weborigin/origin_access_entry.h
[modify] https://crrev.com/6c44900c006b7c7dab5221c2817c233d380ab746/third_party/blink/renderer/platform/weborigin/security_origin.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/71e356e2a44039197139e2f07bb43942df7b3310

commit 71e356e2a44039197139e2f07bb43942df7b3310
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Thu May 23 08:42:24 2019

OOR-CORS: Mechanical changes

- Rename CorsOriginAccessMatchMode to CorsDomainMatchMode
  in order to introduce network::mojom::CorsPortMatchMode.

- Replace int32_t port with uint16_t port and CorsPortMatchMode.

Bug: 936900
Change-Id: Ic5cbf91ee74366f3380fedc35349edf6c5f09bb6
Tbr: rdevlin.cronin@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1626061
Auto-Submit: Takashi Toyoshima <toyoshim@chromium.org>
Commit-Queue: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#662531}

[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/chrome/browser/loader/cors_origin_access_list_browsertest.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/chrome/common/extensions/chrome_extensions_client.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/extensions/common/cors_util.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/extensions/renderer/dispatcher.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/services/network/cors/cors_url_loader_unittest.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/services/network/public/cpp/cors/origin_access_entry.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/services/network/public/cpp/cors/origin_access_entry.h
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/services/network/public/cpp/cors/origin_access_entry_unittest.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/services/network/public/cpp/cors/origin_access_list.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/services/network/public/cpp/cors/origin_access_list.h
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/services/network/public/cpp/cors/origin_access_list_unittest.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/services/network/public/mojom/cors_origin_pattern.mojom
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/third_party/blink/renderer/core/dom/document.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/third_party/blink/renderer/modules/credentialmanager/credentials_container.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/third_party/blink/renderer/platform/weborigin/origin_access_entry.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/third_party/blink/renderer/platform/weborigin/origin_access_entry.h
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/third_party/blink/renderer/platform/weborigin/security_origin.cc
[modify] https://crrev.com/71e356e2a44039197139e2f07bb43942df7b3310/third_party/blink/renderer/platform/weborigin/security_policy.cc


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/dd77b000eb360e79d280975d4eccefce494a927f

commit dd77b000eb360e79d280975d4eccefce494a927f
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Thu May 23 10:20:36 2019

OOR-CORS: Update OriginAccessList to support port matching

This patch enables port matching in network::OriginAccessList.
Callers in Blink and chrome, or extensions will specify port
information to support port matching in following CLs.

In this CL, all callers still use kAnyPort not to make any
behavior changes.

Bug: 936900
Change-Id: I572ee883050035acb719aaabf71355048472c43a
Tbr: rdevlin.cronin@chromium.org
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1617561
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Tom Sepez <tsepez@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Cr-Commit-Position: refs/heads/master@{#662565}

[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/chrome/browser/loader/cors_origin_access_list_browsertest.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/chrome/common/extensions/chrome_extensions_client.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/extensions/common/cors_util.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/extensions/renderer/dispatcher.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/services/network/cors/cors_url_loader_unittest.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/services/network/public/cpp/cors/origin_access_entry.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/services/network/public/cpp/cors/origin_access_entry.h
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/services/network/public/cpp/cors/origin_access_entry_unittest.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/services/network/public/cpp/cors/origin_access_list.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/services/network/public/cpp/cors/origin_access_list.h
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/services/network/public/cpp/cors/origin_access_list_unittest.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/services/network/public/mojom/cors_origin_pattern.mojom
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/third_party/blink/renderer/platform/weborigin/security_policy.cc
[modify] https://crrev.com/dd77b000eb360e79d280975d4eccefce494a927f/third_party/blink/renderer/platform/weborigin/security_policy.h


### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/3c61688678e014ef3536fa13ef3cc69f809b7909

commit 3c61688678e014ef3536fa13ef3cc69f809b7909
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Fri May 24 05:22:12 2019

OOR-CORS: Chrome Extension's manifest supports port limit

With this change, specifying port in the manifest URLPattern
works even for CORS bypassing rules.

Bug: 936900
Change-Id: I3744b65307c923c9c593efef7a41a651ab67d494
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1619530
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Reviewed-by: Devlin <rdevlin.cronin@chromium.org>
Cr-Commit-Position: refs/heads/master@{#662973}

[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/chrome/browser/extensions/background_xhr_browsertest.cc
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/chrome/common/extensions/chrome_extensions_client.cc
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/content/shell/test_runner/test_runner.cc
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/extensions/common/cors_util.cc
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/extensions/renderer/dispatcher.cc
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/services/network/public/cpp/cors/origin_access_list_unittest.cc
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/third_party/blink/public/web/web_security_policy.h
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/third_party/blink/renderer/core/exported/web_security_policy.cc
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/third_party/blink/renderer/platform/weborigin/security_origin_test.cc
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/third_party/blink/renderer/platform/weborigin/security_policy.cc
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/third_party/blink/renderer/platform/weborigin/security_policy.h
[modify] https://crrev.com/3c61688678e014ef3536fa13ef3cc69f809b7909/third_party/blink/renderer/platform/weborigin/security_policy_test.cc


### to...@chromium.org (2019-05-24)

cc: people who were involved in the code reviews above.

Now all CLs were submitted. The feature will be available from m76.
It isn't in Canary yet. Please wait for 1 or 2 days to try it.

https://omahaproxy.appspot.com/
Versions which branch_base_position is >= 662973 will support the feature.

### sh...@chromium.org (2019-05-24)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-20)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-06-20)

Congrats the Panel decided to reward $500 for this report 

### na...@google.com (2019-06-20)

[Empty comment from Monorail migration]

### gr...@gmail.com (2019-06-20)

Hello,

I appreciate and will gladly accept the reward. I was looking over https://www.google.com/about/appsecurity/chrome-rewards/ and it shows "Site Isolation special rewards" and under "In scope:" it lists:

"Bugs that cause cross-site CORB-eligible responses not to be blocked. This includes HTML, XML, and JSON responses that have nosniff headers, assuming sites operators have taken the necessary steps.)"

I do believe the bug I reported was reported with "High-quality report with proof of concept/exploit" and the bug is CORB related (with reward amounts $5,000 - $8,000). Please confirm my eligibility regarding this.

This is my first reported Chrome bug so any additional details around what qualifies for a High-quality report, and how the payment process works would be greatly appreciated.

Thanks!

--Devin

### aw...@google.com (2019-06-24)

+natashapabrai@ for https://crbug.com/chromium/936900#c28

### gr...@gmail.com (2019-07-28)

Hello,

Just checking back on https://bugs.chromium.org/p/chromium/issues/detail?id=936900#c28 . Please confirm my eligibility regarding this.

### ad...@google.com (2019-07-29)

[Empty comment from Monorail migration]

### ad...@google.com (2019-07-29)

grindle09@gmail.com - sorry I can't help with your question in https://crbug.com/chromium/936900#c28, it may need to wait until the VRP panel next meets. But meanwhile please could you let me know how you'd like to be credited in the release notes? Thanks! (And thanks again for the bug report!)

### ad...@google.com (2019-07-29)

grindle09@gmail.com - I spotted it in the original bug description, please ignore.

### ad...@chromium.org (2019-07-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-30)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### is...@google.com (2019-11-23)

This issue was migrated from crbug.com/chromium/936900?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>SecurityFeature>CORS, Platform>Extensions]
[Monorail blocked-on: crbug.com/chromium/908756]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40094171)*
