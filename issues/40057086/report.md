# Security:  Cross-Origin information leak or delete in ContentIndex

| Field | Value |
|-------|-------|
| **Issue ID** | [40057086](https://issues.chromium.org/issues/40057086) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>ContentIndexing |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | so...@gmail.com |
| **Assignee** | ra...@chromium.org |
| **Created** | 2021-08-30 |
| **Bounty** | $5,000.00 |

## Description

**This template is ONLY for reporting security bugs. If you are reporting a**  

**Download Protection Bypass bug, please use the "Security - Download**  

**Protection" template. For all other reports, please use a different**  

**template.**

**Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com>**  

**/chromium/src/+/HEAD/docs/security/faq.md**

**Please see the following link for instructions on filing security bugs:**  

**<https://www.chromium.org/Home/chromium-security/reporting-security-bugs>**

**Reports may be eligible for reward payments under the Chrome VRP:**  

**<http://g.co/ChromeBugRewards>**

**NOTE: Security bugs are normally made public once a fix has been widely**  

**deployed.**

**-------------------------**

**VULNERABILITY DETAILS**  

In the mojo interface ContentIndexService::GetDescriptions, it will go to function |ContentIndexDatabase::GetDescriptionsOnCoreThread|:

"""  

service\_worker\_context\_->GetRegistrationUserDataByKeyPrefix(  

service\_worker\_registration\_id, kEntryPrefix,  

base::BindOnce(&ContentIndexDatabase::DidGetDescriptions,  

weak\_ptr\_factory\_core\_.GetWeakPtr(),  

service\_worker\_registration\_id, std::move(callback)));  

"""

But as you can see, it only take the id of service worker. This is an untrust arguments as it is from render process. From a compromised renderer process, the attacker can easy guest the |service\_worker\_registration\_id|(as it starts from 0) and enum it from 0 to 1000 etc... So I think we should check the origin as well.

This will lead to the attacker can get the information about content index descriptions from all origins which users accessed before.

On the other hand, another interface |Delete| seems like has the same problems.

how to reproduce:  

$python ./copy\_mojo\_js\_bindings.py /path/to/chrome/.../out/Debug/gen  

$out/Debug/chrome --enable-blink-features=MojoJS '<http://localhost:8000/victim.html>'  

$out/Debug/chrome --enable-blink-features=MojoJS '<http://localhost:8001/attacker.html>'

port 8000/victim.html is used for add a description for content index.  

port 8001/attacker.html is used for stole the other origin content index description.

**VERSION**  

**Chrome Version: [x.x.x.x] + [stable, beta, or dev]**  

**Operating System: [Please indicate OS, version, and service pack level]**

**REPRODUCTION CASE**  

**Please include a demonstration of the security bug, such as an attached**  

**HTML or binary file that reproduces the bug when loaded in Chrome. PLEASE**  

**make the file as small as possible and remove any content not required to**  

**demonstrate the bug, or any personal or confidential information.**

**Please attach files directly, not in zip or other archive formats, and if**  

**you've created a demonstration site please also attach the files needed to**  

**reproduce the demonstration locally.**

**FOR CRASHES, PLEASE INCLUDE THE FOLLOWING ADDITIONAL INFORMATION**  

Type of crash: browser  

**Crash State: [see link above: stack trace \*with symbols\*, registers,**  

**exception record]**  

**Client ID (if relevant): [see link above]**

**CREDIT INFORMATION**  

**Externally reported security bugs may appear in Chrome release notes. If**  

**this bug is included, how would you like to be credited?**  

Reporter credit: SorryMybad(@S0rryMybad) of Kunlun Lab

## Attachments

- [PoC.zip](attachments/PoC.zip) (application/octet-stream, 2.4 KB)

## Timeline

### [Deleted User] (2021-08-30)

[Empty comment from Monorail migration]

### dr...@chromium.org (2021-08-30)

I'm not able to reproduce this, and the Mojo interface for ContentIndexService says the origin is validated: https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/public/mojom/content_index/content_index.mojom;drc=9326011fbf774bbf613b8afc03b74d76ee0b5952;l=66

Are there any additional flags/configurations needed to reproduce this?

### so...@gmail.com (2021-08-30)

As I hard encode the launchUrl of |Add| interface to "http://127.0.0.1:8000" in victim.js so may be the victim add the description failed if use |localhost| to access html(Add interface checks origin but the bug is NOT here). This is not related to the bug in |GetDescriptions| interface. Please use this to reproduce:

how to reproduce:
$python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/Debug/gen
$out/Debug/chrome --enable-blink-features=MojoJS  'http://127.0.0.1:8000/victim.html'
$out/Debug/chrome --enable-blink-features=MojoJS  'http://127.0.0.1:8001/attacker.html'

and confirm the victim executed as normal(we need to add the description success otherwise there are no descriptions to get in attacker.js).

The second hard encode is the service id I use 0x0, so you need to confirm the victim.js is the first service worker we access.

Yes, the Mojo interface says the origin is validated but the code NOT, for the interface entry in code:
"""
void ContentIndexServiceImpl::GetDescriptions(
    int64_t service_worker_registration_id,
    GetDescriptionsCallback callback) {
  DCHECK_CURRENTLY_ON(BrowserThread::UI);

  content_index_context_->database().GetDescriptions(
      service_worker_registration_id, std::move(callback));
}
"""
It only transfer |service_worker_registration_id|(without origin) to ContentIndexDatabase::GetDescriptions so it is impossible for validating the origin. The bug in code is clear and may be the owner of ContentIndex will get my point.

### [Deleted User] (2021-08-30)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### so...@gmail.com (2021-09-02)

PING?

### ct...@chromium.org (2021-09-02)

Adding ContentIndexing owners FYI while I work on reproducing this.

I'm running into issues with getting this to repro. Here are the steps I took to try to repro this:

0. Build chrome in outdir ~/chromium/src/out_linux/Release
1. Extract PoC.zip and cd into the directory.
2. Run `python copy_mojo_js_bindings.py ~/chromium/src/out_linux/Release/gen/`
3. In a first terminal, run `python -m SimpleHTTPServer 8000`.
4. In a second terminal, run `python -m SimpleHTTPServer 8001`.
5. In a third terminal, run `mkdir /tmp/crbug1244568`, then cd into ~/chromium/src/ and run `./out_linux/Release/chrome --user-data-dir=/tmp/crbug1244568 --enable-blink-features=MojoJS "http://localhost:8000/victim.html"`

This loads the URL in a tab but the renderer immediately gets killed with RESULT_CODE_KILLED_BAD_MESSAGE which seems like it's running afoul of Mojo message validation.  Reloading the page seems to work.

6. Open a new tab in the chromium instance and navigate to http://localhost:8001/attacker.html

In the attacker tab, I see a console log message "0" for line 31 (`console.log(result.error);`) not for line 33 (which I think is the "successful attack" output line).

Am I doing something wrong in my reproduction steps? Could you provide exact details of the chromium version/checkout revision you used? I'm using a fairly recently updated checkout at r917279.





[Monorail components: Blink>ContentIndexing]

### so...@gmail.com (2021-09-03)

Re https://crbug.com/chromium/1244568#c6

Please check my update comment at https://crbug.com/chromium/1244568#c3, PLEASE USE "http://127.0.0.1:8000/victim.html" and "http://127.0.0.1:8001/attacker.html", DON'T USE localhost

### [Deleted User] (2021-09-03)

Thank you for providing more feedback. Adding the requester to the cc list.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ct...@chromium.org (2021-09-03)

Ah, I missed that clarification -- sorry! Thanks for bearing with me :-) With these updated repro steps I am able to reproduce:

0. Build chrome in outdir ~/chromium/src/out_linux/Release
1. Extract PoC.zip and cd into the directory.
2. Run `python copy_mojo_js_bindings.py ~/chromium/src/out_linux/Release/gen/`
3. In a first terminal, run `python -m SimpleHTTPServer 8000`.
4. In a second terminal, run `python -m SimpleHTTPServer 8001`.
5. In a third terminal, run `mkdir /tmp/crbug1244568`, then cd into ~/chromium/src/ and run `./out_linux/Release/chrome --user-data-dir=/tmp/crbug1244568 --enable-blink-features=MojoJS "http://l127.0.0.1:8000/victim.html"`

If the renderer crashes when loading, reload and it should work before proceeding.

6. Open a new tab in the chromium instance and navigate to http://localhost:8001/attacker.html
7. Check the console and see:

0   attacker.js:31
ContentDescription    attacker.js:33
{
    "id": "123",
    "title": "abc",
    "description": "secret",
    "category": 0,
    "icons": [
        {
            "src": "abc",
            "sizes": null,
            "type": null
        }
    ],
    "launchUrl": "http://127.0.0.1:8000"
}

Which is the cross-origin service worker description.

Looking at the victim.js and attacker.js, it's interesting that both seem to require a compromised renderer (both the victim script and the attacker script are using MojoJS bindings). Reporter: could you clarify what about the MojoJS bindings are required in the victim for this to work? It doesn't make this seem infeasible in practice, I just found it curious enough to warrant further investigation :-)

Setting security labels:
- Security_Severity-High: This is cross-origin disclosure bug, which is potentially a site-isolation bypass. While this does require a compromised renderer, we have historically still assigned such bugs Sev-High (see https://crbug.com/chromium/917668 per the severity guidelines [1])
- FoundIn-77: It looks like this dates back to crrev.com/c/1660655 (and this comment thread [2] from tsepez@ about the IDs from a month later)
- OS=All Blink platforms: It seems likely that this affects all platforms with Blink service worker logic. Feature team please update if this does not affect e.g. Android.

Assigning to rayankans@ now that I've been able to reproduce.


[1] https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-high-severity
[2] https://chromium-review.googlesource.com/c/chromium/src/+/1660655/comments/55a23c38_252fe36f

### [Deleted User] (2021-09-03)

[Empty comment from Monorail migration]

### so...@gmail.com (2021-09-03)

The victim.js DOES NOT require a compromised renderer, you can add description with normal web API like here:
https://developer.mozilla.org/en-US/docs/Web/API/ContentIndex



### ct...@chromium.org (2021-09-03)

Thanks for the clarification! So just a convenience and not necessary, which was my initial guess.

### [Deleted User] (2021-09-04)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-09-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6ef569fd764a8e5f8fba4dcff830d460e406362b

commit 6ef569fd764a8e5f8fba4dcff830d460e406362b
Author: Rayan Kanso <rayankans@google.com>
Date: Mon Sep 06 16:09:15 2021

[ContentIndex] Add Origin checks to mojo methods.

Bug: 1244568
Change-Id: I5a63a2e478577913a3b35154464c1808f7291f40
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140385
Reviewed-by: Richard Knoll <knollr@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Commit-Position: refs/heads/main@{#918606}

[modify] https://crrev.com/6ef569fd764a8e5f8fba4dcff830d460e406362b/content/browser/content_index/content_index_database.cc
[modify] https://crrev.com/6ef569fd764a8e5f8fba4dcff830d460e406362b/content/browser/content_index/content_index_database.h
[modify] https://crrev.com/6ef569fd764a8e5f8fba4dcff830d460e406362b/content/browser/content_index/content_index_database_unittest.cc
[modify] https://crrev.com/6ef569fd764a8e5f8fba4dcff830d460e406362b/content/browser/content_index/content_index_service_impl.cc


### ra...@chromium.org (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-07)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-08)

Requesting merge to extended stable M92 because latest trunk commit (918606) appears to be after extended stable branch point (885287).

Requesting merge to stable M93 because latest trunk commit (918606) appears to be after stable branch point (902210).

Requesting merge to beta M94 because latest trunk commit (918606) appears to be after beta branch point (911515).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-09-08)

This bug requires manual review: We are only 12 days from stable.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/main/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: govind@(Android), harrysouders@(iOS), matthewjoseph@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ra...@chromium.org (2021-09-08)

1. Does your merge fit within the Merge Decision Guidelines?

Yes

2. Links to the CLs you are requesting to merge.

https://chromium-review.googlesource.com/c/chromium/src/+/3140385

3. Has the change landed and been verified on ToT?

Yes

4. Does this change need to be merged into other active release branches (M-1, M+1)?

No

5. Why are these changes required in this milestone after branch?

Security issue

6. Is this a new feature?

No

7. If it is a new feature, is it behind a flag using finch?

N/A

### sr...@google.com (2021-09-08)

Merge approved for M94 branch:4606 pls merge asap

### am...@chromium.org (2021-09-08)

even though it's a non-trivial change it does fix a fairly substantial bug, so unless there's any issues exhibited on Canary thus far or other concerns, please go ahead merge this to branch 4577 by tomorrow (Thursday) 2pm PDT so that this fix can be included in next week's stable channel security refresh. Thank you! 

### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3907d1140b44cac8f2eb71bcc9ec88d4d3e5b2af

commit 3907d1140b44cac8f2eb71bcc9ec88d4d3e5b2af
Author: Rayan Kanso <rayankans@google.com>
Date: Thu Sep 09 11:16:13 2021

[ContentIndex] Add Origin checks to mojo methods.

(cherry picked from commit 6ef569fd764a8e5f8fba4dcff830d460e406362b)

Bug: 1244568
Change-Id: I5a63a2e478577913a3b35154464c1808f7291f40
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140385
Reviewed-by: Richard Knoll <knollr@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#918606}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3149996
Reviewed-by: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Cr-Commit-Position: refs/branch-heads/4577@{#1220}
Cr-Branched-From: 761ddde228655e313424edec06497d0c56b0f3c4-refs/heads/master@{#902210}

[modify] https://crrev.com/3907d1140b44cac8f2eb71bcc9ec88d4d3e5b2af/content/browser/content_index/content_index_database.cc
[modify] https://crrev.com/3907d1140b44cac8f2eb71bcc9ec88d4d3e5b2af/content/browser/content_index/content_index_database.h
[modify] https://crrev.com/3907d1140b44cac8f2eb71bcc9ec88d4d3e5b2af/content/browser/content_index/content_index_database_unittest.cc
[modify] https://crrev.com/3907d1140b44cac8f2eb71bcc9ec88d4d3e5b2af/content/browser/content_index/content_index_service_impl.cc


### gi...@appspot.gserviceaccount.com (2021-09-09)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/3fabcee42cb83e42f86263f8c7b4be9cd0ef6275

commit 3fabcee42cb83e42f86263f8c7b4be9cd0ef6275
Author: Rayan Kanso <rayankans@google.com>
Date: Thu Sep 09 12:50:45 2021

[ContentIndex] Add Origin checks to mojo methods.

(cherry picked from commit 6ef569fd764a8e5f8fba4dcff830d460e406362b)

Bug: 1244568
Change-Id: I5a63a2e478577913a3b35154464c1808f7291f40
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140385
Reviewed-by: Richard Knoll <knollr@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#918606}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3149775
Reviewed-by: Michael van Ouwerkerk <mvanouwerkerk@chromium.org>
Cr-Commit-Position: refs/branch-heads/4606@{#889}
Cr-Branched-From: 35b0d5a9dc8362adfd44e2614f0d5b7402ef63d0-refs/heads/master@{#911515}

[modify] https://crrev.com/3fabcee42cb83e42f86263f8c7b4be9cd0ef6275/content/browser/content_index/content_index_database.cc
[modify] https://crrev.com/3fabcee42cb83e42f86263f8c7b4be9cd0ef6275/content/browser/content_index/content_index_database.h
[modify] https://crrev.com/3fabcee42cb83e42f86263f8c7b4be9cd0ef6275/content/browser/content_index/content_index_database_unittest.cc
[modify] https://crrev.com/3fabcee42cb83e42f86263f8c7b4be9cd0ef6275/content/browser/content_index/content_index_service_impl.cc


### am...@chromium.org (2021-09-09)

there is no longer another test of Extended Stable channel planned for M92 

### am...@chromium.org (2021-09-13)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-13)

[Empty comment from Monorail migration]

### vo...@google.com (2021-09-15)

[Empty comment from Monorail migration]

### [Deleted User] (2021-09-15)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-15)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-09-15)

Hello, SorryMyBad! The VRP Panel has decided to award you $5000 for this report. If you can demonstrate (as with a POC) this issue to be accessible and exploitable via the open web vs the MojoJS bindings (as alluded to/theorized in your https://crbug.com/chromium/1244568#c11), would be happy to revisit this report reassess for a potentially higher reward amount. 
Thank you for this report and nice work! 

### gi...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2021-09-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/dcad2b2a1a2656654a73486499c4c461bd6387c8

commit dcad2b2a1a2656654a73486499c4c461bd6387c8
Author: Zakhar Voit <voit@google.com>
Date: Thu Sep 16 10:42:52 2021

[M90-LTS] [ContentIndex] Add Origin checks to mojo methods.

(cherry picked from commit 6ef569fd764a8e5f8fba4dcff830d460e406362b)

Bug: 1244568
Change-Id: I5a63a2e478577913a3b35154464c1808f7291f40
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3140385
Reviewed-by: Richard Knoll <knollr@chromium.org>
Commit-Queue: Rayan Kanso <rayankans@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#918606}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3162596
Reviewed-by: Jana Grill <janagrill@google.com>
Reviewed-by: Rayan Kanso <rayankans@chromium.org>
Owners-Override: Jana Grill <janagrill@google.com>
Commit-Queue: Zakhar Voit <voit@google.com>
Cr-Commit-Position: refs/branch-heads/4430@{#1604}
Cr-Branched-From: e5ce7dc4f7518237b3d9bb93cccca35d25216cbe-refs/heads/master@{#857950}

[modify] https://crrev.com/dcad2b2a1a2656654a73486499c4c461bd6387c8/content/browser/content_index/content_index_database.cc
[modify] https://crrev.com/dcad2b2a1a2656654a73486499c4c461bd6387c8/content/browser/content_index/content_index_database.h
[modify] https://crrev.com/dcad2b2a1a2656654a73486499c4c461bd6387c8/content/browser/content_index/content_index_database_unittest.cc
[modify] https://crrev.com/dcad2b2a1a2656654a73486499c4c461bd6387c8/content/browser/content_index/content_index_service_impl.cc


### vo...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-09-16)

[Empty comment from Monorail migration]

### am...@google.com (2021-10-08)

[Empty comment from Monorail migration]

### [Deleted User] (2021-12-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1244568?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40057086)*
