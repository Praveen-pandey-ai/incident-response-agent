from typing import TypedDict, List, Dict, Any
from datetime import datetime

from langgraph.graph import StateGraph, END

from agents.triage_agent import TriageAgent
from agents.forensics_agent import ForensicsAgent
from agents.hypothesis_agent import HypothesisAgent
from agents.verifier_agent import VerifierAgent

from tools.file_loader import load_file
from tools.metrics_parser import parse_metrics
from tools.anomaly_detector import detect_anomalies


# -------------------------
# 1. Define shared state
# -------------------------

class IncidentState(TypedDict):
    alerts: list
    chat: str
    raw_metrics: list
    metrics: dict
    anomalies: list
    triage: dict
    timeline: list
    hypotheses: list
    final: dict


# -------------------------
# 2. Node implementations
# -------------------------

def ingest_node(state: IncidentState) -> IncidentState:
    state["alerts"] = load_file("alerts.json")
    state["chat"] = load_file("chat.txt")
    state["raw_metrics"] = load_file("metrics.csv")
    return state


def index_node(state: IncidentState) -> IncidentState:
    state["metrics"] = parse_metrics(state["raw_metrics"])
    state["anomalies"] = detect_anomalies(state["metrics"])
    return state


def triage_node(state: IncidentState) -> IncidentState:
    agent = TriageAgent()
    state["triage"] = agent.run(
        alerts=state["alerts"],
        anomalies=state["anomalies"],
        chat_text=state["chat"]
    )
    return state


def investigate_node(state: IncidentState) -> IncidentState:
    agent = ForensicsAgent()

    log_paths = {
        "auth-service": "logs/auth.log",
        "payments-service": "logs/payments.log",
        "orders-service": "logs/orders.log"
    }

    state["timeline"] = agent.run(
        log_paths=log_paths,
        start_time=state["triage"]["start_time"]
    )
    return state


def hypothesize_node(state: IncidentState) -> IncidentState:
    agent = HypothesisAgent()
    state["hypotheses"] = agent.run(
        timeline=state["timeline"]
    )
    return state


def verify_node(state: IncidentState) -> IncidentState:
    agent = VerifierAgent()
    state["final"] = agent.run(
        triage_result=state["triage"],
        timeline=state["timeline"],
        hypotheses=state["hypotheses"]
    )
    return state


# -------------------------
# 3. Build the graph
# -------------------------

def build_incident_graph():
    graph = StateGraph(IncidentState)

    graph.add_node("ingest", ingest_node)
    graph.add_node("index", index_node)
    graph.add_node("triage", triage_node)
    graph.add_node("investigate", investigate_node)
    graph.add_node("hypothesize", hypothesize_node)
    graph.add_node("verify", verify_node)

    graph.set_entry_point("ingest")

    graph.add_edge("ingest", "index")
    graph.add_edge("index", "triage")
    graph.add_edge("triage", "investigate")
    graph.add_edge("investigate", "hypothesize")
    graph.add_edge("hypothesize", "verify")
    graph.add_edge("verify", END)

    return graph.compile()
