# Security:  heap-use-after-free on BrandcodeConfigFetcher::OnSimpleLoaderComplete

| Field | Value |
|-------|-------|
| **Issue ID** | [40935719](https://issues.chromium.org/issues/40935719) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | UI>Browser>Profiles |
| **Platforms** | Linux, Mac, Windows, ChromeOS |
| **Reporter** | 18...@gmail.com |
| **Assignee** | rs...@chromium.org |
| **Created** | 2023-10-10 |
| **Bounty** | $3,000.00 |

## Description

##  report

Hey, I want to report a UAF bug in `|BrandcodeConfigFetcher::OnSimpleLoaderComplete|` [1] .

``` c++
void BrandcodeConfigFetcher::OnSimpleLoaderComplete(
    std::unique_ptr<std::string> response_body) {
  if (response_body && simple_url_loader_->ResponseInfo() &&
      simple_url_loader_->ResponseInfo()->mime_type == "text/xml") {
    [...]
  } else {
    std::move(fetch_callback_).Run();   //  [+] @a
  }
  simple_url_loader_.reset();   //  [+] @b
  download_timer_.Stop();
}
```

at @a, we run `|fetch_callback_|` first, at `@b`, we access `|this object field simple_url_loader_|`.

In function `|ResetSettingsHandler::HandleResetProfileSettings|` [2] , we could see we bind function `|ResetSettingsHandler::ResetProfile|` to `|fetch_callback_|`:

``` c++
  if (config_fetcher_ && config_fetcher_->IsActive()) {
    // Reset once the prefs are fetched.
    config_fetcher_->SetCallback(base::BindOnce(    //  [+] set `|fetch_callback_|`
        &ResetSettingsHandler::ResetProfile, base::Unretained(this),
        callback_id, send_settings, request_origin));
  }
```

It means `|std::move(fetch_callback_).Run()|` will final `|ResetSettingsHandler::ResetProfile|` [3] , and `|ResetSettingsHandler::ResetProfile|` will free this `|BrandcodeConfigFetcher::OnSimpleLoaderComplete|` object, which lead to UAF bug.

``` c++
void ResetSettingsHandler::ResetProfile(
    const std::string& callback_id,
    bool send_settings,
    reset_report::ChromeResetReport::ResetRequestOrigin request_origin) {
  CHECK(!GetResetter()->IsActive());

  std::unique_ptr<BrandcodedDefaultSettings> default_settings;
  if (config_fetcher_) {
    DCHECK(!config_fetcher_->IsActive());
    default_settings = config_fetcher_->GetSettings();
    config_fetcher_.reset();    //  [+] free |BrandcodeConfigFetcher| object
  } else {
    DCHECK(brandcode_.empty());
  }
  [...]
}
```

1. https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/profile_resetter/brandcode_config_fetcher.cc;l=108
2. https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/settings/reset_settings_handler.cc;l=147
3. https://source.chromium.org/chromium/chromium/src/+/main:chrome/browser/ui/webui/settings/reset_settings_handler.cc;l=237

## Attachments

- [repro.diff](attachments/repro.diff) (text/plain, 1.2 KB)
- [asan.log](attachments/asan.log) (text/plain, 35.6 KB)
- [repro.mp4](attachments/repro.mp4) (video/mp4, 9.7 MB)
- [asan.txt](attachments/asan.txt) (text/plain, 29.9 KB)

## Timeline

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### 18...@gmail.com (2023-10-10)

To reproduce the bug, my chromium version:

```
PS D:\found_new_bug\src> git log
commit 3dfd75b7f885d39eb5c712fa2ba9f65020558796 (grafted, HEAD, origin/main)
Author: Rupert Wiser <bewise@chromium.org>
Date:   Thu Sep 28 12:08:08 2023 +0000
```

apply repro.diff 

>   git apply < repro.diff

compile it with asan version, my args.gn content:

```
# Build arguments go here.
# See "gn args <out_dir> --list" for available build arguments.
is_debug = false
is_asan = true
dcheck_always_on = false
enable_rust = false
treat_warnings_as_errors = false
```

run chrome by `|out/asan/chrome.exe|` , Then use this step to repro it:

1. choose settings
2. choose reset settings
3. choose restore settings to their original defaults
4. click `reset settings` in its dialog.(click this fast)
4. asan log should generate.

##  note

### This repro.patch

In this repro patch, I use to thing to help me repro the bug. It's ok, it just |simulate| some case, which won't influnce the security.

first:

```
+  // [+] set a fake brand code
+  std::string holy = "just_for_test";
+  brand->assign(holy);
+  return true;
```

I set a fake brand code, chromium will set the real brand code, but seems it only set in the release version. So I use a fake code.

```
-      GURL("https://tools.google.com/service/update2"), brandcode_);
+      GURL("http://localhost:8085"), brandcode_);
```

chromium originally to get the profile from `|https://tools.google.com/service/update2|`, I change it to my own website `|http://localhost:8085|`, It just make we could got nothing which in this request.

At here, we don't have server named `|http://localhost:8085|`, which means it will return empty response, which will help us to reproduce the bug.

Another way could archive same thing:

1. DNS overwrite
2. The user network speed is too slow.

### bitset

seems this patch introduce this model:

-   https://chromium-review.googlesource.com/c/chromium/src/+/1890819

##  patch:

```
  if (response_body && simple_url_loader_->ResponseInfo() &&
      simple_url_loader_->ResponseInfo()->mime_type == "text/xml") {
    data_decoder::DataDecoder::ParseXmlIsolated(
        *response_body,
        data_decoder::mojom::XmlParser::WhitespaceBehavior::kIgnore,
        base::BindOnce(&BrandcodeConfigFetcher::OnXmlConfigParsed,
                       weak_ptr_factory_.GetWeakPtr()));
    simple_url_loader_.reset();
    download_timer_.Stop();
  } else {
    simple_url_loader_.reset();
    download_timer_.Stop();
    std::move(fetch_callback_).Run();
  }
}
```

change the code like this should fix the bug, ugly but should work.

##  strange

I think the bug is strange:

1. The bug should be easily trigger and found, so I guess this bug exists because this module don't have enough unit_tests.
    1.1 see chrome/browser/ui/webui/settings/reset_settings_handler_unittest.cc.
2. The bug need user interactive, but the vulnerability happened out-sandbox. And we don't need rce bug in the sandbox. So maybe we should mark it as sec-critical.
3. A video maybe will help u reproduce it, but I don't find suitable app. I will upload it soon.

### 18...@gmail.com (2023-10-10)

[Empty comment from Monorail migration]

### kr...@chromium.org (2023-10-10)

[Empty comment from Monorail migration]

[Monorail components: UI>Browser>Profiles]

### kr...@chromium.org (2023-10-10)

Nice find, reading the code I think you are right. rsesek@ do you think this is correct? I agree it seems strange a UAF in browser process has survived this long.

### [Deleted User] (2023-10-10)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-11)

Setting milestone and target because of high severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2023-10-11)

Setting Pri-0 to match security severity Critical. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### kr...@google.com (2023-10-11)

[Empty comment from Monorail migration]

### kr...@google.com (2023-10-11)

Downgrading to high due to user interactions needed.

### rs...@chromium.org (2023-10-11)

Yes, seems valid. The test for my patch without the corresponding fix triggers an ASan.

https://chromium-review.googlesource.com/c/chromium/src/+/4931200

### rs...@chromium.org (2023-10-11)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-12)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/6f476b91d6c15c26da23ca78d4905332c15bb1c3

commit 6f476b91d6c15c26da23ca78d4905332c15bb1c3
Author: Robert Sesek <rsesek@chromium.org>
Date: Thu Oct 12 16:40:17 2023

Don't access `this` in BrandcodeConfigFetcher after running the callback

The callback in BrandcodeConfigFetcher::OnSimpleLoaderComplete can be
run synchronously, which may delete `this`. Avoid accessing member
variables after running the callback to avoid a use-after-free.

Fixed: 1491296
Change-Id: Id8ce7ce5cde13a81f213f6c54d62de62b566e993
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4931200
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Commit-Position: refs/heads/main@{#1208889}

[modify] https://crrev.com/6f476b91d6c15c26da23ca78d4905332c15bb1c3/chrome/browser/profile_resetter/brandcode_config_fetcher.cc
[modify] https://crrev.com/6f476b91d6c15c26da23ca78d4905332c15bb1c3/chrome/browser/profile_resetter/profile_resetter_unittest.cc


### [Deleted User] (2023-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-12)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-12)

Requesting merge to stable M118 because latest trunk commit (1208889) appears to be after stable branch point (1192594).

Requesting merge to beta M119 because latest trunk commit (1208889) appears to be after beta branch point (1204232).

Thank you for fixing this security bug! We aim to ship security fixes as quickly as possible, to limit their opportunity for exploitation as an "n-day" (that is, a bug where git fixes are developed into attacks before those fixes reach users).

Sheriffbot has determined this fix is necessary on milestone(s): [].

Please answer the following questions so that we can safely process this merge request:
1. Which CLs should be backmerged? (Please include Gerrit links.)
2. Has this fix been tested on Canary?
3. Has this fix been verified to not pose any stability regressions and does it pose potential stability risks?
4. Does this fix pose any known compatibility risks?
5. Does it require manual verification by the test team? If so, please describe required testing.


For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### 18...@gmail.com (2023-10-13)

[Comment Deleted]

### 18...@gmail.com (2023-10-13)

if there are a cve for this, please credit as : @18楼梦想改造家. thx.

### [Deleted User] (2023-10-13)

Merge review required: M118 is already shipping to stable.

Please answer the following questions so that we can safely process your merge request:
1. Why does your merge fit within the merge criteria for these milestones?
- Chrome Browser: https://chromiumdash.appspot.com/branches
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. What changes specifically would you like to merge? Please link to Gerrit.
3. Have the changes been released and tested on canary?
4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?
5. [Chrome OS only]: Was the change reviewed and approved by the Eng Prod Representative? https://goto.google.com/cros-engprodcomponents
6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

Please contact the milestone owner if you have questions.
Owners: govind (Android), govind (iOS), ceb (ChromeOS), danielyip (Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2023-10-16)

> 1. Why does your merge fit within the merge criteria for these milestones?

Sev-High security bug fix.

> 2. What changes specifically would you like to merge? Please link to Gerrit.

https://chromium-review.googlesource.com/c/chromium/src/+/4931200

> 3. Have the changes been released and tested on canary?

Yes

> 4. Is this a new feature? If yes, is it behind a Finch flag and are experiments active in any release channels?

No

> 6. If this merge addresses a major issue in the stable channel, does it require manual verification by the test team? If so, please describe required testing.

No

### am...@chromium.org (2023-10-17)

119 and 118 merges approved for https://crrev.com/c/4931200, please merge this fix to M119 / branch 6045 at your earliest availability so this fix can be included in next 119/beta 
For 118, please merge this fix to branch 5993 by EOD Thursday 19 October so this fix can be included in the next M118 Stable update

### gi...@appspot.gserviceaccount.com (2023-10-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/78f958a002267994d67ad53bbbe03d98d88be0ae

commit 78f958a002267994d67ad53bbbe03d98d88be0ae
Author: Robert Sesek <rsesek@chromium.org>
Date: Wed Oct 18 13:23:31 2023

Don't access `this` in BrandcodeConfigFetcher after running the callback

The callback in BrandcodeConfigFetcher::OnSimpleLoaderComplete can be
run synchronously, which may delete `this`. Avoid accessing member
variables after running the callback to avoid a use-after-free.

(cherry picked from commit 6f476b91d6c15c26da23ca78d4905332c15bb1c3)

Fixed: 1491296
Change-Id: Id8ce7ce5cde13a81f213f6c54d62de62b566e993
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4931200
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1208889}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4949552
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/6045@{#633}
Cr-Branched-From: 905e8bdd32d891451d94d1ec71682e989da2b0a1-refs/heads/main@{#1204232}

[modify] https://crrev.com/78f958a002267994d67ad53bbbe03d98d88be0ae/chrome/browser/profile_resetter/brandcode_config_fetcher.cc
[modify] https://crrev.com/78f958a002267994d67ad53bbbe03d98d88be0ae/chrome/browser/profile_resetter/profile_resetter_unittest.cc


### gi...@appspot.gserviceaccount.com (2023-10-18)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/78067df8f4edf04c92fb2a5107862ca40152766f

commit 78067df8f4edf04c92fb2a5107862ca40152766f
Author: Robert Sesek <rsesek@chromium.org>
Date: Wed Oct 18 13:25:18 2023

Don't access `this` in BrandcodeConfigFetcher after running the callback

The callback in BrandcodeConfigFetcher::OnSimpleLoaderComplete can be
run synchronously, which may delete `this`. Avoid accessing member
variables after running the callback to avoid a use-after-free.

(cherry picked from commit 6f476b91d6c15c26da23ca78d4905332c15bb1c3)

Fixed: 1491296
Change-Id: Id8ce7ce5cde13a81f213f6c54d62de62b566e993
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4931200
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Vasilii Sukhanov <vasilii@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1208889}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4949910
Bot-Commit: Rubber Stamper <rubber-stamper@appspot.gserviceaccount.com>
Cr-Commit-Position: refs/branch-heads/5993@{#1338}
Cr-Branched-From: 511350718e646be62331ae9d7213d10ec320d514-refs/heads/main@{#1192594}

[modify] https://crrev.com/78067df8f4edf04c92fb2a5107862ca40152766f/chrome/browser/profile_resetter/brandcode_config_fetcher.cc
[modify] https://crrev.com/78067df8f4edf04c92fb2a5107862ca40152766f/chrome/browser/profile_resetter/profile_resetter_unittest.cc


### [Deleted User] (2023-10-18)

LTS Milestone M114

This issue has been flagged as a merge candidate for Chrome OS' LTS channel. If selected, our merge team will handle any additional merges. To help us determine if this issue requires a merge to LTS, please answer this short questionnaire:
1. Was this issue a regression for the milestone it was found in?
2. Is this issue related to a change or feature merged after the latest LTS Milestone?



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rs...@chromium.org (2023-10-18)

> 1. Was this issue a regression for the milestone it was found in?

No

> 2. Is this issue related to a change or feature merged after the latest LTS Milestone?


No

### am...@google.com (2023-10-18)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2023-10-18)

Congratulations on another one! The Chrome VRP Panel has decided to award you $2,000 for this report + $1,000 bisect bonus. The reward amount was determined based on this being a highly mitigated security bug [1], mitigated by race condition and non-standard user interaction. Thank you for your efforts and reporting this issue to us!

[1] https://bughunters.google.com/about/rules/5745167867576320/chrome-vulnerability-reward-program-rules#reward-amounts-for-mitigated-security-bugs

### 18...@gmail.com (2023-10-18)

hey,  amyressler@chromium.org, Thx for your generous. I have a little question about this. I offer a fix patch too, and I think the official fix patch is very same as it(Use same way but in different format), could I get the fix patch bonus? Thx!

### rz...@google.com (2023-10-19)

[Empty comment from Monorail migration]

### rz...@google.com (2023-10-20)

[Empty comment from Monorail migration]

### [Deleted User] (2023-10-20)

This issue requires additional review before it can be merged to the LTS channel. Please answer the following questions to help us evaluate this merge:

1. Number of CLs needed for this fix and links to them.
2. Level of complexity (High, Medium, Low - Explain)
3. Has this been merged to a stable release? beta release?
4. Overall Recommendation (Yes, No)



For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### rz...@google.com (2023-10-20)

1. https://crrev.com/c/4954540
2. Low, no conflicts
3. 118, 119
4. Yes

### am...@google.com (2023-10-23)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-24)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-25)

[Empty comment from Monorail migration]

### pg...@google.com (2023-10-25)

[Empty comment from Monorail migration]

### gm...@google.com (2023-10-26)

[Empty comment from Monorail migration]

### na...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### na...@google.com (2023-10-30)

[Empty comment from Monorail migration]

### gi...@appspot.gserviceaccount.com (2023-10-31)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/33da254f34804d83f69e09a9787cfd0bca5a3218

commit 33da254f34804d83f69e09a9787cfd0bca5a3218
Author: Robert Sesek <rsesek@chromium.org>
Date: Tue Oct 31 15:36:59 2023

[M114-LTS] Don't access `this` in BrandcodeConfigFetcher after running the callback

The callback in BrandcodeConfigFetcher::OnSimpleLoaderComplete can be
run synchronously, which may delete `this`. Avoid accessing member
variables after running the callback to avoid a use-after-free.

(cherry picked from commit 6f476b91d6c15c26da23ca78d4905332c15bb1c3)

Fixed: 1491296
Change-Id: Id8ce7ce5cde13a81f213f6c54d62de62b566e993
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4931200
Commit-Queue: Robert Sesek <rsesek@chromium.org>
Cr-Original-Commit-Position: refs/heads/main@{#1208889}
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/4954540
Owners-Override: Victor Gabriel Savu <vsavu@google.com>
Reviewed-by: Victor Gabriel Savu <vsavu@google.com>
Commit-Queue: Roger Felipe Zanoni da Silva <rzanoni@google.com>
Cr-Commit-Position: refs/branch-heads/5735@{#1633}
Cr-Branched-From: 2f562e4ddbaf79a3f3cb338b4d1bd4398d49eb67-refs/heads/main@{#1135570}

[modify] https://crrev.com/33da254f34804d83f69e09a9787cfd0bca5a3218/chrome/browser/profile_resetter/brandcode_config_fetcher.cc
[modify] https://crrev.com/33da254f34804d83f69e09a9787cfd0bca5a3218/chrome/browser/profile_resetter/profile_resetter_unittest.cc


### rz...@google.com (2023-10-31)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### [Deleted User] (2024-01-18)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### is...@google.com (2024-01-18)

This issue was migrated from crbug.com/chromium/1491296?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40935719)*
