from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from typing import Optional
from llm.client import LLMClient
from ui.state import UIStateManager
from ui.components.chat import render_chat_messages

def register_chat_callbacks(app, llm_client: Optional[LLMClient], ui_state: UIStateManager):
    """Register chat-related callbacks"""
    
    @app.callback(
        [Output("main-chat-history", "children"),
         Output("main-chat-input", "value"),
         Output("current-job-store", "data"),
         Output("message-trigger", "data")],
        [Input("main-chat-send", "n_clicks"),
         Input("main-chat-input", "n_submit")],
        [State("main-chat-input", "value"),
         State("message-trigger", "data")],
        prevent_initial_call=True
    )
    def handle_chat(n_clicks, n_submit, user_input, trigger):
        if not user_input:
            raise PreventUpdate
        
        # Add user message
        ui_state.add_chat_message("user", user_input)
        
        # Process with LLM
        if llm_client:
            messages = [
                {"role": msg.role, "content": msg.content}
                for msg in ui_state.chat_messages
            ]
            
            response = llm_client.process_message(messages)
            
            if response["type"] == "tool_use":
                ui_state.add_chat_message(
                    "assistant",
                    response["message"],
                    response["job_id"]
                )
                ui_state.create_job_state(response["job_id"])
                current_job = response["job_id"]
            else:
                ui_state.add_chat_message("assistant", response["message"])
                current_job = ui_state.current_job_id
        else:
            ui_state.add_chat_message(
                "assistant",
                "No LLM client available. Please set ANTHROPIC_API_KEY."
            )
            current_job = None
        
        chat_elements = render_chat_messages(ui_state.chat_messages)
        
        return chat_elements, "", current_job, (trigger or 0) + 1

    @app.callback(
        Output("main-chat-history", "children", allow_duplicate=True),
        [Input("update-interval", "n_intervals")],
        prevent_initial_call=True
    )
    def update_chat_on_interval(n_intervals):
        """Update chat display based on interval (for real-time updates)"""
        if n_intervals is None:
            raise PreventUpdate
        
        # Re-render chat messages to catch any new assistant messages
        chat_elements = render_chat_messages(ui_state.chat_messages)
        return chat_elements
