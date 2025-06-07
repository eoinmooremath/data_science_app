from dash import Input, Output, State, ctx
from dash.exceptions import PreventUpdate
from typing import Optional
from llm.client import LLMClient
from ui.state import UIStateManager
from ui.components.chat import render_chat_messages

def register_chat_callbacks(app, llm_client: Optional[LLMClient], ui_state: UIStateManager):
    """Register chat-related callbacks for LangChain agent"""
    
    @app.callback(
        [Output('main-chat-history', 'children'),
         Output('main-chat-input', 'value'),
         Output('main-chat-send', 'disabled'),
         Output('current-job-store', 'data')],
        [Input('main-chat-send', 'n_clicks'),
         Input('main-chat-input', 'n_submit')],
        [State('main-chat-input', 'value')]
    )
    def handle_chat_message(n_clicks, n_submit, message):
        """Handle chat message submission and update active job"""
        print(f"[DEBUG] Chat callback triggered: n_clicks={n_clicks}, n_submit={n_submit}, message={message}")
        
        if not message or not message.strip():
            print("[DEBUG] No message provided, preventing update")
            raise PreventUpdate
        
        current_job_id = None
        def set_job_id(job_id):
            nonlocal current_job_id
            current_job_id = job_id

        if not llm_client:
            ui_state.add_chat_message("system", "❌ LLM client not available. Please check your API key.")
            return render_chat_messages(ui_state.chat_messages), "", False, PreventUpdate.no_update
        
        # Add user message to state
        ui_state.add_chat_message("user", message.strip())
        
        try:
            print(f"[DEBUG] Processing user message: {message[:100]}...")
            
            # Process message and get the job_id via callback
            result = llm_client.process_message_sync(message.strip(), job_id_callback=set_job_id)
            print(f"[DEBUG] LLM result: {result}")
            
            # Add assistant response to state
            if result.get("success", False):
                response = result.get("response", "I completed your request.")
                print(f"[DEBUG] Assistant response: {response}")
                ui_state.add_chat_message("assistant", response)
            else:
                error_msg = result.get("error", "Unknown error occurred")
                print(f"[DEBUG] Assistant error: {error_msg}")
                ui_state.add_chat_message("assistant", f"❌ I encountered an issue: {error_msg}")
            
        except Exception as e:
            print(f"[DEBUG] Chat callback error: {str(e)}")
            ui_state.add_chat_message("assistant", f"❌ I encountered an error: {str(e)}")
        
        # Return updated chat, clear input, re-enable button, and update the active job
        print(f"[DEBUG] Returning chat messages: {ui_state.chat_messages}")
        return render_chat_messages(ui_state.chat_messages), "", False, current_job_id
    
    @app.callback(
        Output('main-chat-history', 'children', allow_duplicate=True),
        [Input('update-interval', 'n_intervals')],
        prevent_initial_call=True
    )
    def refresh_chat(n_intervals):
        """Refresh chat messages periodically"""
        return render_chat_messages(ui_state.chat_messages)
    
    @app.callback(
        Output('main-chat-clear-btn', 'n_clicks'),
        [Input('main-chat-clear-btn', 'n_clicks')],
        prevent_initial_call=True
    )
    def clear_chat_history(n_clicks):
        print(f"[DEBUG] Clear chat button pressed: n_clicks={n_clicks}")
        if n_clicks and n_clicks > 0:
            print(f"[DEBUG] Clearing chat messages. Before: {ui_state.chat_messages}")
            ui_state.chat_messages.clear()
            if llm_client:
                llm_client.clear_conversation_history()
            print(f"[DEBUG] Chat messages after clear: {ui_state.chat_messages}")
            print("🧹 Chat history cleared")
        return 0
