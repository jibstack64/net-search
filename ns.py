# import required libraries
import subprocess
import sys

# the base command for net user
# parameters are received through args
COMMAND = f"net user{(' ' if len(sys.argv) > 1 else '')+' '.join(sys.argv[1:])}"

#/ core /#

class Account:
    "Holds an account's information."

    def generate(output: str) -> "Account":
        "Generates an account object from a net user output."

        m = {}
        for l in output.split("\n"):
            if l == "The command completed successfully.":
                break
            else:
                switch = False
                key, value = "", ""
                for x in range(0, len(l)):
                    if x < len(l)-1:
                        if l[x] == " " and l[x+1] == " ":
                            switch = True
                    if not switch:
                        key += l[x]
                    else:
                        value += l[x]
                m[key.strip()] = value.strip()

        return Account(**m)

    def __init__(self, **values) -> None:
        # store the raw dictionary
        self._raw = values

        self.username = values.get("User name")
        self.full_name = values.get("Full Name")
        self.comment = values.get("Comment")
        self.self_comment = values.get("User's comment")
        self.region = values.get("Country/region code")
        self.active = values.get("Account active") == "Yes"
        self.expires = values.get("Account expires")

        self.password_last_set = values.get("Password last set")
        self.password_expires = values.get("Password expires")
        self.password_required = values.get("Password required") == "Yes"
        self.user_change_password = values.get("User may change password") == "Yes"

#/ utility /#

def execute(command: str) -> tuple[int, str]:
    "Executes `command` then returns the code and output."
    
    x = subprocess.Popen(list(command.split(" ")), stdout=subprocess.PIPE)
    return x.returncode if x.returncode != None else 0, x.stdout.read().decode()

def purify(output: str) -> str:
    "Purifies command output from annoying breaks and such."

    return output.replace("\r", "")

#/ main /#

lines = purify(execute(COMMAND)[1].split("-")[-1].split("The command completed successfully.")[0]).split("\n")

j = "".join(lines)
unames, i = [], 0
for x in range(0, len(j)):
    if i > len(unames)-1:
        unames.append("")
    if j[x] != " ":
        unames[i] += j[x]
    if x < len(j)-1:
        if j[x+1] != " " and j[x] == " ":
            i += 1


# now get account information

accounts: list[Account] = []
for uname in unames:
    accounts.append(Account.generate(purify(execute(f"{COMMAND} {uname}")[1])))

for account in accounts:
    if account.active and not account.password_required:
        print(f"PERFECT: '{account.username}'")
    elif not account.active and not account.password_required:
        print(f"EH: '{account.username}'")
