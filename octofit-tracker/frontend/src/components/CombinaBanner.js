import React from 'react';
import './CombinaBanner.css';

function CombinaBanner() {
  return (
    <div className="combina-banner">
      <div className="combina-overlay"></div>
      <div className="combina-content">
        <div className="combina-text">
          <h1 className="combina-headline">
            Se tens um pacote <span className="combina-box-group">
              <span className="combina-box">COM</span>
              <span className="combina-box">BI</span>
              <span className="combina-box">NA</span>
            </span>
          </h1>
          <h2 className="combina-subheadline">NOS já estás a poupar</h2>
          
          <div className="combina-partners">
            <div className="partner-logo-container">
              <div className="partner-logo nos-logo">NOS</div>
              <span className="plus-sign">+</span>
              <div className="partner-logo galp-logo">GALP</div>
              <span className="plus-sign">+</span>
              <div className="partner-logo continente-logo">CONTINENTE</div>
            </div>
          </div>
          
          <p className="combina-description">
            Combina o teu pacote NOS com a Galp e o Continente e podes poupar mais de €600 por ano
          </p>
          
          <div className="combina-buttons">
            <button className="btn-combina btn-primary-combina">Sabe mais</button>
            <button className="btn-combina btn-secondary-combina">Descobre os pacotes NOS</button>
          </div>
        </div>
        
        <div className="combina-image-placeholder">
          <div className="image-text">
            <span className="fitness-icon">💪</span>
            <p>Economiza e mantém-te em forma!</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default CombinaBanner;
