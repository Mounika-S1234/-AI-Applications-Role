import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { AppDispatch, RootState } from '../redux/store';
import { fetchHCPInteractions } from '../redux/interactionSlice';
import '../styles/InteractionHistory.css';

export const InteractionHistory: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { selectedHCP } = useSelector((state: RootState) => state.hcp);
  const { interactions, loading } = useSelector((state: RootState) => state.interaction);

  useEffect(() => {
    if (selectedHCP) {
      dispatch(fetchHCPInteractions(selectedHCP.id));
    }
  }, [selectedHCP, dispatch]);

  return (
    <div className="interaction-history-container">
      <h2>Interaction History</h2>

      {!selectedHCP ? (
        <p className="info">Select an HCP to view interaction history</p>
      ) : loading ? (
        <p>Loading interactions...</p>
      ) : interactions.length === 0 ? (
        <p className="info">No interactions logged yet</p>
      ) : (
        <div className="interactions-list">
          {interactions.map((interaction) => (
            <div key={interaction.id} className="interaction-item">
              <div className="interaction-header">
                <h4>{interaction.title}</h4>
                <span className="interaction-type">{interaction.interaction_type}</span>
              </div>
              <p className="interaction-date">
                {new Date(interaction.date).toLocaleDateString()}
              </p>
              {interaction.description && (
                <p className="interaction-description">{interaction.description}</p>
              )}
              {interaction.summary && (
                <div className="interaction-summary">
                  <h5>Summary</h5>
                  <p>{interaction.summary}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
