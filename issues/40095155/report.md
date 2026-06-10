# UAF in content::IndexedDBDatabase::ProcessRequestQueueAndMaybeRelease

| Field | Value |
|-------|-------|
| **Issue ID** | [40095155](https://issues.chromium.org/issues/40095155) |
| **Status** | New |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>Storage>IndexedDB |
| **Platforms** | Linux |
| **Reporter** | cd...@gmail.com |
| **Assignee** | dm...@chromium.org |
| **Created** | 2019-05-24 |
| **Bounty** | $10,500.00 |

## Description

UserAgent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36

Steps to reproduce the problem:
1. Build asan version of chromium. 
2. Make a dir named mojotest in out/gen and set up a webserver in mojotest.Put crash.html in it.
3. Run ./chrome  crash.html 

What is the expected behavior?

What went wrong?
Can stably get uaf crash.

Did this work before? N/A 

Chrome version: 76.0.3804.0  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- [diff](attachments/diff) (text/plain, 718 B)
- [crash.html](attachments/crash.html) (text/plain, 5.6 KB)

## Timeline

### cd...@gmail.com (2019-05-24)

The para run chrome is ./chrome --enable-blink-features=MojoJS crash.html
If can't repro, please try to clean the browser data.

The problem may be caused by delete the protect step in 

content/browser/indexed_db/indexed_db_database.cc:1849
void IndexedDBDatabase::RequestComplete(ConnectionRequest* request) {
  DCHECK_EQ(request, active_request_.get());
  scoped_refptr<IndexedDBDatabase> protect(this);  <-------delete this
  active_request_.reset();                                                  <-------may delete database self

  // Exit early if |active_request_| held the last reference to |this|.
  if (protect->HasOneRef())
    return;

  if (!pending_requests_.empty())
    ProcessRequestQueue();
}
It's similar with my another https://crbug.com/chromium/942898.


So the patch is  protecting it again.Sees in diff.









### ts...@chromium.org (2019-05-24)

Previous indexedDB issues have been sev critical, feel free to downgrade as appropriate.

[Monorail components: Blink>Storage>IndexedDB]

### ts...@chromium.org (2019-05-24)

[Empty comment from Monorail migration]

### dm...@chromium.org (2019-05-24)

[Empty comment from Monorail migration]

### dm...@chromium.org (2019-05-24)

The RequestComplete method needs to grab a weakptr to the database before destructing the active request.

Destructing a request can cause the database to destruct through ConnectionClosed reentry.

### dm...@chromium.org (2019-05-24)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-05-25)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/6cba1182f548fdf914119f071f7138a5c0efb036

commit 6cba1182f548fdf914119f071f7138a5c0efb036
Author: Daniel Murphy <dmurph@chromium.org>
Date: Sat May 25 00:28:58 2019

[IndexedDB] Fix RequestComplete() reentry UAF

Destroying an ConnectionRequest can cause the IndexedDBDatabase to
destruct through ConnectionClosed(). This can cause a UAF in
RequestComplete(). This change creates a WeakPtr there that can be
checked before continuing.

R=pwnall@chromium.org

Bug: 966762
Change-Id: Ieda327d36390d6941771475725415e2ae65f336d
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1629171
Commit-Queue: Daniel Murphy <dmurph@chromium.org>
Reviewed-by: Victor Costan <pwnall@chromium.org>
Cr-Commit-Position: refs/heads/master@{#663344}

[modify] https://crrev.com/6cba1182f548fdf914119f071f7138a5c0efb036/content/browser/indexed_db/indexed_db_database.cc


### sh...@chromium.org (2019-05-25)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-05-25)

This is a critical security issue. If you are not able to fix this quickly, please revert the change that introduced it.

If this doesn't affect a release branch, or has not been properly classified for severity, please update the Security_Impact or Security_Severity labels, and remove the ReleaseBlock label. To disable this altogether, apply ReleaseBlock-NA.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-05-25)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### pw...@chromium.org (2019-05-28)

The cause of this bug landed in M76. The fix above is included in M76. I don't think there's anything else to do here.

### sh...@chromium.org (2019-05-28)

[Empty comment from Monorail migration]

### aw...@google.com (2019-05-28)

Security_Impact-Head to match https://crbug.com/chromium/966762#c11

### na...@google.com (2019-05-28)

[Empty comment from Monorail migration]

### na...@google.com (2019-05-29)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### na...@google.com (2019-05-29)

Congrats! The Panel decided to reward $5,000 for this report!

### cd...@gmail.com (2019-05-30)

Hi natashapabrai@,
Thanks for the reward! 
Do appreciate for your work and could i be able to know if the suggested fix works? 
I report this one by imitating nedwilliamson's(PJ0 member) style ,such as https://crbug.com/chromium/725032. These two vulnerabilities are the same type (out of sandbox, indexed_db, stable uaf). The only differences are the way to triger, mine used mojo js in renderer process while his is patching the souce code.
Could i be able to know what's the inner difference between those vulnerabilities or the cause of as twice of bounty? 
Thanks again.

### aw...@google.com (2019-05-31)

[Empty comment from Monorail migration]

### aw...@google.com (2019-06-07)

re-adding reward-topanel so the panel can take a look at https://crbug.com/chromium/966762#c17

### na...@google.com (2019-06-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
*********************************

### aw...@google.com (2019-06-13)

[Empty comment from Monorail migration]

### na...@google.com (2019-06-13)

Congrats the Panel decided to reward 10,000 + $500 patching bonus for this report! 

### cd...@gmail.com (2019-06-14)

Thanks for the reward and do appreciate for the efficient re-view work! Cheers

### sh...@chromium.org (2019-06-14)

Not requesting merge to M76 because latest trunk commit (663344) appears to be prior to beta branch point (665002). If this is incorrect, please replace the Merge-na label with Merge-Request-76. If other changes are required to fix this bug completely, please request a merge if necessary.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mm...@chromium.org (2020-03-17)

Looks like this shoould've been High severity, as it required MojoJS. Thanks glazunov@ for pointing this out.

### yu...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-06)

This issue was migrated from crbug.com/chromium/966762?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail mergedwith: crbug.com/chromium/966784]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095155)*
