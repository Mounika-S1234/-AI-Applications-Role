import React, { useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../redux/store';
import { logInteractionWithAI, editInteractionWithAI, resetDraftForm } from '../redux/interactionSlice';
import { addMessage, setLoading } from '../redux/chatSlice';
import '../styles/ChatInterface.css';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

export const ChatInterface: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { messages, isLoading } = useSelector((state: RootState) => state.chat);
  const { selectedHCP } = useSelector((state: RootState) => state.hcp);
  const { selectedInteraction, draftForm, lastSummary, actionItems } = useSelector(
    (state: RootState) => state.interaction
  );

  const [inputValue, setInputValue] = useState('');
  const [interactionType, setInteractionType] = useState('call');
  const [mode, setMode] = useState<'new' | 'edit'>('new');

  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = { role: 'user' as const, content: inputValue };
    dispatch(addMessage(userMessage));
    dispatch(setLoading(true));

    try {
      let result;
      const payload = {
        message: inputValue,
        hcp_id: selectedHCP?.id,
        mode,
        existing_form: mode === 'edit' ? draftForm : undefined,
      };

      if (mode === 'new') {
        result = await dispatch(logInteractionWithAI(payload)).unwrap();
      } else {
        if (!selectedInteraction) {
          throw new Error('Select an interaction before using edit mode.');
        }
        result = await dispatch(
          editInteractionWithAI({ id: selectedInteraction.id, data: payload })
        ).unwrap();
      }

      dispatch(
        addMessage({
          role: 'assistant',
          content: result.response || 'AI processed the request successfully.',
        })
      );
    } catch (error) {
      console.error('Error sending message:', error);
      dispatch(
        addMessage({
          role: 'assistant' as const,
          content: 'Error processing your message. Please try again.',
        })
      );
    } finally {
      dispatch(setLoading(false));
      setInputValue('');
    }
  };

  const handleClearChat = () => {
    dispatch(resetDraftForm());
    dispatch(
      addMessage({
        role: 'assistant' as const,
        content: 'AI form draft reset. Start a new interaction to populate the form again.',
      })
    );
  };

  return (
    <div className="chat-interface">
      <div className="chat-header">
        <h2>Interaction Logger - AI Chat Interface</h2>
        {selectedHCP && <p>Selected HCP: {selectedHCP.name}</p>}
      </div>

      <div className="chat-controls">
        <select
          value={interactionType}
          onChange={(e) => setInteractionType(e.target.value)}
          className="interaction-type-select"
        >
          <option value="call">Call</option>
          <option value="meeting">Meeting</option>
          <option value="email">Email</option>
          <option value="conference">Conference</option>
          <option value="webinar">Webinar</option>
        </select>

        <div className="mode-toggle">
          <button
            className={`mode-btn ${mode === 'new' ? 'active' : ''}`}
            onClick={() => setMode('new')}
          >
            New Interaction
          </button>
          <button
            className={`mode-btn ${mode === 'edit' ? 'active' : ''}`}
            onClick={() => setMode('edit')}
            disabled={!selectedInteraction}
          >
            Edit Interaction
          </button>
        </div>
      </div>

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <p>Start logging your HCP interaction here...</p>
            <p className="hint">
              {selectedHCP
                ? `Chat with ${selectedHCP.name}`
                : 'Select an HCP to start logging interactions'}
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role}`}>
              <div className="message-content">{msg.content}</div>
            </div>
          ))
        )}
      </div>

      {lastSummary && (
        <div className="interaction-summary">
          <h4>Summary</h4>
          <p>{lastSummary}</p>
          {actionItems && actionItems.length > 0 && (
            <div>
              <h5>Action Items</h5>
              <ul>
                {actionItems.map((item, idx) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      <div className="chat-input-area">
        <textarea
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={(e) => {
            if (e.key === 'Enter' && e.ctrlKey) {
              handleSendMessage();
            }
          }}
          placeholder="Describe the interaction or ask for help... (Ctrl+Enter to send)"
          disabled={isLoading || !selectedHCP}
          className="chat-input"
        />
        <div className="chat-buttons">
          <button
            onClick={handleSendMessage}
            disabled={isLoading || !selectedHCP || !inputValue.trim()}
            className="btn-primary"
          >
            {isLoading ? 'Processing...' : 'Send'}
          </button>
          <button onClick={handleClearChat} className="btn-secondary">
            Clear Chat
          </button>
        </div>
      </div>
    </div>
  );
};
