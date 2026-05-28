# Security: Heap-use-after-free in ProfileTokenNavigationThrottle::WillProcessRespons 

| Field | Value |
|-------|-------|
| **Issue ID** | [40063703](https://issues.chromium.org/issues/40063703) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Enterprise |
| **Platforms** | Linux |
| **Reporter** | me...@gmail.com |
| **Assignee** | yd...@chromium.org |
| **Created** | 2023-03-21 |
| **Bounty** | $4,000.00 |

## Description

**Steps to reproduce the problem:**  

repro:

1. apply the change.txt and compile chromium with ASAN
2. run `./chrome --user-data-dir=/tmp/noexist --enable-features=EnableProfileTokenManagement http://127.0.0.1:8605/poc.html`

This also could be triggerd by opening `www.google.com` and close it directly, here I use `window.open` to simulate it.

**Problem Description:**

1. Analysis

There is a `Unretained(this)` is posted in function `ProfileTokenNavigationThrottle::WillProcessResponse`[1], it will then be passed into function `GetTokenInfo`[2] and passed into a PostTask. If we could free `this` after this task is posted but before it running, UAF occurs.

Note that in order to trigger this easily, I add a delay to this PostTask. It could also be triggered without any change.

```
content::NavigationThrottle::ThrottleCheckResult  
ProfileTokenNavigationThrottle::WillProcessResponse() {  
  auto host = navigation_handle()->GetURL().host();  
  if (base::Contains(kSupportedHosts, host)) {  
    token_info_getter_->GetTokenInfo(  
        navigation_handle(),  
        base::BindOnce(&ProfileTokenNavigationThrottle::OnTokenInfoReceived,  
                       base::Unretained(this)));  
    return DEFER;  
  }  
  return PROCEED;  
}  

```
```
  void GetTokenInfo(  
      content::NavigationHandle\* navigation_handle,  
      base::OnceCallback<void(const std::string&, const std::string&)> callback)  
      override {  
    auto url = navigation_handle->GetURL();  
    DCHECK_EQ(url.host(), kTestHost);  
    std::string id;  
    std::string token;  
    net::GetValueForKeyInQuery(url, "id", &id);  
    net::GetValueForKeyInQuery(url, "token", &token);  
    base::SequencedTaskRunner::GetCurrentDefault()->PostTask(  
        FROM_HERE, base::BindOnce(std::move(callback), id, token));  
  }  

```

[1] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/profile_token_management/profile_token_navigation_throttle.cc;l=90;drc=2fa00f8e31fb1ad7679cf0a8c6d49d588de8e221;bpv=0;bpt=0>  

[2] <https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/enterprise/profile_token_management/profile_token_navigation_throttle.cc;l=38;drc=2fa00f8e31fb1ad7679cf0a8c6d49d588de8e221;bpv=0;bpt=0>

2. Bisect

This problem is introduced in this commit: 2fa00f8e31fb1ad7679cf0a8c6d49d588de8e221  

<https://chromium-review.googlesource.com/c/chromium/src/+/4311177>

This commit add the use of `tab_id` after its corresponding tab is removed from `saved_tabs_`

3. Suggested Patch

Please pass a WeakPtr to ensure the lifetime of `this`

**Additional Comments:**

\*\*Chrome version: \*\* \*\*Channel: \*\* Not sure

**OS:** Linux

## Attachments

- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2023-03-21)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-03-21)

Upload the change asan and video

### me...@gmail.com (2023-03-21)

I also try to repro this without patch.

Because my bad network condition, opening `www.google.com` is pretty slow. 
I open some `www.google.com` and then dup them to open lots of `www.google.com` at the same time, this will Post many tasks. Then you could use `Ctrl+W` immediately to close the tab to trigger this UAF.


### me...@gmail.com (2023-03-22)

PING

### hc...@google.com (2023-03-22)

@ydago, can you take a look since https://chromium-review.googlesource.com/c/chromium/src/+/4311177 is yours?

also, to confirm, i believe that the EnableProfileTokenManagement feature is not on yet anywhere, is that right?

[Monorail components: Enterprise Services>SignIn]

### bh...@google.com (2023-03-23)

[Empty comment from Monorail migration]

### bh...@google.com (2023-03-23)

[Empty comment from Monorail migration]

### ig...@chromium.org (2023-03-23)

hchao@ correct, EnableProfileTokenManagement is not enabled anywhere, and it won't be in the near future.

The feature (including ProfileTokenNavigationThrottle) is incomplete and will see major changes before launch.

### gi...@appspot.gserviceaccount.com (2023-03-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/aed7b934ce7c0a6081802249031cc41ff52d9a4e

commit aed7b934ce7c0a6081802249031cc41ff52d9a4e
Author: Igor Ruvinov <igorruvinov@chromium.org>
Date: Thu Mar 23 19:47:23 2023

Add weak pointer factory to ProfileTokenNavigationThrottle.

The throttle may be destroyed after making an async call, so this
prevents a use-after-free caused by using base::Unretained(this).

Bug: 1426351
Change-Id: I853a0211234992e525614207f7d90c333c9fb8cc
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4365746
Reviewed-by: Yann Dago <ydago@chromium.org>
Commit-Queue: Igor Ruvinov <igorruvinov@chromium.org>
Reviewed-by: Fabio Tirelo <ftirelo@chromium.org>
Auto-Submit: Igor Ruvinov <igorruvinov@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1121333}

[modify] https://crrev.com/aed7b934ce7c0a6081802249031cc41ff52d9a4e/chrome/browser/enterprise/profile_token_management/profile_token_navigation_throttle.cc
[modify] https://crrev.com/aed7b934ce7c0a6081802249031cc41ff52d9a4e/chrome/browser/enterprise/profile_token_management/profile_token_navigation_throttle.h


### me...@gmail.com (2023-03-28)

Hello, can we mark this as fixed?

### ig...@chromium.org (2023-03-28)

Marking as fixed after confirming that the crash is not reproducible on tip of tree.

The fix made it into M113, so no need for cherry-picking: https://chromiumdash.appspot.com/commit/aed7b934ce7c0a6081802249031cc41ff52d9a4e

### [Deleted User] (2023-03-28)

[Empty comment from Monorail migration]

### [Deleted User] (2023-03-28)

[Empty comment from Monorail migration]

### am...@google.com (2023-04-13)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-04-13)

Congratulations, Krace! The VRP Panel has decided to award you $3,000 for this report of a moderately mitigated security bug + $1,000 bisect bonus. Thank you for your efforts and reporting this issue to us. 

### am...@google.com (2023-04-14)

[Empty comment from Monorail migration]

### me...@gmail.com (2023-06-19)

[Comment Deleted]

### [Deleted User] (2023-07-04)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2023-07-04)

This issue was migrated from crbug.com/chromium/1426351?no_tracker_redirect=1

[Multiple monorail components: Enterprise, Services>SignIn]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40063703)*
