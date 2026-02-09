from dotenv import load_dotenv
from groq import Groq
import json
import re


load_dotenv()

groq = Groq()

def classify_with_llm(log_msg):

    prompt = f'''The given log messages are from linux auth.log.
    Analyze them and find if there is any anomalous behaviour or not.
    Give a one-word output from either of the following words:
    (1) Anomalous, (2) Normal
    Remember: The output must only contain either of the two words above.
    No explanation is needed.
    Log messages: {log_msg}'''

    chat_completion = groq.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
        temperature=0.5
    )

    content = chat_completion.choices[0].message.content
    # match = re.search(r'<category>(.*)<\/category>', content, flags=re.DOTALL)
    #category = "Unclassified"
    # if match:
    #     category = match.group(1)
    
    # category = match.group(1)

    # return category
    return content


if __name__ == "__main__":

#     log_seq = f'''
# aadil-Victus gdm-launch-environment]: pam_unix(gdm-launch-environment:session): session opened for user gdm(uid=120) by (uid=0)
# aadil-Victus systemd-logind[921]: New session c1 of user gdm.
# aadil-Victus (systemd): pam_unix(systemd-user:session): session opened for user gdm(uid=120) by gdm(uid=0)
# aadil-Victus polkitd[895]: Registered Authentication Agent for unix-session:c1 (system bus name :1.38 [/usr/bin/gnome-shell], object path /org/freedesktop/PolicyKit1/AuthenticationAgent, locale en_US.UTF-8)
# aadil-Victus gdm-password]: gkr-pam: unable to locate daemon control file
# aadil-Victus gdm-password]: gkr-pam: stashed password to try later in open session
# aadil-Victus gdm-password]: pam_unix(gdm-password:session): session opened for user aadil(uid=1000) by aadil(uid=0)
# aadil-Victus systemd-logind[921]: New session 2 of user aadil.
# aadil-Victus (systemd): pam_unix(systemd-user:session): session opened for user aadil(uid=1000) by aadil(uid=0)
# aadil-Victus gdm-password]: gkr-pam: unlocked login keyring
# aadil-Victus gnome-keyring-daemon[2202]: The PKCS#11 component was already initialized
# type="error", sender=":1.79" (uid=1000 pid=2199 comm="/usr/bin/wireplumber" label="unconfined") interface="(unset)" member="(unset)"
# '''

#     log_seq = '''
# combo sshd(pam_unix)[19939]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
# combo sshd(pam_unix)[19937]: check pass; user unknown
# combo sshd(pam_unix)[19937]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=218.188.2.4 
# combo sshd(pam_unix)[20882]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo sshd(pam_unix)[20884]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo sshd(pam_unix)[20883]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo sshd(pam_unix)[20885]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo sshd(pam_unix)[20886]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo sshd(pam_unix)[20892]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo sshd(pam_unix)[20893]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo sshd(pam_unix)[20896]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo sshd(pam_unix)[20897]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo sshd(pam_unix)[20898]: authentication failure; logname= uid=0 euid=0 tty=NODEVssh ruser= rhost=220-135-151-1.hinet-ip.hinet.net  user=root
# combo su(pam_unix)[21416]: session opened for user cyrus by (uid=0)
# combo su(pam_unix)[21416]: session closed for user cyrus
# '''

    log_seq = '''
aadil-Victus dbus-daemon[886]: [system] Rejected send message, 0 matched rules; type="error", sender=":1.79" (uid=1000 pid=2199 comm="/usr/bin/wireplumber" label="unconfined") interface="(unset)" member="(unset)" error name="org.bluez.MediaEndpoint1.Error.NotImplemented" requested_reply="0" destination=":1.3" (uid=0 pid=885 comm="/usr/libexec/bluetooth/bluetoothd" label="unconfined")
aadil-Victus dbus-daemon[886]: [system] Rejected send message, 0 matched rules; type="error", sender=":1.79" (uid=1000 pid=2199 comm="/usr/bin/wireplumber" label="unconfined") interface="(unset)" member="(unset)" error name="org.bluez.MediaEndpoint1.Error.NotImplemented" requested_reply="0" destination=":1.3" (uid=0 pid=885 comm="/usr/libexec/bluetooth/bluetoothd" label="unconfined")
aadil-Victus dbus-daemon[886]: message repeated 16 times: [ [system] Rejected send message, 0 matched rules; type="error", sender=":1.79" (uid=1000 pid=2199 comm="/usr/bin/wireplumber" label="unconfined") interface="(unset)" member="(unset)" error name="org.bluez.MediaEndpoint1.Error.NotImplemented" requested_reply="0" destination=":1.3" (uid=0 pid=885 comm="/usr/libexec/bluetooth/bluetoothd" label="unconfined")]
aadil-Victus dbus-daemon[886]: [system] Rejected send message, 0 matched rules; type="error", sender=":1.79" (uid=1000 pid=2199 comm="/usr/bin/wireplumber" label="unconfined") interface="(unset)" member="(unset)" error name="org.bluez.MediaEndpoint1.Error.NotImplemented" requested_reply="0" destination=":1.3" (uid=0 pid=885 comm="/usr/libexec/bluetooth/bluetoothd" label="unconfined")
'''

    print(classify_with_llm(log_seq))