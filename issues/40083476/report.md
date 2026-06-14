# UX and Extensions API confusion when file: URLs have hostnames

| Field | Value |
|-------|-------|
| **Issue ID** | [40083476](https://issues.chromium.org/issues/40083476) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Blink>DOM, Platform>Extensions>API |
| **Reporter** | an...@gmail.com |
| **Assignee** | pa...@chromium.org |
| **Created** | 2015-12-30 |
| **Bounty** | $500.00 |

## Description

UserAgent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36

Steps to reproduce the problem:
1. Save the attached html (chrome.html) in your hard disk 
For the record the html looks like

<h1>Hi</h1>
<script> alert(document.domain)</script>

2. now supposing the file is saved under (in MacOS) /Users/xxx/Downloads/chrome.html open the file from hard disk in this way 

file://mail.google.com/Users/xxx/Downloads/chrome.html

mail.google.com is arbitrary . This can be any domain (hence is universal)

3. Observe the document.domain alerted is mail.google.com !!! (see alert.jpg)

4. observe the cookies transported are the one associated with *.google.com domain !! (cookie.jpg)

What is the expected behavior?
document.domain is null

What went wrong?
document.domain is set by the attacker !!

Did this work before? N/A 

Chrome version: 47.0.2526.106  Channel: stable
OS Version: OS X 10.9.5
Flash Version: Shockwave Flash 20.0 r0

## Attachments

- [alert.png](attachments/alert.png) (image/png, 83.6 KB)
- [chrome.html](attachments/chrome.html) (text/html, 54 B)
- [cookie.png](attachments/cookie.png) (image/png, 231.3 KB)
- [file-problem-2.png](attachments/file-problem-2.png) (image/png, 55.8 KB)
- [file-problem.png](attachments/file-problem.png) (image/png, 34.7 KB)

## Timeline

### mb...@chromium.org (2015-12-31)

Thanks for the report. I've been able to reproduce this.

### cl...@chromium.org (2016-01-04)

[Empty comment from Monorail migration]

### np...@chromium.org (2016-01-06)

palmer -- Can you take a look at this, or find an appropriate owner?  I suspect we should be dropping the domain from file:// URLs.

### pa...@chromium.org (2016-01-06)

Hmm, there is something odd going on. I have created an attack page like so:
<iframe src="https://example.com/" id="goat"></iframe>

<script>
var goat = document.getElementById("goat")
console.log("domain: " + document.domain)
console.log("cookie: " + document.cookie)
console.log("iframe document: " + goat.contentWindow.document)
</script>

(load this as file://example.com/home/you/Downloads/test.html)

Although document.domain is that of another origin, I get the following output in the console: (see screenshot)

If you swap "example.com" in the attack page and in the URL to a domain with cookies (e.g. accounts.google.com), you do get to see cookies in the Origin Info Bubble, but document.cookie is still empty. (See 2nd screenshot)

So, Chrome's UI, and Chrome's Extensions API, are showing/providing cookies for the named domain. But JavaScript can't get at them, and script in the attack page cannot actually control the other origin. So I'm not quite sure how much of an open-web vulnerability this really is? (Even though it's definitely wrong behavior, and exposes too much to extensions!)

Hostnames are a legitimate part of file: URLs (weird, but true); instead of removing them, I think we should make sure JavaScript gets null for document.domain in a file: origin, and that the UX and Extensions API also see null (and hence act accordingly). However, I am not sure if I am the best person to do that.

+jochen for JavaScript/DOM bindings
+meacer for Extension APIs

### pa...@chromium.org (2016-01-06)

Sigh, forgot the 1st screenshot.

### jo...@chromium.org (2016-01-07)

[Empty comment from Monorail migration]

### mk...@chromium.org (2016-01-07)

As Chris notes, this doesn't sound like a UXSS. The `file:` URL has a unique origin, and doesn't gain access to things that it frames, nor does it gain access to cookies on the hostname it asserts, nor are cookies transmitted over the wire as no network connection is actually made. As Chris also noted, hostnames are indeed part of `file:` URLs. I wouldn't mind removing that (unused?) part of the platform, honestly, but it's not clear that we're vulnerable because of it.

antonio.sanso@: Is there any JavaScript-side vulnerability you've discovered that we're missing here? If not, then I don't think this is actually a bug.

### pa...@chromium.org (2016-01-07)

Re: #7: There are definitely bugs here, even if not *vulnerabilities*. I really don't think the UX or Extensions API should be showing/providing cookies for the named host. So we at least would need to fix that.

### dc...@chromium.org (2016-01-07)

This is almost certainly due to the fact that stuff outside of WebKit uses GURL::GetOrigin() to get the security origin. It looks like the implementation just clears the path and several other fields, and returns the result: for a file:// URL, this will (incorrectly) leave the `domain'.

### pa...@chromium.org (2016-01-07)

Wow, it looks like a lot of stuff needs to change from url->GetOrigin to Origin(url).

/ssd/chromium/src $ search -n '\.cc$' -C 'GetOrigin\(' extensions/ -v                                                                                             
extensions/common/url_pattern_set.cc:155:  DCHECK_EQ(origin.GetOrigin(), origin);
extensions/common/url_pattern_set.cc:158:  if (origin_pattern.Parse(origin.GetOrigin().spec()) !=
extensions/common/url_pattern_set.cc
extensions/browser/guest_view/extension_options/extension_options_guest.cc:234:    if (params.url.GetOrigin() != options_page_.GetOrigin()) {
extensions/browser/guest_view/extension_options/extension_options_guest.cc
extensions/browser/guest_view/extension_view/extension_view_guest.cc:49:      (url.GetOrigin() != extension_url_.GetOrigin());
extensions/browser/guest_view/extension_view/extension_view_guest.cc:138:  if (attached() && (params.url.GetOrigin() != url_.GetOrigin())) {
extensions/browser/guest_view/extension_view/extension_view_guest.cc
extensions/browser/api/web_request/web_request_permissions.cc:133:             url.GetOrigin() == extension->url()))) {
extensions/browser/api/web_request/web_request_permissions.cc
extensions/components/javascript_dialog_extensions_client/javascript_dialog_extension_client_impl.cc:66:        web_contents->GetLastCommittedURL().GetOrigin() == origin_url) {
extensions/components/javascript_dialog_extensions_client/javascript_dialog_extension_client_impl.cc
extensions/renderer/programmatic_script_injector.cc:135:            effective_url_.GetOrigin().spec());
extensions/renderer/programmatic_script_injector.cc
extensions/renderer/file_system_natives.cc:45:  std::string name(storage::GetIsolatedFileSystemName(context_url.GetOrigin(),
extensions/renderer/file_system_natives.cc:57:      context_url.GetOrigin(), file_system_id, optional_root_name));
extensions/renderer/file_system_natives.cc

Many more if you search in chrome/browser/ui.

Who wants to help refactor these? :)

### dc...@chromium.org (2016-01-07)

+some other site isolation folks

I don't think we make any security decisions based on GURL::GetOrigin(), even for OOPI, but I'm pretty sure we want this to work and not be subtly incorrect.

(Also, given the Blink-Chrome repo merge, maybe we should consider merging KURL and GURL? And maybe reconsider merging SecurityOrigin stuff too...)

### pa...@chromium.org (2016-01-07)

Some CLs in progress:

https://codereview.chromium.org/1569963002
https://codereview.chromium.org/1567173002/

### pa...@chromium.org (2016-01-07)

Updating to Severity: Low since, AFAICT, the worst problem would be if the person had a malicious extension installed and the cookies leaked to that extension when the browser navigated to a file: URL with a hostname matching that of a domain with cookies. That would indeed be bad, but takes this bug out of the "available to all open-web attackers".

Leaving as Pri-1 though, since the code cleanup job looks to be important. And keep an eye open for new vulnerability scenarios as we do that cleanup (and then re-raise the severity of this bug if necessary).

### bu...@chromium.org (2016-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/58cb65370efa360e924ca222af05c3bef09e168c

commit 58cb65370efa360e924ca222af05c3bef09e168c
Author: palmer <palmer@chromium.org>
Date: Mon Jan 11 19:46:47 2016

Make the Permission Bubble Manager use a correct same-origin check.

GURL::GetOrigin does not do the right thing for all types of URLs.

BUG=573317

Review URL: https://codereview.chromium.org/1569963002

Cr-Commit-Position: refs/heads/master@{#368641}

[modify] http://crrev.com/58cb65370efa360e924ca222af05c3bef09e168c/chrome/browser/ui/website_settings/permission_bubble_manager.cc


### bu...@chromium.org (2016-01-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/a6acbbcaccdb4085f17d0eef1f266d48fa4baff0

commit a6acbbcaccdb4085f17d0eef1f266d48fa4baff0
Author: palmer <palmer@chromium.org>
Date: Mon Jan 11 21:40:39 2016

Show cookies only for HTTP and HTTPS URLs.

Formerly, we would show cookies even if the hostname a file: URL matched a
domain for which there are cookies.

BUG=573317

Review URL: https://codereview.chromium.org/1567173002

Cr-Commit-Position: refs/heads/master@{#368676}

[modify] http://crrev.com/a6acbbcaccdb4085f17d0eef1f266d48fa4baff0/chrome/browser/browsing_data/cookies_tree_model.cc
[modify] http://crrev.com/a6acbbcaccdb4085f17d0eef1f266d48fa4baff0/chrome/browser/browsing_data/cookies_tree_model_unittest.cc
[modify] http://crrev.com/a6acbbcaccdb4085f17d0eef1f266d48fa4baff0/chrome/browser/content_settings/local_shared_objects_container.cc


### me...@chromium.org (2016-01-19)

[Empty comment from Monorail migration]

### ha...@google.com (2016-01-22)

[Empty comment from Monorail migration]

### pa...@chromium.org (2016-02-03)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-03)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5c437bcc7a51edbef45242c5173cf7871fde2866

commit 5c437bcc7a51edbef45242c5173cf7871fde2866
Author: palmer <palmer@chromium.org>
Date: Wed Feb 03 23:21:36 2016

Make extensions use a correct same-origin check.

GURL::GetOrigin does not do the right thing for all types of URLs.

BUG=573317

Review URL: https://codereview.chromium.org/1658913002

Cr-Commit-Position: refs/heads/master@{#373381}

[modify] http://crrev.com/5c437bcc7a51edbef45242c5173cf7871fde2866/extensions/browser/api/web_request/web_request_permissions.cc
[modify] http://crrev.com/5c437bcc7a51edbef45242c5173cf7871fde2866/extensions/browser/guest_view/extension_options/extension_options_guest.cc
[modify] http://crrev.com/5c437bcc7a51edbef45242c5173cf7871fde2866/extensions/browser/guest_view/extension_view/extension_view_guest.cc
[modify] http://crrev.com/5c437bcc7a51edbef45242c5173cf7871fde2866/extensions/common/url_pattern_set.cc
[modify] http://crrev.com/5c437bcc7a51edbef45242c5173cf7871fde2866/extensions/components/javascript_dialog_extensions_client/javascript_dialog_extension_client_impl.cc
[modify] http://crrev.com/5c437bcc7a51edbef45242c5173cf7871fde2866/extensions/renderer/file_system_natives.cc
[modify] http://crrev.com/5c437bcc7a51edbef45242c5173cf7871fde2866/extensions/renderer/programmatic_script_injector.cc
[modify] http://crrev.com/5c437bcc7a51edbef45242c5173cf7871fde2866/url/origin.cc
[modify] http://crrev.com/5c437bcc7a51edbef45242c5173cf7871fde2866/url/origin.h


### pa...@chromium.org (2016-02-03)

AFAICT, this bug is fixed for the Cookie and Extension cases. Please re-open if not.

### cl...@chromium.org (2016-02-04)

[Empty comment from Monorail migration]

### ti...@google.com (2016-02-24)

Low severity bugs roll in off trunk - this will land on stable channel with M50.

### bu...@chromium.org (2016-04-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/8e4a0b36ac3989db1afb69dff442fdc85af047da

commit 8e4a0b36ac3989db1afb69dff442fdc85af047da
Author: battre <battre@chromium.org>
Date: Tue Apr 12 15:49:42 2016

Unhide "Zombie-cookies".

Some cookies would not show up in chrome://settings/cookies or
the site info dialog because the source_ in the CanonicalCookie
is not persisted beyond browser restarts.
https://crrev.com/a6acbbcaccdb4085f17d0eef1f266d48fa4baff0 created
a filter to allow only access to HTTP or HTTPS cookies. This CL
moves the filtering logic a few lines behind a fall back path.

R=msramek@chromium.org,palmer@chromium.org,markusheintz@chromium.org
BUG=573317,601582

Review URL: https://codereview.chromium.org/1870973002

Cr-Commit-Position: refs/heads/master@{#386695}

[modify] https://crrev.com/8e4a0b36ac3989db1afb69dff442fdc85af047da/chrome/browser/browsing_data/cookies_tree_model.cc
[modify] https://crrev.com/8e4a0b36ac3989db1afb69dff442fdc85af047da/chrome/browser/browsing_data/cookies_tree_model_unittest.cc


### mb...@chromium.org (2016-04-12)

[Empty comment from Monorail migration]

### mb...@chromium.org (2016-04-12)

Thanks for the report. How would you like to be credited when we mention this in Chrome's release notes?

### an...@gmail.com (2016-04-12)

hi there,

thanks a lot to you.
If possible it would be nice to credit as:

Antonio Sanso (@asanso) of Adobe

### mb...@chromium.org (2016-04-13)

Thanks again for the report! This one qualified for a $500 reward.

### bu...@chromium.org (2016-04-15)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/44959317e61b85de3c25fdb066cbd8481871f637

commit 44959317e61b85de3c25fdb066cbd8481871f637
Author: Dominic Battre <battre@chromium.org>
Date: Fri Apr 15 07:32:20 2016

Unhide "Zombie-cookies".

Some cookies would not show up in chrome://settings/cookies or
the site info dialog because the source_ in the CanonicalCookie
is not persisted beyond browser restarts.
https://crrev.com/a6acbbcaccdb4085f17d0eef1f266d48fa4baff0 created
a filter to allow only access to HTTP or HTTPS cookies. This CL
moves the filtering logic a few lines behind a fall back path.

R=msramek@chromium.org,palmer@chromium.org,markusheintz@chromium.org
BUG=573317,601582

Review URL: https://codereview.chromium.org/1870973002

Cr-Commit-Position: refs/heads/master@{#386695}
(cherry picked from commit 8e4a0b36ac3989db1afb69dff442fdc85af047da)

Review URL: https://codereview.chromium.org/1891153002 .

Cr-Commit-Position: refs/branch-heads/2704@{#69}
Cr-Branched-From: 6e53600def8f60d8c632fadc70d7c1939ccea347-refs/heads/master@{#386251}

[modify] https://crrev.com/44959317e61b85de3c25fdb066cbd8481871f637/chrome/browser/browsing_data/cookies_tree_model.cc
[modify] https://crrev.com/44959317e61b85de3c25fdb066cbd8481871f637/chrome/browser/browsing_data/cookies_tree_model_unittest.cc


### ti...@google.com (2016-04-23)

Our finance team should reach out within 7 days to collect payment details. If that doesn't happen, please email me at timwillis@ or update this bug.

Thanks again for your report!

### bu...@chromium.org (2016-05-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/b7c0ea69b403ef18e1381c3c78b5a9aea336aa70

commit b7c0ea69b403ef18e1381c3c78b5a9aea336aa70
Author: Dominic Battre <battre@chromium.org>
Date: Fri May 06 19:26:55 2016

Unhide "Zombie-cookies".

Some cookies would not show up in chrome://settings/cookies or
the site info dialog because the source_ in the CanonicalCookie
is not persisted beyond browser restarts.
https://crrev.com/a6acbbcaccdb4085f17d0eef1f266d48fa4baff0 created
a filter to allow only access to HTTP or HTTPS cookies. This CL
moves the filtering logic a few lines behind a fall back path.

R=msramek@chromium.org,palmer@chromium.org,markusheintz@chromium.org
BUG=573317,601582

Review URL: https://codereview.chromium.org/1870973002

Cr-Commit-Position: refs/heads/master@{#386695}
(cherry picked from commit 8e4a0b36ac3989db1afb69dff442fdc85af047da)

Review URL: https://codereview.chromium.org/1947933006 .

Cr-Commit-Position: refs/branch-heads/2661@{#664}
Cr-Branched-From: ef6f6ae5e4c96622286b563658d5cd62a6cf1197-refs/heads/master@{#378081}

[modify] https://crrev.com/b7c0ea69b403ef18e1381c3c78b5a9aea336aa70/chrome/browser/browsing_data/cookies_tree_model.cc
[modify] https://crrev.com/b7c0ea69b403ef18e1381c3c78b5a9aea336aa70/chrome/browser/browsing_data/cookies_tree_model_unittest.cc


### sh...@chromium.org (2016-05-12)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/573317?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>DOM, Platform>Extensions>API]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083476)*
