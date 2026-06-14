# Directory traversal on file:// via escaped slashes

| Field | Value |
|-------|-------|
| **Issue ID** | [40083682](https://issues.chromium.org/issues/40083682) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals>Network |
| **Platforms** | Android, ChromeOS |
| **Reporter** | ja...@googlemail.com |
| **Assignee** | mm...@chromium.org |
| **Created** | 2016-02-12 |
| **Bounty** | $500.00 |

## Description

Steps to reproduce the problem:
On Android, in the Chrome browser, navigate to <file:///sdcard/..%2f..%2f../data/data/com.android.chrome/app_chrome/Default/>.

What is the expected behavior?
The request should either fail because a slash can't be part of a directory or file name or be blocked by ChromeNetworkDelegate::OnCanAccessFile() because the resolved path is outside /sdcard and /mnt/sdcard.

What went wrong?
The request succeeds and a file listing is shown.

FileProtocolHandler::MaybeCreateJob() first calls FileURLToFilePath(), which decodes the encoded slashes (%2f) using UnescapeURLComponent() and collapses consecutive slashes, but doesn't normalize the path or check it for directory traversal again. FileProtocolHandler::MaybeCreateJob() then performs the path whitelisting check using network_delegate->CanAccessFile(), which calls ChromeNetworkDelegate::OnCanAccessFile(). OnCanAccessFile() compares the path to the whitelisted directories using the IsParent() function, but again without normalizing the path first - and as the documentation of IsParent() says: "Does not convert paths to absolute, follow symlinks or directory navigation (e.g. "..")."

Did this work before? N/A 

Chrome version: 48.0.2564.95  Channel: n/a
OS Version: 6.0.1
Flash Version: 

Actually accessing the files doesn't seem to work directly - I'm not yet sure why or whether this can be circumvented.

The same mechanism is also used on Chrome OS to restrict file:// access to a few directories, so it might be interesting to look into what behavior this causes on Chrome OS.

I don't think I have demonstrated significant security impact in this report, but I'm filing it as a security bug in case someone figures out how to actually grab files with this.

## Attachments

- [Screenshot_20160213-000015.png](attachments/Screenshot_20160213-000015.png) (image/png, 261.6 KB)

## Timeline

### ja...@googlemail.com (2016-02-12)

Well, I don't have a Chromebook, but in some ages-old Chromium OS ISO build I installed, this works. So it might be more relevant for Chromium OS than for Android.

### ri...@chromium.org (2016-02-13)

I marked this as medium out of caution for now, since I do not know how much we rely on file:/// whitelisting for security after a renderer has been compromised.

Adding dcheng@, who might be more familiar.

### ri...@chromium.org (2016-02-13)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-02-13)

[Empty comment from Monorail migration]

### ra...@chromium.org (2016-02-15)

On the network side, assigning to rsleevi for triage.

### rs...@chromium.org (2016-02-15)

Hoping mmenke@ can triage as I'm at an event this week.

### mm...@chromium.org (2016-02-15)

file:///sdcard/../..%2f../data/data/com.android.chrome/app_chrome/Default/ is normalized to file:///..%2f../data/data/com.android.chrome/app_chrome/Default/, so presumably the issue is with the normalization logic in FileURLToFilePath() - presumably we should either not unescape %2f, or we should unescape it before path normalization.

I'll dig into it more tomorrow.

### mm...@chromium.org (2016-02-16)

So GURL's constructor collapses "foo/../" in URLs somewhere in url::DoPath, long before the network stack gets a shot at urls.  It also collapses things like "foo/..\".  However, it leaves %2f and %5c alone, escaped.  FileURLToFilePath, on the other hand, unescapes these to references to parent directory.  However, on other desktop platforms, URLRequestFileJob creates a FileStream::Context, which runs a FilePath::ReferencesParent check, and then fails the request because that returns true.

On Android, however, file_stream_context has conditionally compiled code that skips this check.

I think we should do two things:

1)  Fix file_stream_context on Android.
2)  Make FileURLToFilePath and GURL consistent in terms of unescaping %2f and %5c in file URLs.  It looks to me like both FireFox and IE unescape those characters in file URLs, so I'd tend to suggest we go that route in GURL (Though all else being equal, I'd prefer to keep them escaped).

### mm...@chromium.org (2016-02-16)

[+qinmin]:  Looks like you landed the code that introduced the bug in file_stream_context.h.  Care to take a swing at fixing it?

I'm happy to take a swing at GURL changes (Which will independently fix this specific bug, but I suspect there are other problems with not doing the parent check).

### mm...@chromium.org (2016-02-16)

On desktop chrome, on all platforms, file URLs that are directories are *also* missing this check.  Think it makes sense to move a check like this to a higher level, to catch all problems here....  Which I should probably be the one to do, rather than qinmin.  I'm not sure if we need a similar check for content:// URLs on Android.

### qi...@chromium.org (2016-02-16)

Content:// URLs doesn't suffer from this as the URI will need to go through content resolver.


### mm...@chromium.org (2016-02-17)

[Empty comment from Monorail migration]

### mm...@chromium.org (2016-02-18)

[Empty comment from Monorail migration]

### bu...@chromium.org (2016-02-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/30408ae67a9f6aea074b2883ba861613f52bd246

commit 30408ae67a9f6aea074b2883ba861613f52bd246
Author: mmenke <mmenke@chromium.org>
Date: Tue Feb 23 17:28:17 2016

FileURLToFilePath:  Don't unescape '/' and '\\'.

GURL leaves these escaped, and unescaping them in paths changes the
meaning of the path.

Added two values to the UnescapeRule enumeration:
PATH_SEPARATORS and URL_SPECIAL_CHARS_EXCEPT_PATH_SEPARATORS.

In followup CLs, I intend to replace all uses of URL_SPECIAL_CHARS,
in favor of one or both the two new values, and eventually remove
the value, as it's easily to use in an unsafe manner.

BUG=586657

Review URL: https://codereview.chromium.org/1704163003

Cr-Commit-Position: refs/heads/master@{#377013}

[modify] https://crrev.com/30408ae67a9f6aea074b2883ba861613f52bd246/net/base/escape.cc
[modify] https://crrev.com/30408ae67a9f6aea074b2883ba861613f52bd246/net/base/escape.h
[modify] https://crrev.com/30408ae67a9f6aea074b2883ba861613f52bd246/net/base/escape_unittest.cc
[modify] https://crrev.com/30408ae67a9f6aea074b2883ba861613f52bd246/net/base/filename_util.cc
[modify] https://crrev.com/30408ae67a9f6aea074b2883ba861613f52bd246/net/base/filename_util_unittest.cc


### mm...@chromium.org (2016-02-23)

I'll let the fix bake a couple days, and then request a merge.

### mm...@chromium.org (2016-02-23)

Actually, not that far away from release, and this is labelled as a medium severity security issue, so I'll just request the merge now.

### sh...@google.com (2016-02-23)

[Automated comment] Less than 2 weeks to go before stable on M49, manual review required.

### ti...@google.com (2016-02-29)

Shruthi - can you please review this merge request? We'd like to get this in with the final beta tomorrow.

### ti...@google.com (2016-03-03)

Removing merge request - don't want this to land right in the middle of some android stuff. Adding Merge-Triage to revisit this.

### cl...@chromium.org (2016-03-10)

[Empty comment from Monorail migration]

### ti...@google.com (2016-05-09)

This actually shipped with M50 stable based on revision number, so let's note this with 3-M50 notes so Jann get's his credit syndicated.

### ti...@google.com (2016-05-12)

[Comment Deleted]

### ti...@google.com (2016-05-12)

Congratulations - $500 for this report! (Deleted comment was me copypasting the wrong panel notes to this bug) 

### sh...@chromium.org (2016-06-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### aw...@chromium.org (2016-06-08)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### aw...@chromium.org (2018-04-25)

[Empty comment from Monorail migration]

### is...@google.com (2018-04-25)

This issue was migrated from crbug.com/chromium/586657?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40083682)*
