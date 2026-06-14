# Security: The CSP reports and stacktraces of errors leaks post-redirect URL for <script>

| Field | Value |
|-------|-------|
| **Issue ID** | [40052109](https://issues.chromium.org/issues/40052109) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>SecurityFeature |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | ob...@gmail.com |
| **Assignee** | ar...@chromium.org |
| **Created** | 2020-04-24 |
| **Bounty** | $5,000.00 |

## Description

Chrome Version       : 81.0.4044.122
OS Version: Windows 10 \ Ubuntu
Safari: UNTESTED
Firefox: FAIL
IE/Edge: PARTIAL

Hello

If the javascript is loaded as a result of some redirect it can contain the sensitive data and the final url can be known in the current domain context.

1. If the loaded script do some action, what restricted by CSP (create images for e.g.) I see the post-redirect URL with sensitive data in the CSP report (the source-file field)
2. If I call some function from loaded script and it causes an error - I see the post-redirect URL in the stacktrace of the catched error.

This bug can be used for steal sensitive data from uri in some OAuth-like flows or for steal some other sensitive data from url after redirects.

The example of page and screenshots in the attach.

## Attachments

- [screenshot_010.png](attachments/screenshot_010.png) (image/png, 98.0 KB)
- [screenshot_011.png](attachments/screenshot_011.png) (image/png, 166.7 KB)
- [CSP_TRACES_EXAMPLE.zip](attachments/CSP_TRACES_EXAMPLE.zip) (application/octet-stream, 1.8 KB)
- [out.ogv](attachments/out.ogv) (video/ogg, 2.1 MB)
- [Screenshot from 2020-05-26 15-02-19.png](attachments/Screenshot from 2020-05-26 15-02-19.png) (image/png, 181.4 KB)
- [Screenshot from 2020-05-26 15-26-43.png](attachments/Screenshot from 2020-05-26 15-26-43.png) (image/png, 269.5 KB)

## Timeline

### ob...@gmail.com (2020-04-24)

just for clarify: my attached example doesn't use different hosts, but you can check the same situation in this page: https://obmi.me/pocs/chromebugcsptrace_751cb9eb-bfe5-42be-9c9c-bd6e7c9d170d

### me...@chromium.org (2020-04-24)

Arthur, can I assign this to you as well? I'm not sure if there is anything we can do to prevent this.

[Monorail components: Blink>SecurityFeature]

### [Deleted User] (2020-04-25)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2020-04-27)

Yes, I will take a look.

### ar...@chromium.org (2020-04-27)

We can do 2 things:
1) Hide the path after the redirect. This is easy, but this will also make legitimate reports less informatives.
2) In https://crbug.com/chromium/932892: they proposed to display the initial origin instead of the destination URL. This is an upgrade to the spec that hasn't been implemented by Chrome yet. See https://w3c.github.io/webappsec-csp/#create-violation-for-request

Ideally (2) should be done, because it would make (1) irrelevant. However this is harder to do. I think I will start with (1) this week if I find some time.

### aa...@google.com (2020-04-27)

FWIW there is also some more investigation of this in the (internal) bug: http://b/154583085#https://crbug.com/chromium/1074317#c21

### ar...@chromium.org (2020-04-30)

So there are 2 bugs reported here:
1) Reports should strip the URL's path.
2) When throwing an exception from script's onload handler, we should not be able to infer the final URL's of the blocked script.

Your repro steps is using only one origin. This would have been better with two origin malicious.com and victim.com. We sometime strip data from the URL when they are sent cross origin. I am currently working on making some good reproducer. I will also check on Firefox for their current behavior.


### ob...@gmail.com (2020-04-30)

Hello. I provided the example with different origins before, in comment https://crbug.com/chromium/1074317#c1

I placed it here: https://obmi.me/pocs/chromebugcsptrace_751cb9eb-bfe5-42be-9c9c-bd6e7c9d170d

### ar...@chromium.org (2020-04-30)

Ooops I missed https://crbug.com/chromium/1074317#c2. I will take a look.

### ar...@chromium.org (2020-04-30)

All right! I took me 3 hours to really understand what this bug was about. I should have read more carefully.

Initially I thought this was about leaking data about the (report-only) blocked URL post-redirect. This isn't really about it.

This has nothing to do bug:
http://b/154583085#https://crbug.com/chromium/1074317#c21
(+aaj@ FYI: I was hoping I could use this bug as a reproducer of b/154583085. Turns out  this isn't related at all. I will need to find what b/154583085 is really about)

What this bug is about:
=======================

When we throw a javascript exception, the exception contains a trace of the call stack. Every functions called contain the script's URL the function are defined from. This shows the script's URL. This might contains a /path, an ?attribute and maybe a #ref.

Is this really a security issue? mkwst@ what do think? Do you know someone I could ask this.

So far, this isn't related to CSP at all. However if a CSP report is sent from this location then it will contain the URL of the script causing the CSP violation. I guess this is expected?

### ar...@chromium.org (2020-04-30)

[Empty comment from Monorail migration]

### aa...@google.com (2020-05-01)

I'm not sure I understand the summary in https://bugs.chromium.org/p/chromium/issues/detail?id=1074317#c10 so I'll attempt to summarize it, and if I have it wrong, I'm hoping obmihail@gmail.com will correct me.

First, the security property we're trying to preserve is the secrecy of URLs after a cross-origin redirect. If a.com loads a resource from b.com which redirects to b.com/sensitive?auth=secret we don't want to allow a.com to read the final URL to which the request was redirected, despite being able to load the resource itself. Leaking the URL to a.com is a vulnerability which can lead to information leaks and potentially account takeover in services which use secrets in URLs (many web applications) because the post-redirect URLs can contain auth / capability tokens.

This bug and http://b/154583085 describe two distinct Chrome behaviors that undermine this security property:
1. The `source-file` property in CSP violation reports contains the post-redirect URL when a cross-origin script is responsible for generating a CSP violation. The attacker can set a CSP in their document which will be violated when a script loaded from the victim's site executes, then load that script and see the post-redirect URL in the violation report (which is sent to the attacker).
2. Unrelated to CSP, if the attacker loads a script from the victim's site, and then forces an exception by executing a function defined in that script, then the stacktrace (which the attacker has access to) will contain the post-redirect URL.
3. [There's another vector captured in https://b.corp.google.com/issues/154485260#https://crbug.com/chromium/1074317#c10. obmihail@gmail.com, could you describe it here?

So AFAIU there are several different issues here that all allow leaking post-redirect URLs; these issues may need separate fixes.


### aa...@google.com (2020-05-01)

[Empty comment from Monorail migration]

### aa...@google.com (2020-05-01)

[Empty comment from Monorail migration]

### ob...@gmail.com (2020-05-01)

I completely agree with https://crbug.com/chromium/1074317#c12 . 
The mentioned vector is: 
1. Load a script via redirect from a.com to b.com via importScripts function in the Web Worker initialized in a.com domain.
2. Call some function from the loaded script, which will throw an error
3. The stacktrace of the catched error will includes the full url of script in b.com domain.

I placed an example here:  https://obmi.me/pocs/webworkerexample_5b52f35f-807f-4255-8429-f61a588f404c

You can see in the page body the stacktrace with a script url in domain iam-gserviceaccount.com which includes the sensitive data (which was added after redirect).

### [Deleted User] (2020-05-02)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2020-05-04)

So we can leak the post-redirect URL using a:
(1) CSP report > 'source-file'
(2) StackTrace.

Since (1) is also computed from (2). See SourceLocation::Capture(...). Then we just need to fix (2).

### ar...@chromium.org (2020-05-04)

I am currently making some WPT regressions tests to help fixing this -- I will update this soon.

### ar...@chromium.org (2020-05-04)

+verwaest@
Could you please help us here? This bug is about abusing Error.stack for learning about post-redirect URLs.

I guess stripping every cross-origin URL from the StackTrace is undesirable, so I am not sure what to do.
Do you think it would be feasible replacing the final-URL by the initial-URL in the StackTrace?
More generally, what is your opinion here?

Here are some WPT tests about this bug we have to fix:
https://chromium-review.googlesource.com/c/chromium/src/+/2179508

In the meantime, I think I will apply some bandage(s) to CSP source-file. Maybe just stripping the ?attribute and #ref from the URL;
This won't be perfect, as it will still be possible from malicious.html to access them using a function from victim.js throwing an error.

### ve...@chromium.org (2020-05-04)

+sigurds for DevTools

I don't think V8 cares about URLs, and V8 simply renders whatever is attached as the resource URL (unless it's overwritten by a source url annotation).

As simplest solution you could provide the pre-redirect URL as resource URL to V8. (option 1) This would affect embedders that read the URL from V8, as e.g., DevTools would.

If you need a mapping from pre-redirect to post-redirect URL though, we might want to let you initialize the "source url" through the API to the pre-redirect URL, and V8 will simply render that instead of the resource URL. (option 2) The weirdness here is that unless a source_url annotation is provided, "source url" which currently is the most up-to-date knowledge of the url (it can be annotation provided) will now no longer be that; it'll be the pre-redirect URL where the resource url will be the post-redirect url. We could keep a flag though that allows the embedder to know which of the 2 urls is the most accurate; or something like that.

The final question is whether you want to render the pre-redirect URL or the source url from the annotation in case there is one. In (option 2) we could ignore the source_url annotation if the embedder has already provided one. (Or if we implement it with a setter, we either overwrite the script-provided value or drop the incoming value depending on what semantics we want.)

Basically for (option 2): source url has precedence over resource url for printing, which is why I'd store the pre-redirect url there if we need to keep around the resource url as well. If we don't, (option 1) is the simplest.

Finally we could also simply keep all 3 urls and print depending on which we have.

### ar...@chromium.org (2020-05-04)

Thanks for this answer! This is really useful.

Yes, option (2) sounds like the right thing to do.
However implementing (2) is going to take me {1,2,3} weeks. I think I will start with option (1), in order to be more familiarized with the code. I am curious about how many things this is going to break ;-) Then I will likely try option (2).
If you have some time and want to help, that would be much appreciated.

The WIP CSP bandage I was talking about in https://crbug.com/chromium/1074317#c19:
https://chromium-review.googlesource.com/c/chromium/src/+/2179884
(I also found a bug along the way, which is nice)


### si...@chromium.org (2020-05-04)

In any case, it would be good if DevTools had access to the post-redirect URL, as this will provide the better debugging experience.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/88f4429867a3b24969e6a4d4110d7d7baa5a5fb7

commit 88f4429867a3b24969e6a4d4110d7d7baa5a5fb7
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Tue May 05 14:18:37 2020

Add WPT tests for https://crbug.com/chromium/1074317

BUG=1074317

Change-Id: I3bcc915642b06f1370fe15d2331014297992adfa
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2179508
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Daniel Vogelheim <vogelheim@chromium.org>
Cr-Commit-Position: refs/heads/master@{#765533}

[add] https://crrev.com/88f4429867a3b24969e6a4d4110d7d7baa5a5fb7/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/post-redirect-stacktrace.https-expected.txt
[add] https://crrev.com/88f4429867a3b24969e6a4d4110d7d7baa5a5fb7/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/post-redirect-stacktrace.https.html
[add] https://crrev.com/88f4429867a3b24969e6a4d4110d7d7baa5a5fb7/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/post-redirect-stacktrace.https.html.headers
[add] https://crrev.com/88f4429867a3b24969e6a4d4110d7d7baa5a5fb7/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/support/throw-function.js


### si...@chromium.org (2020-05-05)

Maybe I wasn't super clear, but I think we need to make sure DevTools gets first-class URL information after this change. IIUC that means it would be good if V8 knew all the URLs, not just the pre-redirect URL.

Adding Yang to get his perspective.

### ya...@chromium.org (2020-05-05)

I think this is fundamentally a problem of the way DevTools consumes stack traces from V8. V8 only provides DevTools with a string for the stack trace, not a structured stack trace. So DevTools has to come along and e.g. parse the stack trace to turn source URLs to links. That way, DevTools also has no good way to map URLs before and after redirect, even if it had another way to get to this information e.g. from the network service.

### ve...@chromium.org (2020-05-05)

As you know V8 renders stack traces and throws away structured information for memory reasons. If V8 has both names though, we could have an API that allows DevTools to map pre-redirect names to post-redirect URLs (assuming that there are unique mappings :s).

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-05)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b209fbffb50a92e8933149b19ed694b2f89a7633

commit b209fbffb50a92e8933149b19ed694b2f89a7633
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Tue May 05 16:27:49 2020

Strip URL attribute in CSP report source-file.

Three things in this patch:

1) There was a bug in CspViolationReportBody constructor. No matter what
   SourceLocation was provided, it was capturing another one. This means
   all the sanitizing work done by the caller using
   StripURLForUseInReport(..) was wasted.

2) Strip the URL's attribute as well. Fixing https://crbug.com/1074317

3) Add one TODO. What we do in StripURLForUseInReport doesn't make
   sense for the 'source-file'. We need one more follow-up to figure out
   what is thing here.

Bug: 1074317
Change-Id: I639ff4ee9b160e00e82416c1121ce2a19fa19292
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2179884
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Daniel Vogelheim <vogelheim@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#765591}

[modify] https://crrev.com/b209fbffb50a92e8933149b19ed694b2f89a7633/third_party/blink/renderer/core/frame/csp/content_security_policy.cc
[modify] https://crrev.com/b209fbffb50a92e8933149b19ed694b2f89a7633/third_party/blink/renderer/core/frame/csp/csp_violation_report_body.h
[modify] https://crrev.com/b209fbffb50a92e8933149b19ed694b2f89a7633/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/post-redirect-stacktrace.https-expected.txt


### ar...@chromium.org (2020-05-06)

The previous patch added a quick mitigation. This isn't possible anymore to learn about the script's post-redirect URL's attribute using CSP's 'source-file'.

This will be part of Chrome version 84:
- Beta   2020-05-20. (14 days)
- Stable 2020-07-14. (68 days)

I don't think this is a bad-enough bug to try to merge back to M83 6 days before the stable cut. M83 is going to be a quite difficult release already.

We still need to find a solution for the main problem using Error.stack. This one is going to be hard.

### si...@chromium.org (2020-05-06)

+ Simon who has worked on error stack in the past.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f4152597fb034b9c520eebdaa6902e7673ff453d

commit f4152597fb034b9c520eebdaa6902e7673ff453d
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Thu May 07 15:07:03 2020

Improve test: csp/reporting/post-redirect-stacktrace.https.html

The test was checking no post-redirect information was leaked.
Unfortunately, there was a bug in the test. The same data was present in
both the final URL and the post-redirect URL.

This patch make the post-redirect URL no to have the data.

BUG=1074317

Change-Id: I40a698b8edf6ff651dda5d0e82b803a60ccaac7b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2187711
Reviewed-by: Daniel Vogelheim <vogelheim@chromium.org>
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Cr-Commit-Position: refs/heads/master@{#766412}

[modify] https://crrev.com/f4152597fb034b9c520eebdaa6902e7673ff453d/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/post-redirect-stacktrace.https.html
[add] https://crrev.com/f4152597fb034b9c520eebdaa6902e7673ff453d/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/support/redirect-throw-function.sub.py


### ar...@chromium.org (2020-05-07)

I prepared a fix. I did (1) from https://crbug.com/chromium/1074317#c20.
https://chromium-review.googlesource.com/c/chromium/src/+/2187792

I know you would have preferred (2) instead, but this is way beyond my comfort zone. This looks like a real project. I don't want to do it myself, otherwise I would waste my quarter on this.

Would you be happy with (1)? The M84 branch cut is next Tuesday. It would be nice getting the security issue fixed quickly (http://b/154583085 )
I prepared a video for you to visualize what the user would see. This is looking good enough in my opinion.

If you categorically don't want (1) for M84, do you know who would be happy working on (2) instead?

### ve...@chromium.org (2020-05-08)

I'm personally fine with (1), it seems like the simplest fix indeed. It works well for V8. The reason why I outlined the other solutions is because DevTools might want or need them. It seems fine by me to see this as follow-up work that the DevTools team might want to invest time in to improve the feature. I think fixing the security issue trumps blocking this on possibly better tooling support.

### si...@chromium.org (2020-05-08)

I'm surprised that (1) doesn't break any tests in DevTools.

My general concern is that the DevTools front-end gets confused by (potentially) having two different names for the same file. 

More specifically, I think this might break some cases of source map usage (where the source map is specified by a relative URL), because DevTools will try to resolve the relative URL using the pre-redirect URL (instead of the post-redirect URL).

I'll have to construct a repro and test if this is the case.


### si...@chromium.org (2020-05-08)

Thinking some more about it, I guess we need a translation service in the embedder that handles URLs.

Is there a reason a script needs to know its own URL?

A good design would be to just address scripts by e.g. scriptId and translate that to a stack trace in the embedder. The stack trace could then be translated depending on context to preserve security properties.

This would be a large refactoring, so the question is what to do in the meantime.

### ya...@chromium.org (2020-05-08)

Maybe we have no tests that cover the case where request url is not equal response url?

### ve...@chromium.org (2020-05-08)

I agree. (1) was the way to make V8 care least, with additional work needed on the outside. (2) was an olive branch to possibly simplify mapping by reusing V8 structures. It's possible there are no tests. I'd be very surprised if this is an important DevTools usecase, although it will possibly break that usecase. OTOH as long as the URL resolution is stable it'll probably work?

If the latter is true, do you think it's absolutely required for all possible DevTools workflows to work before this security leak is fixed?

### si...@chromium.org (2020-05-08)

> If the latter is true, do you think it's absolutely required for all possible DevTools workflows to work before this security leak is fixed?

I have no idea how many pages actually rely on redirects to serve their js sources. Do big CDNs do that? If so might break debugging for everything on such CDNs.

I can try to repro this tomorrow, and if I get a repro it will help us understand how bad things are broken.

But you are getting to the point: We possibly need to trade-off debuggability against security.

### ve...@chromium.org (2020-05-08)

Why would all redirects break? If you open a script using a pre-redirect url, wouldn't DevTools be able to load the script? Or would it get confused about what script it was talking about when it talks to V8?

Anyway, this is why I looped you in: I know you've spent some time dealing with how we match scripts and devtools windows for source :D

### si...@chromium.org (2020-05-11)

Here is a glitch that show that this patch causes source map URLs to be computed in the wrong way, resulting in 404s (and hence source mapping to stop working):  https://redirect-source-map.glitch.me/source.map

The reason is that we try to load https://redirect-source-map.glitch.me/source.map as source map (derived from the pre-redirect url) instead of the source map derived from the post-redirect URL.

To fix this, we need the post-redirect URL in DevTools. verwaest: Could you implement (2)? It should be relatively quick for you to do. 

The only remaining concern that I have is that even if we do this, the URLs in the stack traces will not match the URLs in the source maps. I think we need some additional fixes there.

Mike West: This is classified as HIGH, is this an accurate classification? The main question regarding the buggy fix in https://chromium-review.googlesource.com/c/chromium/src/+/2187792 is whether the severity of this issue justifies breaking DevTools, and I don't think I'm the right person to make the judgement.

### aa...@google.com (2020-05-11)

This behavior allows account takeover in web applications that append an auth token in a redirect after authenticating the user -- this includes some major, sensitive web properties. Mike and/or other Chrome Security folks should make the call, but IMHO this does warrant an expedited fix. 

### ar...@chromium.org (2020-05-11)

https://crbug.com/chromium/1074317#c39: I guess the link is https://redirect-source-map.glitch.me/

--------------------------------------------------------------

I tried a few things using Firefox.

Firefox uses the initial request URL in StackTrace. Hence they are passing the regression test:
https://wpt.fyi/results/content-security-policy/reporting/post-redirect-stacktrace.https.html?label=experimental&label=master&aligned
Applying the proposed fix https://chromium-review.googlesource.com/c/chromium/src/+/2187792 will align Chrome with Firefox.

I tried https://redirect-source-map.glitch.me/ I looks like Firefox is not able get the right sourcemap. This is likely because of the redirect.

--------------------------------------------------------------

This document says
https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit#

~~~
Regardless of the method used to retrieve the source mapping URL the same process is used to resolve it, which is as follows:
 When the source mapping URL is not absolute, then it is relative to the generated code’s “source origin”. The source origin is determined by one of the following cases:

1) If the generated source is not associated with a script element that has a “src” attribute and there exists a //# sourceURL comment in the generated code, that comment should be used to determine the source origin. Note: Previously, this was “//@ sourceURL”, as with “//@ sourceMappingURL”, it is reasonable to accept both but //# is preferred.

2) If the generated code is associated with a script element and the script element has a “src” attribute, the “src” attribute of the script element will be the source origin.

3) If the generated code is associated with a script element and the script element does not have a “src” attribute, then the source origin will be the page’s origin.

4) If the generated code is being evaluated as a string with the eval() function or via new Function(), then the source origin will be the page’s origin.
~~~

So (1) doesn't apply because there are no "//@ sourceURl" defined.
(2) apply and we should resolve the relative URL against the script src.

Maybe the new behavior is more correct relatively to this document and Firefox implementation?

--------------------------------------------------------------

### ar...@chromium.org (2020-05-11)

We discussed on chat with Sigurd. We agreed landing this patch, but putting the old behavior being a flag:
--enable-features=UnsafeScriptReportPostRedirectURL

This means this security issue will be fixed for M84.
Chrome is now aligned with the spec and with Firefox.
- If nobody complains, we can remove the flag and keep only the new behavior.
- If some devtools users complain, we can ask them to use the flag. Then we can implement (2) for the next release to fix the issue.
- If this cause a major issue on M84 stable, we can use Finch to restore the old behavior as a last resort.

I added the flag to my previous fix:
https://chromium-review.googlesource.com/c/chromium/src/+/2187792
and tested the behavior with/without the switch.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-05-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/0b707cbaa2cb806162797be55caf9f8074fbdccf

commit 0b707cbaa2cb806162797be55caf9f8074fbdccf
Author: arthursonzogni <arthursonzogni@chromium.org>
Date: Mon May 11 15:58:36 2020

Stop leaking cross-origin post-redirect data using StackTrace.

Whenever a URL is provided to the ScriptSourceCode constructor, use
the "request URL" instead of the "response URL".

This avoids malicious website to get access to the post-redirect URL.
They can get this by throwing an error and inspecting the error.stack.

The new behavior can be observed in:
1) The 'source-file' in CSP violations reports.
2) The URL(s) in javascript stack traces.
3) How relative source map are resolved.

After this patch (1), (2), (3) are now aligned with Firefox.

After this patch (3) is now matching with the specification:
https://docs.google.com/document/d/1U1RGAehQwRypUTovF1KRlpiOFze0b-_2gc6fAH0KY0k/edit#

This patch might break some client using devtool (See 3). A temporary command
line argument is provided to restore the old behavior:
--enable-features=UnsafeScriptReportPostRedirectURL
If you are using this flag, please let us know by filling a bug on
https://crbug.com

This flags can potentially be used to restore the old behavior on stable
using Finch if needed.

If nobody is complaining about the new behavior. The flag can be removed
after one release.

Bug: 1074317
Change-Id: I3629a5a0f8d67c13127f08ab36dc3df69aa0f98f
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2187792
Commit-Queue: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Sigurd Schneider <sigurds@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#767326}

[modify] https://crrev.com/0b707cbaa2cb806162797be55caf9f8074fbdccf/third_party/blink/renderer/bindings/core/v8/script_source_code.cc
[modify] https://crrev.com/0b707cbaa2cb806162797be55caf9f8074fbdccf/third_party/blink/renderer/bindings/core/v8/script_source_code.h
[modify] https://crrev.com/0b707cbaa2cb806162797be55caf9f8074fbdccf/third_party/blink/renderer/core/workers/worker_global_scope.cc
[delete] https://crrev.com/ebd5d87b720b7ba9e03d2caf328e8b8f3e6090f9/third_party/blink/web_tests/external/wpt/content-security-policy/reporting/post-redirect-stacktrace.https-expected.txt


### ar...@chromium.org (2020-05-11)

I am considering this to be fully fixed now. Let's see how it goes in M84 beta (see https://crbug.com/chromium/1074317#c42)

I won't request a M83 merge (stable cut is tomorrow).
The 2 fixes will land in M84 (branch cut is in 3 days)

### [Deleted User] (2020-05-11)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-11)

Requesting merge to stable M81 because latest trunk commit (767326) appears to be after stable branch point (737173).

Requesting merge to beta M83 because latest trunk commit (767326) appears to be after beta branch point (756066).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-05-11)

This bug requires manual review: To minimize risk and increase branch stability, all merge requests are being reviewed manually by the release team.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), cindyb@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2020-05-11)

+adetaylor@ to review and confirm a merge for M-83, see https://crbug.com/chromium/1074317#c44

### ad...@chromium.org (2020-05-11)

This has devtool client visible changes, so let's not merge to M83 at the last minute.

### ve...@chromium.org (2020-05-12)

+cbruni

### hi...@chromium.org (2020-05-13)

[Empty comment from Monorail migration]

### na...@google.com (2020-05-19)

[Empty comment from Monorail migration]

### hi...@chromium.org (2020-05-20)

[Empty comment from Monorail migration]

### ob...@gmail.com (2020-05-20)

The small question about the CSP fix https://crbug.com/chromium/1074317#c27. I found that the 'onsecuritypolicyviolation' js event allows to capture the post-redirect url too via the same field (sourceFile). Is that the separate case or it will be fixed here too? 

For fast check go to https://obmi.me/pocs/chromebugcsptrace_751cb9eb-bfe5-42be-9c9c-bd6e7c9d170d

and run the next js in the console:

```
document.onsecuritypolicyviolation = function(ev) { console.log("onsecuritypolicyviolation: ",ev, ev.sourceFile) }
var script = document.createElement('script')
script.src = `https://obmi.me/pocs/someredirect_18f572f4-0e72-4fc1-99cc-4432d2b72af4?dest=https://iam-gserviceaccount.com/static/js/bar.js?`
script.onload = ()=>{ count=0;_int=setInterval(()=>{ { if(count>5) clearInterval(_int) } count++; img() }, 1000) }
document.body.append(script)
```

### wf...@chromium.org (2020-05-20)

arthursonzogni@chromium.org or others can you look at #54 and decide whether this has to be re-opened or a new bug filed? Re-opening to make sure this gets looked at.

### [Deleted User] (2020-05-21)

[Empty comment from Monorail migration]

### [Deleted User] (2020-05-21)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ar...@chromium.org (2020-05-26)

Re https://crbug.com/chromium/1074317#c54.

There are two patches:
1) Strip the ?ref from the post-redirect URL in CspReport.sourceFile.
2) Use the initial URL instead of the final URL in StackTrace and CspReport.sourceFile.

(1) was a temporary patch, I didn't believe I would be able to make (2) on time. It turns out I was able to.
I will likely remove (1) at some point.

With both 1) and 2), I believe we are good.

The WPT test shows what browsers are leaking the post-redirect URL:
https://wpt.fyi/results/content-security-policy/reporting/post-redirect-stacktrace.https.html?label=experimental&label=master&aligned
- Firefox: Success
- Chrome: Success (because of {1,2})
- Edge: Currently failing. We just need for Edge to rebase for this to work.
- Webkit: Fail

I will recompile Chrome today and double check on the provided URL. I will update this thread if this isn't working as intended.

### ar...@chromium.org (2020-05-26)

[Comment Deleted]

### ar...@chromium.org (2020-05-26)

> I will recompile Chrome today and double check on the provided URL. I will update this thread if this isn't working as intended.

Fixed as intended:



### ob...@gmail.com (2020-05-26)

arthursonzogni@chromium.org could you set the onsecuritypolicyviolation event handler from https://crbug.com/chromium/1074317#c54 and check the output in console? Or it will be the same output as in the http requests?

### ar...@chromium.org (2020-05-26)

Yes, it will be the same in theory. It doesn't hurt double-checking. See the associated screenshot below:

### ob...@gmail.com (2020-05-26)

thank you :-)

### na...@google.com (2020-05-27)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2020-05-29)

Congrats! The Panel decided to award $5,000 for this report. 

### ob...@gmail.com (2020-05-29)

Thank you! :-)

### na...@google.com (2020-05-29)

[Empty comment from Monorail migration]

### do...@google.com (2020-06-15)

Any objections to me adding some folks from Mozilla and Apple to this and https://crbug.com/chromium/1082086? We have started privately discussing spec-side mitigations for https://crbug.com/chromium/1082086 at least, and this would be useful context for them.

### do...@chromium.org (2020-06-15)

Uh, oops, I forgot to remove the CC when I switched my comment from "I'm adding" to "any objections to me adding?" Sorry about that...

### aa...@google.com (2020-06-15)

AFAIK obmihail@gmail.com reported related bugs on the Mozilla and WebKit bug trackers and that their engineers are aware of the details, so I see no problem with adding a few folks here.

### do...@chromium.org (2020-06-15)

Great; I'm adding Anne and Youenn to this and https://crbug.com/chromium/1082086 so they have the extra context.

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-13)

obmihail@gmail.com - thanks for the report - how would you like to be credited in the Chrome release notes?

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### ob...@gmail.com (2020-07-13)

adetaylor@google.com Hello. You're welcome. Mention me as Mikhail Oblozhikhin, please.

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-28)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2021-11-10)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e2d82a30b2b81899a42cded440fbf314f5240609

commit e2d82a30b2b81899a42cded440fbf314f5240609
Author: Hiroshige Hayashizaki <hiroshige@chromium.org>
Date: Wed Nov 10 05:10:59 2021

Remove UnsafeScriptReportPostRedirectURL feature flag

The flag can be removed, because it has been staying
for 1.5 years since
https://chromium-review.googlesource.com/c/chromium/src/+/2187792
and the CL description said:

> If nobody is complaining about the new behavior.
> The flag can be removed after one release.

Bug: 1074317
Change-Id: I8cafc202659b5c13d878592b995a1b154adaade2
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3261495
Reviewed-by: Arthur Sonzogni <arthursonzogni@chromium.org>
Reviewed-by: Kouhei Ueno <kouhei@chromium.org>
Commit-Queue: Hiroshige Hayashizaki <hiroshige@chromium.org>
Cr-Commit-Position: refs/heads/main@{#940191}

[modify] https://crrev.com/e2d82a30b2b81899a42cded440fbf314f5240609/third_party/blink/renderer/core/workers/worker_global_scope.cc
[modify] https://crrev.com/e2d82a30b2b81899a42cded440fbf314f5240609/third_party/blink/renderer/bindings/core/v8/script_source_code.h
[modify] https://crrev.com/e2d82a30b2b81899a42cded440fbf314f5240609/third_party/blink/renderer/bindings/core/v8/script_source_code.cc


### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1074317?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1082086]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052109)*
