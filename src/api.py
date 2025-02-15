from langgraph_sdk import get_sync_client
import pprint
client = get_sync_client(url="http://localhost:2024")


def fetch_backend(in_line, in_msg, in_history):
    last_chunk = None
    for chunk in client.runs.stream(
        None,  # Threadless run
        "agent",  # Name of assistant. Defined in langgraph.json.
        input={
            "in_line": in_line,
            "in_msg": in_msg,  # Fixed typo from im_msg to in_msg
            "in_history": in_history,
        },
        stream_mode="updates",
    ):
        last_chunk = chunk
        print(f"Receiving new event of type: {chunk.event}...")
        print(chunk.data)
        print("\n\n")
    
    return last_chunk