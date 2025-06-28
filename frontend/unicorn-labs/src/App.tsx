import React from 'react';
import './App.css';

// --- SVG Icon Components (Updated for new image) ---

const ProofIcon = () => (
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <rect x="4" y="4" width="16" height="16" rx="2" stroke="#495057" strokeWidth="2.5"/>
    </svg>
);

const RedoIcon = ({ size = 20, color = "#495057" }) => (
    <svg width={size} height={size} viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M21.5 2V6H17.5" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
        <path d="M3 12C3 16.9706 7.02944 21 12 21C16.9706 21 21 16.9706 21 12C21 7.02944 16.9706 3 12 3C9.07094 3 6.48625 4.38543 4.99999 6.5" stroke={color} strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"/>
    </svg>
);

const GearIcon = () => (
    <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"/>
        <path d="M19.1213 4.87868L18.4142 5.58579C17.4332 6.56684 17.4332 8.15685 18.4142 9.1379L19.1213 9.845C20.1024 10.8261 20.1024 12.4161 19.1213 13.3971L18.4142 14.1042C17.4332 15.0853 17.4332 16.6753 18.4142 17.6563L19.1213 18.3634C19.6839 18.926 20.444 19.2426 21.2322 19.2426V19.2426C22.0205 19.2426 22.7805 18.926 23.3431 18.3634L23.3431 18.3634C24.4673 17.2391 24.4673 15.3859 23.3431 14.2616L22.636 13.5546C21.655 12.5735 21.655 10.9835 22.636 10.0025L23.3431 9.29539C24.4673 8.17115 24.4673 6.31799 23.3431 5.19375L23.3431 5.19375C22.7805 4.63112 22.0205 4.31454 21.2322 4.31454V4.31454C20.444 4.31454 19.6839 4.63112 19.1213 5.19375L18.4142 5.90089"/>
        <path d="M4.87868 4.87868L5.58579 5.58579C6.56684 6.56684 6.56684 8.15685 5.58579 9.1379L4.87868 9.845C3.89763 10.8261 3.89763 12.4161 4.87868 13.3971L5.58579 14.1042C6.56684 15.0853 6.56684 16.6753 5.58579 17.6563L4.87868 18.3634C4.31605 18.926 3.55603 19.2426 2.76777 19.2426V19.2426C1.9795 19.2426 1.21948 18.926 0.656854 18.3634L0.656854 18.3634C-0.467389 17.2391 -0.467389 15.3859 0.656854 14.2616L1.36396 13.5546C2.34501 12.5735 2.34501 10.9835 1.36396 10.0025L0.656854 9.29539C-0.467389 8.17115 -0.467389 6.31799 0.656854 5.19375L0.656854 5.19375C1.21948 4.63112 1.9795 4.31454 2.76777 4.31454V4.31454C3.55603 4.31454 4.31605 4.63112 4.87868 5.19375L5.58579 5.90089"/>
    </svg>
);

const MicIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"/>
        <path d="M19 10v2a7 7 0 0 1-14 0v-2"/>
        <line x1="12" y1="19" x2="12" y2="23"/>
        <line x1="8" y1="23" x2="16" y2="23"/>
    </svg>
);

const SpeakerIcon = () => (
    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" xmlns="http://www.w3.org/2000/svg">
        <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/>
        <path d="M15.54 8.46a5 5 0 0 1 0 7.07"/>
    </svg>
);

// --- Main App Component ---

function App() {
  return (
    <div className="page-container">
      <header className="page-header">
        <div className="logo-container">
            <div className="logo-icon-wrapper">
                <ProofIcon />
            </div>
            <span className="logo-text">Unicorn Labs</span>
        </div>
        <div className="header-action-icon">
            <RedoIcon size={22} />
        </div>
      </header>

      <main className="main-content">
        <h1 className="main-heading">See It In Action</h1>
        <p className="main-subheading">
          Experience the power of AI-driven idea validation with our interactive demo
        </p>

        <div className="demo-card">
          <div className="card-header">
            <div className="gear-icon-wrapper">
                <GearIcon />
            </div>
            <p>Ready to create your brand & validation strategy</p>
          </div>
          
          <div className="chat-interface">
            <div className="message-row">
              <div className="avatar ai-avatar">
                <ProofIcon />
              </div>
              <div className="message-bubble ai-bubble">
                Hi! I'm your AI brand & validation assistant. Tell me about your business idea and I'll create a complete brand identity and TikTok strategy for validation.
              </div>
            </div>
            
            <div className="message-row user-row">
              <div className="message-bubble user-bubble">
                Click the microphone to describe your idea
              </div>
              <div className="avatar user-avatar">
                You
              </div>
            </div>
          </div>
          
          <div className="controls-section">
            <div className="button-group">
              <button className="control-button primary">
                <MicIcon />
              </button>
              <button className="control-button secondary">
                <SpeakerIcon />
              </button>
              <button className="control-button secondary">
                <RedoIcon size={20} />
              </button>
            </div>
            <p className="controls-caption">
              Click the microphone and describe your business idea to get started
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default App;