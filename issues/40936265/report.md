# Security: Persistent XSS via malicious user-uploaded PaymentRequest manifest and service worker

| Field | Value |
|-------|-------|
| **Issue ID** | [40936265](https://issues.chromium.org/issues/40936265) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Payments |
| **Platforms** | Android, Fuchsia, Linux, Mac, Windows, ChromeOS |
| **Reporter** | se...@gmail.com |
| **Assignee** | sm...@chromium.org |
| **Created** | 2023-10-14 |
| **Bounty** | $16,000.00 |

## Description

**VULNERABILITY DETAILS**  

This vulnerability enables an attacker to execute XSS on websites that allow the uploading of arbitrary JavaScript files, provided that the Content-Type header is correctly set (e.g., text/javascript, application/javascript, etc.).

**VERSION**  

Chrome Version: [118.0.5993.70] stable, [120.0.6066.1] dev, [120.0.6062.2] beta

**REPRODUCTION CASE**

1. Host the 'server.js' file along with the "uploads" folder containing scripts on your secure HTTPS server.
2. Replace "default\_applications" (payment-manifest.js) with the actual domain name of your uploaded files.
3. Host the "exploit.html" (Also change fileName and BASE variables) file on the attacker's website.
4. Navigate to "exploit.html" in your web browser; you should observe a pop-up alert.

ROOT CAUSES  

This exploit utilizes the Payment Request API. According to the specification at <https://www.w3.org/TR/payment-method-manifest/>:

"The resource identified by the payment method identifier URL does not directly contain the machine-readable payment method manifest. It is often a generic URL (such as "<https://alicepay.com/>") which is more suitable for human-readable content. Instead, a HTTP Link header is used to direct user agents seeking out the payment method manifest toward another location. [RFC8288]"

However, Chromium, if it doesn't find the Link header, simply uses the request body. This violates the concepts of the web standard, as serving files for download should not lead to XSS.

We only serve the file with the text/javascript (or application/javascript) type because we are loading a service worker, which requires a specific MIME type.

If we're discussing the source code, the vulnerability lies in chromium/components/payments/core/payment\_manifest\_downloader.cc:

```
  std::string link_header;  
  headers->GetNormalizedHeader("link", &link_header);  
  if (link_header.empty()) {  
    // Fallback to HTTP GET when HTTP HEAD response does not contain a Link  
    // header.  
    FallbackToDownloadingResponseBody(final_url, std::move(download));  
    return;  
  }  

```

This was added in the latest patch concerning payment\_manifest\_downloader.cc:  

<https://github.com/chromium/chromium/commit/faf93efcd47aa9a96fa0800d4ebc0f52ddccc303>

FIX  

I strongly recommend reverting this change (because it jeopardizes hundreds of thousands of websites).  

As a patch, it is sufficient to roll back payment\_manifest\_downloader to the version before this commit.  

I also advise you to add a Content-Type check for payment-manifest, as it is currently being ignored.

IMPACT  

This completely violates the concept that any files can be safely served on the server and served with "Content-Disposition: attachment;".  

I haven't done much research on this topic, but I already know that some Microsoft and Apple services are affected by this vuln.

**CREDIT INFORMATION**  

Reporter credit: Vsevolod Kokorin (Slonser) of Solidlab

## Attachments

- [chrome-0day.mp4](attachments/chrome-0day.mp4) (video/mp4, 2.0 MB)
- [exploit.html](attachments/exploit.html) (text/plain, 1.1 KB)
- [server.js](attachments/server.js) (text/plain, 539 B)
- [logo.jpg](attachments/logo.jpg) (image/jpeg, 15.6 KB)
- [manifest.js](attachments/manifest.js) (text/plain, 334 B)
- [payment-manifest.js](attachments/payment-manifest.js) (text/plain, 162 B)
- [sw-slonser.js](attachments/sw-slonser.js) (text/plain, 250 B)

## Timeline

### [Deleted User] (2023-10-14)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-17)

smcgruer@ could you take a look? I haven't repro'd locally yet but wanted to send this your way to assist with evaluating. cc'ing other Payments folks for visibility as well.

I'm having some trouble understanding how all of the pieces here fit together, and what is actually occurring. My understanding of this issue is that:

1. An attacker origin A that can initiate a payment handler from origin B
2. That payment request fails
3. Origin A triggers a redirect to a path on origin B that should start a download (document.location = `${BASE}/C4T BuT S4D`)
4. That path on Origin B uses Express's res.download() method to indicate a download [1]
5. Instead of that occurring [this part is unclear] the service worker from Origin A fires and intercepts the request to instead serve the <script> result?

Reporter could you clarify exactly what you believe is occurring with a bit more detail? This will help us triage and set accurate security labels.

[1]: https://expressjs.com/en/api.html#:~:text=Transfers%20the%20file%20at%20path%20as%20an%20%E2%80%9Cattachment%E2%80%9D.%20Typically%2C%20browsers%20will%20prompt%20the%20user%20for%20download.%20By%20default%2C%20the%20Content%2DDisposition%20header%20%E2%80%9Cfilename%3D%E2%80%9D%20parameter%20is%20derrived%20from%20the%20path%20argument%2C%20but%20can%20be%20overridden%20with%20the%20filename%20parameter.

[Monorail components: Blink>Payments]

### se...@gmail.com (2023-10-17)

Hello, the exploitation chain is like this:
1. The attacker places my attached manifest.json, payment-manifest.js, and sw-slonser.js on a host that is not their own (for example, using a upload functionality of the site).
2. After that, on the domain controlled by the attacker, we initiate a payment request specifying payment-manifest.js from the target site.
3. Due to the fact that the request body is now accepted for payment request, the service worker from manifest.js will be registered on target site, leading to XSS

So if a site allows us to upload our file with the .js extension, then this leads to XSS

### ro...@chromium.org (2023-10-17)

Calling `PaymentRequest(supportedMethods: 'https://49a0-185-219-81-55.ngrok-free.app/download/payment-manifest.js')` is expected to register the service worker 'https://49a0-185-219-81-55.ngrok-free.app/download/sw-slonser.js' in accordance with just-in-time installation behavior for Payment Handlers.

When 'exploit.html' redirects to 'https://49a0-185-219-81-55.ngrok-free.app/download/C4T BuT S4D' upon failed[1] payment, it is expected that the newly registered service worker could intercept fetch requests for its own server.

Regarding the fall-back from the missing Link header to the HTTP GET, that's the desired behavior in Chrome. If the spec is not aligned with this, we can update the spec.

I need guidance on how this falls under the XSS umbrella. cthomp@ - do you know?

- - - - - - - - - - - - - - - - - - - -

[1] Payment fails after registering the 'sw-slonser.js' service worker and firing the 'paymentrequest' event inside of it. The failure occurs because the service worker does not have an event handler for the 'paymentrequest' event.

### se...@gmail.com (2023-10-17)

Your desired behavior leads to a new type of XSS attacks on users of your browser. Because many sites have the function of downloading and sharing arbitrary files.

### se...@gmail.com (2023-10-17)

"Regarding the fall-back from the missing Link header to the HTTP GET, that's the desired behavior in Chrome. If the spec is not aligned with this, we can update the spec."
Are you sure that this is a good idea, this action will put many sites at risk? 
This functionality should not lead to XSS. If earlier the maximum impact from downloading malicious JS to target site was bypassing CSP policies, now the attacker receives a full-fledged XSS

### sm...@chromium.org (2023-10-17)

> This was added in the latest patch concerning payment_manifest_downloader.cc:
https://github.com/chromium/chromium/commit/faf93efcd47aa9a96fa0800d4ebc0f52ddccc303

As a brief note (and not a commentary on the severity of the bug, I need to spend some time to fully understand it) - as far as I know, the behavior of falling back from Link header to body content is not new in this patch. It has always (?) been the case, since Payment Handler was implemented years ago.

cthomp@ - I think we need some XSS experts in here asap; I'm happy to make time on my and Rouslan's calendar for us to explain how Payment Handler works today, but we don't have enough knowledge of XSS to determine the threat level here.

### sm...@chromium.org (2023-10-17)

cthomp@ - I've started an internal write-up here (internal only), https://docs.google.com/document/d/1InaU5_B0O09kKKazAqTlzcKmq59BSyN7ZCmYW9fGT-E/edit . I'd like some eyes from security folks, XSS experts, and folks familiar with service workers ASAP.

### sm...@chromium.org (2023-10-17)

[Empty comment from Monorail migration]

### ct...@chromium.org (2023-10-17)

We discussed this internally and have an plan of action which we are circulating with our internal experts for feedback.

Setting security labels according to our understanding:

- Severity-High: This allows semi-universal XSS, but noting that this does require the target origin serve user uploaded files, and does require the victim visit the attacker's page.
- FoundIn-116: This has likely been possible for a while now, but marking FoundIn-116 to at least cover all our current releases.

### sm...@chromium.org (2023-10-17)

Copying over content from the internal doc, now that we've solidified on understanding. Apologies for the wall of text incoming!

# Background - Payment Handlers 

Payment Handlers are intended to be a way for payment apps such as Google Pay or PayPal to integrate deeper with the browser, providing a better user experience for paying. They exist in two forms of note here:

- Service-worker based 'web' Payment Handlers
- Native Android app Payment Handlers

The usual use-case for a Payment Handler is:

1. User is on merchant checkout flow, merchant.example
2. They click on a payment app's button as their payment method, e.g. Google Pay
3. From the merchant.example site, a Payment Request pointing to e.g., pay.google.com is triggered.
4. This causes the Google Pay Payment Handler to start
    - For a web-based Payment Handler, this means firing an event at an installed service-worker owned by pay.google.com, which can then open a form of pop-up window to interact with the user.
    - For a native Android app Payment Handler, this means intent-ing from Chrome to the native app.

In both cases, a Payment Handler for e.g. pay.google.com (or more broadly, paymentapp.example) needs some way to be installed and in the case of native Android apps to be connected between the native app and the 'owning' site paymentapp.example.

# Background - JIT-install of Payment Handlers // The manifest file
https://w3c.github.io/payment-method-manifest/

In order to support installing Payment Handlers without needing to visit paymentapp.example directly (so called Just-In-Time install, during a checkout flow on merchant.example), as well as provide a way for paymentapp.example to define linkage to native apps, the Payment Method Manifest spec defines a manifest file that can be hosted on paymentapp.example.

It's a bit confusing as there are basically two layers of manifest involved:

The payment method manifest is loaded first, and it defines where to look for the Payment Handler
{
  "default_applications": ["app/webappmanifest.json"],
  "supported_origins": [
    "https://bobpay.xyz",
    "https://alicepay.friendsofalice.example"
  ]
}

Then a web-app manifest is loaded, which defines the web-app itself and any native app linkage:
{
  "short_name": "Payment App",
  "name": "Payment App",
  "icons": [{
    "src": "https://www.paymentapp.example/icon.svg"
  }],
  "serviceworker": {
    "src": "/path/to/service_worker.js",
    "use_cache": true
  }
}

The JIT path works as follows:

1. https://merchant.example script creates a PaymentRequest object, pointing at https://paymentapp.example/optionally/some/path
2. Inside the browser, we check if there is already a Payment Handler service worker installed for paymentapp.example
3. If not, then the browser loads https://paymentapp.example/optionally/some/path, and:
    a. First checks for a Link header with rel="payment-method-manifest".
    b. If present, load that content, replacing the specified URL.
    c. Otherwise, just use the content of the specific URL.
4. Treat the loaded content (either originally specified URL or the Link header redirect) as a payment method manifest file.
5. Parse the payment method manifest, and for the first URL string in default_applications:
    a. Load the contents of the URL as a web app manifest file
    b. For this web app manifest file, create a Payment Handler in the browser with a name, icon, etc. (Out of scope for this doc).
    c. For this web app manifest file, if a serviceworker argument exists:
        i. Install the service worker specified with serviceworker[src] as a service worker for paymentapp.example

Step 5.c.i is the interesting one here. The original idea was that paymentapp.example is in control of its own payment method manifest file, and so controls what web app manifests might be parsed by the browser. But that may not be valid as an assumption.

(... to be cont'd)

### [Deleted User] (2023-10-17)

[Empty comment from Monorail migration]

### sm...@chromium.org (2023-10-17)

# The attack in this bug

If I understand correctly, this bug envisages a service, hostingapp.example, where users can upload content and end up with it hosted on URLs such as https://hostingapp.example/download/myfilehere.arbitraryextension

The attack then is:

1. [On attackers computer] Upload a payment method manifest, a web app manifest, and a service worker source script to the hosting site.
These end up at (say) /download/user1234/payment_method_manifest.json, /download/user1234/web_app_manifest.json, and /download/user1234/service_worker_src.js
2. [On users computer] From an attacker-controlled website that the user visits, https://attacker.example, trigger a Payment Request targeting the uploaded payment method manifest
    a. const request = new PaymentRequest("https://hostingapp.example/download/user1234/payment_method_manifest.json")
    b. This causes the browser to do steps 1-5b in the above example, but not to install the service worker yet.
3. [On users computer] Call request.show(), which causes the attacker-controlled service worker to be installed (step 5.c)
4. [On users computer] In the attack provided, the injected service worker has a fetch handler, which can then e.g. rewrite HTML requests the user makes on hostingapp.example

self.addEventListener("fetch", (event) => {
console.log(`Handling fetch event for ${event.request.url}`);
let blob = new Blob(["<script>alert('pwned by Slonser')</script>"],{type:"text/html"});
event.respondWith(new Response(blob));
});
5. [On users computer] Redirect user to a hostingapp.example URL, which then hits the service worker instead, which e.g., injects content to steal cookies/other attack.

# How long has it existed for?

We launched Payment Handlers in April 2018, and I think it's been vulnerable from the start. (https://groups.google.com/u/1/a/chromium.org/g/blink-dev/c/fVxkGlKpDbU/m/-wtiE0w1AwAJ)

# How quickly could we disable this attack?

We have a base::Feature flag for JIT install, kWebPaymentsJustInTimePaymentApp, which in theory could be Finch kill-switched. We would have to test to see whether or not turning it off works, because we haven't touched it in 5 years. The code is likely quite bit-rotted.

I suspect from looking at code that it might work to stop the JIT install (and thus this attack), but it would break known payment app flows if we do so (untested).

Disabling the flag would not remove any previously installed service workers. I do not currently know if we have a method to do that, or if we would want to do it either.

# How can we defend against this attack // modify Payment Handler?

Option #1
- payment method manifest needs to be served as Content-Type: application/payment-manifest+json
- (optionally?) web app manifest needs to be served as Content-Type: application/manifest+json

Option #2:
- The service worker script needs to be served as Content-Type: application/payment-request+javascript (or similar)

Option #3:
- The content-disposition for the payment method manifest needs to not be set as 'attachment'

Option #4:
- The content-disposition for the payment method manifest needs to be set as (a new) 'payment-request' disposition

## Other options identified along the way

1. Remove the ability to specify a payment method manifest directly, and require the Link header be used.
    - This means an attacker needs to get the host to serve *some* URL with a Link header pointing at their uploaded payment method manifest file. Likely means that the host must be providing arbitrary header writing capabilities to the attacker.

2. Remove the ability to do JIT install entirely, and require installs to be triggered from a first-party context (e.g. when user is directly on https://hostingapp.example, and that website directly installs the service worker).
    - There is no current mechanism to do direct install of a Payment Handler from a 1p context (we just removed it earlier in 2023 for privacy reasons!!).

3. Remove the service worker part of Payment Handler, and basically reduce it to just a type of pop-up window.
   - This is basically equivalent to #2.

4. Change Payment Handler to require going via a .well-known URL on the server instead?

(... to be cont'd)

### sm...@chromium.org (2023-10-17)

# Currently Proposed Path Forward

From internal discussion, we believe that the best approach here is to introduce a new mime type for payment method manifests, Content-Type: application/payment-method-manifest+json (similar to the existing Content-Type: application/manifest+json for web app manifests). The browser would then require this Content-Type to be present when it fetches a payment method manifest file, or it would fail the Payment Request call and wouldn't load the web app manifest (and ultimately install the service worker).

This would be a breaking change for all users of Payment Handler. We have ways to contact some of that list, and can do an announcement to e.g. blink-dev@, HOWEVER we have no way of knowing if there are other affected parties.

It would be safe for affected parties to update their Content-Types ahead of time (e.g., today). Currently, Chrome does no checking of the payment method manifest MIME type.

Open question: There was some debate as to whether the correct thing to do instead would be to introduce a new required Content-Disposition of "payment-request". The author is not familiar with Content-Type vs Content-Disposition.

### ct...@chromium.org (2023-10-17)

(Updating title a bit for clarity)

### aa...@google.com (2023-10-18)

[Empty comment from Monorail migration]

### se...@gmail.com (2023-10-18)

Small notice, you said: 
> "If I understand correctly, this bug envisages a service, hostingapp.example, where users can upload content and end up with it hosted on URLs such as https://hostingapp.example/download/myfilehere.arbitraryextension"

This is not entirely accurate; a file can be stored in various ways or accessed via a key, as in some Object Storage systems (e.g., https://hostingapp.example/download?key=RANDOM_KEY). The crucial point lies in the specified Content-Type (not in file extension in the url), while the rest depends on the logic of the web application.



### se...@gmail.com (2023-10-18)

I also have my own opinion regarding your "Open question". It seems to me that introducing a new Content-Disposition is excessive. Currently, Content-Disposition has a small and limited set of values regulated by RFC. In contrast, Content-Type does not have such strict limitations because new MIME types are constantly emerging. Therefore, the decision with Content-Type that you have chosen now is more optimal (developers will only need to change its value to the new one).

### [Deleted User] (2023-10-18)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@chromium.org (2023-10-18)

Another option being discussed currently: instead of either Content-Type or Content-Disposition, 'just' make the existing Link header mandatory. That is, for a Payment Request call:

new PaymentRequest([{supportedMethods: 'https://paymentapp.example/some/path'}], ...);

The server hosting https://paymentapp.example/some/path MUST respond with a Link header with rel="payment-method-manifest", with the location of the payment method manifest. That location could be the same as the original path, e.g.:

new PaymentRequest([{supportedMethods: 'https://paymentapp.example/app/payment_method_manifest.json'}], ...);
+
Link: </app/payment_method_manifest.json>; rel="payment-method-manifest"

Is valid.

### se...@gmail.com (2023-10-19)

If you are interested in my opinion. It sounds like the best architectural solution because you won't have to change the specifications.
But I think it's worth adding an additional check for the content-type in the manifest. This will help prevent additional attack vectors in the future. It's not necessary to introduce a new mime type; it's sufficient to perform a check for already existing types like application/json or application/manifest+json, as currently it accepts files with content marked as text/plain or text/html.

### se...@gmail.com (2023-10-19)

> We launched Payment Handlers in April 2018, and I think it's been vulnerable from the start. (https://groups.google.com/u/1/a/chromium.org/g/blink-dev/c/fVxkGlKpDbU/m/-wtiE0w1AwAJ)

I conducted some research, and this is not entirely true. Versions released after 2020 (release 83) are vulnerable.
I think it's root of the problem - https://groups.google.com/a/chromium.org/g/paymentrequest/c/w4OO802SR5U
Commit: https://github.com/chromium/chromium/commit/4ab8845ffc07354385e6459d03b46d19881ca046
"After this patch, it's possible to host the payment method manifest
directly at the URL of the payment method identifier, which makes
testing Chrome and developing payment apps easier."

### sm...@chromium.org (2023-10-19)

Thanks sevakokorin80, that's great sleuthing! It's not great to see that we made that change without even an Intent to Ship around it (that I can find, went looking in blink-dev to no avail). crbug.com/1035147#c10 makes some claim that the security team were involved at the time, but it's sadly not clear.

Long term, I think we may want to move towards option #3 mentioned in the TAG review (https://github.com/w3c/payment-method-manifest/issues/10); requiring the use of a .well-known URL. However that would be a breaking change and a large shift for everyone involved, so we'll start with going back to requiring a Link header, and work from there :).

Separately, I now have a CL up and in review which I believe correctly implements the idea to require a Link header - https://chromium-review.googlesource.com/c/chromium/src/+/4954394

### sm...@chromium.org (2023-10-19)

Some sleuthing of my own: https://crbug.com/chromium/853937 is a near exact duplicate of this bug before the direct-GET was added, which was reported resolved by https://chromium-review.googlesource.com/c/chromium/src/+/1132116 . It's not clear to me if it really was (I think maybe, in the world before direct-GET of the payment method manifest), but it's a real shame that we knew the exact attack vector (file-upload to target site) and ended up making the same mistake only 2 years later on the same API :(.

### se...@gmail.com (2023-10-19)

A small note regarding the payment API: in Apple WebKit, calling it requires user interaction, whereas in Chromium it does not. I suggest you take this into consideration to minimize potential damage from attacks in the future.

```
SecurityError: show() must be triggered by user activation
```




### gi...@appspot.gserviceaccount.com (2023-10-19)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/8eddc1354a929176bdd7514d0f8e55a7aa0d7389

commit 8eddc1354a929176bdd7514d0f8e55a7aa0d7389
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Thu Oct 19 17:11:12 2023

[PaymentHandler] Require Link header when fetching payment method manifests

Bug: 1492698
Change-Id: Ib8213f2826cfb94b8c2c63a4f4b7b5ae3dd26ea9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4954394
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1212234}

[modify] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/payments/core/native_error_strings.cc
[modify] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/payments/core/payment_manifest_downloader.h
[modify] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/payments/core/features.cc
[add] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/test/data/payments/abort_responder_app.json.mock-http-headers
[modify] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/payments/core/native_error_strings.h
[modify] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/chrome/browser/ui/views/payments/payment_request_can_make_payment_metrics_browsertest.cc
[add] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/test/data/payments/app_store_billing_tests/method_manifest.json.mock-http-headers
[add] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/test/data/payments/paulpay.test/pay.mock-http-headers
[modify] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/payments/core/payment_manifest_downloader_unittest.cc
[add] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/test/data/payments/orenpay.test/pay.mock-http-headers
[add] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/test/data/payments/just-in-time/pay.json.mock-http-headers
[add] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/test/data/payments/nickpay.test/pay.mock-http-headers
[add] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/test/data/payments/can_make_payment_event_fields/app/pay.mock-http-headers
[modify] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/payments/core/features.h
[modify] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/payments/core/payment_manifest_downloader.cc
[add] https://crrev.com/8eddc1354a929176bdd7514d0f8e55a7aa0d7389/components/test/data/payments/redirect/destination/pay.mock-http-headers


### sm...@chromium.org (2023-10-19)

Per security process, I'm marking this bug fixed. Next steps:

1. Verify this fix on Canary (will re-ping the bug once the fix is in a Canary release), both that it avoids the security issue and hasn't broken known payment apps.
2. Outreach to payment apps about the new requirement for the Link header.
3. Merge this back as far as security team requires (TBD how far)
4. Update the payment-method-manifest spec to match the new behavior, with (possibly after the public opening of this bug) a new security section talking about the risk of hosting services + payment method manifests.
5. Consider follow on improvements/fixes, such as:
  i. Doing Content-Type checks
  ii. Adding a Content-Disposition check (!= attachment)
  iii. Maybe one day moving entirely to a .well-known file approach.

(Others - feel free to chime in with other items to be done!)

### sm...@chromium.org (2023-10-19)

Oh, and:

6. Update all the demo payment apps we have on https://rsolomakhin.github.io/, to host them somewhere that can serve a Link header -_-.

### [Deleted User] (2023-10-19)

[Empty comment from Monorail migration]

### se...@gmail.com (2023-10-19)

In my personal opinion:
Speaking about Content-Type, it will help to address issues when a web application has Header Injection (or injections in the Link header) on one of the API endpoints, as this currently leads to XSS along with the possibility of file uploads. Therefore, I think it's worth checking the Content-Type and verifying it against a specific mime type (application/manifest+json), because it's not automatically set based on the file's content.

Unfortunately, this may also potentially break many applications, so you should think about how to make such a transition smoother.

As for checking Content-Disposition - it doesn't seem like a sensible solution, because valid applications may serve payment manifests for download. I believe there's no problem with that.

### [Deleted User] (2023-10-19)

Requesting merge to stable M118 because latest trunk commit (1212234) appears to be after stable branch point (1192594).

Requesting merge to beta M119 because latest trunk commit (1212234) appears to be after beta branch point (1204232).

Merge review required: a commit with .grd/.json string changes was detected.

Merge review required: a commit with .grd/.json string changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@chromium.org (2023-10-20)

The fix has now landed in Canary versions 120.0.6078.0 and above. Currently available in Mac, Windows, and Android at least.

Reporter - if you can verify independently that your reproduction no longer works on 120.0.6078.0+, that would be great!

Rouslan - I'm OOO today, could you do me a favour and verify that Canary is behaving as expected (e.g., doesn't allow direct payment_method_manifest.json loads, requires a Link header), and then answer the questions in https://crbug.com/chromium/1492698#c31 ? Thank you!!

### ro...@google.com (2023-10-20)

Verified working as expected in Chrome Canary 120.0.6078.0 (Official Build) canary (arm64). 

Payment apps with HTTP header Link rel="payment-method-manifest" continue to work. E.g., see the test page @ https://rsolomakhin.github.io/pr/bob/ or https://rsolomakhin.github.io/pr/payjs/.

Payment apps without the HTTP header Link rel="payment-method-manifest" no longer work. E.g., see the test page @ https://rsolomakhin.github.io/pr/ph-icon-size/ or https://rsolomakhin.github.io/pr/ph-themes/.


### ro...@google.com (2023-10-20)

> 1. Which CLs should be backmerged? (Please include Gerrit links.)

https://crrev.com/c/4954394

> 2. Has this fix been tested on Canary?

Yes, the fix has been tested on Chrome Canary 120.0.6078.0 (Official Build) canary (arm64) on MacOS.

> 3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

No known stability regressions or risks.

> 4. Does this fix pose any known compatibility risks?

Yes, there is a compatibility risk for existing payment apps. The team is reaching out to the known payment apps that are potentially affected.

> 5. Does it require manual verification by the test team? If so, please describe required testing.

No need for manual verification by the test team.

### [Deleted User] (2023-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-20)

Requesting merge to stable M118 because latest trunk commit (1212234) appears to be after stable branch point (1192594).

Requesting merge to beta M119 because latest trunk commit (1212234) appears to be after beta branch point (1204232).

Merge review required: a commit with .grd/.json string changes was detected.

Merge review required: a commit with .grd/.json string changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ro...@google.com (2023-10-20)

> Please answer the following questions so that we can safely process this merge request:

Answered in https://crbug.com/chromium/1492698#c34.

### se...@gmail.com (2023-10-21)

I have analyzed the patch from my side, and as a reporter of the issue, I can say that the initial attack vector no longer works.

I also tested the popular Payment APIs, and it seems that major services won't be heavily affected because they also strive to support Apple WebKit, which doesn't exhibit this behavior. Therefore, transitioning to the new component logic should be smoother.

### [Deleted User] (2023-10-21)

Requesting merge to stable M118 because latest trunk commit (1212234) appears to be after stable branch point (1192594).

Requesting merge to beta M119 because latest trunk commit (1212234) appears to be after beta branch point (1204232).

Merge review required: a commit with .grd/.json string changes was detected.

Merge review required: a commit with .grd/.json string changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-22)

Requesting merge to stable M118 because latest trunk commit (1212234) appears to be after stable branch point (1192594).

Requesting merge to beta M119 because latest trunk commit (1212234) appears to be after beta branch point (1204232).

Merge review required: a commit with .grd/.json string changes was detected.

Merge review required: a commit with .grd/.json string changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@chromium.org (2023-10-23)

Looks like sheriff-bot is stick here -_-. I'll follow up internally, but copying from Rouslan's https://crbug.com/chromium/1492698#c34:

> 1. Which CLs should be backmerged? (Please include Gerrit links.)

https://crrev.com/c/4954394

> 2. Has this fix been tested on Canary?

Yes, the fix has been tested on Chrome Canary 120.0.6078.0 (Official Build) canary (arm64) on MacOS.

> 3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?

No known stability regressions or risks.

> 4. Does this fix pose any known compatibility risks?

Yes, there is a compatibility risk for existing payment apps. The team is reaching out to the known payment apps that are potentially affected.

> 5. Does it require manual verification by the test team? If so, please describe required testing.

No need for manual verification by the test team.

### am...@chromium.org (2023-10-23)

Thanks for the quick turnaround on this issue. Sheriffbot isn't stuck, it's just nagging due to this being a sev-high issue and also there being two pending merges. 
Due to the timing of this report and fix being landed, it wasn't going to make deadlines for merge for this week's updates also considering the need for sufficient bake time. 
Have all the payment apps this would affect been notified at this time? I'd like to ensure that this have been initiated before we merge to 119 (which will be promoted to Stable next week) or 118 (which will become Extended Stable next week) to eliminate potentially unnecessary reports of functional regressions from those vendors.  

In order to get this fix into Early Stable and last beta for 119, we'll need to get this merged by EOD tomorrow (Tuesday, 24 October). Please confirm the outreach to the payment apps vendors has been initiated and we can look at approvals today or tomorrow. Thank you. 

### am...@chromium.org (2023-10-23)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-23)

Requesting merge to stable M118 because latest trunk commit (1212234) appears to be after stable branch point (1192594).

Requesting merge to beta M119 because latest trunk commit (1212234) appears to be after beta branch point (1204232).

Merge review required: a commit with .grd/.json string changes was detected.

Merge review required: a commit with .grd/.json string changes was detected.

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [118, 119].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@chromium.org (2023-10-23)

> Have all the payment apps this would affect been notified at this time? I'd like to ensure that this have been initiated before we merge to 119 (which will be promoted to Stable next week) or 118 (which will become Extended Stable next week) to eliminate potentially unnecessary reports of functional regressions from those vendors.  

We have now contacted all known payment apps that might be affected by this change.

### am...@chromium.org (2023-10-23)

119 and 118 merges approved for https://crrev.com/c/4954394
please merge this fix to branch 6045 by EOD tomorrow Tuesday 24 October so this fix can be included in last 119 beta and early stable
please merge this fix to branch 5993 by EOD Friday, 27 October so this fix can be included in the first 118 Extended Stable release 

### gi...@appspot.gserviceaccount.com (2023-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/b87ce81fcf70c97c12a3f3294f986dac35f79017

commit b87ce81fcf70c97c12a3f3294f986dac35f79017
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Tue Oct 24 14:48:29 2023

[PaymentHandler] Require Link header when fetching payment method manifests

(cherry picked from commit 8eddc1354a929176bdd7514d0f8e55a7aa0d7389)

Bug: 1492698
Change-Id: Ib8213f2826cfb94b8c2c63a4f4b7b5ae3dd26ea9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4954394
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1212234}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4969474
Cr-Commit-Position: refs/branch-heads/6045@{#887}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/payments/core/native_error_strings.cc
[modify] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/payments/core/payment_manifest_downloader.h
[modify] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/payments/core/features.cc
[add] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/test/data/payments/abort_responder_app.json.mock-http-headers
[modify] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/payments/core/native_error_strings.h
[modify] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/chrome/browser/ui/views/payments/payment_request_can_make_payment_metrics_browsertest.cc
[add] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/test/data/payments/app_store_billing_tests/method_manifest.json.mock-http-headers
[add] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/test/data/payments/paulpay.test/pay.mock-http-headers
[modify] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/payments/core/payment_manifest_downloader_unittest.cc
[add] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/test/data/payments/orenpay.test/pay.mock-http-headers
[add] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/test/data/payments/just-in-time/pay.json.mock-http-headers
[add] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/test/data/payments/nickpay.test/pay.mock-http-headers
[add] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/test/data/payments/can_make_payment_event_fields/app/pay.mock-http-headers
[modify] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/payments/core/features.h
[modify] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/payments/core/payment_manifest_downloader.cc
[add] https://crrev.com/b87ce81fcf70c97c12a3f3294f986dac35f79017/components/test/data/payments/redirect/destination/pay.mock-http-headers


### [Deleted User] (2023-10-24)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### gi...@appspot.gserviceaccount.com (2023-10-24)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f536dbec7d08b9cca3076b22f88415fa1eb774b3

commit f536dbec7d08b9cca3076b22f88415fa1eb774b3
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Tue Oct 24 16:18:45 2023

[PaymentHandler] Require Link header when fetching payment method manifests

(cherry picked from commit 8eddc1354a929176bdd7514d0f8e55a7aa0d7389)

Bug: 1492698
Change-Id: Ib8213f2826cfb94b8c2c63a4f4b7b5ae3dd26ea9
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4954394
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Stephen McGruer <smcgruer@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1212234}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4969080
Cr-Commit-Position: refs/branch-heads/5993@{#1417}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/payments/core/native_error_strings.cc
[modify] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/payments/core/payment_manifest_downloader.h
[modify] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/payments/core/features.cc
[add] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/test/data/payments/abort_responder_app.json.mock-http-headers
[modify] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/payments/core/native_error_strings.h
[modify] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/chrome/browser/ui/views/payments/payment_request_can_make_payment_metrics_browsertest.cc
[add] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/test/data/payments/paulpay.test/pay.mock-http-headers
[add] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/test/data/payments/app_store_billing_tests/method_manifest.json.mock-http-headers
[modify] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/payments/core/payment_manifest_downloader_unittest.cc
[add] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/test/data/payments/orenpay.test/pay.mock-http-headers
[add] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/test/data/payments/just-in-time/pay.json.mock-http-headers
[add] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/test/data/payments/nickpay.test/pay.mock-http-headers
[add] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/test/data/payments/can_make_payment_event_fields/app/pay.mock-http-headers
[modify] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/payments/core/features.h
[modify] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/payments/core/payment_manifest_downloader.cc
[add] https://crrev.com/f536dbec7d08b9cca3076b22f88415fa1eb774b3/components/test/data/payments/redirect/destination/pay.mock-http-headers


### am...@google.com (2023-10-26)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-26)

Congratulations Vsevolod! The Chrome VRP Panel has decided to award you $15,000 for this high quality and novel report of a XSS + $1,000 bisect bonus. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your excellent efforts here in discovering this issue and we appreciate you reporting this to us -- great work! 

### se...@gmail.com (2023-10-26)

Thank you very much for the prompt resolution of this issue and the generous reward!

I would like to inquire about the timeline for when this ticket will become public. In this case, the bug can be quickly restored after the fix, and hiding the label will no longer make sense when creating a PR for web standards.

I'm also interested in knowing when the patch will be released for most devices in the stable branch.

(I am curious about the CVE registration process.)

### rz...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### rz...@google.com (2023-10-26)

The fixed method (FallbackToDownloadingResponseBody) doesn't exist in 114

### am...@chromium.org (2023-10-26)

re: https://crbug.com/chromium/1492698#c52,

>>> I would like to inquire about the timeline for when this ticket will become public. 
Security fixes are publicly disclosed automatically 14 weeks after they are fixed. By my rough math that should be on 25 January 2024

>>> In this case, the bug can be quickly restored after the fix, and hiding the label will no longer make sense when creating a PR for web standards.
I'm not sure I'm following regarding the part of "the bug can be quickly restored after the fix" 
We will keep this issue closed until 25 January since the specifics about the bug and how it can be exploited are detailed here. 
We do this so that we can ensure all users are likely to have updated to a version of Chrome with the fix before these details are made public.
A request or PR for a change in web standards can be achieved without details how a specific bug can be exploited in a given software application. 

Perhaps I am not following and you are expressing an intent to disclose? We'd appreciate you letting us know if that is the case.

>>> I'm also interested in knowing when the patch will be released for most devices in the stable branch
This fix was just backmerged to 119 earlier this week. Barring any issues, this fix will be released in the first Stable channel of 119, scheduled for next Tuesday, 31 October: https://chromiumdash.appspot.com/schedule

>>> (I am curious about the CVE registration process.)
A CVE will be issued for this bug at the time of Stable channel release. The CVE will be appended directly on this issue at that time. 




### se...@gmail.com (2023-10-26)

Okay, thank you for the response, I'll be waiting.

### sm...@chromium.org (2023-10-26)

> The fixed method (FallbackToDownloadingResponseBody) doesn't exist in 114

To be clear - the vulnerability *DOES* exist in 114, but there was a refactor between then and now which introduced the particular method where I did the fix. So if we wanted/needed to fix 114, then I would need to develop a new patch specific to that version. Let me know if that's needed (and how to checkout/build LTS!)

### rz...@google.com (2023-10-27)

Thanks smcgruer@,  since it's a high severity bug it would be ideal to have the fix backported the LTS branch. To work on it, you would need to checkout the branch https://chromium.googlesource.com/chromium/src.git/+log/refs/branch-heads/5735. (you need to run a gclient sync --with_branch_heads to update your references)

### sm...@chromium.org (2023-10-27)

> Thanks smcgruer@,  since it's a high severity bug it would be ideal to have the fix backported the LTS branch.

Ack. Have sent out https://chromium-review.googlesource.com/c/chromium/src/+/4985681/ for review.

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### rz...@google.com (2023-10-30)

Thanks for working on this smcgruer@, I will make the merge request for the LTS branch

### [Deleted User] (2023-10-30)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sm...@chromium.org (2023-10-30)

1. Number of CLs needed for this fix and links to them.
1 - https://chromium-review.googlesource.com/c/chromium/src/+/4985681, NOT YET REVIEWED

2. Level of complexity (High, Medium, Low - Explain)

Medium - The change is not dissimilar to the fix in trunk (see below), but it is different and the area of code in question is quite complex and has been the source of significant bugs before. There is however good unit-testing (which was added due to previous bugs!) which likely lowers the risk here.

3. Has this been merged to a stable release? beta release?

No; a similar fix was landed in trunk and merged to both beta and stable, but the patch for LTS is different.

4. Overall Recommendation (Yes, No)

Yes, pending review of the CL (expected to take a few days, primary reviewer is unavailable currently).

### gm...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-30)

@smcgruer Please take al; the time you need to make sure the CL is fully reviewed and tested. 

### pg...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### pg...@google.com (2023-11-01)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-11-02)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/98d48a00cd992c73fe75c7d1d3e044d4a519363b

commit 98d48a00cd992c73fe75c7d1d3e044d4a519363b
Author: Stephen McGruer <smcgruer@chromium.org>
Date: Thu Nov 02 16:24:14 2023

[PaymentHandler] Require Link header when fetching payment method manifests

This is a manual cherry-pick of https://crrev.com/8eddc1354,
modified for the M114 LTS branch.

Bug: 1492698
Change-Id: I21d18d1ef0811d78208276e6ae8d546a9dc10473
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4985681
Reviewed-by: Rouslan Solomakhin <rouslan@chromium.org>
Commit-Queue: Zakhar Voit <voit@google.com>
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1636}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/payments/core/native_error_strings.cc
[modify] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/payments/core/features.cc
[add] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/test/data/payments/abort_responder_app.json.mock-http-headers
[modify] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/payments/core/native_error_strings.h
[modify] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/chrome/browser/ui/views/payments/payment_request_can_make_payment_metrics_browsertest.cc
[add] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/test/data/payments/paulpay.test/pay.mock-http-headers
[add] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/test/data/payments/app_store_billing_tests/method_manifest.json.mock-http-headers
[modify] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/payments/core/payment_manifest_downloader_unittest.cc
[add] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/test/data/payments/orenpay.test/pay.mock-http-headers
[add] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/test/data/payments/just-in-time/pay.json.mock-http-headers
[add] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/test/data/payments/nickpay.test/pay.mock-http-headers
[add] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/test/data/payments/can_make_payment_event_fields/app/pay.mock-http-headers
[modify] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/payments/core/features.h
[modify] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/payments/core/payment_manifest_downloader.cc
[add] https://crrev.com/98d48a00cd992c73fe75c7d1d3e044d4a519363b/components/test/data/payments/redirect/destination/pay.mock-http-headers


### vo...@google.com (2023-11-03)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-25)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-25)

This issue was migrated from crbug.com/chromium/1492698?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

### ap...@google.com (2024-11-22)

Project: chromium/src  

Branch: main  

Author: Stephen McGruer <[smcgruer@chromium.org](mailto:smcgruer@chromium.org)>  

Link:      <https://chromium-review.googlesource.com/6038799>

Remove the kPaymentHandlerRequireLinkHeader feature flag.

---


Expand for full commit details
```
Remove the kPaymentHandlerRequireLinkHeader feature flag. 
 
This flag was added in M120 as a kill-switch, and is now safe to 
remove as the feature has landed safely. 
 
Bug: 40936265 
Change-Id: Id245772f00766f41c7beed3f20eb02aa0c2b73b5 
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6038799 
Reviewed-by: Slobodan Pejic <slobodan@chromium.org> 
Commit-Queue: Stephen McGruer <smcgruer@chromium.org> 
Cr-Commit-Position: refs/heads/main@{#1386830}

```

---

Files:

- M `components/payments/core/features.cc`
- M `components/payments/core/features.h`
- M `components/payments/core/payment_manifest_downloader.cc`
- M `components/payments/core/payment_manifest_downloader.h`
- M `components/payments/core/payment_manifest_downloader_unittest.cc`

---

Hash: 5f6ac908a32261dccd269dd66ca6ed4f0c90fcc6  

Date:  Fri Nov 22 15:27:55 2024


---

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40936265)*
