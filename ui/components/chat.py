import dash_bootstrap_components as dbc
from dash import html, dcc
from typing import List
from ui.state import ChatMessage

def create_chat_component(chat_id: str = "chat"):
    """Create the chat interface component"""
    return dbc.Card([
        dbc.CardHeader("Data Science Assistant"),
        dbc.CardBody([
            html.Div(
                id=f"{chat_id}-history",
                style={
                    "height": "400px",
                    "overflowY": "scroll",
                    "border": "1px solid #ddd",
                    "padding": "10px",
                    "borderRadius": "5px",
                    "marginBottom": "10px",
                    "backgroundColor": "#f8f9fa"
                }
            ),
            dbc.InputGroup([
                dbc.Input(
                    id=f"{chat_id}-input",
                    placeholder="Ask me to analyze data...",
                    type="text"
                ),
                dbc.Button("Send", id=f"{chat_id}-send", color="primary")
            ])
        ])
    ])

def render_chat_messages(messages: List[ChatMessage]) -> List[html.Div]:
    """Render chat messages"""
    elements = []
    
    for msg in messages:
        if msg.role == "user":
            elements.append(
                html.Div([
                    html.Strong("You: "),
                    html.Span(msg.content)
                ], style={
                    "marginBottom": "10px",
                    "padding": "10px",
                    "backgroundColor": "#e3f2fd",
                    "borderRadius": "5px",
                    "marginLeft": "20%"
                })
            )
        else:
            elements.append(
                html.Div([
                    html.Strong("Assistant: "),
                    html.Span(msg.content),
                    html.Small(f" (Job: {msg.job_id})", style={"color": "#666"}) if msg.job_id else None
                ], style={
                    "marginBottom": "10px",
                    "padding": "10px",
                    "backgroundColor": "#f5f5f5",
                    "borderRadius": "5px",
                    "marginRight": "20%"
                })
            )
    
    return elements