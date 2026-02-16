import json


def extract_core_fields(log_entry):
    """
    Extract only required core fields from a journalctl JSON log.
    Missing fields are handled safely.
    """
    return {
        "systemd_unit": log_entry.get("_SYSTEMD_UNIT"),
        "syslog_identifier": log_entry.get("SYSLOG_IDENTIFIER"),
        "priority": int(log_entry["PRIORITY"]) if "PRIORITY" in log_entry else None,
        "message": log_entry.get("MESSAGE"),
        "timestamp": int(log_entry["__REALTIME_TIMESTAMP"]) if "__REALTIME_TIMESTAMP" in log_entry else None,
        "pid": int(log_entry["_PID"]) if "_PID" in log_entry else None,
        # "hostname": log_entry.get("_HOSTNAME"),
    }


def preprocess_logs(input_log):
    try:
        log_entry = json.loads(input_log.strip())
        cleaned_entry = extract_core_fields(log_entry)

        # Skip empty or invalid messages
        if cleaned_entry["message"]:
            return cleaned_entry

    except json.JSONDecodeError:
        print("Json decode error.")
        pass  # skip malformed lines



if __name__ == "__main__":
    log_msg = '''{"_SELINUX_CONTEXT":"unconfined\\n","SYSLOG_IDENTIFIER":"wpa_supplicant","PRIORITY":"5","__REALTIME_TIMESTAMP":"1771152541827242","_HOSTNAME":"aadil-Victus","MESSAGE":"wlp4s0: CTRL-EVENT-SIGNAL-CHANGE above=1 signal=-48 noise=9999 txrate=270000","_PID":"949","_SYSTEMD_UNIT":"wpa_supplicant.service"}'''
    
    print(preprocess_logs(log_msg))