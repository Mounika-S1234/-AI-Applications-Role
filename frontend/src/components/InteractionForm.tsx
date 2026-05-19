import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../redux/store';
import { createInteraction } from '../redux/interactionSlice';
import '../styles/InteractionForm.css';

export const InteractionForm: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { selectedHCP } = useSelector((state: RootState) => state.hcp);
  const { draftForm, lastSummary, actionItems } = useSelector(
    (state: RootState) => state.interaction
  );

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!selectedHCP) {
      alert('Please select an HCP from the left panel before saving.');
      return;
    }

    if (!draftForm.title.trim()) {
      alert('Use the AI assistant on the right to fill the form before saving.');
      return;
    }

    await dispatch(
      createInteraction({
        hcp_id: selectedHCP.id,
        interaction_type: draftForm.interaction_type,
        title: draftForm.title,
        description: draftForm.description,
      })
    );
  };

  return (
    <div className="interaction-form-container">
      <h2>AI-Controlled Interaction Form</h2>
      <p className="form-note">
        The AI assistant on the right fills this form for you. Please do not edit the fields directly.
      </p>
      <div className="form-group">
        <label>Selected HCP</label>
        <input
          value={draftForm.hcp_name || selectedHCP?.name || ''}
          disabled
          placeholder="HCP name will be extracted by AI"
        />
      </div>

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Date</label>
          <input value={draftForm.date} disabled placeholder="Auto-filled by AI" />
        </div>

        <div className="form-group">
          <label>Interaction Type</label>
          <input value={draftForm.interaction_type} disabled />
        </div>

        <div className="form-group">
          <label>Sentiment</label>
          <input value={draftForm.sentiment} disabled placeholder="Positive / Neutral / Negative" />
        </div>

        <div className="form-group">
          <label>Brochures Shared</label>
          <input
            value={draftForm.brochures_shared === true ? 'Yes' : draftForm.brochures_shared === false ? 'No' : ''}
            disabled
          />
        </div>

        <div className="form-group">
          <label>Product / Topic</label>
          <input value={draftForm.products_discussed} disabled placeholder="Extracted product details" />
        </div>

        <div className="form-group">
          <label>Interaction Title</label>
          <input value={draftForm.title} disabled placeholder="AI suggested title" />
        </div>

        <div className="form-group">
          <label>Description</label>
          <textarea value={draftForm.description} disabled rows={6} />
        </div>

        <button type="submit" className="btn-primary" disabled={!selectedHCP || !draftForm.title.trim()}>
          Save Interaction
        </button>
      </form>

      {lastSummary && (
        <div className="interaction-summary">
          <h4>AI Summary</h4>
          <p>{lastSummary}</p>
        </div>
      )}

      {actionItems && actionItems.length > 0 && (
        <div className="interaction-summary">
          <h4>Action Items</h4>
          <ul>
            {actionItems.map((item, idx) => (
              <li key={idx}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
