import React, { useState } from 'react';
import { Provider } from 'react-redux';
import { store } from '../redux/store';
import { HCPList } from './HCPList';
import { ChatInterface } from './ChatInterface';
import { InteractionForm } from './InteractionForm';
import '../styles/App.css';

export const App: React.FC = () => {
  return (
    <Provider store={store}>
      <div className="app-container">
        <header className="app-header">
          <h1>AI-First CRM HCP Module</h1>
          <p>Healthcare Professional Interaction System with AI-driven form automation.</p>
        </header>

        <div className="app-grid">
          <section className="app-left">
            <HCPList />
            <InteractionForm />
          </section>

          <section className="app-right">
            <ChatInterface />
          </section>
        </div>

        <footer className="app-footer">
          <p>AI-Powered CRM System © 2026</p>
        </footer>
      </div>
    </Provider>
  );
};

export default App;
