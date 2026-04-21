# Security: Crazy Linker on Android allows modification of Chrome APK without breaking signature

| Field | Value |
|-------|-------|
| **Issue ID** | [40082940](https://issues.chromium.org/issues/40082940) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Internals |
| **Platforms** | Android |
| **CVE IDs** | CVE-2015-6783 |
| **Reporter** | be...@gmail.com |
| **Assignee** | [Deleted User] |
| **Created** | 2015-09-29 |
| **Bounty** | $1,000.00 |

## Description

**VULNERABILITY DETAILS**  

Chrome on Android loads it's libraries using it's own fork of Android Crazy Linker, which parses Chrome APK file itself, bit differently than Android does. In particular when looking for end-of-central-directory-record signature (PK\5\6), Chrome's Crazy Linker starts searching at file size minus length of signature and Android starts searching at file size minus size of EocdRecord. This leads to Chrome-specific variant of Android "Master Key" bug.

**VERSION**  

Chrome Version: 45.0.2454.94 stable  

Operating System: Android

**REPRODUCTION CASE**  

Unpack attached archive, copy properly signed chrome apk as base.apk and run crazyzip.py to create output.apk. (10MB attachment size limit doesn't allow me attaching generated apk)  

Then install output.apk on Android device with ARM architecture, it will replace currently installed Chrome. Modified version will just run "id > /sdcard/chrome-id.txt" and exit. Note that this "update" will have access to files that normal Chrome has (such as cookies). Also note that installing this through on device installer will not work if there's already installed Chrome with same or greater versionCode; in that case modified APK can be installed through adb:  

adb install -r output.apk

## Attachments

- [crazy-linker-zip.zip](attachments/crazy-linker-zip.zip) (application/zip, 3.3 KB)

## Timeline

### pa...@chromium.org (2015-09-29)

[Empty comment from Monorail migration]

### te...@chromium.org (2015-09-29)

[Empty comment from Monorail migration]

### es...@chromium.org (2015-09-29)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-09-29)

[Empty comment from Monorail migration]

### [Deleted User] (2015-09-30)

[Empty comment from Monorail migration]

### an...@chromium.org (2015-09-30)

Important mitigation: The Play Store verifies the integrity of the entire APK file after downloading to secure storage and prior to installation, so it should not be possible to MitM the APK if it is downloaded from the Play Store. Therefore this attack would require either sideloading via ADB or installing Chrome from a third party app.

### [Deleted User] (2015-09-30)

> In particular when looking for end-of-central-directory-record signature (PK\5\6), Chrome's Crazy Linker starts searching at file size minus length of signature and Android starts searching at file size minus size of EocdRecord.

Please can you explain why you see this difference as an indication that Android is immune to the APK change you have made but the crazy linker is vulnerable?

The EocdRecord is actually variable length due to the trailing 'comment' field. A comment can itself contain a full and valid EocdRecord. A search for EocdRecord must run backwards from the file end. The crazy linker begins searching at filelen-4, but while Android can start a bit back from this, if the 'valid' EocdRecord is amended so that its comment is another EocdRecord then both the crazy linker and Android will find this second EocdRecord and use it (because Android cannot start its search more than 20 bytes back from the file end, otherwise it would miss the EocdRecord it needs to find on unmodified APK files).

Thanks.


### be...@gmail.com (2015-09-30)

The vulnerability is that these zip parsers aren't working identically same, so we cannot say that one is 'immune' and other is 'vulnerable'. I've reported this here because Crazy Linker is embedded inside Chrome apk (through it's forked from Android, however zip support was added only on Chromium's fork), through maybe this should be reported to Android as well (to ban 'PK\4\5' inside zip comment).

The modified apk has at end an EocdRecord which is found by Android and in it's comment it has EocdRecord without last field (There's end of file where it should be).

So at the end of file we have:
struct EocdRecord { // Seen by Android
  uint32_t eocd_signature; // PK\5\6
  uint16_t disk_num;
  uint16_t cd_start_disk;
  uint16_t num_records_on_disk;
  uint16_t num_records;
  uint32_t cd_size;
  uint32_t cd_start_offset;
  // Android starts PK\5\6 scan here (filesize - sizeof(EocdRecord))
  uint16_t comment_length; // 20 (sizeof(EocdRecord) - 2)
};
struct EocdRecord { // Seen by Crazy Linker
  uint32_t eocd_signature; // PK\5\6
  uint16_t disk_num;
  uint16_t cd_start_disk;
  uint16_t num_records_on_disk;
  uint16_t num_records;
  uint32_t cd_size;
  // Crazy linker starts PK\5\6 scan here (filesize - sizeof("PK\4\5"))
  uint32_t cd_start_offset;
  // uint16_t comment_length; // Omitted, end of file instead
};

### [Deleted User] (2015-10-01)

> The vulnerability is that these zip parsers aren't working identically same,...

Thank you for the extra information. It is now clearer as to how this divergent behaviour can affect things. When I first asked I was thinking of Android's unzip purely in the context of loading from APK (not a real unzip), rather than the more general SHA checking.

I am looking at ways to mitigate this in the chromium linker, but it seems that while I may be able to catch some things like that, ultimately if a file owned by an app is on the device then the app code has to trust it. While an APK's _contents_ can be trusted, the outer APK itself apparently has less protection.

As you note, banning zip comments from containing the EocdRecord signature would be advisable. Ideally we should prevent such files ever landing on the device at all, perhaps through either the package manager or the Play store (or maybe both). I will see what can be done in these areas.

In the meantime, I will investigate how hard it would be to make the crazy linker's zip functionality converge with Android's used for SHA checking.

Thanks again for the fuller explanation.


### cl...@chromium.org (2015-10-02)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-10-06)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/d9e316238aee59acf665d80b544cf4e1edfd3349

commit d9e316238aee59acf665d80b544cf4e1edfd3349
Author: Simon Baldwin <simonb@chromium.org>
Date: Tue Oct 06 10:23:26 2015

crazy linker: Alter search for zip EOCD start

When loading directly from APK, begin searching backwards
for the zip EOCD record signature at size of EOCD record
bytes before the end of the file.

BUG=537205
R=rmcilroy@chromium.org

Review URL: https://codereview.chromium.org/1390553002 .

Cr-Commit-Position: refs/heads/master@{#352577}

[modify] http://crrev.com/d9e316238aee59acf665d80b544cf4e1edfd3349/third_party/android_crazy_linker/README.chromium
[modify] http://crrev.com/d9e316238aee59acf665d80b544cf4e1edfd3349/third_party/android_crazy_linker/src/src/crazy_linker_zip.cpp


### [Deleted User] (2015-10-06)

[Empty comment from Monorail migration]

### cl...@chromium.org (2015-10-06)

Adding Merge-Triage label for tracking purposes.

Once your fix had sufficient bake time (on canary, dev as appropriate), please nominate your fix for merge by adding the Merge-Requested label.

When your merge is approved by the release manager, please start merging with higher milestone label first. Make sure to re-request merge for every milestone in the label list. You can get branch information on omahaproxy.appspot.com.

- Your friendly ClusterFuzz

### [Deleted User] (2015-10-07)

[Empty comment from Monorail migration]

### ti...@google.com (2015-10-07)

Approved for M47 (branch: 2526)

### bu...@chromium.org (2015-10-07)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/7e39d690c4d9563954304ae31352ace3822caa07

commit 7e39d690c4d9563954304ae31352ace3822caa07
Author: Simon Baldwin <simonb@chromium.org>
Date: Wed Oct 07 17:00:34 2015

crazy linker: Alter search for zip EOCD start

When loading directly from APK, begin searching backwards
for the zip EOCD record signature at size of EOCD record
bytes before the end of the file.

BUG=537205
R=rmcilroy@chromium.org

Review URL: https://codereview.chromium.org/1390553002 .

Cr-Commit-Position: refs/heads/master@{#352577}
(cherry picked from commit d9e316238aee59acf665d80b544cf4e1edfd3349)

Review URL: https://codereview.chromium.org/1393813003 .

Cr-Commit-Position: refs/branch-heads/2526@{#28}
Cr-Branched-From: cb947c0153db0ec02a8abbcb3ca086d88bf6006f-refs/heads/master@{#352221}

[modify] http://crrev.com/7e39d690c4d9563954304ae31352ace3822caa07/third_party/android_crazy_linker/README.chromium
[modify] http://crrev.com/7e39d690c4d9563954304ae31352ace3822caa07/third_party/android_crazy_linker/src/src/crazy_linker_zip.cpp


### [Deleted User] (2015-10-07)

[Empty comment from Monorail migration]

### bu...@chromium.org (2015-10-08)

The following revision refers to this bug:
  https://chrome-internal.googlesource.com/bling/chromium.git/+/7e39d690c4d9563954304ae31352ace3822caa07

commit 7e39d690c4d9563954304ae31352ace3822caa07
Author: Simon Baldwin <simonb@chromium.org>
Date: Wed Oct 07 17:00:34 2015


### ti...@google.com (2015-10-12)

I understand that we're too late for M-46 for Android, so updating labels for an M-47 release. Adding kerz@ in case I'm incorrect.

### ti...@google.com (2015-10-12)

Adding reward-topanel for reward program consideration (details here: https://www.google.com/about/appsecurity/chrome-rewards/)

### pa...@google.com (2015-10-15)

[Empty comment from Monorail migration]

### ti...@google.com (2015-12-01)

Reducing severity based on mitigating factors and prerequisites for successful exploitation.

### ti...@google.com (2015-12-01)

Thanks for the report - our reward panel awarded you $1,000 for reporting this to us. Congratulations!

We'll credit you in our release notes as "Michal Bednarski". If you would prefer to use another name, please update this bug and I can update the release notes. We'll also provide a CVE ID in a few hours time for your reference.

Someone from our finance team should be in contact within a week to arrange payment. If this doesn't happen, please either update this bug or reach out to me directly at timwillis@

Thanks again for your report!

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an established charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.
********************************* 

### ti...@google.com (2015-12-01)

CVE-2015-6783

### ti...@google.com (2015-12-14)

[Empty comment from Monorail migration]

### ti...@google.com (2016-01-05)

[Empty comment from Monorail migration]

### cl...@chromium.org (2016-01-12)

Bulk update: removing view restriction from closed bugs.

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

### wf...@gmail.com (2018-12-24)

[Comment Deleted]

### is...@google.com (2018-12-24)

This issue was migrated from crbug.com/chromium/537205?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082940)*
