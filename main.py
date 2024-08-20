from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from langchain_core.messages import HumanMessage, SystemMessage
from Agent.agent import ChatStateGraph
from Agent.prompt import get_prompt
import uvicorn
import json

app = FastAPI()
agent = ChatStateGraph()
thread_record = set()


class InputRequest(BaseModel):
    thread_id: str
    user_input: str

    def __repr__(self):
        return f"InputRequest(thread_id={self.thread_id}, user_input={self.user_input})"


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat")
async def chat(thread_id: str = Query(..., description="The thread ID"), user_input: str = Query(..., description="The user input"), file: Optional[UploadFile] = None):
    user_input = user_input
    config = {"configurable": {"thread_id": thread_id}}
    if not thread_id:
        raise HTTPException(status_code=404, detail="Thread not found")
    else:
        if file is not None:
            # Process the file
            contents = await file.read()
            contents = contents.decode("utf-8")
            user_input += '\n' + \
                f"filename: {file.filename}\n" + contents
        if thread_id in thread_record:
            message = {"messages": [HumanMessage(content=user_input)]}
        else:
            message = {"messages": [SystemMessage(content=get_prompt()),
                                    HumanMessage(content=user_input)]}
        thread_record.add(thread_id)
        r = agent.graph.invoke(message, config)
        s = r["messages"][-1].content
        # Remove the triple backticks and "json" label
        s = s.replace("```json\n", "").replace("\n```", "")
        # Load the string as JSON
        data = json.loads(s)
        return data


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
