# Security: Custom Tab HTTP Header Injection

| Field | Value |
|-------|-------|
| **Issue ID** | [40060115](https://issues.chromium.org/issues/40060115) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>SecurityFeature>CORS |
| **Platforms** | Android |
| **Reporter** | ph...@gmail.com |
| **Assignee** | ph...@chromium.org |
| **Created** | 2022-06-30 |
| **Bounty** | $3,000.00 |

## Description

**VULNERABILITY DETAILS**

## Overview

Google Chrome Custom Tab only allows adding CORS whitelisted HTTP headers to Custom Tab requests when the relationship between the website, which is opened in the Custom Tab, and the application that embeds the Custom Tab, is proven by a Digital Asset Link. Adding whitelisted CORS headers can be achieved by using the following code in the Android application:

```
val headers = Bundle()  
headers.putString(<header-key>, <header-value>)  
intent.putExtra(Browser.EXTRA_HEADERS, headers)  

```

Due to missing sanitisation in Google Chrome, it is possible to add non-whitelisted HTTP headers to Custom Tab-initiated requests, even when the relationship between the website and the application is not proven, thus bypassing Digital Asset Link verification.  

The non-whitelisted `Cookie` header, as an example, can be added as follows:

```
val headers = Bundle()  
headers.putString("sec-fetch-ua-full", "\nCookie: secret=cookie")  
intent.putExtra(Browser.EXTRA_HEADERS, headers)  

```

In this example, the `sec-fetch-ua-full` header is used to carry another header as its value.  

By providing the newline character `\n` in the header value, followed by the header to add, an attacker can add non-whitelisted headers to requests.

Apart from the `sec-fetch-ua-full` header, the following headers also do not perform proper sanitisation and can thus be used to inject other headers:

- `intervention`
- `sec-ch-viewport-height`
- `sec-ch-ua`
- `sec-ch-ua-platform`
- `sec-ch-ua-arch`
- `sec-ch-ua-model`
- `sec-ch-ua-mobile`
- `sec-ch-ua-full-version`
- `sec-ch-ua-platform-version`
- `sec-ch-ua-bitness`
- `sec-ch-ua-reduced`
- `sec-ch-prefers-color-scheme`
- `sec-ch-device-memory`
- `sec-ch-dpr`
- `sec-ch-width`
- `sec-ch-ua-full-version-list`
- `sec-ch-ua-wow64`

## Security Implications

Allowing an entity that operates an application which uses Custom Tabs to inject non-whitelisted CORS HTTP request headers on third-party origins can have unforseen consequences. This is primarly due to the fact that Custom Tabs share state with the underlying browser, i.e., browsing data is shared between the Custom Tab and Chrome. Injection of non-whitelisted CORS headers on arbitrary requests initiated by a Custom Tab enables, among others, the capabilites listed below. As a threat model, we assume a malicious application installed on a user's device that uses Custom Tabs. The injection of request headers can be combined with the attack described in [https://crbug.com/chromium/1235142](https://bugs.chromium.org/p/chromium/issues/detail?id=1235142), which allows a malicious application to stealthily launch a target website in a Custom Tab in the background. Issuing a request in a Custom Tab with additional non-whitelisted CORS headers can thus be performed fully stealthily.

1. Session instantiation/swapping  
   
   A maliciouis entity can set the `Cookie` header to log the victim in on a benign website. By setting the cookies of a session on the benign website of the malicious entity in the Custom Tab request, the malicious entity can log in the victim into the malicious entity's account. This is similar to the Login CSRF attack proposed by [Barth et al.](https://doi.org/10.1145/1455770.1455782). User activities are then performed on behalf of the attacker, e.g. the user enters her credit card details on the legitimate website opened in the Custom Tab, but is signed in with the attackers account. In this way, the attacker gains knowledge of the user's credit card details. (also see \*limitations\*)

Similarly, also the `Authorization` header can be abused for session swapping. If a website uses a bearer token issued by an identity provider to set a session cookie to establish the session associated with the token, and this process is done using a `GET` request, a malicious entity can set her token in the request's `Authorization` header to instantiate the session.

2. Origin Spoofing  
   
   A malicious entity can add the `Origin` header and spoof another site's origin. This can be used for CSRF attacks on websites that check the Origin of the request for CSRF mitigation, as further described below.
3. Cross-Site Request Forgery  
   
   The `X-HTTP-Method`, `X-HTTP-Method-Override` and `X-Method-Override` request headers are non-standard HTTP headers that are used to declare the request to use a different HTTP method than the original request's method. As an example, a `GET` request containing the `X-HTTP-Method: POST` header is actually treated as a `POST` request, if the server/middleware supports the header.  
   
   Attackers can issue a `GET` request in a Custom Tab and set the method override header to indicate that the `GET` request should be treated as another request method, e.g. as a `POST` or `DELETE` request. An attacker can use this technique to make state-changing requests on the victims behalf, possibly logging users in/out or issuing orders on e-commerce websites, assuming that protection against CSRF attacks is enforced by Origin checking (see \*Origin Spoofing\*), SameSite cookies (see [https://crbug.com/chromium/1334240](https://bugs.chromium.org/p/chromium/issues/detail?id=1334240)) or custom headers.  
   
   These headers are also used in practice. [Nguyen et al.](https://doi.org/10.1145/3319535.3354215) show that using such headers in `GET` requests to perform other request methods is possible in at least the Flask and Play 1 frameworks. [Likaj et al.](https://doi.org/10.1145/3471621.3471846) also perform an analyis of the header support in web frameworks.

## Limitations

The following headers \*cannot\* be added by using the described approach:

- `Content-Length`
- `Host`
- `Trailer`
- `TE`
- `Upgrade`
- `Cookie2`
- `Keep-Alive`
- `Transfer-Encoding`
- Headers that start with `Proxy`

Furthermore, if values already exist for the following (\*non-exhaustive\*) list of headers, they are not changed by using the approach:

- `Cookie` (i.e., if Chrome adds cookies for the request, the manually added cookies are overwritten by Chrome)
- `Referer`
- `Sec-Fetch-Mode`
- `Sec-Fetch-User`
- `Sec-Fetch-Dest`
- `Sec-Fetch-Site`

Since the CORS whitelisted request headers, which value is used to inject another header, can only contain values with a length of <= 128, the additionally injected headers can only contain <= 127 characters. This is because the newline character `\n` already takes up 1 character.

## Suggested Mitigation

The vulnerability is due to a missing validation in the [`IsCorsSafelistedHeader`](https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/cors/cors.cc;drc=4dafa607c24d6ec8f7c0a9400815ef9c33e2ddc2;bpv=1;bpt=1;l=282?gsn=IsCorsSafelistedHeader&gs=kythe%3A%2F%2Fchromium.googlesource.com%2Fchromium%2Fsrc%3Flang%3Dc%252B%252B%3Fpath%3Dservices%2Fnetwork%2Fpublic%2Fcpp%2Fcors%2Fcors.h%23c-1hHWn8zEOuJkMjoJQNdi0vl0zziMuim7e9aXy38Rw&gs=kythe%3A%2F%2Fchromium.googlesource.com%2Fchromium%2Fsrc%3Flang%3Dc%252B%252B%3Fpath%3Dservices%2Fnetwork%2Fpublic%2Fcpp%2Fcors%2Fcors.cc%23C1QyemnQe-I0zUEQktPMQE5hMK9O0o4gi6EgDpUxH6A) method in the `cors.cc` file.

There is no proper sanitisation of the value for the above listed HTTP headers. The vulnerability can be mitigated by adding a sanitisation for the values of these methods, i.e. checking if the value contains the newline character `\n` and if so, not allow adding the corresponding header.

**VERSION**  

Chrome Version: 102.0.5005.125 stable  

Operating System: Android 12

**REPRODUCTION CASE**  

The source code of the proof of concept application can be found at <https://gitfront.io/r/user-7458426/ttncDoVYkJth/custom-tab-headers-poc/>.  

On start of the application, one can define the URL that the application launches in the Custom Tab, as well as one HTTP header-value pair that is added to the request. Note that the attack is not limited to specifying only one HTTP header.

**CREDIT INFORMATION**  

Reporter credit: Philipp Beer (TU Wien)

## Timeline

### [Deleted User] (2022-06-30)

[Empty comment from Monorail migration]

### ca...@chromium.org (2022-06-30)

Thanks for all the details. Passing to peconn for further triage.

peconn: Can you PTAL? Feel free to reassign as appropriate

[Monorail components: UI>Browser>Mobile>CustomTabs]

### [Deleted User] (2022-06-30)

[Empty comment from Monorail migration]

### pe...@chromium.org (2022-07-01)

Yeah, it seems to be (from my PoV) an oversight that `network::cors::IsCorsSafelistedHeader` doesn't check whether or not the value contains a newline.

I'm going to set the component to Blink>SecurityFeatures>CORS, and because I'm not 100% sure on the visibility restrictions for Restrict-View-SecurityTeam, I'm going to assign this bug to clamy@ who can hopefully direct it further.

[Monorail components: -UI>Browser>Mobile>CustomTabs Blink>SecurityFeature>CORS]

### [Deleted User] (2022-07-01)

Setting milestone and target because of medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-01)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2022-07-14)

clamy: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### cl...@chromium.org (2022-07-20)

@phao: could you take a look at this bug?

### ph...@chromium.org (2022-07-20)

[Empty comment from Monorail migration]

### ph...@chromium.org (2022-07-21)

CL in review https://chromium-review.googlesource.com/c/chromium/src/+/3776721

### yh...@chromium.org (2022-07-22)

```
val headers = Bundle()
headers.putString("sec-fetch-ua-full", "\nCookie: secret=cookie")
intent.putExtra(Browser.EXTRA_HEADERS, headers)
```

I think allowing the second line is problematic. For example, the fetch API rejects such headers.

```js
const r = new Request('/', {headers: {'foo': 'bar\nCookie: hoo'}});
```

This is rejected, as specified at [1] and [2]. Trigerring a CORS preflight is not the right solution I believe.

1: https://fetch.spec.whatwg.org/#concept-headers-append
2: https://fetch.spec.whatwg.org/#header-value

### ph...@chromium.org (2022-07-22)

Hi yhirano@

```
val headers = Bundle()
headers.putString("sec-fetch-ua-full", "\nCookie: secret=cookie")
intent.putExtra(Browser.EXTRA_HEADERS, headers)
```

I'm not sure if there's anything we can do with chromium about the second line because that seems to be Android app API.
Is there anything we can do in chromium to make sure that we reject newlines from the headers that the Android custom tab try to add?

### yh...@chromium.org (2022-07-25)

How about adding a check for header values in CorsURLLoaderFactory::IsValidRequest[1]?

1: https://source.chromium.org/chromium/chromium/src/+/main:services/network/cors/cors_url_loader_factory.cc;l=351

### ph...@chromium.org (2022-07-25)

This CL https://chromium-review.googlesource.com/c/chromium/src/+/3783023 adds a check to IsRequestHeaderSafe which in turn used by AreRequestHeadersSafe[1] and should make CorsURLLoaderFactory::IsValidRequest return false [2]. 

However, I found that HttpRequestHeaders::SetHeader has a CHECK that makes sure the header value is value, so not sure whether my CL is really necessary.

[1] https://source.chromium.org/chromium/chromium/src/+/main:services/network/public/cpp/header_util.cc;l=104;drc=8adc9cb73b65f12d089dabbad06a9fb7446e478f
[2] https://source.chromium.org/chromium/chromium/src/+/main:services/network/cors/cors_url_loader_factory.cc;l=512
[3] https://source.chromium.org/chromium/chromium/src/+/main:net/http/http_request_headers.cc;l=127;drc=8adc9cb73b65f12d089dabbad06a9fb7446e478f;bpv=1;bpt=1

### yh...@chromium.org (2022-07-27)

> https://crbug.com/chromium/1340879#c14

Have you reproduced the issue? According to https://crbug.com/chromium/1340879#c14 it sounds like the issue cannot be reproducible so I'm confused.

### ph...@chromium.org (2022-07-27)

I haven't been able to reproduce it because of the necessary Android environment.  I'll get back when I can reproduce the issue.

### ph...@chromium.org (2022-08-05)

I run the PoC app in an emulator and added debug messages in chromium.  I was able to reproduce the bug.

It seems that when the app tries to add an extra header by 
```
val headers = Bundle()
headers.putString("sec-fetch-ua-full", "\nCookie: secret=cookie")
intent.putExtra(Browser.EXTRA_HEADERS, headers)
```

The intent handler will begin with calling IsCorsSafelistedHeader with name = "sec-fetch-ua-full" and value = "\nCookie: secret=cookie" [1].
Our only chance in chromium is to validate the value and return false here.   If we return false here, instead of triggering a preflight, this extra header will be ignored by the intent handler.

If we return true here, allowing this header,  the app will load the URL by calling NavigationControllerAndroid::LoadUrl [2] with an extra_headers string concatenated from the name and value above, i.e. "sec-fetch-ua-full\nCookie: secret=cookie" .  At this point, chromium is not able to distinguish it from a legitimately constructed header because it looks exactly the same as two valid headers.  HttpRequestHeaders::AddHeadersFromString [3] will just split it by new line and add each header separately, so no more checks can tell that it was injected.

Therefore, I think on the chromium side, the best we can do is what I did in this CL https://chromium-review.googlesource.com/c/chromium/src/+/3776721, invalidating header values with new line characters in IsCorsSafelistedHeader.  I will restore this CL.

[1]: https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/android/intent_handler.cc;l=22;drc=06060773a35b1c48704f507c1c207afc4b161974
[2] https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_controller_android.cc;l=237;drc=8adc9cb73b65f12d089dabbad06a9fb7446e478f
[3] https://source.chromium.org/chromium/chromium/src/+/main:net/http/http_request_headers.cc;l=190-192

### yh...@chromium.org (2022-08-08)

Thank you for the investigation. I think I understand the situation.

JNI_IntentHandler_IsCorsSafelistedHeader is called by getExtraHeadersFromIntent in chrome/android/java/src/org/chromium/chrome/browser/IntentHandler.java [1](via JNI).

The code is here.

```
for (String key : bundleExtraHeaders.keySet()) {
    String value = bundleExtraHeaders.getString(key);

    if (!HttpUtil.isAllowedHeader(key, value)) {
        Log.w(TAG, "Ignoring forbidden header " + key + " in EXTRA_HEADERS.");
        // (A)
    }

    ...
    if (!fromChrome) {
        ...
        if (!shouldAllowNonSafelistedHeaders
            && !IntentHandlerJni.get().isCorsSafelistedHeader(key, value)) {
            Log.w(TAG, "Ignoring non-CORS-safelisted header " + key + " in EXTRA_HEADERS.");
            continue;
        }
    }

    if (extraHeaders.length() != 0) extraHeaders.append("\n");
    extraHeaders.append(key);
    extraHeaders.append(": ");
    extraHeaders.append(value);
}
```

We run HttpUtil.isAllowedHeader which returns false for a header value containing newline, but we do nothing other than printing a warning.
Rhe right fix is ignore the value at (A) rather than adding the logic in network::cors::IsCorsSafelistedHeader.

1: https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/IntentHandler.java;l=856

### ph...@chromium.org (2022-08-08)

Thanks Yutaka.  That makes sense.  I've tried to do it myself and add a `continue` statement in https://chromium-review.googlesource.com/c/chromium/src/+/3816064 but it breaks a lot of tests, so the fix may not be that straightforward.  Since the fix should be in the IntentHandler, I'll assign this back to Peter to find a better owner.

### pe...@chromium.org (2022-08-23)

Hey jochen@ in [1], we changed:

    if (!HttpUtil.isAllowedHeader(key, value)) continue;

To:

            if (!HttpUtil.isAllowedHeader(key, value)) {
                Log.w(TAG, "Ignoring forbidden header " + key + "in EXTRA_HEADERS.");
            }

Do you remember why that was done? It seems the `continue` should have been left in, but adding it now breaks tests (in the comment above).

[1]: https://chromium-review.googlesource.com/c/chromium/src/+/2252143
    

### pe...@chromium.org (2022-09-15)

[Empty comment from Monorail migration]

### jo...@chromium.org (2022-09-16)

I don't think the continue statement was removed intentionally. 

Are you sure it actually breaks tests? It looks like on the one builder, for whatever reason some shards weren't executing any tests (all failures are unexpectedly skipped)? 

### jo...@chromium.org (2022-09-16)

I tried the bots again, and they're green. phao@ can you get the CL reviewed and land it plz?

### ph...@google.com (2022-09-20)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2022-09-20)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/e4a83c4363411824307834cbe19cf5f31615aae9

commit e4a83c4363411824307834cbe19cf5f31615aae9
Author: Jonathan Hao <phao@chromium.org>
Date: Tue Sep 20 16:18:19 2022

Ignore forbidden extra header in IntentHandler

The `continue` statement was unintentionally removed.  Adding it back in
this CL so that we do ignore forbidden headers.

Bug: 1340879
Change-Id: I4757e2bafa42840f544d22c4a59faee8d5afb3e7
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/3816064
Auto-Submit: Jonathan Hao <phao@chromium.org>
Reviewed-by: Michael Thiessen <mthiesse@chromium.org>
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1049141}

[modify] https://crrev.com/e4a83c4363411824307834cbe19cf5f31615aae9/chrome/android/java/src/org/chromium/chrome/browser/IntentHandler.java
[modify] https://crrev.com/e4a83c4363411824307834cbe19cf5f31615aae9/chrome/android/javatests/src/org/chromium/chrome/browser/IntentHandlerUnitTest.java


### ph...@chromium.org (2022-09-26)

[Empty comment from Monorail migration]

### ph...@gmail.com (2022-09-26)

Hello, does this bug qualify for the bug bounty program?

### [Deleted User] (2022-09-26)

[Empty comment from Monorail migration]

### [Deleted User] (2022-09-26)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-09-28)

Hello, (in ref to https://crbug.com/chromium/1340879#c27) now that this issue is fixed the bot has applied the reward-topanel label, which means it will be evaluated for a potential VRP reward at a future VRP panel session. As it was just updated as fixed a day ago, it was not included in this week's VRP panel, but will be discussed at a future panel. 

### am...@google.com (2022-10-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2022-10-14)

Congratulations, Tu Wien! The VRP Panel has decided to award you $3,000 for this report. A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in finding and reporting this issue to us! 

### am...@google.com (2022-10-14)

[Empty comment from Monorail migration]

### am...@chromium.org (2022-11-28)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### pg...@google.com (2022-11-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-01-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1340879?no_tracker_redirect=1

[Monorail mergedwith: crbug.com/chromium/1120257]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40060115)*
