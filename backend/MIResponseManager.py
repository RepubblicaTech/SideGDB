from pprint import pformat


class MIPromptManager:
    @staticmethod
    def formatResponseMessage(miResponse: dict) -> str:
        if (miResponse.get("message")):
            return f"[MI::{str(miResponse.get("message")).upper()}] "
        else:
            return ""

    @staticmethod
    def formatResponsePayload(miResponse: dict):
        payload = miResponse.get("payload", None)
        if (not payload):
            return ""

        formatted = ""

        match(miResponse.get("type")):
            case "log":
                return ""
            case "console":
                return str(payload)
            case "result" | "notify":
                pass
            case _:
                return pformat(payload) + "\n"

        match(miResponse.get("message")):
            case "thread-group-added":
                return f"Thread group {miResponse["payload"]["id"]} added\n"
            case "thread-group-started":
                return f"Thread group {miResponse["payload"]["id"]} started\n"
            case "thread-created":
                thread = miResponse["payload"]
                return f"Thread {thread["id"]} (group {thread["group-id"]}) created\n"
            case "cmd-param-changed":
                cmdParam = dict(miResponse["payload"])
                return f"{cmdParam["param"]} set to {cmdParam["value"]}\n"
            case "stopped":
                formatted = "Program stopped.\n"
                match(list(dict(miResponse["payload"]).keys())[0]):
                    case "reason":
                        formatted += f"Reason: {str(miResponse["payload"]["reason"]).upper()}\n"
                    case _:
                        formatted += pformat(miResponse["payload"]) + "\n"
                return formatted
            case None:
                return str(payload)
            case _:
                pass

        payloadKeys = list(dict(payload).keys())
        match(payloadKeys[0]):
            case "msg":
                formatted = payload["msg"]
            case "bkpt":
                breakpoint = payload["bkpt"]
                formatted = f"Breakpoint {breakpoint.get("number", "X")} created: {breakpoint.get("func", "<unknown>")}() @ {breakpoint.get("file", "/???.?")}:{breakpoint.get("line", "??")}"
            case "BreakpointTable":
                breakpointTable = dict(payload["BreakpointTable"])
                breakpointsList = list(breakpointTable["body"])
                if (not breakpointsList):
                    return "No breakpoints set.\n"
                formatted = "Breakpoints list:\n"
                for breakpoint in breakpointsList:
                    formatted += f"\t[{breakpoint.get("number", "X")}]: {breakpoint.get("func", "<unknown>")}() @ {breakpoint.get("file", "/???.?")}:{breakpoint.get("line", "??")}\n"
                    return formatted
            case _:
                formatted = pformat(payload)

        return formatted + "\n"
