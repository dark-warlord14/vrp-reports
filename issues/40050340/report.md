# PaymentManager: attacker has some control over PaymentManager/PaymentInstruments of a cross-origin context

| Field | Value |
|-------|-------|
| **Issue ID** | [40050340](https://issues.chromium.org/issues/40050340) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>Payments, Internals>Sandbox>SiteIsolation |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | we...@gmail.com |
| **Assignee** | ro...@chromium.org |
| **Created** | 2019-10-05 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36

Steps to reproduce the problem:
PaymentManager api's Init method has two argument, one is scope url and the other is context url. In the renderer we could fake it because there are some validation. But in compromise renderer we could fake the context url and scope url, in fact we can change the other site's Payment Instrument.

To reproduce you need a local build of chrome; run the attached script 

$ python ./copy_mojo_js_bindings.py /path/to/chrome/.../out/Asan/gen
$ python -m SimpleHTTPServer&
$ out/Asan/chrome --enable-blink-features=MojoJS --user-data-dir=/tmp/nonexist 'http://localhost:8000/payment.html'

Now open the develope tool, execute:

pa.getPaymentInstrument("dc2de27a-ca5e-4fbd-883e-b6ded6c69d4f"); 

you will find the bobpay's  instrument has been edited.

and another instrument has not been edited:

pa.getPaymentInstrument("new-card"); 

so I can read and write the other scope's payment instrument

What is the expected behavior?
The browser should validate the last committed origin of the renderer.

What went wrong?
The browser has not validate the last committed origin of the renderer.

Did this work before? N/A 

Chrome version: 78.0.3904.21  Channel: beta
OS Version: 78.0.3904.21
Flash Version:

## Attachments

- [copy_mojo_js_bindings.py](attachments/copy_mojo_js_bindings.py) (text/plain, 513 B)
- deleted (application/octet-stream, 0 B)
- [payment.html](attachments/payment.html) (text/plain, 850 B)

## Timeline

### we...@gmail.com (2019-10-05)

I think maybe this bug could be more dangerous, when I change the instrument's method to localhost:8888 and use the payment request I will get HEAD request in my server, may be it could be used to hijack the payment request.

I have edited the payment.html, so I upload it again.

### mp...@google.com (2019-10-08)

rouslan@, can you take a look at this? What kind of damage can be caused if you are given false URLs for context and scope?

I'm assuming the worst that can happen is that an attacker can hijack a payment instrument and see all of the amounts the user tries to pay. Can an attacker get at shipping addresses or contact info here?

Tentatively marking as medium severity, but could be downgraded.

[Monorail components: Internals>Sandbox>SiteIsolation UI>Browser>Payments]

### mp...@google.com (2019-10-08)

But since you might be able to register a service worker for a different domain, this could be more severe?

### sh...@chromium.org (2019-10-08)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-08)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cr...@chromium.org (2019-10-08)

Thanks for the report!  At first glance it does sound like we should be using browser-side information (e.g., RenderFrameHost::GetLastCommittedURL()) rather than trusting the renderer, but I don't have the context on the PaymentManager code.  Hopefully rouslan@ can weigh in on the impact of this and what changes we might consider.  (In general, Site Isolation bypasses are High, but it will depend on what is possible if these URLs are spoofed.)

[Monorail components: Blink>Payments]

### ro...@chromium.org (2019-10-08)

TL;DR: This is low impact, but should be fixed.

The impact is that a compromised renderer can read and write any payment app's "instrument" metadata, which contains the following fields:
1) Required: method name, e.g., "https://google.com/pay" or "basic-card". 
2) Optional: card capabilities, such as card type and network.

In the case of Google Pay, it sets only the method name: "https://google.com/pay".

In the case of the demo at https://rsolomakhin.github.io/pr/apps/basic-card/, it sets the method name "basic-card", card type "credit", and card network "visa".

That's the information that the compromised renderer can read, which is not much.

If the compromised renderer deletes an instrument, that's equivalent to uninstalling a payment handler. That would be a denial of service attack.

The more complicated event is when a compromised renderer updates the "instrument" metadata in a payment handler.

If the instrument method name is changed from "basic-card" to "https://google.com/pay", then those merchants that request tokens from Google Pay would instead get raw credit card numbers from a possible payment handler, although I'm not aware of any production payment handler serving up "basic-card" today.

If the instrument method name is changed from "https://google.com/pay" to "basic-card", then those merchants that request raw credit card numbers will send a "paymentrequest" event to Google Pay instead. Since Google Pay requires the merchant to register and specify a bunch of method-specific parameters that would be absent from a "basic-card" request, then Google Pay will not be able to provide any response and will return an error.

In summary, the overall impact is low.

The fix is to use check the context_url and scope against the origin of the RenderProcessHost that owns the payment_manager.cc.

### ro...@google.com (2019-10-09)

Localhost TL;DR: Localhost HEAD request is not an issue.

>  when I change the instrument's method to localhost:8888 and use the payment request I will get HEAD request in my server

For this to work, it sounds like you called `new PaymentRequest([{supportedMethods: 'https://localhost:8888'}], details)` from payment.html. 

This HEAD request is looking for a payment method manifest location:
https://w3c.github.io/payment-method-manifest/

Then the browser is looking for a `Link: rel="payment-method-manifest"` in the HTTP response headers. For example:
Link: <payment-method-manifest.json>; rel="payment-method-manifest"

If that header is present, the browser will download the file https://localhost:8888/payment-method-manifest.json and parse it using SafeJsonParser:
https://cs.chromium.org/chromium/src/components/payments/content/utility/payment_manifest_parser.cc?l=380&rcl=c96c622ef3c6a4979ea069b8d5165ce30c00b925

The browser will look for the "supported_origins" field in the parsed payment method manifest file to determine whether the service worker's origin is allowed to handle payments for the "https://localhost:8888" payment method identifier.

This will not expose the payment details (total, line items, shipping address, contact info, card number, etc) to localhost.

Keep in mind that (by design) calling `new PaymentRequest([{supportedMethods: 'https://localhost:8888'}], details)` from any origin will make a HEAD request for "https://localhost:8888" in search of a payment handler to be installed just-in-time. Just-in-time installation of payment handlers is a feature in Chrome that enables downloading and installing service workers when a request for payment via their origins is made on the page.

Therefore, the HEAD request to localhost is not a new attack surface.

### we...@gmail.com (2019-10-10)

Thanks for your response! I agree with you, this is not a new attack surface and the impact is low.

### lu...@chromium.org (2019-10-11)

Thanks rouslan@ and weiwangpp93@!  Based on https://crbug.com/chromium/1011600#c7-#c9, I think we should change the bug title (since it is not really a "Site Isolation bypass" - there is no cross-site data disclosure and no incorrect renderer process sharing) and lower the security severity to low.  Please shout if you think these bug edits are wrong or if I misunderstood anything.  Also feel free to tweak the bug title further (I tried to do my best to summarize the contents of https://crbug.com/chromium/1011600#c7-#c8, but I am not sure if I understand all the details here).

RE: The fix is to use check the context_url and scope against the origin of the RenderProcessHost that owns the payment_manager.cc.

Yeah - I think using ChildProcessSecurityPolicyImpl::CanAccessDataForOrigin(process_id, context_url) should work.

Alternatively, maybe the PaymentManager can be more directly associated/bound to a particular RenderFrameHost (and/or document hosted within RenderFrameHost) - I am not sure what is the latest mojo guidance/approach for such association/binding (but I hope that dcheng@ and/or rockot@ in CC can help with this if needed).

### ro...@google.com (2019-10-13)

> ChildProcessSecurityPolicyImpl::CanAccessDataForOrigin(process_id, context_url) should work.

Thank you so much for the pointer!

### ro...@google.com (2019-10-16)

> Alternatively, maybe the PaymentManager can be more directly associated/bound to a particular RenderFrameHost.

I don't think PaymentManager can be associated with a RenderFrameHost, because a PaymentManager is accessible from a service worker, which is not inside of a frame, so will not have a RenderFrameHost, correct?

### lu...@chromium.org (2019-10-16)

RE: https://crbug.com/chromium/1011600#c12: rouslan@:

Good point - as you say, PaymentManager cannot be associated with RenderFrameHost, because PaymentManager is exposed not only through frames, but also through service workers.

Maybe dcheng@ and/or rockot@ know how to associate a mojo interface with an origin / execution context / frame-or-service-worker.  If this is difficult to achieve, then I think that CanAccessDataForOrigin (from https://crbug.com/chromium/1011600#c10/#c11) should be a reasonable approach.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8788e25455fd0556e908d5b536f3fa132af72cbe

commit 8788e25455fd0556e908d5b536f3fa132af72cbe
Author: Rouslan Solomakhin <rouslan@chromium.org>
Date: Thu Oct 24 01:10:05 2019

[Payment Handler] Tie payment manager to origin.

Before this patch, a compromised renderer could read-write the
instrument metadata for any origin.

This patch ties the payment manager to the origin of its context.

After this patch, cross-origin payment manager access should not be
possible.

Bug: 1011600
Change-Id: I22142bdca98de9c9334c0f5e62f9f0268cda8f87
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1865770
Reviewed-by: Oliver Chang <ochang@chromium.org>
Reviewed-by: Matt Falkenhagen <falken@chromium.org>
Reviewed-by: Łukasz Anforowicz <lukasza@chromium.org>
Commit-Queue: Rouslan Solomakhin <rouslan@chromium.org>
Cr-Commit-Position: refs/heads/master@{#708867}

[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/browser_interface_binders.cc
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/frame_host/render_frame_host_impl.cc
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/frame_host/render_frame_host_impl.h
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/payments/payment_app_content_unittest_base.cc
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/payments/payment_app_context_impl.cc
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/payments/payment_app_context_impl.h
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/payments/payment_manager.cc
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/payments/payment_manager.h
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/renderer_host/render_process_host_impl.cc
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/renderer_host/render_process_host_impl.h
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/service_worker/service_worker_provider_host.cc
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/worker_host/dedicated_worker_host.cc
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/browser/worker_host/shared_worker_host.cc
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/public/browser/render_process_host.h
[modify] https://crrev.com/8788e25455fd0556e908d5b536f3fa132af72cbe/content/public/test/mock_render_process_host.h


### ro...@google.com (2019-10-24)

weiwangpp93@: Could you please verify the fix is working on Chrome tip-of-the tree? The info at https://chromiumdash.appspot.com/commit/8788e25455fd0556e908d5b536f3fa132af72cbe shows the fix has not been shipped to Canary yet.

### ro...@google.com (2019-10-24)

[Empty comment from Monorail migration]

### we...@gmail.com (2019-10-24)

Ok, I will verify it after I finished compile the commit, thanks for your quick review and fix.

### we...@gmail.com (2019-10-25)

Yes, I think it has been fixed correctly

### ro...@chromium.org (2019-10-25)

Requesting a merge of https://chromium.googlesource.com/chromium/src.git/+/8788e25455fd0556e908d5b536f3fa132af72cbe into M-79, which branched about a week ago.

Not requesting a merge into M-78, because it's already in stable and the severity is low.

### sh...@chromium.org (2019-10-25)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-26)

Your change meets the bar and is auto-approved for M79. Please go ahead and merge the CL to branch 3945 (refs/branch-heads/3945) manually. Please contact milestone owner if you have questions.
Merge instructions: https://www.chromium.org/developers/how-tos/drover
Owners: benmason@(Android), kariahda@(iOS), cindyb@(ChromeOS), govind@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-10-26)

[Empty comment from Monorail migration]

### ro...@chromium.org (2019-10-27)

Merged in https://crrev.com/622e25f609f5db4260b9c85ba97f789ac515b14f

### na...@google.com (2019-10-28)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-05)

[Empty comment from Monorail migration]

### ad...@google.com (2019-12-06)

weiwangpp93@gmail.com - how would you like to be credited in the release notes?

### ad...@chromium.org (2019-12-06)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-12-10)

[Empty comment from Monorail migration]

### we...@gmail.com (2019-12-12)

Keep me anonymous is ok.

### na...@google.com (2019-12-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-12-19)

Congrats! The Panel decided to reward $500 for this report!

### na...@google.com (2019-12-19)

[Empty comment from Monorail migration]

### sh...@chromium.org (2020-01-31)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-01-21)

Reward has been donated to a charitable organization! 

### am...@google.com (2021-01-21)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/1011600?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Payments, Internals>Sandbox>SiteIsolation]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40050340)*
