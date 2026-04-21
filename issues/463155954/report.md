# Extensions can hijack Gemini in the browser webview process to perform PE attacks by abusing DNR permissions, allowing stealing prompts, PII leakage, unrestricted access to camera-microphone and more

| Field | Value |
|-------|-------|
| **Issue ID** | [463155954](https://issues.chromium.org/issues/463155954) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SecurityFeature>ContentSecurityPolicy |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, iOS, ChromeOS |
| **Reporter** | we...@gmail.com |
| **Assignee** | ke...@chromium.org |
| **Created** | 2025-11-23 |
| **Bounty** | $7,000.00 |

## Description

---

### Report description

Extensions can hijack Gemini in the browser webview process to perform PE attacks by abusing DNR permissions, allowing stealing prompts, PII leakage, unrestricted access to camera-microphone and more

---

### Bug location

#### Where do you want to report your vulnerability?

Chrome VRP – Report security issues affecting the Chrome browser. [See program rules](https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules)

#### Which URL (or repository) have you found the vulnerability in?

Gemini (webview) in the browser

---

### The problem

#### Please describe the technical details of the vulnerability

(DEMO VID - <https://drive.google.com/file/d/1rA5FdPQwvEtuskNB_qaGXIXdXksAYjma/view?usp=sharing>)

New Gemini in the browser feature in Chrome allows users to activate a new window that renders a special component of a Gemini instance that combines capabilities of generating remote Gemini AI responses and manipulating the browser based on them.

This new component is very clearly a browser-level entity, baked into the browser, aiming to be a builtin enhancement of it, thus superior to websites and installed extensions.

This is clearly proven by Chrome's implemented enforcement around this new component, where affecting it from outside isn't allowed and explicitly blocked. For example, executing content-scripts or attaching debugger capabilities against the special component fail to take place completely.

What's further clear is that this isn't an origin-level decision, but a process decision, because injecting content-scripts to `gemini.google.com` via extensions is allowed if loaded as an ordinary website, but not when attempted against the new special component.

This expresses how Gemini in the browser is a feature that serves the browser itself and therefore must remain superior to inferior entities such as websites an extensions.

Unfortunately, it seems that DeclarativeNetRequests (DNR) permissions were not taken into account, with which a malicious extension can inject code directly under gemini.google.com within the special webview component of Gemini in the browser, thus allowing to undermine and hijack it completely.

All an attacker has to do is to use DNR to remove protecting headers (e.g. CSP, DiP, CORP, etc) and then redirect one script served by the Gemini app with an attacker controlled script.

To be more specific, here are the challenges required to tackle in order to perform the attack successfully:

1. First, find a script that is not necessary for the Gemini web app so we can replace it with our own. For that I picked `https://www.gstatic.com/feedback/js/help/prod/service/lazy.min.js` and used DNR to redirect it to `https://weizmangal.com/public/try.js` which is a JS I control
2. CSP won't allow it, therefore we craft a DNR rule to drop CSP of `gemini.google.com` all together
3. Within the webview context, the Gemini app counts on SAB which requires a document-isolation-policy. This is a problem because that same policy rejects my script coming from a cross-origin, so I simply replace its value to `isolate-and-credentialless` so that SAB works but pulling cross-origin scripts works too
4. Next, since DNR works with `https:` URLs, I had to pull my malicious code from the web, but I didn't want people to see what I'm up to online and also I needed a faster way to work than deploy scripts online every few seconds. Therefore, I implemented a mechanizm that implements the attack in B64 and sets it to the DNR URL as a query param, pointing at a constant online script that takes the B64 from the query param and executes it (this is essentially the only visible difference between each of the attached `rules.json` files).

#### Impact analysis – Please briefly explain who can exploit the vulnerability, and what they gain when doing so

(DEMO VID - <https://drive.google.com/file/d/1rA5FdPQwvEtuskNB_qaGXIXdXksAYjma/view?usp=sharing>)

Anyone with access to installed extensions with common DNR permissions can perform this attack, whether by tricking users into installing malicious extensions or by infecting already legit extensions into doing this (e.g. AdBlock already has necessary permissions to perform such an attack). For starters, `rules.json` shows how we manage to run a simple `console.log` under `gemini.google.com` within the webview.

The impact that can be achieved is as wide as the range of capabilities the Gemini in the browser process is exposed to, for example:

1. An attacker can intercept requests and responses within the app to steal/fabricate prompt communication with Gemini (`rules_intercept.json`)
2. An attacker can phish the user into interacting with fake layout to be tricked into providing sensitive information (`rules_phish.json`)
3. An attacker can ride on the already established communication channel with the host of the webview (`chrome://glic`) and intercept post messages to either steal sensitive information or force the browser to perform sensitive actions (`rules_leak_pii.json`)
4. An attacker can escalate its privileges and access capabilities it does not hold from the stance of an extension, such as camera and microphone (`rules_pe.json`)

All of those will be demonstrated in the attached PoC.

At first glance it might seem that most of this impact can be trivially achieved once an extension has access to DNR permissions. For example, intercepting Gemini requests and/or drawing fraudulent phishing layout can be done against the web app just as well. However, this is fundamentally different for the following reason:

As opposed to the Gemini web app, to which an extension is naturally superior, the Gemini in the browser webview is served as part of the browser, which sends a message to the user that says "this is a highly trusted component, not like websites". Given that, undermining it is more impactful. A proof of that is how the Gemini web app is allowed to be injected with content-scripts, but when loaded within the webview, isn't.

Not only the component can be attacked when looked at as the ordinary Gemini web app, but within this special context, new attack surface becomes available. I was able to ride on the established communication with the embedder of the webview and intercept exchanged messages between them. For example, I've learned how message `glicBrowserGetUserProfileInfo` leaks the name and gmail account that is logged into the browser on the profile level, which is not trivially accessible to extensions. Furthermore, I was able to make the host perform any operation it is designed to support coming from the app, such as opening new tabs, resizing the webview window and more.

This discovery arrives just in time, right before `glicBrowserCreateTask`, `glicBrowserPerformActions`, `glicBrowserJournalSnapshot` and more are fully utilized, allowing attackers to perform far more damage by learning what Gemini actors do and perhaps instruct them maliciously.

On top of that, since the process is endowed with special capabilities such as access to camera or microphone (after user settings activation), malicious code running within this process can access those without prompting the user for permission, unlike how site permissions usually work. This effectively allows an attacker coming from an extension without such power, to ride the Gemini in browser webview and access such devices without any need for user interaction (except for starting Gemini) - aka, a classic escalation of privileges attack.

---

### The cause

#### What version of Chrome have you found the security issue in?

142.0.7444.176 stable

#### Is the security issue related to a crash?

No, it is not related to a crash.

#### Choose the type of vulnerability

Privilege Escalation

#### How would you like to be publicly acknowledged for your report?

Gal Weizman

## Attachments

- README.md (application/octet-stream, 7.7 KB)
- rules_pe.json (application/json, 4.1 KB)
- rules_intercept.json (application/json, 3.0 KB)
- rules.json (application/json, 2.5 KB)
- rules_phish.json (application/json, 4.4 KB)
- rules_leak_pii.json (application/json, 3.1 KB)
- manifest.json (application/json, 1012 B)
- gemini_demo2.mov (video/quicktime, 117.9 MB)
- bnbndddd3.pdf (application/pdf, 10.3 KB)
- index.html (text/html, 11.5 KB)
- manifest.json (application/json, 1.1 KB)
- rules_local_file_read.json (application/json, 11.2 KB)
- README.md (text/markdown, 8.9 KB)
- gemini_demo.mov (video/quicktime, 214.9 MB)

## Timeline

### we...@gmail.com (2025-11-24)

Seems like the standard funnel of reporting via bughunters.google.com did not focus on steps to reproduce. While they can be found within the attached README file, I'm adding them here as well for visibility:

To perform the most basic PoC, which shows how code is executed under `gemini.google.com` within the special webview component, simply:

1. Place all files (`manifest.json` and rules files) within a single folder
2. Load them as unpacked extension via `chrome://extensions` under `Developer Mode`
3. Open the browser and start Gemini in the browser - the attack should take place without additional interaction (the default attack that is enabled abuses code execution for `console.log` purposes only and is therefore visible only via devtools - for more visible attacks, try enabling `rules_phish` or `rules_pe`)

As described further below, here are attached a `manifest.json` and a few rules files. There are 5 attacks to be demonstrated.
In order to reproduce each attack, simply enable it by changing `enabled` from `false` to `true` in the `manifest.json` file for the desired attack to be shown. Please have only one enabled at a time. Then, follow the same steps as described above.

### we...@gmail.com (2025-11-24)

Hi folks,

Since yesterday, I managed to escalate the impact significantly to:

- open tabs and focus on them
- read their contents
- take screenshots of them

Since all of the above apply to `file://` URLs just as well, this attack allowed me to successfully read local files, list directories, access PDF contents, etc - requiring zero interaction from the user once the webview process was started.

I am adding here a few extra files to run this demo as well:

- `gemini_demo2.mov` - the demo video of this attack specifically
- `rules_local_file_read.json` - the DNR JSON file that performs this new attack
- `manifest.json` - the same as before, only with reference to the new JSON rules file (enabled by default)
- `README.md` - the same README file as before, only updated to include this impact enhancement and steps to reproduce
- `index.html` - the file I was using in the demo video to quickly show the artifcats of the attack (served over either `http:` or `file:`)
- `bnbndddd3.pdf` - the PDF file the attack reads. place under `/var/tmp/bnbndddd3.pdf` (test on Mac OS)

Also, on top of the former shared steps-to-reproduce, the following instructions were added to the attached README file:

NOTICE: in order to examine attack #6 (aka `rules_local_file_read.json`), in addition to the instructions above, please also place the attached PDF file under `/var/tmp/bnbndddd3.pdf` (test on Mac OS). After the attack completes, open the devtools of the Gemini webview process and run `copy(results)` in the console - this will copy a JSON of the results of the attack onto your clipboard. To easily view the results, visit the attached `index.html` file and throw the JSON in the textarea box (for context, even though is not shown in this demo, leaking this information from the process to a remote server is trivial since CSP headers are being removed as part of the attack).

p.s. I added here the former video too so it is more accessible

### fl...@google.com (2025-11-25)

Security shepherd here.

I will confess I don't know enough about CSP and related headers to fully triage this one myself.  mkwst@, I'm hoping perhaps you can lend some help here :) 

I think this *might* be covered by the security extensions FAQ: https://chromium.googlesource.com/chromium/src/+/main/extensions/docs/security_faq.md#I_ve-found-written-an-extension-that-can-access-sensitive-user-data_like-passwords-and-emails_Is-this-a-security-bug-in-Chromium  If `declarativeNetRequest` is inherently a permission that lets an extension futz with network requests, and that includes CSP, then this may be working-as-intended.

But if the set of permissions in manifest.json *should* be insufficient for the behavior shown in this exploit, then that is a problem.

Out of an abundance of caution I'm setting a provisional severity of S1, to ensure this gets triaged swiftly in the event it's in fact that serious (I'm not sure if this would count as a full vs partial circumvention).  But mkwst@ please update the bug / downgrade the severity as necessary as I'm somewhat out of my depth!

### mk...@chromium.org (2025-11-25)

If an extension has host privileges for a given origin, then it's unsurprising that it can control that domain's headers and content. That's a risk decision we allow users to make when installing extensions, and many popular and useful extensions depend upon that ability.

That said, if it's the case that we're giving `gemini.google.com` additional privileges when it's running in the context of the embedded sidebar experience (either directly or by giving it privileged access to `chrome://glic`), then it might make sense for us to treat it with a level of care similar to our stance on other WebUI pages or the similarly-empowered `chromewebstore.google.com`. Preventing extension access (directly or indirectly) to that privileged context might be reasonable.

Shifting this to rdcronin@ for the extension question, and adding vollick@ and carlosk@ as owners of the relevant browser-side component who might be able to help us opine on the expected threat model.

### we...@gmail.com (2025-11-25)

> If an extension has host privileges for a given origin, then it's unsurprising that it can control that domain's headers and content. That's a risk decision we allow users to make when installing extensions, and many popular and useful extensions depend upon that ability.

I disagree here. While it’s true the user takes upon themselves that the extension they install may interfere with content their user agent renders, that clearly extends no further than just websites. Installing an extension is never a user consent for it to interfere with other extensions they have, or even worse - a browser level component, regardless of whether it is loaded via chrome:// or https://.

The power of the permission isn’t enough on its own to determine whether it can be activated or not, but jurisdiction matters too - extensions should not have such power over other extensions or browser level component such as gemini in the browser.

Content scripts are an excellent analogy here, because they do adhere to this approach. In fact, they do so here as well exactly how I’d expect from dnr - they are 100% attachable to the genini web app when visited via an ordinary tab, but are not attachable when loaded within the webview process as part of the browser (even though both scenarios load the exact same app). This is the correct behavior that dnr should apply as well.

The context here btw is bigger - i was able to compromise multiple other vendors due to this behavior which raises a bigger question of how should this be addressed? Should vendors become aware of this and avoid loading sub resources in sensitive areas (extensions/browser components), or should the platform (chromium) redefine dnr to defend against this?

For starters, vendors should definitely find safer ways to load sub resources to avoid this type of attack. Then a discussion around dnr should start too. IMO.

### ch...@google.com (2025-11-25)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-11-25)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### mk...@chromium.org (2025-11-25)

I think we're more or less agreeing here: it could make sense to limit the ability to extensions to interfere with a web origin when it's being loaded in a privileged context distinct from a normal browser tab, just as we do when the web origin itself is privileged.

I'll defer to Devlin on the expectations from the extensions team, but that seems like a reasonable line to draw from my perspective.

### rd...@chromium.org (2025-11-25)

Yeah, this is *not* WAI IMO. Gemini in chrome has special powers, and it should be isolated. This is supposed to happen as part of gemini being embedded (in this context) in a <webview>, which should prevent extensions (other than the embedding extension, if there is one) from running in it. We do this for webRequest [here](https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/web_request/extension_web_request_event_router.cc;l=2561-2567;drc=b32663066c4707a90f117b579f1993c7b74a0ad1). If we don't do that for DNR, we should.

kelvinjiang@, can you take a look?

erikchen@, FYI (and please confirm that gemini is still being embedded in a <webview>, which is an important part of the security assumptions.)

### er...@google.com (2025-11-25)

> erikchen@, FYI (and please confirm that gemini is still being embedded in a <webview>, which is an important part of the security assumptions.)

Yes, we are still embedding in <webview>, see: 
https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/resources/glic/webview.ts;l=134

### we...@gmail.com (2025-11-25)

> I think we're more or less agreeing here: it could make sense to limit the ability to extensions to interfere with a web origin when it's being loaded in a privileged context distinct from a normal browser tab, just as we do when the web origin itself is privileged.

100%.

> Yeah, this is not WAI IMO. Gemini in chrome has special powers, and it should be isolated. This is supposed to happen as part of gemini being embedded (in this context) in a <webview>, which should prevent extensions (other than the embedding extension, if there is one) from running in it. We do this for webRequest here. If we don't do that for DNR, we should.

Agree on the "not WAI", a 100%.

However, focusing on it being a webview and deriving the solution from there won't give us the end result we're after, because the problem here is bigger than the brand of the embedder.

The bigger context as mentioned above, is that because of how DNR is permitted against `https:` requests (e.g. `https://example.com/good.js`) within any `https://` context (e.g. `https://example.com`), its successful activation is agnostic to whether the intercepted context is embedded via a webview or an iframe for example.

This was successfully proved in a number of ways:

1. In addition to Gemini in the browser, we are working with multiple other vendors who were similarly vulnerable via this attack. For them it was via an iframe rather than a webview, but it was the same attack.
2. No need to seek so far - `gemini.google.com` embeds an iframe to `accounts.google.com/rotateCookies` (or something similar), which is vulnerable to this hijack just as well. In other words, if you fix this for webviews specifically, an attacker could revive this attack via that iframe instead.

As far as I see this, you have two possible ways to go about this:

1. Fix DNR (Chromium) - declare this to be a flaw in the specification/implementation of extensions in chromium and force any context to reject DNR powers if that context is embedded within a privileged page.
2. Fix Gemini in the browser (Chrome) - decide this isn't a flaw in DNR and that this behaviour is intentional, and therefore fix the implementation specifically. For example, implement the webview fix you propose but also remove the iframe since it is hijackable too. This choice btw will force all vendors around the world who are currently affected by this to adjust themselves (and quickly after this becomes public), and based on what I've seen so far, it's going to be quite hard and painful for them.

I would strongly advise choosing the former option, but my knowledge of the system and spec decisions is limited.

I hope I clarified how I see this, I just don't want you to address this from one perspective (e.g. `webview`) only to remain vulnerable from another (e.g. rotateCookies `iframe`).

Happy to hear your thoughts.

### we...@gmail.com (2025-11-25)

On top of that, one may wonder why this report was initially framed as a vulnerability in GITB specifically, only to arrive at a conclusion that this is a DNR implementation flaw instead, so i feel the need to clarify:

This report really addresses both, expecting one or the other to be fixed (fixing both is redundant).

Whether resolving this issue is fixing DNR or GITB implementation is up for us to discuss, and whatever you end up choosing will be the issue this report represents.

What I’m aiming at is to say that both discoveries are hereby disclosed to you as two individuals, but under one ticket since fixing the overall issue requires addressing only one (either “GITM is hijackable via DNR” or “DNR works against resources embedded under privileged pages”).

As clarified above, i lean towards fixing DNR itself.

### rd...@chromium.org (2025-11-25)

The concept of a "privileged page" is ambiguous. In general, we very rarely restrict sites in Chrome via the origin -- the primary cases we do that are only for things like the webstore and safe browsing. Restrictions are more commonly handled by either changing the scheme (e.g. to chrome://) or via things like <webview>, where we (should) look at the embedder to determine if an extension is allowed to run.

Extensions can access and run, by design, in the web interface for gemini.google.com; that's unlikely to change. If there's any surface that's using gemini.google.com and *not* embedding it through another mechanism, it should anticipate that (appropriately permissioned) extensions can run, and, similarly, it should *not* be granted extra powers by the browser. In this case, we isolate gemini.google.com in the webview precisely so that it is cordoned off from the rest of the browser, and the capabilities should not be exposed to the same site if you visited it in a tab.

So, for something like this:

> No need to seek so far - gemini.google.com embeds an iframe to accounts.google.com/rotateCookies (or something similar), which is vulnerable to this hijack just as well. In other words, if you fix this for webviews specifically, an attacker could revive this attack via that iframe instead.

If you visit gemini.google.com, even if you modified accounts.google.com/rotateCookies (or just ran a content script on the page), that should not result in being able to manipulate the *browser* in the same way that modifying the gemini surface in the browser is able to. If those capabilities are exposed to gemini.google.com in a surface outside the webview where it's embedded by webui, that's a bug and, I believe, against the intended design of embedding gemini in the browser.

### ke...@chromium.org (2025-11-25)

I'll be away starting tomorrow for 1.5 weeks but I can take a look:

As Devlin mentioned [here](https://issues.chromium.org/u/1/issues/463155954#comment10), the browser explicitly prevents listeners from matching on a request. For DNR, during relevant request phases, the browser finds any matching rules and acts upon them and this check does not apply for DNR.

[this](https://source.chromium.org/chromium/chromium/src/+/main:extensions/browser/api/declarative_net_request/ruleset_manager.cc;l=509;drc=4c86c7940a47c36b8bf52c134483ef2da86caa62;bpv=1;bpt=1) is probably where we should add "don't evaluate this request since it's a webview" logic for DNR

### we...@gmail.com (2025-11-26)

I am not at all saying you should restrict DNR based on a specific origin like you do with webstore. I am saying that before matching a DNR rule, you should bail if the matched-against context is either (a) embedded by a webview, or (b) embedded under a top that its origin is of a privileged page.

> The concept of a "privileged page" is ambiguous

Fair enough, in this context I refer to pages of extensions (`chrome-extension://<ID>/*`) or a browser-level component (`chrome://*`, `chrome-error://*`, etc) - just as you do with content scripts btw.

Which, AFAIU, correlates well with what you're saying so I believe we agree.

> Extensions can access and run, by design, in the web interface for gemini.google.com; that's unlikely to change. If there's any surface that's using gemini.google.com and not embedding it through another mechanism, it should anticipate that (appropriately permissioned) extensions can run, and, similarly, it should not be granted extra powers by the browser. In this case, we isolate gemini.google.com in the webview precisely so that it is cordoned off from the rest of the browser, and the capabilities should not be exposed to the same site if you visited it in a tab.

I completely agree with this paragraph, and at no point I meant otherwise.

> If you visit gemini.google.com, even if you modified accounts.google.com/rotateCookies (or just ran a content script on the page), that should not result in being able to manipulate the browser in the same way that modifying the gemini surface in the browser is able to. If those capabilities are exposed to gemini.google.com in a surface outside the webview where it's embedded by webui, that's a bug and, I believe, against the intended design of embedding gemini in the browser.

This is the part that requires more discussion, because I believe it misses a significant point.

The notion that the problem is merely the exposure of the app to powerful capabilities and that this needs to be the metric of whether DNR should be allowed or not is not accurate. The problem is more fundamental than that - it is the fact that a component served by the browser is susceptible to being influenced by an inferior entity (such as an extension) to begin with.

The best example to emphasis this message is the phishing example I shared in the initial report. The phishing example demonstrates how significant impact can be delivered via DNR without requiring access to powerful capabilities. As opposed to the other examples where I abuse the hijacked context's established communication channel with its privileged embedder (`chrome://glic`), in the phishing example I perform my attack with most standard capabilities accessible to me (DOM and fetch).

While being able to do that as an extension is trivial if `gemini.google.com` is loaded via an ordinary tab (rightfully so), once `gemini.google.com` gets loaded within a webview, which is an enhancement served on behalf of the browser itself - that's where being able to pull this off escapes the browser's threat model. Because phishing attack injected into a website by an extension is part of the TM, but abusing a browser-level component to do so isn't, and it's not a matter of powers, it's a matter of one entity (extension) being able to abuse a superior one (GITB). In other words, the browser allowing an attacker to deploy a phishing attack via an entity of the browser itself is the line to draw, as it is a more significant breach of user trust (users are responsible to avoid phishing attacks via websites they visit, but are they responsible to avoid those when are presented by the browser itself?).

Out of that, the metric shouldn't be "is this extension-provided DNR rule matching against a context with access to elevated capabilities", but rather "is this extension-provided DNR rule matching against a context that is out of its jurisdiction (which would be any privileged page as defined above).

Translating this "is" question into an "if" statement can be the code fix for this issue the way I see it.

Keep in mind that addressing this as suggested will also address this issue for more impacted vendors other than just GITB. I was able to identify multiple vendors who are vulnerable to this attack via iframes, regardless of whether the hijacked context carries access to elevated capabilities. For some of them, the phishing scenario is their concern, where some extension can hijack their extension's tab via an embedded iframe in a way they did not take into account, resulting in a phishing attack against their users.

Would love to hear your thoughts on this.

### mk...@chromium.org (2025-12-02)

Handing this back to Devlin in the hopes that it can be reassigned while Kelvin is OOO. It would be ideal to have a mitigation plan sooner rather than later, as the behavior we're discussing does seem unexpected.

### we...@gmail.com (2025-12-09)

Hi, is there any update regarding this ticket? I ping you as I find this flaw to be of significant priority due to its proven impact on Chrome as well as other vendors.

If I can be of service to help push this forward, please lmk.

Thanks!

### aj...@google.com (2025-12-23)

Bumping the priority here as it reduces the isolation the <webview> should be providing for glic.

### ke...@chromium.org (2025-12-24)

^We know, I'm working on a fix... The fix itself is easy but I'm working on a test repro

### ke...@chromium.org (2025-12-24)

I managed to get a test repro, will upload the fix for review in the next few days!

The only "problem" is that the test is only enabled on Windows given the test setup, though the extension behavior should be the same across all extension-enabled platforms

### we...@gmail.com (2025-12-24)

Awesome news! Thank you.

Is it focused on dnr fundamental issue? Or the webview-glic glue specifically?

### dx...@google.com (2025-12-30)

Project: chromium/src  

Branch:  main  

Author:  Kelvin Jiang [kelvinjiang@chromium.org](mailto:kelvinjiang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7354432>

[Extensions] Do not apply DNR rules for Webview requests

---


Expand for full commit details
```
     
    Extensions should not be able to apply DNR rules to requests originating 
    from WebViews. 
     
    Bug: 463155954 
    Change-Id: I50bcf9d32480407cfa76bb0bfe6cab67351c43ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7354432 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1563452}

```

---

Files:

- M `chrome/browser/apps/guest_view/web_view_browsertest.cc`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/manifest.json`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/rules.json`
- M `extensions/browser/api/declarative_net_request/ruleset_manager.cc`

---

Hash: [28628907f24e27fff20d26471482f377047db3c8](https://chromiumdash.appspot.com/commit/28628907f24e27fff20d26471482f377047db3c8)  

Date: Tue Dec 30 19:22:24 2025


---

### ke...@chromium.org (2025-12-30)

Should be fixed with the change above

### ke...@chromium.org (2025-12-30)

@weizman,

This fix is focused on the DNR fundamental issue: DNR should not have access to requests originating from WebViews

### ch...@google.com (2025-12-31)

Security Merge Request Consideration: Requesting merge to extended stable (M142) because latest trunk commit (1563452) appears to be after extended stable branch point (1522585).
Security Merge Request Consideration: Requesting merge to stable (M143) because latest trunk commit (1563452) appears to be after stable branch point (1536371).
Security Merge Request Consideration: Requesting merge to beta (M144) because latest trunk commit (1563452) appears to be after beta branch point (1552494).
Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ch...@google.com (2025-12-31)

Merge review required: M144 is already shipping to beta.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: alonbajayo (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-12-31)

Merge review required: M143 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: lmenezes (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), harrysouders (Mobile US), eakpobaro (Mobile EMEA)

### ch...@google.com (2025-12-31)

Merge review required: M142 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:

1. Why does your merge fit within the merge criteria for these milestones?

- Chrome Browser: <https://chromiumdash.appspot.com/branches>
- Chrome OS: <https://goto.google.com/cros-release-branch-merge-guidelines>

2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? <https://goto.google.com/cros-engprodcomponents>
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: andywu (ChromeOS), srinivassista (Desktop US), danielyip (Desktop EMEA), govind (Mobile US), eakpobaro (Mobile EMEA)

### dr...@chromium.org (2026-01-05)

Following up on the merges: I think this should be S2, since it has the mitigation of needing a malicious extension. That means we won't be merging to M142 or M143. I'll take another look to review the M144 merge once we have some Canary data from <https://crrev.com/c/7354432>.

### dr...@chromium.org (2026-01-05)

Ah, it looks like I was checking something wrong. We do have Canary stability data, and there are no crashes. Approving the merge to M144. kelvinjiang@ - we're cutting M144 at 10am tomorrow. Please complete the merge by then.

### go...@google.com (2026-01-05)

Please merge your change to M144 by 10:00 AM PT tomorrow, Jan 6th so we can take it in for M144 Early Stable release on Wednesday, Jan 7th.  Thank you.

### go...@google.com (2026-01-05)

Please merge your change to M144 by 10:00 AM PT tomorrow, Jan 6th so we can take it in for M144 Early Stable release on Wednesday, Jan 7th.  Thank you.

### aj...@google.com (2026-01-05)

This should be merged to stable as it affects an important project.

### dr...@chromium.org (2026-01-05)

Discussed offline with ajgo@ as well. Given the simplicity of the fix and the implications for the Gemini launch, we do want to merge to M142 and M143 as well. Approving both.

### ha...@google.com (2026-01-05)

We are cutting the M143 refresh today in the next ~1 hour. If this is truly critical, someone will need to cherry pick this ASAP. It does not cherry pick cleanly.

### go...@google.com (2026-01-05)

[Bulk Edit]

Please merge to M144 by 10:00 AM PT tomorrow, Jan 6th so we can take it in for M144 Early Stable RC cut.

If it is already merged to M144 and nothing pending, please mark the bug as fixed. 

### dx...@google.com (2026-01-05)

Project: chromium/src  

Branch:  refs/branch-heads/7559  

Author:  Kelvin Jiang [kelvinjiang@chromium.org](mailto:kelvinjiang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7397673>

[M144][Extensions] Do not apply DNR rules for Webview requests

---


Expand for full commit details
```
     
    Extensions should not be able to apply DNR rules to requests originating 
    from WebViews. 
     
    (cherry picked from commit 28628907f24e27fff20d26471482f377047db3c8) 
     
    Bug: 463155954 
    Change-Id: I50bcf9d32480407cfa76bb0bfe6cab67351c43ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7354432 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1563452} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7397673 
    Auto-Submit: Kelvin Jiang <kelvinjiang@chromium.org> 
    Reviewed-by: Emilia Paz <emiliapaz@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7559@{#3026} 
    Cr-Branched-From: 223dfbac1c7542a06b422390d954afe5b560b607-refs/heads/main@{#1552494}

```

---

Files:

- M `chrome/browser/apps/guest_view/web_view_browsertest.cc`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/manifest.json`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/rules.json`
- M `extensions/browser/api/declarative_net_request/ruleset_manager.cc`

---

Hash: [a0a39c9066e316aa3c40e0f069a200c742c4c966](https://chromiumdash.appspot.com/commit/a0a39c9066e316aa3c40e0f069a200c742c4c966)  

Date: Mon Jan 5 22:30:55 2026


---

### dx...@google.com (2026-01-05)

Project: chromium/src  

Branch:  refs/branch-heads/7499  

Author:  Kelvin Jiang [kelvinjiang@chromium.org](mailto:kelvinjiang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7397190>

[M143][Extensions] Do not apply DNR rules for Webview requests

---


Expand for full commit details
```
     
    Extensions should not be able to apply DNR rules to requests originating 
    from WebViews. 
     
    (cherry picked from commit 28628907f24e27fff20d26471482f377047db3c8) 
     
    Bug: 463155954 
    Change-Id: I50bcf9d32480407cfa76bb0bfe6cab67351c43ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7354432 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1563452} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7397190 
    Auto-Submit: Kelvin Jiang <kelvinjiang@chromium.org> 
    Reviewed-by: Emilia Paz <emiliapaz@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7499@{#4081} 
    Cr-Branched-From: b30439823e5177773584139e72e0593e36863899-refs/heads/main@{#1536371}

```

---

Files:

- M `chrome/browser/apps/guest_view/web_view_browsertest.cc`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/manifest.json`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/rules.json`
- M `extensions/browser/api/declarative_net_request/ruleset_manager.cc`

---

Hash: [22f433e4c8556c33111e758c96aa8d215dab05f3](https://chromiumdash.appspot.com/commit/22f433e4c8556c33111e758c96aa8d215dab05f3)  

Date: Mon Jan 5 22:37:12 2026


---

### dx...@google.com (2026-01-05)

Project: chromium/src  

Branch:  refs/branch-heads/7444  

Author:  Kelvin Jiang [kelvinjiang@chromium.org](mailto:kelvinjiang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7397946>

[M142][Extensions] Do not apply DNR rules for Webview requests

---


Expand for full commit details
```
     
    Extensions should not be able to apply DNR rules to requests originating 
    from WebViews. 
     
    (cherry picked from commit 28628907f24e27fff20d26471482f377047db3c8) 
     
    Bug: 463155954 
    Change-Id: I50bcf9d32480407cfa76bb0bfe6cab67351c43ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7354432 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1563452} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7397946 
    Auto-Submit: Kelvin Jiang <kelvinjiang@chromium.org> 
    Reviewed-by: Emilia Paz <emiliapaz@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7444@{#4339} 
    Cr-Branched-From: 29907d3c18078029695f458b42fb8e6fda3e493d-refs/heads/main@{#1522585}

```

---

Files:

- M `chrome/browser/apps/guest_view/web_view_browsertest.cc`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/manifest.json`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/rules.json`
- M `extensions/browser/api/declarative_net_request/ruleset_manager.cc`

---

Hash: [9722f06a26ed9376ee395a4de8c472268d88a4fb](https://chromiumdash.appspot.com/commit/9722f06a26ed9376ee395a4de8c472268d88a4fb)  

Date: Mon Jan 5 23:20:51 2026


---

### pe...@google.com (2026-01-06)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### ke...@chromium.org (2026-01-06)

1. This was not a regression: the underlying issue has always existed since the DeclarativeNetRequest API was added.
2. No (based on the answer above)

### pe...@google.com (2026-01-07)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)

### qk...@google.com (2026-01-07)

1. <https://chromium-review.googlesource.com/c/chromium/src/+/7373684>
2. Low - There was a trivial conflict.
3. 142, 143, and 144
4. Yes, According to the [comment #42](https://issues.chromium.org/issues/463155954#comment42), this issue was not a regression, but it's the underlying issue has existed since the DeclarativeNetRequest API was added.

### dx...@google.com (2026-01-08)

Project: chromium/src  

Branch:  refs/branch-heads/7204  

Author:  Kelvin Jiang [kelvinjiang@chromium.org](mailto:kelvinjiang@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7373684>

[M138-LTS][Extensions] Do not apply DNR rules for Webview requests

---


Expand for full commit details
```
     
    Extensions should not be able to apply DNR rules to requests originating 
    from WebViews. 
     
    (cherry picked from commit 28628907f24e27fff20d26471482f377047db3c8) 
     
    Bug: 463155954 
    Change-Id: I50bcf9d32480407cfa76bb0bfe6cab67351c43ec 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7354432 
    Reviewed-by: Devlin Cronin <rdevlin.cronin@chromium.org> 
    Commit-Queue: Kelvin Jiang <kelvinjiang@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1563452} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7373684 
    Reviewed-by: Kelvin Jiang <kelvinjiang@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7204@{#3473} 
    Cr-Branched-From: d5de512dc9dc8ddfe4e6d71b0637578bb6158683-refs/heads/main@{#1465706}

```

---

Files:

- M `chrome/browser/apps/guest_view/web_view_browsertest.cc`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/manifest.json`
- A `chrome/test/data/extensions/api_test/declarative_net_request/block_chrome_signin/rules.json`
- M `extensions/browser/api/declarative_net_request/ruleset_manager.cc`

---

Hash: [004bc0f66ba9f97eea54aff5aa29e354d8653d35](https://chromiumdash.appspot.com/commit/004bc0f66ba9f97eea54aff5aa29e354d8653d35)  

Date: Thu Jan 8 22:35:44 2026


---

### aj...@google.com (2026-01-21)

Agreed with reporter on disclosure in early March.

### sp...@google.com (2026-01-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $7000.00 for this report.

Rationale for this decision:
Web platform privilege escalation, high quality and high impact


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### we...@gmail.com (2026-01-27)

The award is highly appreciated. Thank you!

### aj...@google.com (2026-01-28)

Thanks again - please let us know when your publication goes live.

### ss...@paloaltonetworks.com (2026-02-03)

redacted

### aj...@google.com (2026-02-05)

I will restrict your comment 50 as it includes PII

> Hello! I lead the team that will be publishing the vulnerability submitter's research on the Palo Alto Networks Unit 42 website. My understanding is that Gal is targeting March 2nd, which was agreed upon with the researchers on the Chrome side.

> Can we please confirm this date is acceptable? If not, let's decide on a date here that is visible on this page so we are all aligned.

Yep March 2 is fine.

### we...@gmail.com (2026-03-03)

Hi folks,

Thanks again for the engagement on this report.

As previously agreed, we have published our content yesterday.

Would this be a good time to:

- Sort out the payment
- Make this report publicly visible?

Thanks, Gal

### aj...@google.com (2026-03-04)

Opening access. Thanks for the update.

### aj...@google.com (2026-03-04)

For payment please follow the instructions in comment 47.

## Bounty Award

> Web platform privilege escalation, high quality and high impact

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/463155954)*
