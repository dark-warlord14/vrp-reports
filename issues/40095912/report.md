# Leaking size of cross-origin resource by using Range Requests and Service Workers

| Field | Value |
|-------|-------|
| **Issue ID** | [40095912](https://issues.chromium.org/issues/40095912) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Blink>PerformanceAPIs>ResourceTiming, Blink>ServiceWorker, Internals>Media>Network |
| **Platforms** | Android, Linux, Mac, Windows, ChromeOS |
| **Reporter** | he...@gmail.com |
| **Assignee** | yo...@chromium.org |
| **Created** | 2019-08-05 |
| **Bounty** | $2,000.00 |

## Description

**VULNERABILITY DETAILS**  

When a cross-origin resource is used in an audio/video tag, a request containing the Range header asking for bytes=0- is issued.  

If the request is intercepted using a Service Worker and we respond with an arbitrary body, e.g:  

e.respondWith(new Response("aaa", {status: 206, headers: {"Content-Range": "bytes 0-1337/13370" }}));

Chrome will be tricked into thinking it got the first 3 bytes of the audio/video and then ask for the remaining bytes by issuing a new request containing the "Range: bytes=3-" header. Note that Chrome only cares for the body size of the response when determining how many bytes to ask next.

If we decide not to intercept the subsequent request, it will go directly to the server and ask for the bytes we stipulated. Instead of asking only for 3 bytes, we could ask for "bytes=5000-", and if the response size of the resource is smaller than that, the server will throw a "416 Range Not Satisfiable" error response code.

We can detect when the server was able / was not able to fulfill our ranged request by counting the number of resources in performance.getEntries(). Successful requests (2xx) get added as an entry and requests that were unsuccessful (4xx) do not.

In the PoC, the size of <https://www.google.com/robots.txt> is being brute-forced starting on byte 7240. In a real attack, it would be trying to get the size through binary search.

This vulnerability is useful for XS-Search attacks. A real-world example is <https://medium.com/@luanherrera/xs-searching-googles-bug-tracker-to-find-out-vulnerable-source-code-50d8135b7549> (more on <https://github.com/xsleaks/xsleaks/wiki/Real-World-Examples>).

**VERSION**  

Version 76.0.3809.87 (Official Build) stable (64-bit)  

Version 78.0.3874.3 (Official Build) canary (64-bit)

**REPRODUCTION CASE**

1. Access <https://lbherrera.github.io/lab/chrome-8b024c22/sizeleak.html>.
2. After a moment, you should see a message saying the exact leaked size of the cross-origin resource.

**CREDIT INFORMATION**  

Reporter credit: Luan Herrera (@lbherrera\_)

This bug is subject to a 90 day disclosure deadline. After 90 days elapse  

or a patch has been made broadly available (whichever is earlier), the bug  

report will become visible to the public.

## Timeline

### do...@chromium.org (2019-08-06)

Thanks for the report - + some media folks. I'm assigning a High severity as this leaks the size of a cross-origin resource.

[Monorail components: Blink>Media>Audio Blink>Media>Video]

### gr...@chromium.org (2019-08-06)

[Empty comment from Monorail migration]

### gr...@chromium.org (2019-08-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-08-06)

Setting milestone and target because of Security_Impact=Stable and high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ke...@chromium.org (2019-08-06)

cc jakearchibald@, who had done some earlier investigation into the safety of Ranger header availability in Service Workers.

### ml...@google.com (2019-08-07)

This should be assigned to dalecurtis@ has the videostack team owns the network code but the specific owner left the team. Assigning to liberato@ in case of he knows who could be a good fallback.

[Monorail components: -Blink>Media>Audio -Blink>Media>Video Internals>Media>Network]

### li...@chromium.org (2019-08-07)

i'd normally look into this myself, but i'm ooo from pretty much now until the end of next week.  if it can wait until then, i'll look at it when i get back.

=> wolenetz for comment, since "web workers".  i know very little about them.

first thought is that it seems like ranged requests in general could be susceptible from this type of attack when combined with the performance log.  it's unclear to me (with very little background on the subject) that non-media paths couldn't have this problem too.

also, this line in the exploit confuses me:

sound.src = `${url}?size=${size}&${Math.random()}`;

i'm not sure at which layer the uniqueness of the url helps the attack.  have to look at the media multibuffer code (been years) to see if it or the underlying chrome cache behaves differently when we don't do this.

### jd...@chromium.org (2019-08-19)

liberato@: welcome back. I'm assigning this back to you, but feel free to re-assign again; I just want to make sure we see movement on our high-severity bugs.

Thanks!
- a friendly security sheriff.

### sh...@chromium.org (2019-08-22)

liberato: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### li...@chromium.org (2019-08-22)

n minutes and n+1 emergencies.

### li...@chromium.org (2019-08-22)

actually, +nags.  probably a good idea in this case.

### li...@chromium.org (2019-08-22)

after more thought, i'm entirely unsure that we can add cross-origin performance events without exactly this sort of problem happening.

### li...@chromium.org (2019-08-22)

+mlamouri

### mi...@chromium.org (2019-08-22)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-08-23)

[Empty comment from Monorail migration]

### li...@chromium.org (2019-08-30)

i haven't forgotten about this.  trying to decide between:

(a) turning off performance events for cases like this, where "like this" is the main thing i need to figure out.
(b) disallowing different URLs entirely if we have a partial download in the cache already.  this seems more robust (why would we ever want to allow it?).

### gr...@chromium.org (2019-09-02)

[Empty comment from Monorail migration]

### ja...@chromium.org (2019-09-02)

Sorry for the slow reply. I was on leave. Unless I'm mistaken, this is almost identical to "Attack 1" as described in https://github.com/whatwg/fetch/issues/144#issuecomment-368040980, and the solution is the same, right?

### li...@chromium.org (2019-09-04)

=>dalecurtis

### da...@chromium.org (2019-09-04)

Jake, that looks like the attack, but the solution seems to rely on validating the responses. In this case, it looks like to prevent the attack we'd need to never send the request. Which means we need to know that a given request is going to end up opaque before we send it -- or otherwise have some method for preventing a response that we detect as opaque from showing up in performance.getEntries();

+yhirano who's helped out on similar issues in the past.

### ja...@chromium.org (2019-09-05)

Unless I've misunderstood the attack, the leak here is caused by revealing details about the response, not by making the request.

Here's how I understand it:

Request 1: Request for range 0-
Response 1: A non-opaque response for 3 bytes.
or
Response 1: A cached opaque response for 3 bytes, from URL [A].

Request 2: Request for range 4-
Response 2: Pass through to the server

Then, performance.getEntries() will leak whether the response was 2xx or 4xx.

But, with the mitigations in https://github.com/whatwg/fetch/issues/144#issuecomment-368040980, response 2 should always be classed as failure, because it's mixing opaque and non-opaque data, or opaque data from two different URLs.

### yh...@chromium.org (2019-09-05)

[Empty comment from Monorail migration]

[Monorail components: Blink>ServiceWorker]

### da...@chromium.org (2019-09-05)

yhirano: How would you mark a response as failed at time of didReceiveResponse()?
https://cs.chromium.org/chromium/src/media/blink/resource_multibuffer_data_provider.cc?l=207

We have some failure cases in there, but I don't see how that would preclude the response from showing up in performance.getEntries(). Or are you suggesting that we fail the response at some lower level?

### yh...@chromium.org (2019-09-06)

[Empty comment from Monorail migration]

### fa...@chromium.org (2019-09-06)

There's some prior similar bugs at https://crbug.com/chromium/505829 and https://crbug.com/chromium/489060.

### fa...@chromium.org (2019-09-06)

Also https://crbug.com/chromium/780435 mentioned range requests.

### yh...@chromium.org (2019-09-06)

> #23
A: WebAssociatedURLLoader's cancel is asynchronous (see Resource::AllClientsAndObserversRemoved), so it's possible that even if you cancel the request it's seen as completion from PerformanceEntry POV.

I'd like to know where are Dale and Jake's difference from. Is A the reason?

In any case, IIUC cancelling the request when the response arrives at the media element would not be a solution even if we didn't have A. Since resource timing API is available on service worker, you don't need to return the second response to the media element. You can just write

// in SW
onFetch((e) => {
  if (/* |e| is the first request */) {
    // As described in the issue description
    e.respondWith(new Response(...));
    return;
  }
  if (/* |e| is the second request */) {
    fetch(e.request).then((res) => {
      return res.text();
    }).then(() => {
      // We can inspect the ResourceTiming entry here.
    });

    // Just wait for one second to keep this SW alive.
    e.respondWith(new Promise(resolve, reject) => setTimeout(reject, 1000));
    return;
  }
});



### ja...@chromium.org (2019-09-06)

Ahhh I'm on the same page now. Although the response is rejected, it may still show up as a success in ResourceTiming. Sorry it took me so long to see that.

Yeah, this is a leak in resource timing. Fetch deliberately does not expose the status of opaque responses https://fetch.spec.whatwg.org/#concept-filtered-response-opaque. We had some discussion of this in the early days of fetch https://github.com/whatwg/fetch/issues/14.

There are lots of elements that hint at the status/content of opaque responses, but we avoid adding new ones, and it feels like resource timing exposes too much.

### ja...@chromium.org (2019-09-06)

I can't find the bit in https://w3c.github.io/resource-timing/#processing-model that says 4xx responses shouldn't be added. Is it in another spec?

### da...@chromium.org (2019-09-09)

Bump for folks on this since it's an active security issue. Jake, we're you expecting yhirano@ to respond? +Resource>Timing folks who might be able to respond.

[Monorail components: Blink>PerformanceAPIs>ResourceTiming]

### yh...@chromium.org (2019-09-10)

npm@, can you answer #29?

### ja...@chromium.org (2019-09-10)

I don't think we should provide 200 vs 400 for no-cors responses at all, but maybe folks came up with a good reason why it's generally ok (which is why I was trying to find the spec which grants this power). Are we exposing anything else slightly worrying about these responses?

If it turns out we can't 'fix' resource timing in this way, I'd propose fixing it for any response that was requested with a range header.

### yo...@chromium.org (2019-09-10)

npm@ is OOO, but I can answer in his stead.

Treating 404 (or other error codes) as aborts is not specified [1], and something that Chromium is doing wrong [2]. We should fix it.
Will fixing that also fix the underlying cross-origin leak? If so, that would certainly bump up the priority for the mentioned issue.

[1] https://github.com/w3c/resource-timing/issues/165
[2] https://bugs.chromium.org/p/chromium/issues/detail?id=883400


### ja...@chromium.org (2019-09-11)

> Will fixing that also fix the underlying cross-origin leak?

Yes, I think so.

If the result is 4xx and 2xx no-cors responses become indistinguishable via resource timing, yep, that fixes it.

### yo...@chromium.org (2019-09-11)

CL at https://chromium-review.googlesource.com/c/chromium/src/+/1796544

### yo...@chromium.org (2019-09-11)

Another take-away from this issue is that if in the future we will add response status to Resource Timing, we'd need to have that gated behind TAO.

### ja...@chromium.org (2019-09-11)

Yeah, if fetch() doesn't expose it, Resource Timing shouldn't by default.

### sh...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-09-11)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/5e556dd80e03b7a217e10990d71be25d07e1ece7

commit 5e556dd80e03b7a217e10990d71be25d07e1ece7
Author: Yoav Weiss <yoavweiss@chromium.org>
Date: Wed Sep 11 13:28:25 2019

[resource-timing] Report performance entries with failing status codes

Currently we don't report performance entries with failing status codes.
From the spec's perspective, reporting aborts is a MAY, but failing
status code responses should not be considered aborts. [1]
Chromium is the only engine which doesn't report those entries.
This CL fixes that to report them similarly to successful status codes.

Bug: 883400, 990849
Change-Id: Ic5e99e3df77f3869aa0dd70f0141d88016fdb972

[1] https://github.com/w3c/resource-timing/issues/165#issuecomment-441413636

Change-Id: Ic5e99e3df77f3869aa0dd70f0141d88016fdb972
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1796544
Commit-Queue: Yoav Weiss <yoavweiss@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Mike West <mkwst@chromium.org>
Cr-Commit-Position: refs/heads/master@{#695596}

[modify] https://crrev.com/5e556dd80e03b7a217e10990d71be25d07e1ece7/third_party/blink/renderer/platform/loader/fetch/resource_fetcher.cc
[delete] https://crrev.com/17a3f5843af93fe99c44029da37fa00feebed169/third_party/blink/web_tests/external/wpt/resource-timing/resource_ignore_failures.html
[add] https://crrev.com/5e556dd80e03b7a217e10990d71be25d07e1ece7/third_party/blink/web_tests/external/wpt/resource-timing/resources/status-code.py
[add] https://crrev.com/5e556dd80e03b7a217e10990d71be25d07e1ece7/third_party/blink/web_tests/external/wpt/resource-timing/status-codes-create-entry.html
[modify] https://crrev.com/5e556dd80e03b7a217e10990d71be25d07e1ece7/third_party/blink/web_tests/external/wpt/service-workers/service-worker/resource-timing.sub.https.html


### yo...@chromium.org (2019-09-11)

I've landed a fix. Please test it to make sure the attack is no longer feasible.
Also - please let me know soon if you'd want me to merge this to M77.

### yo...@chromium.org (2019-09-11)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-11)

This bug requires manual review: Request affecting a post-stable build
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), kariahda@(iOS), dgagnon@(ChromeOS), lakpamarthy@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-11)

Please mark security bugs as fixed as soon as the fix lands, and before requesting merges. This update is based on the merge- labels applied to this issue. Please reopen if this update was incorrect.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-12)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-13)

Also requesting merge to M78 since the fix isn't in that branch yet either.

### sh...@chromium.org (2019-09-13)

This bug requires manual review: We don't branch M78 until 2019-09-05.
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://goto.google.com/chrome-release-branch-merge-guidelines
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), kariahda@(iOS), geohsu@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sr...@google.com (2019-09-13)

pls help answer the questions in c#46 for merge review

### sr...@google.com (2019-09-16)

friendly ping to help update the info for merge review request. (Answer C#46)

### na...@google.com (2019-09-16)

[Empty comment from Monorail migration]

### da...@chromium.org (2019-09-16)

@srinivasista: Aren't security bugs auto-approved for merge?

### be...@chromium.org (2019-09-16)

Please merge to M78, branch 3904.

### da...@chromium.org (2019-09-16)

Done, since I think many of these folks are TPAC or elsewhere.

### go...@chromium.org (2019-09-16)

Thank you dalecurtis@.

M78 merge is here - https://chromium.googlesource.com/chromium/src.git/+/d8908b3d5d567bb67c7ae93f6176d85fbbc472fc

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $2,000 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### ad...@google.com (2019-09-26)

yoavweiss@ dalecurtis@ - there's an upcoming M77 security respin and we are going to consider merging this. We didn't want to push to get this into the initial M77 stable release since it hadn't had bake time in beta, and from https://crbug.com/chromium/990849#c39 it does look like it has an intentional behavior change. But presumably it's now had a bit of bake time - are we confident that this has had no ill-effects and we can merge into an M77 respin?

### da...@chromium.org (2019-09-26)

Defer to yoav, it seems safe enough to me though.

### yo...@chromium.org (2019-09-27)

Seems safe to me as well, as this is a one line change

### la...@google.com (2019-09-27)

merge approved for M77 branch 3865

### da...@chromium.org (2019-09-27)

Merged https://chromium-review.googlesource.com/c/chromium/src/+/1829742

### sh...@chromium.org (2019-10-01)

This issue has been approved for a merge. Please merge the fix to any appropriate branches as soon as possible!

If all merges have been completed, please remove any remaining Merge-Approved labels from this issue.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### la...@google.com (2019-10-01)

yoavweiss@ - please merge ASAP

### da...@chromium.org (2019-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-10-07)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/990849?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>PerformanceAPIs>ResourceTiming, Blink>ServiceWorker, Internals>Media>Network]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40095912)*
