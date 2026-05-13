import { useEffect, useRef, useState } from "react";
import API from "../api/api";
import "./messages-page.css";

function sortThreads(list) {
  return [...list].sort((left, right) => {
    const leftTime = new Date(left.latest_activity_at || left.created_at || 0).getTime();
    const rightTime = new Date(right.latest_activity_at || right.created_at || 0).getTime();
    return rightTime - leftTime;
  });
}

function upsertThread(list, nextThread) {
  const remaining = list.filter((item) => item.application_id !== nextThread.application_id);
  return sortThreads([nextThread, ...remaining]);
}

function upsertMessage(list, nextMessage) {
  if (list.some((item) => item.id === nextMessage.id)) {
    return list;
  }

  return [...list, nextMessage].sort((left, right) => {
    const leftTime = new Date(left.created_at || 0).getTime();
    const rightTime = new Date(right.created_at || 0).getTime();
    if (leftTime !== rightTime) {
      return leftTime - rightTime;
    }
    return left.id - right.id;
  });
}

function formatThreadTime(value) {
  if (!value) {
    return "";
  }

  const date = new Date(value);
  const now = new Date();
  const sameDay = date.toDateString() === now.toDateString();

  if (sameDay) {
    return date.toLocaleTimeString([], { hour: "numeric", minute: "2-digit" });
  }

  return date.toLocaleDateString([], { month: "short", day: "numeric" });
}

function formatMessageTime(value) {
  if (!value) {
    return "";
  }

  return new Date(value).toLocaleString([], {
    month: "short",
    day: "numeric",
    hour: "numeric",
    minute: "2-digit",
  });
}

function getMessagesSocketUrl() {
  const baseUrl = API.defaults.baseURL || "http://127.0.0.1:8000";
  const socketBase = baseUrl.startsWith("https://")
    ? baseUrl.replace("https://", "wss://")
    : baseUrl.replace("http://", "ws://");
  return `${socketBase}/ws/messages`;
}

function MessagesPage() {
  const role = localStorage.getItem("role") || "student";
  const token = localStorage.getItem("token") || "";
  const requestedThreadId = Number(new URLSearchParams(window.location.search).get("applicationId")) || null;

  const requestedThreadIdRef = useRef(requestedThreadId);
  const activeThreadIdRef = useRef(null);
  const profileIdRef = useRef(null);
  const socketRef = useRef(null);

  const [profile, setProfile] = useState(null);
  const [threads, setThreads] = useState([]);
  const [activeThreadId, setActiveThreadId] = useState(null);
  const [activeThread, setActiveThread] = useState(null);
  const [messages, setMessages] = useState([]);
  const [draft, setDraft] = useState("");
  const [workspaceLoading, setWorkspaceLoading] = useState(false);
  const [threadLoading, setThreadLoading] = useState(false);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState("");
  const [status, setStatus] = useState("");
  const [socketStatus, setSocketStatus] = useState("Connecting...");

  const homePath = role === "recruiter" ? "/recruiter" : "/student";

  useEffect(() => {
    activeThreadIdRef.current = activeThreadId;
  }, [activeThreadId]);

  useEffect(() => {
    profileIdRef.current = profile?.id ?? null;
  }, [profile]);

  const applyThreadList = (nextThreads, preserveSelection = true) => {
    const sortedThreads = sortThreads(nextThreads);
    setThreads(sortedThreads);
    setActiveThreadId((current) => {
      if (
        requestedThreadIdRef.current &&
        sortedThreads.some((item) => item.application_id === requestedThreadIdRef.current)
      ) {
        const nextId = requestedThreadIdRef.current;
        requestedThreadIdRef.current = null;
        return nextId;
      }

      if (preserveSelection && current && sortedThreads.some((item) => item.application_id === current)) {
        return current;
      }

      return sortedThreads[0]?.application_id ?? null;
    });
  };

  const loadThreads = async (preserveSelection = true) => {
    const res = await API.get("/messages/threads");
    applyThreadList(res.data, preserveSelection);
    return res.data;
  };

  const markThreadAsRead = async (applicationId) => {
    try {
      await API.post(`/messages/threads/${applicationId}/read`);
      setThreads((current) =>
        current.map((thread) =>
          thread.application_id === applicationId
            ? { ...thread, unread_count: 0 }
            : thread
        )
      );
      setActiveThread((current) =>
        current && current.application_id === applicationId
          ? { ...current, unread_count: 0 }
          : current
      );
    } catch {
      // Ignore optimistic read sync failures for now.
    }
  };

  useEffect(() => {
    let cancelled = false;

    async function loadWorkspace() {
      try {
        setWorkspaceLoading(true);
        const [meRes, threadsRes] = await Promise.all([API.get("/me"), API.get("/messages/threads")]);
        if (cancelled) {
          return;
        }

        setProfile(meRes.data);
        applyThreadList(threadsRes.data, true);
        setError("");
      } catch (err) {
        if (!cancelled) {
          setError(err.response?.data?.detail || "Failed to load messages");
        }
      } finally {
        if (!cancelled) {
          setWorkspaceLoading(false);
        }
      }
    }

    void loadWorkspace();

    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!activeThreadId) {
      setActiveThread(null);
      setMessages([]);
      return;
    }

    let cancelled = false;

    async function loadThreadDetails() {
      try {
        setThreadLoading(true);
        const res = await API.get(`/messages/threads/${activeThreadId}`);
        if (cancelled) {
          return;
        }

        setActiveThread(res.data.thread);
        setMessages(res.data.messages);
        setThreads((current) => upsertThread(current, res.data.thread));
        setError("");
      } catch (err) {
        if (!cancelled) {
          setError(err.response?.data?.detail || "Failed to load conversation");
        }
      } finally {
        if (!cancelled) {
          setThreadLoading(false);
        }
      }
    }

    void loadThreadDetails();

    return () => {
      cancelled = true;
    };
  }, [activeThreadId]);

  useEffect(() => {
    const url = new URL(window.location.href);
    if (activeThreadId) {
      url.searchParams.set("applicationId", String(activeThreadId));
    } else {
      url.searchParams.delete("applicationId");
    }
    window.history.replaceState({}, "", `${url.pathname}${url.search}`);
  }, [activeThreadId]);

  useEffect(() => {
    if (!token) {
      return undefined;
    }

    const socket = new WebSocket(`${getMessagesSocketUrl()}?token=${encodeURIComponent(token)}`);
    socketRef.current = socket;
    setSocketStatus("Connecting...");

    socket.onopen = () => {
      setSocketStatus("Live");
    };

    socket.onerror = () => {
      setSocketStatus("Offline");
    };

    socket.onclose = () => {
      setSocketStatus("Offline");
    };

    socket.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        if (payload.type !== "message.created") {
          return;
        }

        const nextMessage = payload.message;
        const isActiveThread = activeThreadIdRef.current === payload.application_id;

        if (isActiveThread) {
          setMessages((current) => upsertMessage(current, nextMessage));
          setActiveThread((current) =>
            current
              ? {
                  ...current,
                  unread_count: 0,
                  latest_activity_at: nextMessage.created_at,
                  last_message: {
                    id: nextMessage.id,
                    text: nextMessage.message,
                    created_at: nextMessage.created_at,
                    sender_name: nextMessage.sender_name,
                  },
                }
              : current
          );

          if (nextMessage.recipient_id === profileIdRef.current) {
            void markThreadAsRead(payload.application_id);
          }
        } else if (nextMessage.recipient_id === profileIdRef.current) {
          setStatus(`New message from ${nextMessage.sender_name}`);
        }

        void loadThreads(true);
      } catch {
        setSocketStatus("Offline");
      }
    };

    const pingId = window.setInterval(() => {
      if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: "ping" }));
      }
    }, 25000);

    return () => {
      window.clearInterval(pingId);
      socket.close();
      if (socketRef.current === socket) {
        socketRef.current = null;
      }
    };
  }, [token]);

  const sendMessage = async (e) => {
    e.preventDefault();

    if (!activeThreadId || !draft.trim()) {
      return;
    }

    try {
      setSending(true);
      const res = await API.post(`/messages/threads/${activeThreadId}`, {
        message: draft.trim(),
      });
      setDraft("");
      setMessages((current) => upsertMessage(current, res.data.message));
      setActiveThread(res.data.thread);
      setThreads((current) => upsertThread(current, res.data.thread));
      setError("");
      setStatus("Message sent");
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to send message");
    } finally {
      setSending(false);
    }
  };

  const openHome = () => {
    window.location.href = homePath;
  };

  const logout = () => {
    localStorage.clear();
    window.location.href = "/";
  };

  const emptyThreadCopy =
    role === "recruiter"
      ? "Open an applicant from your posted jobs to start a live conversation."
      : "Apply to a job and your recruiter conversations will appear here.";

  return (
    <div className="messages-shell">
      <header className="messages-topbar">
        <div>
          <h1>Live Messages</h1>
          <p>
            Chat in real time about job applications, updates, and next steps.
          </p>
        </div>

        <div className="messages-top-actions">
          <span
            className={`socket-pill ${
              socketStatus === "Live" ? "is-live" : socketStatus === "Offline" ? "is-offline" : ""
            }`}
          >
            {socketStatus}
          </span>
          <button type="button" className="ghost-btn" onClick={openHome}>Back</button>
          <button type="button" className="ghost-btn" onClick={logout}>Logout</button>
        </div>
      </header>

      <main className="messages-layout">
        <aside className="thread-panel">
          <div className="thread-panel-head">
            <div>
              <h2>Conversations</h2>
              <p>{threads.length} thread(s)</p>
            </div>
            <button
              type="button"
              className="ghost-btn"
              onClick={() => void loadThreads(true)}
              disabled={workspaceLoading}
            >
              Refresh
            </button>
          </div>

          {workspaceLoading && <div className="panel-note">Loading conversations...</div>}
          {!workspaceLoading && threads.length === 0 && (
            <div className="panel-empty">{emptyThreadCopy}</div>
          )}

          <div className="thread-list">
            {threads.map((thread) => (
              <button
                key={thread.application_id}
                type="button"
                className={`thread-card ${thread.application_id === activeThreadId ? "active" : ""}`}
                onClick={() => {
                  setActiveThreadId(thread.application_id);
                  setStatus("");
                }}
              >
                <div className="thread-card-top">
                  <strong>{thread.counterpart.name}</strong>
                  <span>{formatThreadTime(thread.latest_activity_at)}</span>
                </div>

                <p className="thread-job-line">
                  {thread.job_title} at {thread.company_name}
                </p>

                <p className="thread-preview">
                  {thread.last_message?.text || "No messages yet. Start the conversation."}
                </p>

                <div className="thread-card-bottom">
                  <span className="thread-role-pill">{thread.counterpart.role}</span>
                  <span className="thread-status-pill">{thread.application_status}</span>
                  {thread.unread_count > 0 && (
                    <span className="thread-unread-pill">{thread.unread_count} new</span>
                  )}
                </div>
              </button>
            ))}
          </div>
        </aside>

        <section className="conversation-panel">
          {error && <div className="messages-error">{error}</div>}
          {status && <div className="messages-status">{status}</div>}

          {!activeThread && !threadLoading && (
            <div className="conversation-empty">
              <h2>No conversation selected</h2>
              <p>{emptyThreadCopy}</p>
            </div>
          )}

          {activeThread && (
            <>
              <div className="conversation-head">
                <div>
                  <h2>{activeThread.counterpart.name}</h2>
                  <p>
                    {activeThread.job_title} at {activeThread.company_name}
                  </p>
                </div>

                <div className="conversation-meta">
                  <span className="thread-role-pill">{activeThread.counterpart.role}</span>
                  <span className="thread-status-pill">{activeThread.application_status}</span>
                </div>
              </div>

              <div className="messages-stream">
                {threadLoading && <div className="panel-note">Loading messages...</div>}

                {!threadLoading && messages.length === 0 && (
                  <div className="panel-empty">
                    No messages yet. Start the conversation from below.
                  </div>
                )}

                {!threadLoading &&
                  messages.map((message) => {
                    const isOwnMessage = message.sender_id === profile?.id;
                    return (
                      <article
                        key={message.id}
                        className={`message-bubble ${isOwnMessage ? "mine" : "theirs"}`}
                      >
                        <div className="message-meta">
                          <strong>{isOwnMessage ? "You" : message.sender_name}</strong>
                          <span>{formatMessageTime(message.created_at)}</span>
                        </div>
                        <p>{message.message}</p>
                      </article>
                    );
                  })}
              </div>

              <form className="composer-form" onSubmit={sendMessage}>
                <textarea
                  rows="3"
                  value={draft}
                  onChange={(e) => setDraft(e.target.value)}
                  placeholder="Write your message here..."
                />
                <div className="composer-actions">
                  <span className="composer-hint">Messages update live for both sides.</span>
                  <button type="submit" className="primary-btn" disabled={sending || !draft.trim()}>
                    {sending ? "Sending..." : "Send Message"}
                  </button>
                </div>
              </form>
            </>
          )}
        </section>
      </main>
    </div>
  );
}

export default MessagesPage;
