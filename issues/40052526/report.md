# Restrictions on navigation to the content scheme can be bypassed on Android

| Field | Value |
|-------|-------|
| **Issue ID** | [40052526](https://issues.chromium.org/issues/40052526) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | wy...@gmail.com |
| **Assignee** | mt...@chromium.org |
| **Created** | 2020-06-08 |
| **Bounty** | $3,000.00 |

## Description

Originally reported in https://crbug.com/chromium/1092025:

You know, chrome blocked jumping to 'content://' from 'http://' directly.

At first, we succeeded bypassing it on version 81.0.4044.138 as follows:

```
top.location = "android-app://com.android.chrome/content/media/external/downloads/xx"; //'xx' is the id of your downloaded file 
```

But, chrome filter 'content' scheme since version 83.

After deeper research, we bypassed it again by a new and interesting skill, we named it 'reflection attack':

we found that 'com.google.android.googlequicksearchbox' APP defines the following activity with 'android-app' scheme in the intent-filter, and the AppIndexingActivity class will parse the incoming 'android-app://' data to an Intent object and then send it.

```
<activity android:excludeFromRecents="true" android:exported="true" android:launchMode="singleTop" android:name="com.google.android.search.calypso.AppIndexingActivity" android:noHistory="true" android:process=":search" android:taskAffinity="" android:theme="@android:style/Theme.NoDisplay">
    <intent-filter>
        <action android:name="android.intent.action.VIEW"/>
        <category android:name="android.intent.category.BROWSABLE"/>
        <category android:name="android.intent.category.DEFAULT"/>
        <data android:scheme="android-app"/>
    </intent-filter>
</activity>
```

So, we can jump to 'com.google.android.googlequicksearchbox' APP, then jump back to chrome as follows:

```
top.location = "android-app://com.google.android.googlequicksearchbox/android-app/com.android.chrome/content/media/external/downloads/xx"; //'xx' is the id of your downloaded file 
```

...


As for the cross-domain jumping bug, the chrome has realized the bug and taken measures to filter 'content' scheme of 'android-app://' since version 83.

```
//components/external_intents/android/java/src/org/chromium/components/external_intents/ExternalNavigationHandler.java

/** The "content:" scheme is disabled in Clank. Do not try to start an activity. */
private boolean hasContentScheme(
        ExternalNavigationParams params, Intent targetIntent, boolean hasIntentScheme) {
    String url;
    if (hasIntentScheme) {
        url = targetIntent.getDataString();
        if (url == null) return false;
    } else {
        url = params.getUrl();
    }
    if (!url.startsWith(UrlConstants.CONTENT_URL_SHORT_PREFIX)) return false;
    if (DEBUG) Log.i(TAG, "Navigation to content: URL");
    return true;
}
```

But, the security of chrome is also influenced by external environment, such as system apps.

Chrome accepts intents from external app with "content://" data as follows, so we can jump to 'com.google.android.googlequicksearchbox' APP, then jump back to chrome.

```
<activity-alias n1:exported="true" n1:name="com.google.android.apps.chrome.IntentDispatcher" n1:targetActivity="org.chromium.chrome.browser.document.ChromeLauncherActivity">
    <intent-filter>
        <action n1:name="android.intent.action.VIEW"/>
        <category n1:name="android.intent.category.DEFAULT"/>
        <category n1:name="android.intent.category.BROWSABLE"/>
        <category n1:name="com.google.intent.category.DAYDREAM"/>
        <data n1:scheme="googlechrome"/>
        <data n1:scheme="http"/>
        <data n1:scheme="https"/>
        <data n1:scheme="about"/>
        <data n1:scheme="javascript"/>
        <data n1:scheme="content"/>
        <data n1:mimeType="text/html"/>
        <data n1:mimeType="text/plain"/>
        <data n1:mimeType="application/xhtml+xml"/>
    </intent-filter>
</activity-alias>
```


## Timeline

### mb...@chromium.org (2020-06-08)

[Empty comment from Monorail migration]

### mt...@chromium.org (2020-06-08)

The GSA AppIndexingActivity is kind of sketchy, it's using regex to parse URIs, and send an intent based off of the BROWSABLE intent URI. It's at least keeping the BROWSABLE category on the intent as far as I can tell.

I think we need to either remove BROWSABLE from out intent filters that handle content: URIs, or we need to somehow be much more careful with handling incoming content URIs (but I'd have to leave that to somebody who understands how content: URIs work)

cc rsesek and tedchoc for opinions

### te...@chromium.org (2020-06-08)

We've had content:// present since upstreaming:
https://source.chromium.org/chromium/chromium/src/+/2f7c5984b86186dedeb17d551b9159df0462a8b5:chrome/android/java/AndroidManifest.xml;drc=2f7c5984b86186dedeb17d551b9159df0462a8b5;l=153?originalUrl=%2F

Granted, I thought it was primarily present for handling mhtml and offline content., but I believe the content URIs also allows viewing HTML content from file viewer applications (I believe Samsung in particular uses this...or at least I think I've gotten bugs about that in the past).

### mt...@chromium.org (2020-06-08)

Right, what's not clear to me is when supporting the browsable category on those intents would be necessary. Should untrusted content be able to launch content URIs as this bug managed to do?

### te...@chromium.org (2020-06-08)

In general, I don't see why we'd need BROWSABLE on content intent filters, but I'm not sure if we have cases where we send content URIs to ourselves via an intent.

+dimich and +qinmin for historical content intent knowledge.

### mt...@chromium.org (2020-06-08)

If we're sending to ourselves via an intent, then we shouldn't actually care what the filter specifies, as we use explicit intents.

(Sidenote, I often wonder just how many app bugs could be exposed with explicit intents that don't conform to what we expect to receive with our filters)

### [Deleted User] (2020-06-09)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-06-09)

Setting Pri-1 to match security severity Medium. If this is incorrect, please reset the priority. Sheriffbot won't make this change again.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2020-06-09)

[Empty comment from Monorail migration]

### ad...@google.com (2020-06-09)

[Empty comment from Monorail migration]

### mt...@chromium.org (2020-06-16)

ping dimich, qinmin. Thoughts?

### qi...@chromium.org (2020-06-16)

For system apps, it is possible that they launch an intent to open a downloaded html file, so I guess we still need to support those.

But I guess with https://chromium-review.googlesource.com/c/chromium/src/+/2240040 landed, we can probably stop content URI from being launched if the intent has EXTRA_REQUEST_METADATA_TOKEN in it?  It that happens, chrome cannot launch a renderer initiated or a non-user gesture intent with content URI to itself, but other apps can still do that?


### [Deleted User] (2020-07-01)

mthiesse: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-07-02)

mthiesse: Uh oh! This issue still open and hasn't been updated in the last 15 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mt...@chromium.org (2020-07-02)

Whoops, somehow missed your response qinmin@.

I don't think I understand your comment though, are you suggesting that when the system apps launch an intent to open a file they apply the BROWSABLE category? I'm not suggesting we remove content: intent support, just that we remove the BROWSABLE category from it as we shouldn't allow content URIs from untrusted sources like web pages.

Feels like a big hack to look at an intent extra and block it if Chrome provided the extra, and wouldn't work anyways because googlequicksearchbox doesn't preserve Extras.

### qi...@chromium.org (2020-07-06)

So what I mean is that we check if EXTRA_REQUEST_METADATA_TOKEN extra exists in the intent. If the extra indicates that the intent is renderer initiated or without user gesture, then we ignore the intent if it is a content URI. Otherwise, we will launch the URI.

### mt...@chromium.org (2020-07-06)

As I said, that wouldn't work anyways for this issue as that extra would be dropped.

### mt...@chromium.org (2020-07-23)

ping dimich, qinmin

### qi...@chromium.org (2020-07-23)

I am fine removing BROWSERSABLE category for content scheme. I don't know if there are any cases we are using it today inside Chrome, as I cannot find any usage of  content URIs links.


### mt...@chromium.org (2020-07-28)

[Empty comment from Monorail migration]

### bu...@chops-service-accounts.iam.gserviceaccount.com (2020-08-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/f10e7b2e87322ec19701cea0f868dc4197cf8d5f

commit f10e7b2e87322ec19701cea0f868dc4197cf8d5f
Author: Michael Thiessen <mthiesse@chromium.org>
Date: Fri Aug 07 19:15:53 2020

Remove BROWSABLE category from content URI intent filters

Chrome does not allow sites to navigate to content URIs, but the Google
Search app parses and re-sends URIs, including content URIs, sent to it.
This allows intents sent to GSA to bypass this content URI restriction.

In order to prevent this bypass, we can simply remove the BROWSABLE
category from our intent filters that handle content URIs, as we don't
need to handle content URIs coming from other browsers.

This change also adds tests for our Intent Filters, which, as far as I
can tell, were untested before this change. I also fixed a few edge
cases with the intent filters I modified as revealed by the tests.

Note that for some intent filters I removed the content scheme
altogether. In these cases the filter wasn't useful because a file
extension was specified, making it impossible for the content scheme to
be matched.

I also suppressed some AppLinkUrlErrors: "Error: Activity supporting
ACTION_VIEW is not set as BROWSABLE". This isn't an error. I don't know
why lint flags it other than to make sure you know what you're doing and
don't accidentally prevent browsers from launching your View intent
Activity.

Bug: 1092453
Change-Id: I167d2e41c0d9c75c0b80a5a1778817b42016e21b
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2321522
Commit-Queue: Michael Thiessen <mthiesse@chromium.org>
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Reviewed-by: Ted Choc <tedchoc@chromium.org>
Cr-Commit-Position: refs/heads/master@{#796040}

[modify] https://crrev.com/f10e7b2e87322ec19701cea0f868dc4197cf8d5f/chrome/android/chrome_test_java_sources.gni
[modify] https://crrev.com/f10e7b2e87322ec19701cea0f868dc4197cf8d5f/chrome/android/expectations/monochrome_public_bundle.AndroidManifest.expected
[modify] https://crrev.com/f10e7b2e87322ec19701cea0f868dc4197cf8d5f/chrome/android/expectations/trichrome_chrome_bundle.AndroidManifest.expected
[modify] https://crrev.com/f10e7b2e87322ec19701cea0f868dc4197cf8d5f/chrome/android/java/AndroidManifest.xml
[add] https://crrev.com/f10e7b2e87322ec19701cea0f868dc4197cf8d5f/chrome/android/javatests/src/org/chromium/chrome/browser/IntentFilterUnitTest.java


### mt...@chromium.org (2020-08-10)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-10)

[Empty comment from Monorail migration]

### ad...@google.com (2020-08-17)

[Empty comment from Monorail migration]

### [Deleted User] (2020-08-17)

Requesting merge to beta M85 because latest trunk commit (796040) appears to be after beta branch point (782793).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2020-08-17)

This bug requires manual review: We are only 7 days from stable.
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
Owners: benmason@(Android), bindusuvarna@(iOS), dgagnon@(ChromeOS), srinivassista@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### go...@chromium.org (2020-08-17)

+adetaylo@ for M85 merge review and approval. Thank you.

 Please note we're cutting M85 Stable RC tomorrow, Tuesday noon (PDT). 

### ad...@google.com (2020-08-17)

mthiesse@ - normally we'd merge externally-reported medium severity fixes to beta, but this doesn't look like a trivial fix. M85 is not very far away. Could you comment on your confidence in this fix? We'd need to be absolutely 100% sure that there were no compatibility concerns before merging this, and it looks to me that it's difficult to make that statement with anything that relates to intent handling? So I'm minded to have this fix wait for M86. WDYT?

### mt...@chromium.org (2020-08-17)

I think waiting for M86 would be prudent, this change is fairly likely to pose compatibility concerns.

### ad...@chromium.org (2020-08-17)

Thanks!

### ad...@google.com (2020-08-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### ad...@google.com (2020-08-19)

Thanks for this part of your bug chain along with all the others wykcomputer@. The VRP panel has decided to award $3000 for this bit.

### ad...@google.com (2020-08-20)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-01)

[Empty comment from Monorail migration]

### ad...@google.com (2020-10-05)

[Empty comment from Monorail migration]

### ad...@google.com (2020-11-03)

[Empty comment from Monorail migration]

### [Deleted User] (2020-11-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1092453?no_tracker_redirect=1

[Monorail blocking: crbug.com/chromium/1092025]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40052526)*
