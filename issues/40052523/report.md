# Cross-domain content can be fetched from resources loaded by the content scheme

| Field | Value |
|-------|-------|
| **Issue ID** | [40052523](https://issues.chromium.org/issues/40052523) |
| **Status** | Assigned |
| **Severity** | Unknown |
| **Priority** | P1 |
| **Component** | Blink>SecurityFeature>CORS |
| **Platforms** | Android |
| **CVE IDs** | CVE-2020-6516 |
| **Reporter** | wy...@gmail.com |
| **Assignee** | to...@chromium.org |
| **Created** | 2020-06-08 |
| **Bounty** | $20,000.00 |

## Description

Originally reported in https://crbug.com/chromium/1092025. Reporter's comments on the issue pasted here:

We can cross-domain fetch other content://xxx under one content://xxx by XMLHttpRequest.

Originally, the SOP of chrome takes isolation measures between 'content' schemes, just like 'file' scheme. But we found that the isolation measures disappeared since version 79. So the bug exists in chrome from version 79 to the latest version.

The way to fetching data in other content:// is conventional, you can get the details in the attached 'exp_payload.a' file.

As for the reason why this bug has been introduced again since 79, we will analyse the root case in section 'ROOT CASE ANALYSE AND SUGGESTED PATCH'.

...

This bug is the key of our attack chain.

The SOP policy of chrome works well before chrome version 79. We can not fetch data of other 'content://' under one 'content://'.

But it changes since 79. During our research, we target the new chrome feature 'OutOfBlinkCors'. We did a test on version 78.0.3904.108, with 'OutOfBlinkCors' disabled by default. We can't cross-domain between 'content://' scheme by default. But we can do it if we enalbe 'OutOfBlinkCors' manually.

So we think the root case of bug #4 is because of the lack of SOP policy out of blink when 'OutOfBlinkCors' feature is enabled by default.

As for suggested patch, enforcing should be added on the network or browser process side, such as 'content/browser/android/content_url_loader_factory.cc'.

You know, the 'OutOfBlinkCors' feature is an important security measures(https://www.chromestatus.com/feature/5768642492891136) from the view of security architecture design. The big change will introduce new bugs if enforceing is lost on network or browser process.

And 'OutOfBlinkCors' maybe influences the security of other modules, which should be reviewed.

## Timeline

### to...@chromium.org (2020-06-08)

As I commented at crbug.com/1092025#c10, it looks we should not allow any CORS-enabled request from content:// to content://.
I will work on fixing this now as I'm afraid that WebView apps may start depending on this unexpected behavior if I don't fix this immediately.

I think we'd like to fix this at least in 84 Beta.

### to...@chromium.org (2020-06-08)

cc: dharani

This is not WebView specific, and mainly affects Android Chrome from m79 with OOR-CORS enabled.
This won't be a real issue for WebView as it blocks content:// by default, and even if the app enables it, content:// are still under the app's control. But we don't want new apps to depend on this unexpected behavior. In Android Chrome, it stores downloaded files in content://, and it makes this a real issue.

Thus, this don't block the OOR-CORS WebView launch, I think. But need a quick fix.

My plan is to have a fix ASAP and merge it to Beta 84 so that we can minimize the opportunity for new apps to expect this behavior.

### to...@chromium.org (2020-06-08)

cc: team members

### mb...@chromium.org (2020-06-09)

Additional information from the reporter:

Hello, after our deeper research, we gain more information about the root case of bug #4, hope to help you fixing as soon as possible.

If 'OutOfBlinkCors' feature is enabled, the following two enforcing are invalid:

```
//third_party/blink/renderer/core/loader/threadable_loader.cc
void ThreadableLoader::DispatchInitialRequest(ResourceRequest& request) {
  if (out_of_blink_cors_ || (!request.IsExternalRequest() && !cors_flag_)) {        //if 'OutOfBlinkCors' is enabled, 'out_of_blink_cors_' is true 
    LoadRequest(request, resource_loader_options_);
    return;
  }

  DCHECK(cors::IsCorsEnabledRequestMode(request.GetMode()) ||
         request.IsExternalRequest());

  MakeCrossOriginAccessRequest(request);                                            //enforcing not work
}
```

```
//third_party/blink/renderer/core/loader/threadable_loader.cc
void ThreadableLoader::ResponseReceived(Resource* resource,
                                        const ResourceResponse& response) {
    //...

    if (out_of_blink_cors_ && !response.WasFetchedViaServiceWorker()) {             //if 'OutOfBlinkCors' is enabled, 'out_of_blink_cors_' is true 
        DCHECK(actual_request_.IsNull());
        fallback_request_for_service_worker_ = ResourceRequest();
        client_->DidReceiveResponse(resource->InspectorId(), response);
        return;
    }

    //...

    if (cors_flag_) {                                                               //enforcing not work
        base::Optional<network::CorsErrorStatus> access_error = cors::CheckAccess(
            response.CurrentRequestUrl(), response.HttpHeaderFields(),
            credentials_mode_, *GetSecurityOrigin());
        if (access_error) {
        ReportResponseReceived(resource->InspectorId(), response);
        DispatchDidFail(
            ResourceError(response.CurrentRequestUrl(), *access_error));
        return;
        }
    }

    //...
}
```

So, enforcing in blink is invalid any more when 'OutOfBlinkCors' is enabled, enforcing should be added out of blink, such as 'content_url_loader_factory.cc'.

Enforcing can be added following function 'FileURLLoaderFactory::CreateLoaderAndStart' in 'file_url_loader_factory.cc':

```
//content/browser/loader/file_url_loader_factory.cc
void FileURLLoaderFactory::CreateLoaderAndStart(
    mojo::PendingReceiver<network::mojom::URLLoader> loader,
    int32_t routing_id,
    int32_t request_id,
    uint32_t options,
    const network::ResourceRequest& request,
    mojo::PendingRemote<network::mojom::URLLoaderClient> client,
    const net::MutableNetworkTrafficAnnotationTag& traffic_annotation) {

    //...
    
    // CORS mode requires a valid |request_inisiator|.
    if (network::cors::IsCorsEnabledRequestMode(request.mode) &&
        !request.request_initiator) {
        mojo::Remote<network::mojom::URLLoaderClient>(std::move(client))
            ->OnComplete(
                network::URLLoaderCompletionStatus(net::ERR_INVALID_ARGUMENT));
        return;
    }

    // |mode| should be kNoCors for the case of |shared_cors_origin_access_list_|
    // being nullptr. Only internal call sites, such as ExtensionDownloader, is
    // permitted to specify nullptr.
    DCHECK(!network::cors::IsCorsEnabledRequestMode(request.mode) ||
            shared_cors_origin_access_list_);

    // If kDisableWebSecurity flag is specified, make all requests pretend as
    // "no-cors" requests. Otherwise, call IsSameOriginWith for a file scheme
    // check that takes --allow-file-access-from-files into account.
    // CORS is not available for the file scheme, but can be exceptionally
    // permitted by the access lists.
    bool is_allowed_access =
        base::CommandLine::ForCurrentProcess()->HasSwitch(
            switches::kDisableWebSecurity) ||
        (request.request_initiator &&
        (request.request_initiator->IsSameOriginWith(
                url::Origin::Create(request.url)) ||
            (shared_cors_origin_access_list_ &&
            shared_cors_origin_access_list_->GetOriginAccessList()
                    .CheckAccessState(GetCorsOrigin(request), request.url) ==
                network::cors::OriginAccessList::AccessState::kAllowed)));

    network::mojom::FetchResponseType response_type =
        CalculateResponseType(request.mode, is_allowed_access);

    CreateLoaderAndStartInternal(request, response_type, std::move(loader),
                                std::move(client));
}
```

### ad...@google.com (2020-06-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-09)

I've moved ReleaseBlock-Beta from the parent bug (https://crbug.com/chromium/1092025) into here. As I understand it, this is the key fix required to break the chain.

### go...@chromium.org (2020-06-09)

M84 is already in Beta and we already cut M84 Beta RC tomorrow. We don't have fix ready to merge for this, can this wait until next week beta?

+adetaylor@ (Security TPM)
+benmason@ (Chrome on Android M83 Release TPM) just in case if any merge is needed for M83 per bug (https://crbug.com/chromium/1092025) .



### ad...@google.com (2020-06-09)

Sheriffbot deems this bug (specifically the parent bug, https://crbug.com/chromium/1092025) to be ReleaseBlock-Beta because overall the chain is of Critical severity. Sheriffbot doesn't like us to make _any_ release (beta or stable) when there is a known outstanding Critical severity bug, even if it's not a regression.

That said, as you've already cut beta, go ahead and release. We'll definitely want to merge this fix into the next M83 stable, once we have a fix, and assuming it's not crazily complicated.

### wy...@gmail.com (2020-06-10)

During our research, webView is unaffected. 
We can not cross-domain fetch other 'content://' resources under one 'content://' by default. So only chrome should be focused for this bug.

### to...@chromium.org (2020-06-10)

adetaylor@, govind@:
Thank you for discussing this bug's impact and release plans.
Now, I'm focusing on this bug, and hope to land a fix in days so that we can merge a fix to release branches ASAP.

### to...@chromium.org (2020-06-10)

P0 as the parent is.

### to...@chromium.org (2020-06-11)

cc: more people to ask questions in the code review.

### to...@chromium.org (2020-06-11)

possible fix: https://chromium-review.googlesource.com/c/chromium/src/+/2239605
and thinking about autoamted tests for Android Chrome and WebView.

### wy...@gmail.com (2020-06-11)

After reviewing the fix, I think it's fine. The added enforcing will break cross-domian fetching by 'XMLHttpRequest'.

### to...@chromium.org (2020-06-12)

I clarify detailed original behaviors.

setAllowContentAccess(true)
  XHR (content -> content) -> block due to CORS from origin ’null’  // This case is wrong if OOR-CORS is enabled
  XHR (content -> file) -> block due to CORS from origin ’null’
  XHR (file -> content) -> block due to CORS from origin ’null’
  XHR (file -> file) -> block due to CORS from origin ’null’

setAllowFileAccessFromFileURLs
  XHR (content -> content) -> OK
  XHR (content -> file) -> block from origin ‘content://’
  XHR (file -> content) -> block due to CORS from origin ‘file://’
  XHR (file -> file) -> OK

setAllowUniversalAccessFromFileURLs
  XHR (content -> content) -> OK
  XHR (content -> file) -> block due to CORS from origin ‘content://’
  XHR (file -> content) -> OK
  XHR (file -> file) -> OK

In all cases, Fetch does not allow content and file schemes.

### go...@chromium.org (2020-06-12)

Is this only applicable to Android?
 Per chat with dharani@, this could be applicable to Desktop and Chrome OS. If it is, please apply appropriate OSs label. Thank you.

### [Deleted User] (2020-06-12)

Setting Pri-1 to match security severity High. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### to...@chromium.org (2020-06-13)

govind@
Relevant code affect only Andorid Chrome and WebView as the "content://" is a concept of Android OS.
Also, the attack sequence of https://crbug.com/chromium/1092025 works only with Android Chrome.

### go...@chromium.org (2020-06-15)

Thank you  toyoshim@.

When do we expect fix to be landed in trunk?

### to...@chromium.org (2020-06-15)

govind:
CL is now ready and review is just started: https://chromium-review.googlesource.com/c/chromium/src/+/2239605

### go...@chromium.org (2020-06-15)

Looks like CQ dry run failed: https://chromium-review.googlesource.com/c/chromium/src/+/2239605. I just retry dry run. 

### to...@chromium.org (2020-06-16)

Now the base fix is split into https://chromium-review.googlesource.com/c/chromium/src/+/2247920 as WebView seems to need more works to keep the compatibility.

### go...@chromium.org (2020-06-17)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/c6e232163d52e4334f7227ef30634b707e44a903

commit c6e232163d52e4334f7227ef30634b707e44a903
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Thu Jun 18 01:16:09 2020

OOR-CORS: each content:// should be assumed as an opaque origin

On Android Chrome, each content:// should be assumed as an opaque
origin, and should not allow CORS-enabled requests among content://
URLs. Also content:// can not load legacy worker scripts from
content:// URLs as the mode "same-origin" is not permitted too.

TEST=./out/a/bin/run_chrome_public_test_apk -A Feature=CORS

Bug: 1092449
Change-Id: I83d15f4c1e2f2d88e219032952a7da78f470c16a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2247920
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Tommy Nyquist <nyquist@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Cr-Commit-Position: refs/heads/master@{#779596}

[modify] https://crrev.com/c6e232163d52e4334f7227ef30634b707e44a903/chrome/android/javatests/src/org/chromium/chrome/browser/UrlSchemeTest.java
[add] https://crrev.com/c6e232163d52e4334f7227ef30634b707e44a903/chrome/test/data/android/content_url_load_content_worker.html
[add] https://crrev.com/c6e232163d52e4334f7227ef30634b707e44a903/chrome/test/data/android/content_url_make_cors_to_content.html
[add] https://crrev.com/c6e232163d52e4334f7227ef30634b707e44a903/chrome/test/data/android/worker.js
[modify] https://crrev.com/c6e232163d52e4334f7227ef30634b707e44a903/content/browser/android/content_url_loader_factory.cc
[modify] https://crrev.com/c6e232163d52e4334f7227ef30634b707e44a903/content/browser/loader/file_url_loader_factory.cc
[modify] https://crrev.com/c6e232163d52e4334f7227ef30634b707e44a903/services/network/public/cpp/cors/cors.cc
[modify] https://crrev.com/c6e232163d52e4334f7227ef30634b707e44a903/services/network/public/cpp/cors/cors.h


### to...@chromium.org (2020-06-18)

OK, #25 was the fix for the Android Chrome security issue.
Another CL will be submitted for WebView, but we'd handle them separately as the severity is different between Android Chrome and WebView.

### to...@chromium.org (2020-06-18)

Also, the complexity for the fix is very diferent. I think we need to pay more attentions for the WebView fix as it is compatibility sensitive change.

### go...@chromium.org (2020-06-18)

Merge change listed at #25 to current canary branch 4176, canary version #85.0.4176.0 (currently building) includes this change: https://chromium-review.googlesource.com/c/chromium/src/+/2250471

### wy...@gmail.com (2020-06-18)

Sorry for the wrong info in #10.
We maybe didn't update the webview to higher version during previous tests.
We did it again, the webview is also affected. Waiting for your fix.

### to...@chromium.org (2020-06-18)

#29, OOR-CORS wasn't enabled for WebView until m83, and incremental launch for m83 was just finished.
So, it was a little difficult to test this on WebView until today unless you use https://chromium.googlesource.com/chromium/src/+/HEAD/android_webview/docs/developer-ui.md

Also, since the WebView don't store users' content in content:// automatically by default, this is rather a compatibility issue than a severe security issue.
Please correct me if my understanding is wrong, as my knowledge on WebView is not perfect.

### wy...@gmail.com (2020-06-18)

[Comment Deleted]

### wy...@gmail.com (2020-06-18)

[Comment Deleted]

### wy...@gmail.com (2020-06-18)

#30, I succeeded reproducing this bug on webview 80.0.3987.99. And I don't know why I can.
So should you repro it on version under m83, such as m80, m81 or m82?

And, although the WebView don't store users' content in content:// automatically, but I can still steal user's private info by 'content://media/external/file/id', just as the attack chain in https://crbug.com/chromium/1092025.

### ad...@google.com (2020-06-18)

The WebView variant has been raised as https://crbug.com/chromium/1096677, so I'm marking this as Fixed. Sheriffbot would add merge requests so I'll do it myself now.

Specifically, Sheriffbot will want us to merge this back to M83 as well as M84 and will give merge questionnaires. We are about to make a final new version of M83, and as this is the key part of a full attack chain, it would be great to include it. But my sense is that the fix is too complex to merge back to M83. toyoshim@, as well as answering all the questions in Sheriffbot's merge questionnaires, please would you comment more generally on any stability risks with this fix and whether you think we should merge to M83 as well as M84?

### ad...@google.com (2020-06-18)

[Empty comment from Monorail migration]

### [Deleted User] (2020-06-18)

This bug requires manual review: M84's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on master/ToT?
4. Why are these changes required in this milestone after branch?
5. Is this a new feature?
6. If it is a new feature, is it behind a flag using finch?

Please contact the milestone owner if you have questions.
Owners: govind@(Android), bindusuvarna@(iOS), marinakz@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-06-18)

Re #34, 
There is no plan M83 respin for Android any more. +benmason (Chrome on Android M83 Release TPM)

For M84 merge,  let's wait for more canary coverage and pls update bug with canary result on Monday morning. 

### ad...@google.com (2020-06-18)

Oh yes! Good point. I had forgotten that the refresh is desktop only.

### ad...@google.com (2020-06-18)

Setting flags back to as they were.

### to...@chromium.org (2020-06-19)

1. Does your merge fit within the Merge Decision Guidelines?
  => Definitely yes.

2. Links to the CLs you are requesting to merge.
  => https://crbug.com/chromium/1092449#c25

3. Has the change landed and been verified on master/ToT?
  => being baked in Canary this weekend

4. Why are these changes required in this milestone after branch?
  => High severity security issue was found after the feature was shipped

5. Is this a new feature?
  => No. Refactoring project launched t m79.

6. If it is a new feature, is it behind a flag using finch?
  => No, but behind a finch.

### ad...@chromium.org (2020-06-19)

Thanks. I'm going to approve merge to M84 but, per https://crbug.com/chromium/1092449#c37, please wait for a weekend of Canary coverage first. Then if all is well please merge to M84, branch 4147.

We are getting close to the initial launch of M84, and it's no-meetings-weeks, and this is the sort of fairly complex fix where I'd be more comfortable if it went via a beta cycle too. But as the key element in a full attack chain I feel we should try to get it into the initial M84 release if at all possible. If you have any doubts at all though toyoshim@ - don't merge :)

### go...@chromium.org (2020-06-22)

toyoshim@, how is the change looking in canary? If it looks good, please merge to M84 branch 4147 based on https://crbug.com/chromium/1092449#c41. Thank you. 

Note: We're cutting M84 last Beta/Stable RC tomorrow, Tuesday.

### to...@chromium.org (2020-06-23)

https://chromium-review.googlesource.com/c/chromium/src/+/2259113 is now in CQ

### ad...@google.com (2020-06-23)

toyoshim@, if this is believed fixed apart from the WebView part (which is tracked independently in https://crbug.com/chromium/1096677) please mark this as Fixed. It looks like this landed in M84 about half an hour ago too. Thanks!

### to...@chromium.org (2020-06-23)

Commit log was delayed?
OK, let me close as Fixed!

### go...@chromium.org (2020-06-23)

Adjusting merge labels per https://crbug.com/chromium/1092449#c44 to #46. 

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-06-23)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4

commit bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4
Author: Takashi Toyoshima <toyoshim@chromium.org>
Date: Tue Jun 23 05:26:46 2020

OOR-CORS: each content:// should be assumed as an opaque origin

On Android Chrome, each content:// should be assumed as an opaque
origin, and should not allow CORS-enabled requests among content://
URLs. Also content:// can not load legacy worker scripts from
content:// URLs as the mode "same-origin" is not permitted too.

TEST=./out/a/bin/run_chrome_public_test_apk -A Feature=CORS

(cherry picked from commit c6e232163d52e4334f7227ef30634b707e44a903)

Bug: 1092449
Change-Id: I83d15f4c1e2f2d88e219032952a7da78f470c16a
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2247920
Commit-Queue: Takashi Toyoshima <toyoshim@chromium.org>
Reviewed-by: Tommy Nyquist <nyquist@chromium.org>
Reviewed-by: Yutaka Hirano <yhirano@chromium.org>
Reviewed-by: Kinuko Yasuda <kinuko@chromium.org>
Cr-Original-Commit-Position: refs/heads/master@{#779596}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2259113
Reviewed-by: Takashi Toyoshima <toyoshim@chromium.org>
Cr-Commit-Position: refs/branch-heads/4147@{#756}
Cr-Branched-From: 16307825352720ae04d898f37efa5449ad68b606-refs/heads/master@{#768962}

[modify] https://crrev.com/bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4/chrome/android/javatests/src/org/chromium/chrome/browser/UrlSchemeTest.java
[add] https://crrev.com/bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4/chrome/test/data/android/content_url_load_content_worker.html
[add] https://crrev.com/bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4/chrome/test/data/android/content_url_make_cors_to_content.html
[add] https://crrev.com/bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4/chrome/test/data/android/worker.js
[modify] https://crrev.com/bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4/content/browser/android/content_url_loader_factory.cc
[modify] https://crrev.com/bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4/content/browser/loader/file_url_loader_factory.cc
[modify] https://crrev.com/bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4/services/network/public/cpp/cors/cors.cc
[modify] https://crrev.com/bfefdbf7aa0bab97a500b989cd5a53e13b0cfee4/services/network/public/cpp/cors/cors.h


### [Deleted User] (2020-06-23)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### na...@google.com (2020-07-13)

[Empty comment from Monorail migration]

### ad...@chromium.org (2020-07-13)

[Empty comment from Monorail migration]

### wy...@gmail.com (2020-07-15)

Hello, there is something wrong with the credit info of CVE-2020-6516 in 'https://chromereleases.googleblog.com/2020/07/stable-channel-update-for-desktop.html'

Would you modify it to "Yongke Wang(@Rudykewang) and Aryb1n(@aryb1n) of Tencent Security Xuanwu Lab (腾讯安全玄武实验室）"?

I have offered the info in 'https://bugs.chromium.org/p/chromium/issues/detail?id=1092025'. Thanks!

### ad...@chromium.org (2020-07-15)

Done. Thanks!

### ad...@google.com (2020-07-22)

[Empty comment from Monorail migration]

### ad...@google.com (2020-07-23)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-07-23)

Congratulations wykcomputer@. The VRP panel has decided to award $20000 for this report. (This also covers https://crbug.com/chromium/1096677). A member of our finance team will be in touch to arrange payment.

### ad...@google.com (2020-07-23)

[Empty comment from Monorail migration]

### qi...@chromium.org (2020-08-28)

[Empty comment from Monorail migration]

### [Deleted User] (2020-09-29)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1092449?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1092025]
[Monorail mergedwith: crbug.com/chromium/1107100]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052523)*
