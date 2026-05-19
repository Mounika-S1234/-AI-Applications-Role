import React, { useEffect, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { fetchHCPs, selectHCP, createHCP } from '../redux/hcpSlice';
import { AppDispatch, RootState } from '../redux/store';
import '../styles/HCPList.css';

export const HCPList: React.FC = () => {
  const dispatch = useDispatch<AppDispatch>();
  const { hcps, loading } = useSelector((state: RootState) => state.hcp);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    specialty: '',
    organization: '',
    email: '',
    phone: '',
    location: '',
  });

  useEffect(() => {
    dispatch(fetchHCPs());
  }, [dispatch]);

  const handleSelectHCP = (hcp: any) => {
    dispatch(selectHCP(hcp));
  };

  const handleCreateHCP = async () => {
    if (formData.name.trim()) {
      await dispatch(createHCP(formData));
      setFormData({
        name: '',
        specialty: '',
        organization: '',
        email: '',
        phone: '',
        location: '',
      });
      setShowForm(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  return (
    <div className="hcp-list-container">
      <div className="hcp-header">
        <h2>Healthcare Professionals</h2>
        <button className="btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancel' : 'Add New HCP'}
        </button>
      </div>

      {showForm && (
        <div className="hcp-form">
          <h3>Add New HCP</h3>
          <div className="form-group">
            <label>Name *</label>
            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleInputChange}
              placeholder="HCP Name"
              required
            />
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Specialty</label>
              <input
                type="text"
                name="specialty"
                value={formData.specialty}
                onChange={handleInputChange}
                placeholder="Specialty"
              />
            </div>
            <div className="form-group">
              <label>Organization</label>
              <input
                type="text"
                name="organization"
                value={formData.organization}
                onChange={handleInputChange}
                placeholder="Organization"
              />
            </div>
          </div>
          <div className="form-row">
            <div className="form-group">
              <label>Email</label>
              <input
                type="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                placeholder="Email"
              />
            </div>
            <div className="form-group">
              <label>Phone</label>
              <input
                type="tel"
                name="phone"
                value={formData.phone}
                onChange={handleInputChange}
                placeholder="Phone"
              />
            </div>
          </div>
          <div className="form-group">
            <label>Location</label>
            <input
              type="text"
              name="location"
              value={formData.location}
              onChange={handleInputChange}
              placeholder="Location"
            />
          </div>
          <button className="btn-primary" onClick={handleCreateHCP}>
            Create HCP
          </button>
        </div>
      )}

      {loading ? (
        <p>Loading HCPs...</p>
      ) : (
        <div className="hcp-grid">
          {hcps.map((hcp) => (
            <div
              key={hcp.id}
              className="hcp-card"
              onClick={() => handleSelectHCP(hcp)}
            >
              <h3>{hcp.name}</h3>
              <p><strong>Specialty:</strong> {hcp.specialty || 'N/A'}</p>
              <p><strong>Organization:</strong> {hcp.organization || 'N/A'}</p>
              <p><strong>Email:</strong> {hcp.email || 'N/A'}</p>
              <p><strong>Phone:</strong> {hcp.phone || 'N/A'}</p>
              <p><strong>Location:</strong> {hcp.location || 'N/A'}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
