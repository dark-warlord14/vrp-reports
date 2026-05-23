# Cross-context string leakage via V8 string_table

| Field | Value |
|-------|-------|
| **Issue ID** | [430336833](https://issues.chromium.org/issues/430336833) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Bindings |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | sh...@gmail.com |
| **Assignee** | ca...@chromium.org |
| **Created** | 2025-07-09 |
| **Bounty** | $5,000.00 |

## Description

## VULNERABILITY DETAILS

The `string_table` in V8 is a per-isolate hash table storing internalized strings. As V8 in Chromium uses a heap snapshot for startup this means that the `hashseed` is known and fixed. This allows an attacker to compute the hash of any string and construct an oracle which can reliably test whether a particular string occurs in the `string_table`. As cross-origin documents can occur in the same isolate, in certain cases this oracle provides a way to leak information cross-origin. Additionally, as the contexts of extension content scripts occur in the same isolate as the contexts of the main document, it's possible to leak which extensions a user is using and also, potentially more critically, it's possible to leak information about the execution / control flow of the content scripts.

### THE ORACLE

Suppose we want to know whether a string `x` occurs in the `string_table`. Suppose `x` hashes to `h`. Now, as we know the hash function we brute force strings which hash to `h`, `h + 1`, `h + 1 + 2`, `h + 1 + 2 + 3`, ... (the quadratic probing pattern used in the `string_table`). We insert those strings into the `string_table` and after that we measure how long it takes to insert `x` into the `string_table`. If `x` was already in the `string_table` before insertion of the "chain" we expect to find `x` quickly. On the other hand, if `x` wasn't in the table already we will have to traverse the entire chain we've just inserted, taking measurably longer to complete the insertion. Note that the chain can be made arbitrarily long to ensure the time difference is detectable.

## VERSION

Chrome Version: 138.0.7204.92 stable   

Operating System: Arch Linux (64-bit) Linux 6.15.5-arch1-1

## REPRODUCTION CASE

1. Compile `gen.cpp` with `clang++ -O3 -march=native gen.cpp -o gen`.
2. Run `python3 server.py` and forward some URL `url` to it.
3. Replace `ATTACKER_URL` in `poc.html` with `url` and open the file in Chromium.
4. Change the `test` and `TARGET` variables to test leaking different strings.

Note: The timing is hardware dependent so tweaking the `THRESHOLD` variable might be required. Adjusting the threshold could technically be done on the fly by calculating the latency on the particular machine.

### CREDIT INFORMATION

Reporter credit: Mate Marjanović (SharpEdged)

## Attachments

- [gen.cpp](attachments/gen.cpp) (text/x-c++src, 5.8 KB)
- [poc.html](attachments/poc.html) (text/html, 1.8 KB)
- [server.py](attachments/server.py) (text/x-python, 396 B)
- [gen.cpp](attachments/gen.cpp) (text/x-c++src, 5.8 KB)
- [server.py](attachments/server.py) (text/x-python, 396 B)
- [poc.html](attachments/poc.html) (text/html, 1.6 KB)
- [target.html](attachments/target.html) (text/html, 243 B)
- [poc2.html](attachments/poc2.html) (text/html, 1.9 KB)
- [target2.html](attachments/target2.html) (text/html, 260 B)
- [gen.cpp](attachments/gen.cpp) (text/x-c++src, 5.9 KB)
- [poc.html](attachments/poc.html) (text/html, 2.0 KB)
- [server.py](attachments/server.py) (text/x-python, 422 B)

## Timeline

### cl...@chromium.org (2025-07-09)

Interesting report. This would potentially qualify as a "Cross-site data disclosure", so indeed S1 according to <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/severity-guidelines.md>.

Let me try to figure out what to do which this report.

### cl...@chromium.org (2025-07-09)

What's not clear to me yet is this part:
"As cross-origin documents can occur in the same isolate, in certain cases this oracle provides a way to leak information cross-origin."

With site isolation, I would have expected that that's not possible.

### ma...@google.com (2025-07-09)

Hi, thanks for the report.

I'll expand a bit on [comment#3](https://issues.chromium.org/issues/430336833#comment3): if there are platforms where (1) Site Isolation is enabled and (2) documents from different sites end up in the same process, that is definitely a bug we want to take a look at. Can you offer more details on the assertion that "cross-origin documents can occur in the same isolate"?

Otherwise, Chrome's threat model assumes that the OS process is the smallest enforceable confidentiality boundary[1], so we *do not* consider it a high-severity security bug when code is able to read information leaked from within the same process. See e.g. [here](https://v8.dev/blog/spectre#site-isolation): "Thus Chrome’s security model no longer assumes language-enforced confidentiality within a renderer process."

### el...@chromium.org (2025-07-09)

Security shepherd: Needs-Feedback for the question in #3 and #4.

### el...@chromium.org (2025-07-09)

Also, marking FoundIn and OS based on the report - I have not tried to repro this locally.

### sh...@gmail.com (2025-07-09)

The instances of isolate sharing I've seen are indeed same-site documents which means potential leakage if the website isn't on the public suffix list (but I'm assuming that's not a concern based on your comments), a document and a data: URL it embeds which could potentially be more interesting as data: URLs are null origin according to the spec so they could be used for isolating user content which allows scripting.

The last and most interesting instance I found is extensions which get attached automatically on a document meaning data can be leaked from the content script (not to mention extensions accepting postMessage, which could allow for an even more interesting oracle if we could craft a message to send that will induce the extension to add strings to the `string_table` in a way which leaks the state of the extension). It does also allow for leaking all the extensions that got attached to the document which might be a privacy concern but I'm not sure if that is considered a vulnerability.

### pe...@google.com (2025-07-09)

Thank you for providing more feedback. Adding the requester to the CC list.

### ml...@chromium.org (2025-07-10)

Thank you for the feedback.

As noted in [comment #4](https://issues.chromium.org/issues/430336833#comment4): OS process is the smallest enforceable confidentiality boundary. Any caches within a process are susceptible to timing attacks like shown in your POC.

I will close this bug here as working as intended.

I think discussion on what can and should be segregated (e.g. content scripts) should be filed separately as really that's an overall concern and unrelated to V8 here.

### sh...@gmail.com (2025-07-14)

I have made it work cross-isolate too by freezing a target frame with an appropriate postMessage payload and have opened a new issue detailing that attack but it hasn't seen any attention yet (should I have simply posted a comment here?).

### ml...@chromium.org (2025-07-14)

Can you confirm that you can leak cross-Isolate with *different* OS processes? For Isolates that run in the same process this is WAI, see [comment #4](https://issues.chromium.org/issues/430336833#comment4).

### sh...@gmail.com (2025-07-14)

Yes, I've tested and it can leak across OS processes (according to chrome://discards/graph).

### ml...@chromium.org (2025-07-14)

Can you share your exact setup now? We need a POC in Chrome.

### sh...@gmail.com (2025-07-14)

Copied from the other issue:

## REPRODUCTION CASE

1. Compile `gen.cpp` with `clang++ -O3 -march=native gen.cpp -o gen`.
2. Run `python3 server.py` and forward some URL `url1` to it.
3. Host `target.html` on some cross-site URL `url2`.
4. Replace `ATTACKER_URL` in `poc.html` with `url1` and `target.com/target.html` with `url2` and open the file in Chromium.
5. Change the `test` and `TARGET` variables to test leaking different strings.

Note: The timing is hardware dependent so tweaking the `THRESHOLD` variable might be required. Adjusting the threshold could technically be done on the fly by calculating the latency on the particular machine. I've made the timing gap quite large for ease of demonstration. On my machine I get ~100 ms when the string is in the `string_table` and ~1000 ms when it's not.

### ml...@chromium.org (2025-07-14)

How is `gen.cpp` related in all of this? That's no Chrome and it's not used anyhwere?

### sh...@gmail.com (2025-07-14)

`server.py` runs it so it can generate strings which will collide with some target string.

### ml...@chromium.org (2025-07-14)

Can you describe the setup more with the URLs and which Isolates host them. It's unclear to me where the boundaries are at this point.

The initial comment in #0 mentions "... cross-origin documents can occur in the same isolate...".

### sh...@gmail.com (2025-07-14)

That comment was from when I was describing a leak that only works when both the attacker and target document are in the same isolate (which, as mentioned is not considered a vulnerability, though I didn't know that at the time).

The latest setup is like this:   

Say A is the attacker's domain and T is the target's domain.   

poc.html is on A and that is located in isolate 1.   

target.html is on T and that is located in isolate 2.

server.py is hosted on any URL (potentially on A), it's not relevant as the only thing that happens with it is fetching some data.

### sh...@gmail.com (2025-07-14)

Oh right, also, this was only mentioned in the other issue but this latest leak requires the target site to have a message event handler, that's why it appears in `target.html`. The message handler in `target.html` also sends a message back to make it easier to time how long it took to process the message but this isn't required, that part can be leaked by navigating the target frame and timing how long it takes (as it should be frozen while processing the message if `TARGET` wasn't in the `string_table`).

### ml...@chromium.org (2025-07-14)

So, this is a timing attack where the ping-pong via postMessage leaks whether the string is present in some other Isolate's string table?

### sh...@gmail.com (2025-07-14)

Yeah, the crux of the attack is that we send a specially crafted object with postMessage and via a timing attack we can extract whether a particular string appears in the other Isolate's `string_table`. (As I mentioned already, the "ping-pong" is not required but only for simplicity sake here, we could leak the string even if the target's message handler didn't respond to us)

### ma...@google.com (2025-07-14)

[security shepherd] This updated issue from [#comment14](https://issues.chromium.org/issues/430336833#comment14) was filed as [crbug.com/431371246](https://crbug.com/431371246)

### ml...@chromium.org (2025-07-15)

I spent some time yesterday digging here.

Basically, `postMessage()` [1](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage#security_concerns) already has a security section that mentions that one needs to check `origin` and `source` properties before trusting the message and accessing `data`.

As for eager deserialization: I could not find a place where we would eagerly deserialize the actual data contents. This is not surprising as everything here is implemented using the regular bindings mechansims which creates a `MessageEvent` that can be passed to V8. Only the actual `data()` accessor will deserialize the contents [2](https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/renderer/core/events/message_event.cc;l=294;drc=f22b514ad5ae298c735546ecc1de402a74210f93;bpv=1;bpt=1). Note that since `postMessage()` uses the `structuredClone()` algorithm this also accepts numbers and regex. Basically any internal component is prone to timing attacks here.

sharpedged2: As f or [comment #21](https://issues.chromium.org/issues/430336833#comment21) and [comment #22](https://issues.chromium.org/issues/430336833#comment22): The POC requires interaction (ping-pong) from the target. If you think this is exploitable without target handling the message please provide a POC and we can reconsider this.

### sh...@gmail.com (2025-07-15)

Sure, here is a new POC that doesn't require a response from the target. It makes a new iframe embedding the target site and times how long it takes for onload to fire as it will be stalled in the task queue by the postMessage we sent. (Note that there is another variable in poc2.html to be set, `TARGET_URL`)

For accessing `data`: while it's of course true that a site should check the sender's origin before **using** any of the event data, I doubt any web dev is aware that simply accessing the `data` field would make their site vulnerable. From code I've seen "in the wild" it's actually very common for a message handler to access the `data` field and store it in a variable before any origin checks. Indeed, JS minifiers seem to extract `event.data` into a variable at the start of message handlers to spare a few characters as it commonly appears in the body of the function. From their point of view this should be completely harmless as simply accessing the `data` field earlier shouldn't change the semantics of the code.

I'm not really sure I understand what point you are making about timing attacks on the `structuredClone` algorithm using numbers / regex. Timing attacks across process boundaries are hopeless due to noise. This attack is only a timing attack in spirit, the timing differential can be made arbitrarily long to allow for it to be detected when mixed in with the OS noise.

### ml...@google.com (2025-07-15)

`target2.html` is still setting up a handler that eagerly deserializes `event.data`. This doesn't happen internally on users behalf but instead happens explicitly from JS. I believe this is necessary for the attack which is against the spirit of the `postMessage()` documentation [1](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage#security_concerns).

I mentioned `structuredClone` because that's how the `postMessage` parameter is defined. There's likely more timing attacks lingering in there (not just strings) as there's no principled design to avoid that.

That said, I do agree that this seems fragile and a footgun on the API side. There's ways to intercept this internally to warn if `data` is accessed before `origin` e.g. on the DevTools console. Better yet, we could even propose changing the API shape to throw if this happens. These are longer term efforts though.

+mkwst

### sh...@gmail.com (2025-07-15)

Again, I don't see how you can claim there's "likely more timing attacks lingering in there" as it would:   

a) require a way to amplify the timing to be detectable across the process boundary   

b) require the timing to actually depend on something that should be confidential

Sure, maybe it's possible to leak something about the execution of `structuredClone`, but the algorithm is cloning attacker provided data, I really don't see what else this leaks apart from `string_table` entries. (Though honestly I wouldn't even be certain that part a) is doable...)

From a bit of (miserable) reading of minified JS it seems that accounts.google.com eagerly deserializes in one of its message event handlers, which means data is leakable from there and also anything same-site to it (so \*.google.com). I'm almost certain such leaks are possible for most websites as all that is required is a single eagerly deserializing message handler on some same-site document.

It feels like a futile effort to warn developers of accessing `data` before checking `origin` as it's almost impossible we're going to see all deployed message handlers changing to fix that. It also feels especially weird because this vulnerability is almost trivial to fix on the browser side, all it requires is picking a new `hashseed` and rehashing heap snapshot strings, which is already a functionality that exists in V8 behind a flag.

### ve...@chromium.org (2025-07-15)

You can't embed accounts.google.com in a cross-origin iframe though. There are clear rules to set up pages securely. Randomly accepting postMessage from unrelated origins isn't typically part of the thread model.

### sh...@gmail.com (2025-07-15)

This attack doesn't require embedding it in an iframe, the attack still works with only having a reference to the window (it does require to be able to embed something that is same-site to it, but that is almost always possible). Also, this attack doesn't require a site to accept postMessages randomly, all it has to do is touch `event.data` before checking the origin and returning.

### sh...@gmail.com (2025-07-15)

Here's a POC which revives the XS-Search vulnerability on Gmail (Can I get a bounty for that lol?). Enter a string you want to XS-Search leak, click on "search gmail" and wait a bit for it to fully load. Then click on "leak result" and wait a bit. It will leak whether the search returned any results or not. If you want to test it again make sure to close both tabs so the Isolates don't get re-used. The only thing that needs changing is `ATTACKER_URL` in `poc.html`, that should again be the URL which forwards to `server.py`. (Also note that `gen.cpp` is different, it needs to be recompiled).

There's also a few other cool things I've found about the vulnerability: it can bypass COOP protection as it doesn't require a direct handle on the window we are leaking from, only a handle on something that is same-isolate with it (and has a "bad" message event handler). Another fun thing: if a user has an extension which has a "bad" message event handler, that allows an attacker to leak data from any site the extension attaches to using that handler. From the few extensions I have installed Metamask has such a "bad" handler which means I would be vulnerable to that variant... :(

The "bad" is in quotes as almost any site I checked has them, so I feel like claiming this is the fault of the developers just doesn't follow. I think [the docs](https://developer.mozilla.org/en-US/docs/Web/API/Window/postMessage#security_concerns) are taken out of context by claiming that their "spirit" forbids `event.data` from being touched before origin checks, where is that mentioned?

### mk...@chromium.org (2025-07-16)

This PoC is unfortunately pretty cool, thanks for digging into it. When I talked to mlippautz@ yesterday, I was myopically focused on leaking secrets through brute force, but this is a much clearer example of the risk.

With that in mind, it seems worth reopening and looking into a few things:

1.  For `google.com` specifically: I'd have expected the GMail window with COOP assertions to be in a distinct browsing context group from the framed `favicon.ico`, so it surprises me that they end up in the same process with the same string table. clamy@, perhaps you have some insight here? (As an aside, it also surprises me a tiny bit that `google.com` hasn't locked down framing for non-document resources; perhaps aaj@ could help us find a good contact for a discussion there).

2.  Short-term: it would be helpful to understand the perf implications for re-seeding the hash when initializing isolates so we can reason about the mitigations that might be possible. mlippautz@ had some other ideas about more narrow approaches that might be possible if re-seeding generally is too expensive.

3.  Long-term: Maybe it's a good time to revisit the ~decade old discussion around `postMessage()`'s sharp edges. We made little progress on it when slekies@ sketched http://sebastian-lekies.de/new_pm_api.js a million years ago, but we could try again.

### sh...@gmail.com (2025-07-16)

For 1. I just want to mention that weirdly enough mail.google.com doesn't actually have COOP, I just mentioned COOP as even if it did have it, the attack would still work (with some adjustments) as it doesn't require postMessage directly on the target window, only on a window that is same-isolate with the target. I was considering leaking directly from google.com to demonstrate the COOP bypass but this seemed cooler so that's what I did. (At least from my tests I think it can bypass COOP, if I open x.com/a (that has COOP) and frame x.com/b (no COOP) the browser has no problem placing them in the same isolate)

### ml...@chromium.org (2025-07-16)

Thanks again for the updated PoCs.

Few bits for the V8 side:

- Not internalizing strings based on e.g. `postMessage()` is not really an option. V8's object model requires internalizing property keys and making our object model more complex usually results in more security issues down the line. (It's already arguably to complex.)
- Per-process hash seed determined at running time
  - This requires rehashing after deserializing the heap snapshot. We implemented this for Node for our old custom hash (<https://v8.dev/blog/hash-flooding>)
  - Even if we had that, it's unclear if that's going to fix it because there's still timings there that are just not amplified with hash collisions. I recall some research papers that recover fine-grained timings in noise environments.
  - A runtime hash seed may not be enough: Node seems to have problems with hash flooding + rapidhash (<https://github.com/nodejs/node/releases/tag/v24.4.1>)
  - It has performance implications on pageload which is why it never shipped for the browser. It's not easily shippable as this needs to go through Finch.

### ch...@google.com (2025-07-16)

Setting milestone because of s0/s1 severity.

### ch...@google.com (2025-07-16)

Setting Priority to P1 to match Severity s1. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### sh...@gmail.com (2025-07-16)

Funnily enough I'm the one that reported the Node.js hash flooding too. The problem there was that with rapidhash it's possible to carefully choose strings which will collide regardless of the `hashseed`. For this vulnerability we need to be able to find strings that collide with a particular target string and it's not immediately clear how that could be done, but it's clear that rapidhash isn't a particularly strong hash function so it's not out of question that it might be possible.

### xi...@chromium.org (2025-07-16)

[Security Shepherd] Thanks for the report. We generally prefer security bugs with an owner. +clamy@ for questions on #comment30. Thanks!

### ml...@chromium.org (2025-07-16)

> Funnily enough I'm the one that reported the Node.js hash flooding too...

Oh well... nice :)

The requirements for hashing in V8 were never around being cryptograpihcally secure, or reducing collisions to a bare minimum; instead we require the hash to be fast and somewhat okay wrt to collisions and use for one and two-byte cases.

Talked a bit more with mkwst@ about possible mitigations. Rehashing for V8 is currently being fixed for Node but it's unclear whether we can deploy this for the browser as we have very strict latency budgets for page load.

Instead, here's a different proposal:

1. We can actually detect the case where we load `.data` before `.origin` as they are both already hooked in Blink via IDL getters.
2. We should also be able to detect the cross-origin case for `postMessage()`.

We can then add various levels of noise in that case that should make this undetectable.

If that's too intrusive and triggering too often we can return an interceptor object from `.data` that can only adds noise on actual use of the data and allows assigning it to a local as used by minifiers.

caseq@, can you have a look whether this is doable on the bindings side?

### ch...@google.com (2025-07-31)

caseq: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-08-04)

Project: chromium/src  

Branch:  main  

Author:  Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6787964>

Mask deserialization time of cross-origin messages from unchecked origins

---


Expand for full commit details
```
     
    This tracks whether `MessageEvent::origin` property of cross-origin message events has been accessed prior to the `data` property and if not, uses a newly-created isolate to deserialize the message few more times to obscure any timing differences induced by deserialization, e.g.  timings of string table operations. 
     
    Bug: 430336833 
    Change-Id: Idcc4d7322ff7f5c5bcfbcae97ba43004652fdc78 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6787964 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Andreas Haas <ahaas@chromium.org> 
    Reviewed-by: Mike West <mkwst@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1496454}

```

---

Files:

- M `third_party/blink/public/mojom/use_counter/metrics/web_feature.mojom`
- M `third_party/blink/renderer/bindings/core/v8/serialization/serialized_script_value.h`
- M `third_party/blink/renderer/bindings/core/v8/serialization/v8_script_value_deserializer.cc`
- M `third_party/blink/renderer/bindings/core/v8/serialization/v8_script_value_deserializer.h`
- M `third_party/blink/renderer/bindings/core/v8/serialization/v8_script_value_serializer.cc`
- M `third_party/blink/renderer/bindings/core/v8/serialization/v8_script_value_serializer.h`
- M `third_party/blink/renderer/core/events/message_event.cc`
- M `third_party/blink/renderer/core/events/message_event.h`
- M `third_party/blink/renderer/core/events/message_event.idl`
- M `third_party/blink/renderer/core/events/message_event_test.cc`
- M `third_party/blink/renderer/core/exported/web_dom_message_event.cc`
- M `third_party/blink/renderer/core/frame/local_dom_window.cc`
- M `third_party/blink/renderer/core/frame/local_frame.cc`
- M `third_party/blink/renderer/core/workers/dedicated_worker_messaging_proxy.cc`
- M `third_party/blink/renderer/modules/broadcastchannel/broadcast_channel.cc`
- M `third_party/blink/renderer/modules/service_worker/service_worker_container.cc`
- M `third_party/blink/renderer/platform/runtime_enabled_features.json5`
- A `third_party/blink/web_tests/http/tests/messaging/message-event-slow-deserialization-expected.txt`
- A `third_party/blink/web_tests/http/tests/messaging/message-event-slow-deserialization.html`
- M `tools/metrics/histograms/metadata/blink/enums.xml`

---

Hash: [5dce1815e20eeda684ff15dac7767c2e67d39cc2](http://crrev.com/5dce1815e20eeda684ff15dac7767c2e67d39cc2)  

Date: Mon Aug 4 17:54:04 2025


---

### ch...@google.com (2025-08-15)

caseq: Uh oh! This issue still open and hasn't been updated in the last 29 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### dx...@google.com (2025-08-20)

Project: chromium/src  

Branch:  main  

Author:  Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6862301>

Set status of MaskDeserializationTimeForCrossOriginMessages to stable

---


Expand for full commit details
```
     
    Bug: 430336833 
    Change-Id: I632046741fb7bc9b97825e998aedba05e1946bf6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6862301 
    Reviewed-by: Mike West <mkwst@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Auto-Submit: Andrey Kosyakov <caseq@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1504009}

```

---

Files:

- M `third_party/blink/renderer/platform/runtime_enabled_features.json5`

---

Hash: [dbc005390a0dbe9044348b2c69bcfab1ac21c8a0](https://chromiumdash.appspot.com/commit/dbc005390a0dbe9044348b2c69bcfab1ac21c8a0)  

Date: Wed Aug 20 16:35:22 2025


---

### ch...@google.com (2025-08-30)

caseq: Uh oh! This issue still open and hasn't been updated in the last 44 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.[internal debugging info: security\_nag\_check]

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### ch...@google.com (2025-09-08)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ca...@chromium.org (2025-09-08)

Marked as fixed since we flipped the status to "stable" in the commit referenced at #41.

### ch...@google.com (2025-09-08)

Dear owner, thanks for fixing this bug. We've reopened it because:

- It is not clear which CLs have ‘fixed’ (=required to consider the bug resolved; e.g. not logging) this bug. Please fill in the “Fixed By Code Changes” field with the appropriate Gerrit url to disambiguate using the following guidelines:
  - If there are multiple CLs required, please list all.
  - If the fix landed in a third party library (v8, Dawn, etc), please list the third party commits - not the rolls.
  - If there are cherrypicks or back merges, please list the original commits which landed on HEAD.
  - If there is no relevant Gerrit link (i.e. the fix does not live in or roll into Chromium), please use the value ‘NA’.
  - If this is a non-browser ChromeOS-specific bug, please move it to component 1335705 in the Google issue tracker.
  - If this field requires human intervention for some reason, please add this bug to the hotlist id 6265590.
    After resolving the above issue(s), this bug can be marked closed again. Thanks for your time!

### ch...@google.com (2025-09-09)

We commit ourselves to a 60 day deadline for fixing for s1 severity vulnerabilities, and have exceeded it here. If you're unable to look into this soon, could you please find another owner or remove yourself so that this gets back into the security triage queue?

### ch...@google.com (2025-09-17)

Security Merge Request Consideration: This is sufficiently serious that it should be merged to stable. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M140. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request Consideration: This is sufficiently serious that it should be merged to beta. But I can't see a Chromium repo commit here,so you will need to investigate what - if anything - needs to be merged to M141. Is there a fix in some other repo which should be merged? Or, perhaps this ticket is a duplicate of some other ticket which has the real fix: please track that down and ensure it is merged appropriately.
Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request - Manual Review: Merge review required: no relevant commits could be automatically detected (via Git Watcher comments), sending to merge review for manual evaluation. If you have not already manually listed the relevant commits to be merged via a comment above, please do so ASAP.

Security Merge Request: Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

We have determined this fix is necessary on milestone(s): [140, 141].

Please answer the following questions so that we can safely process this merge request:

1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been verified on Canary to not pose any stability regressions?
3. Does this fix pose any potential non-verifiable stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.
6. (no answer required) Please check the OS custom field to ensure all impacted OSes are checked!

### ts...@google.com (2025-09-17)

FYI, looks like the bulk of the work already landed in M140 (as 1496454 < 1496484 branch point) and was defaulted "on" in M141 (as 1504009 < 1509326 branch point).

### ts...@google.com (2025-09-17)

Please merge the change in #41 to M140 (7339) by Friday September 19th. 

### dx...@google.com (2025-09-17)

Project: chromium/src  

Branch:  refs/branch-heads/7339  

Author:  Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)  

Link:    <https://chromium-review.googlesource.com/6961636>

[m140] Set status of MaskDeserializationTimeForCrossOriginMessages to stable

---


Expand for full commit details
```
     
    (cherry picked from commit dbc005390a0dbe9044348b2c69bcfab1ac21c8a0) 
     
    Bug: 430336833 
    Change-Id: I632046741fb7bc9b97825e998aedba05e1946bf6 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6862301 
    Reviewed-by: Mike West <mkwst@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Auto-Submit: Andrey Kosyakov <caseq@chromium.org> 
    Cr-Original-Commit-Position: refs/heads/main@{#1504009} 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6961636 
    Reviewed-by: Nate Chapin <japhet@chromium.org> 
    Commit-Queue: Nate Chapin <japhet@chromium.org> 
    Reviewed-by: Tom Sepez <tsepez@chromium.org> 
    Cr-Commit-Position: refs/branch-heads/7339@{#2039} 
    Cr-Branched-From: 27be8b77710f4405fdfeb4ee946fcabb0f6c92b2-refs/heads/main@{#1496484}

```

---

Files:

- M `third_party/blink/renderer/platform/runtime_enabled_features.json5`

---

Hash: [f9d894f1cc0b9e09b962cda147f9610c54209493](https://chromiumdash.appspot.com/commit/f9d894f1cc0b9e09b962cda147f9610c54209493)  

Date: Wed Sep 17 20:57:21 2025


---

### pe...@google.com (2025-09-23)

LTS Milestone M138

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:

1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?

### aw...@google.com (2025-09-23)

Adding OS of Android, presuming it affects all platforms with Blink, please update if incorrect.

### sp...@google.com (2025-09-26)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
high quality but lower impact user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.

### sh...@gmail.com (2025-09-27)

Could I get an explanation of why this is considered lower impact? The Gmail XSSearch can potentially leak the entirety of the victim's inbox and it requires only 1 click (though that would take a while, it would probably be better to search for something like "Your password is: ..." and then leak passwords character by character), shouldn't that be higher impact?

### qk...@google.com (2025-09-29)

Labeled as not applicable for M132/138 LTS because the fix required to add a new feature(MaskDeserializationTimeForCrossOriginMessages)[1].
[1] https://chromium-review.googlesource.com/c/chromium/src/+/6787964

### dx...@google.com (2025-10-01)

Project: chromium/src  

Branch:  main  

Author:  Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7001453>

Only defer to slow deserialization for messages beyond certain size.

---


Expand for full commit details
```
     
    Bug: 430336833 
    Change-Id: I6b15a8bf5c12fd0baaca2f5f67e4fb27e6e3cd99 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7001453 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Nate Chapin <japhet@chromium.org> 
    Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1523761}

```

---

Files:

- M `third_party/blink/renderer/core/events/message_event.cc`
- M `third_party/blink/web_tests/http/tests/messaging/message-event-slow-deserialization-expected.txt`
- M `third_party/blink/web_tests/http/tests/messaging/message-event-slow-deserialization.html`

---

Hash: [9b39eef5f01b9c244e5f020ad9e93cd4f9c35599](https://chromiumdash.appspot.com/commit/9b39eef5f01b9c244e5f020ad9e93cd4f9c35599)  

Date: Wed Oct 1 18:54:54 2025


---

### dx...@google.com (2025-10-06)

Project: chromium/src  

Branch:  main  

Author:  Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7007083>

Revert "Only defer to slow deserialization for messages beyond certain size."

---


Expand for full commit details
```
     
    This reverts commit 9b39eef5f01b9c244e5f020ad9e93cd4f9c35599. 
     
    Reason for revert: this shows regression on pinpoint (see b/448759753), while this is weird considering the nature of the change, I'm reverting it while investigating. 
     
    Original change's description: 
    > Only defer to slow deserialization for messages beyond certain size. 
    > 
    > Bug: 430336833 
    > Change-Id: I6b15a8bf5c12fd0baaca2f5f67e4fb27e6e3cd99 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7001453 
    > Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    > Reviewed-by: Nate Chapin <japhet@chromium.org> 
    > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > Cr-Commit-Position: refs/heads/main@{#1523761} 
     
    Bug: 430336833 
    Change-Id: Ib29fdafa29f3ae1f6d2163b70c13af99d4b218a5 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7007083 
    Commit-Queue: Nate Chapin <japhet@chromium.org> 
    Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Nate Chapin <japhet@chromium.org> 
    Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Cr-Commit-Position: refs/heads/main@{#1525902}

```

---

Files:

- M `third_party/blink/renderer/core/events/message_event.cc`
- M `third_party/blink/web_tests/http/tests/messaging/message-event-slow-deserialization-expected.txt`
- M `third_party/blink/web_tests/http/tests/messaging/message-event-slow-deserialization.html`

---

Hash: [b679beeacbc0db5d2b8d9f946f3a54777e44ab9f](https://chromiumdash.appspot.com/commit/b679beeacbc0db5d2b8d9f946f3a54777e44ab9f)  

Date: Mon Oct 6 22:32:03 2025


---

### dx...@google.com (2025-10-07)

Project: chromium/src  

Branch:  main  

Author:  Andrey Kosyakov [caseq@chromium.org](mailto:caseq@chromium.org)  

Link:    <https://chromium-review.googlesource.com/7014630>

Reland "Only defer to slow deserialization for messages beyond certain size."

---


Expand for full commit details
```
     
    This reverts commit b679beeacbc0db5d2b8d9f946f3a54777e44ab9f. 
     
    Reason for revert: metric change is WAI (and is actually fixed), see b/448759753 for analysis. 
     
    BUG: 448759753, 430336833 
     
    Original change's description: 
    > Revert "Only defer to slow deserialization for messages beyond certain size." 
    > 
    > This reverts commit 9b39eef5f01b9c244e5f020ad9e93cd4f9c35599. 
    > 
    > Reason for revert: this shows regression on pinpoint (see b/448759753), while this is weird considering the nature of the change, I'm reverting it while investigating. 
    > 
    > Original change's description: 
    > > Only defer to slow deserialization for messages beyond certain size. 
    > > 
    > > Bug: 430336833 
    > > Change-Id: I6b15a8bf5c12fd0baaca2f5f67e4fb27e6e3cd99 
    > > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7001453 
    > > Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    > > Reviewed-by: Nate Chapin <japhet@chromium.org> 
    > > Reviewed-by: Michael Lippautz <mlippautz@chromium.org> 
    > > Cr-Commit-Position: refs/heads/main@{#1523761} 
    > 
    > Bug: 430336833 
    > Change-Id: Ib29fdafa29f3ae1f6d2163b70c13af99d4b218a5 
    > Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7007083 
    > Commit-Queue: Nate Chapin <japhet@chromium.org> 
    > Commit-Queue: Andrey Kosyakov <caseq@chromium.org> 
    > Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Auto-Submit: Andrey Kosyakov <caseq@chromium.org> 
    > Reviewed-by: Nate Chapin <japhet@chromium.org> 
    > Commit-Queue: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    > Cr-Commit-Position: refs/heads/main@{#1525902} 
     
    Bug: 430336833 
    Change-Id: I52e2b242e4a17fbe33a51c53e2e2612fda1860f2 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/7014630 
    Commit-Queue: Nate Chapin <japhet@chromium.org> 
    Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com> 
    Auto-Submit: Andrey Kosyakov <caseq@chromium.org> 
    Reviewed-by: Nate Chapin <japhet@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1526341}

```

---

Files:

- M `third_party/blink/renderer/core/events/message_event.cc`
- M `third_party/blink/web_tests/http/tests/messaging/message-event-slow-deserialization-expected.txt`
- M `third_party/blink/web_tests/http/tests/messaging/message-event-slow-deserialization.html`

---

Hash: [b484dd779733b13464ac59b692950504583fcf6a](https://chromiumdash.appspot.com/commit/b484dd779733b13464ac59b692950504583fcf6a)  

Date: Tue Oct 7 16:31:10 2025


---

### wf...@chromium.org (2025-10-17)

The VRP panel did a very rigorous re-evaluation of the reward amount for this issue and decided that the $5000 was an appropriate amount.

### ch...@google.com (2025-12-24)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

## Bounty Award

> high quality but lower impact user information disclosure

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/430336833)*
