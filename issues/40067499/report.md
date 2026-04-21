# XSS on Image Loader extension and chrome://resources, abusable by extensions to access private APIs

| Field | Value |
|-------|-------|
| **Issue ID** | [40067499](https://issues.chromium.org/issues/40067499) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Unknown |
| **Platforms** | ChromeOS |
| **Reporter** | ma...@gmail.com |
| **Assignee** | ch...@google.com |
| **Created** | 2023-07-16 |
| **Bounty** | $5,000.00 |

## Description

**Steps to reproduce the problem:**

1. Download the attached extension
2. Observe alert in the Image Loader extension
3. A picture taken from your camera will be written onto chrome://resources

**Problem Description:**  

This is very similar to <https://crbug.com/1464456>, but with different effects.

The "Image Loader" component extension (BLESSED\_EXTENSION) chrome-extension://pmfjbimdmchhbnneeidfognadeopoehp on ChromeOS creates filesystem: URLs with user files. When opened, these filesystem: URLs can load downloaded HTML files in the context of the extension. They can also run downloaded JS files, leading to XSS in the scope of the component extension.

To abuse this, a crafted extension has to:

- Download an HTML and JS file with malicious content
- Find the user hash with chrome.downloads (although there are other ways)
- Use chrome.tabs.create to open a crafted filesystem: URL belonging to the Image Loader extension

```
filesystem:chrome-extension://pmfjbimdmchhbnneeidfognadeopoehp/external/Downloads-8cb5f450b3d4722d4e9463de5f787d80b8f05e9a/xss.html  

```

---

Once XSS is achieved, a lot can be done with this component extension:

- `Mojo` exists
- `chrome.mojoPrivate` exists
- `chrome.fileManagerPrivate` exists [1], exposing 85 functions to create/edit local files
- `chrome.dashboardPrivate` exists
- `chrome.feedbackPrivate` exists

Since the extension also has access to chrome://resources, it can run scripts on that chrome:// domain:

```
chrome.tabs.create({url:"chrome://resources/js/open_window_proxy.js"},tab=>{  
    chrome.tabs.executeScript(tab.id,{code:'alert(origin)'})  
})  

```

With access to a chrome:// URL, multiple sensitive things can be done:

- User camera and microphone can be accessed without asking permission
- Sensitive pages like chrome://prefs-internals can be fetched with XMLHttpRequest
- More Mojo

```
const xhr = new XMLHttpRequest;  
xhr.open("GET", "chrome://prefs-internals", false);  
xhr.send();  
console.log(JSON.parse(xhr.responseText))  

```

And all this can be done within 1 second of installing a crafted extension, with no user interaction at all. An example extension and POC video are attached below.

---

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/common/extensions/api/_permission_features.json;l=354?q=74e2d32a61b08d29521a8c4e360f581de78f5ca5&ss=chromium%2Fchromium%2Fsrc>

**Additional Comments:**  

By the way, chrome-extension://pmfjbimdmchhbnneeidfognadeopoehp/manifest.json (Image Loader) has a CSP typo.

"script-src 'self' 'wasm-eval' blob: filesystem: chrome://resources style-src 'self' blob: filesystem:;"  

should be  

"script-src 'self' 'wasm-eval' blob: filesystem: chrome://resources; style-src 'self' blob: filesystem:;"

\*\*Chrome version: \*\* 117.0.0.0 \*\*Channel: \*\* Not sure

**OS:** Chrome OS

## Attachments

- [image_loader_code_exec_poc.mp4](attachments/image_loader_code_exec_poc.mp4) (video/mp4, 508.6 KB)
- [image_loader_code_exec_extension.zip](attachments/image_loader_code_exec_extension.zip) (application/octet-stream, 1.4 KB)
- [background.js](attachments/background.js) (text/plain, 2.3 KB)
- [manifest.json](attachments/manifest.json) (text/plain, 256 B)
- [background.js](attachments/background.js) (text/plain, 2.3 KB)
- [image_loader_code_exec_extension.zip](attachments/image_loader_code_exec_extension.zip) (application/octet-stream, 1.4 KB)

## Timeline

### [Deleted User] (2023-07-16)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-16)

On second thought, this is a very different bug from https://crbug.com/1464456 because this one's vulnerabilities stem from the filesystem:chrome-extension:// protocol, which has completely different permissions and behavior compared to the filesystem:chrome:// protocol.

### bo...@chromium.org (2023-07-16)

It sounds like this issue may be specific to ChromeOS, so I'm routing to the CrOS sheriff for triage.

### ma...@gmail.com (2023-07-16)

Yes, it is a ChromeOS issue only.

### ch...@google.com (2023-07-17)

Your report will be worked on in the Buganizer system (link: https://issuetracker.google.com/issues/291526810). You have been cc'ed on that report and should have access to it at this time to follow along while it is being worked on. We are setting Security_Severity-High as a default and the priority may either increase or decrease once their report is fully triaged and analyzed

[Monorail blocking: b/291526810]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-17)

[Comment Deleted]

### ma...@gmail.com (2023-07-17)

[Comment Deleted]

### [Deleted User] (2023-07-17)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-07-17)

[Comment Deleted]

### dc...@chromium.org (2023-07-18)

[Empty comment from Monorail migration]

### ch...@google.com (2023-07-18)

Dear all,

Please only use https://issuetracker.google.com/issues/291526810 for comments and updates!



### ma...@gmail.com (2023-07-22)

[Comment Deleted]

### ma...@gmail.com (2023-08-05)

[Comment Deleted]

### ch...@google.com (2023-08-08)

Fix for M117 landed in 117.0.5912.0, which released today into dev channel 117.0.5920.0.  I am planning to wait approx 1 week before merging to M116 (beta) or M115 (stable).

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-08)

[Empty comment from Monorail migration]

### ch...@google.com (2023-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-10)

This bug is a regression and does not impact stable or extended stable.Removing incorrectly added Release- labels.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ma...@gmail.com (2023-08-11)

Hi chmiel@google.com, can you update the original message with the files attached here? (I'm not sure if it's possible to do that) There was a typo breaking some functionalities of the script.

### ma...@gmail.com (2023-08-11)

Also, https://crbug.com/chromium/1465203#c19 is wrong and this bug definitely does affect stable. I may have mistakenly entered it as a regression in the wizard, I'm not sure.

### ma...@gmail.com (2023-08-16)

chmiel@google.com sorry to bother you but this bug is not a regression and the release tag was mistakenly removed by sherrifbot.

### st...@google.com (2023-08-29)

[Empty comment from Monorail migration]

### [Deleted User] (2023-08-30)

Setting Pri-2 to match security severity Low. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ch...@google.com (2023-09-20)

Exploitability: Explain why/why not the bug is reachable and/or exploitable
Extensions can request the browser to load a html file with the url "filesystem:chrome-extension://[extension_id]/external/file", then the html file will be executed in the context of the extension. In particular, the image loader extension, which is used to download, create, and install Chromeos images, has access to private APIs. So exploiting the image loader extension will gain access to some private APIs.

Privileges and Capabilities
filesystem:chrome-extension://[extension_id]/external/file is incorrectly treated as code from chrome-extension://[extension_id].

Origin of fix - Is the issue already known upstream, fixed by work from a previously known or reported issue, provided by the reporter, or any other information that would be relevant toward reward eligibility
The fix is authored by a Google engineer.

Mitigations - Detail any regarding mitigation considerations (we're run across a few comments, such as "we considered this issue to be highly mitigated" without explanation)
The mitigation is to disallow render to load external files pointed by "filesystem:". This is done by https://chromium-review.googlesource.com/c/chromium/src/+/4705137

Severity assessment - why not higher, why not lower
High severity. Why not higher/lower: According to the guideline, this is Critical severity downgraded to High due to requiring user actions to trigger. When exploited, its severity is critical, it allows code injection that can utilize Chrome private APIs that read/write system data, communicate with system processes. The exploit requires a user action to trigger, which is to install a malicious extension.

### am...@chromium.org (2023-09-26)

[Empty comment from Monorail migration]

### ma...@gmail.com (2023-10-04)

https://bugs.chromium.org/p/chromium/issues/detail?id=1464456 got a CVE number. This bug has equal severity so will it get one too?

### ch...@google.com (2023-10-26)

Congratulations! 
The VRP Panel has decided to award you $5000 for this report. 
A member of our finance team will be in touch with you soon to arrange payment. Thank you for your efforts in discovering and reporting this issue to us -- great work! 
Please be mindful that previous reward decisions made by the Chrome VRP should not be considered precedent for potential future ChromeOS VRP reward amounts or decisions.

Can you please tell us your desired credit name? --< e.g.  mathia.is.fun ?

### ma...@gmail.com (2023-10-26)

"Derin Eryilmaz" is what I'd like to go by. Thanks. 

### ma...@gmail.com (2023-10-26)

Also, thanks so much for the reward!

### am...@google.com (2023-10-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-11-14)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-11-14)

This issue was migrated from crbug.com/chromium/1465203?no_tracker_redirect=1

[Monorail blocking: b/291526810]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40067499)*
