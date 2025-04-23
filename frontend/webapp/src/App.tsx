import { useState, useEffect } from 'react';
import './App.css';
// Import updateItem as well
import { fetchInventory, deleteItem, addItem, updateItem, InventoryItem } from './http_handler';
// Import the modal component (ensure name matches the export)
import ItemFormModal from './AddItemModal'; // Use the potentially renamed component
// Import the modal CSS
import './Modal.css';
import React from 'react';

function App() {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<InventoryItem | null>(null);
  // State for the API Base URL
  const [apiBaseUrl, setApiBaseUrl] = useState<string>('/api'); // Default to relative /api

  const [showPasteModal, setShowPasteModal] = useState(false);
  const [pasteText, setPasteText] = useState('');
  const [pasteResult, setPasteResult] = useState<{ url: string; expires_at: string } | null>(null);
  const [pasteLoading, setPasteLoading] = useState(false);
  const [pasteError, setPasteError] = useState<string | null>(null);

  const [environment, setEnvironment] = useState<any | null>(null);
  const [envLoading, setEnvLoading] = useState(false);
  const [envError, setEnvError] = useState<string | null>(null);

  const loadInventory = async () => {
    setError(null); // Clear previous errors
    setLoading(true);
    try {
      const data = await fetchInventory(apiBaseUrl);
      setInventory(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load inventory.');
      console.error(err);
      setInventory([]); // Clear inventory on load failure
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (itemId: number) => {
    if (!window.confirm(`Are you sure you want to delete item ID ${itemId}?`)) {
      return;
    }
    setDeletingId(itemId);
    setError(null); // Clear previous errors
    try {
      await deleteItem(apiBaseUrl, itemId);
      await loadInventory();
    } catch (err) {
      const errorMsg = err instanceof Error ? err.message : `An unexpected error occurred while trying to delete item ${itemId}.`;
      setError(errorMsg); // Set error state
      console.error(`Error during delete operation for item ${itemId}:`, err);
    } finally {
      setDeletingId(null);
    }
  };

  // --- Modal Handling ---

  const handleOpenAddModal = () => {
    setEditingItem(null); // Ensure we are not in edit mode
    setError(null); // Clear errors
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (item: InventoryItem) => {
    setEditingItem(item); // Set the item to edit
    setError(null); // Clear errors
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
    setEditingItem(null); // Clear editing state when closing
  };

  // Unified function to handle adding or updating an item
  const handleSaveItem = async (itemData: Omit<InventoryItem, 'id'>) => {
    setError(null); // Clear previous errors
    try {
      if (editingItem) {
        await updateItem(apiBaseUrl, editingItem.id, itemData);
        console.log(`Item ${editingItem.id} updated successfully.`);
      } else {
        await addItem(apiBaseUrl, itemData);
        console.log(`Item added successfully.`);
      }
      handleCloseModal();
      await loadInventory();
    } catch (err) {
      console.error("Error saving item:", err);
      setError(err instanceof Error ? err.message : "An unexpected error occurred while saving.");
    }
  };

  // Pastebin handlers
  const openPasteModal = () => {
    setPasteText('');
    setPasteResult(null);
    setPasteError(null);
    setShowPasteModal(true);
  };
  const closePasteModal = () => {
    setShowPasteModal(false);
    setPasteText('');
    setPasteResult(null);
    setPasteError(null);
    setPasteLoading(false);
  };
  const handlePasteSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setPasteError(null);
    setPasteLoading(true);
    setPasteResult(null);
    try {
      const resp = await fetch(`${apiBaseUrl}/pastebin`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: pasteText }),
      });
      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.error || resp.statusText);
      }
      const data = await resp.json();
      setPasteResult({ url: data.url, expires_at: data.expires_at });
    } catch (err) {
      setPasteError(err instanceof Error ? err.message : 'Failed to create paste.');
    } finally {
      setPasteLoading(false);
    }
  };

  // Handler for fetching environment info
  const handleFetchEnvironment = async () => {
    setEnvLoading(true);
    setEnvError(null);
    setEnvironment(null);
    try {
      const resp = await fetch(`${apiBaseUrl}/environment`);
      if (!resp.ok) {
        const err = await resp.json().catch(() => ({}));
        throw new Error(err.error || resp.statusText);
      }
      const data = await resp.json();
      setEnvironment(data);
    } catch (err) {
      setEnvError(err instanceof Error ? err.message : 'Failed to fetch environment.');
    } finally {
      setEnvLoading(false);
    }
  };

  useEffect(() => {
    loadInventory();
  }, [apiBaseUrl]);

  return (
    <div>
      <h1>DevOps LabKit</h1>

      {/* API URL Configuration */}
      <div style={{ marginBottom: '20px', padding: '10px', border: '1px solid #ccc', borderRadius: '4px' }}>
        <label htmlFor="apiUrl" style={{ marginRight: '10px', fontWeight: 'bold' }}>API Base URL:</label>
        <input
          type="text"
          id="apiUrl"
          value={apiBaseUrl}
          onChange={(e) => setApiBaseUrl(e.target.value)}
          placeholder="/api or http://localhost:5000"
          style={{ width: '300px', padding: '5px' }}
        />
        <p style={{ fontSize: '0.8em', color: '#555', marginTop: '5px' }}>
          (Inventory will reload automatically when URL changes or on refresh/CRUD actions)
        </p>
        {/* Environment Button */}
        <button
          onClick={handleFetchEnvironment}
          style={{ marginLeft: '10px' }}
          disabled={envLoading}
        >
          {envLoading ? 'Loading Environment...' : 'Show Environment'}
        </button>
      </div>
      {/* Environment Output */}
      {envError && <div className="error-message">{envError}</div>}
      {environment && (
        <pre
          style={{
            background: '#f6f8fa',
            border: '1px solid #e1e4e8',
            borderRadius: '4px',
            padding: '12px',
            marginBottom: '20px',
            fontSize: '0.95em',
            overflowX: 'auto',
            textAlign: 'left'
          }}
        >
          {JSON.stringify(environment, null, 2)}
        </pre>
      )}

      {/* Use handler to open modal for adding */}
      <button onClick={handleOpenAddModal} className="add-item-button">
        Add New Item
      </button>

      {/* Pastebin Button */}
      <button onClick={openPasteModal} style={{ marginBottom: '20px', marginLeft: '10px' }}>
        New Pastebin
      </button>

      {/* Render the modal */}
      <ItemFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSaveItem}
        initialData={editingItem}
      />

      {/* Pastebin Modal */}
      {showPasteModal && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>New Pastebin</h2>
            <form onSubmit={handlePasteSubmit}>
              <div className="form-group">
                <label htmlFor="pasteText">Paste Text:</label>
                <textarea
                  id="pasteText"
                  value={pasteText}
                  onChange={e => setPasteText(e.target.value)}
                  rows={6}
                  style={{ width: '100%' }}
                  required
                  disabled={pasteLoading}
                />
              </div>
              <div className="modal-actions">
                <button type="submit" disabled={pasteLoading || !pasteText}>
                  {pasteLoading ? 'Submitting...' : 'Submit'}
                </button>
                <button type="button" onClick={closePasteModal} disabled={pasteLoading}>
                  Cancel
                </button>
              </div>
            </form>
            {pasteError && <p className="error-message">{pasteError}</p>}
            {pasteResult && (
              <div style={{ marginTop: '15px', wordBreak: 'break-all' }}>
                <strong>Paste URL:</strong>
                <div>
                  <a href={pasteResult.url} target="_blank" rel="noopener noreferrer">
                    {pasteResult.url}
                  </a>
                </div>
                <div style={{ fontSize: '0.9em', color: '#555' }}>
                  Expires at: {pasteResult.expires_at}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Inventory Table */}
      {loading && <p>Loading inventory...</p>}
      {error && <p className="error-message">{error}</p>}
      {!loading && !error && (
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Quantity</th>
              <th>Price</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {inventory.length > 0 ? (
              inventory.map((item) => (
                <tr key={item.id}>
                  <td>{item.id}</td>
                  <td>{item.name}</td>
                  <td>{item.quantity}</td>
                  <td>${item.price.toFixed(2)}</td>
                  <td>
                    {/* Update Button */}
                    <button
                      onClick={() => handleOpenEditModal(item)}
                      className="update-item-button"
                      disabled={deletingId === item.id}
                      style={{ marginRight: '5px' }}
                    >
                      Update
                    </button>
                    {/* Delete Button */}
                    <button
                      onClick={() => handleDelete(item.id)}
                      disabled={deletingId === item.id}
                      className="delete-item-button"
                    >
                      {deletingId === item.id ? 'Deleting...' : 'Delete'}
                    </button>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={5}>No inventory items found.</td>
              </tr>
            )}
          </tbody>
        </table>
      )}

      <button onClick={loadInventory} className="refresh-button" disabled={loading}>
        {loading ? 'Refreshing...' : 'Refresh List'}
      </button>
    </div>
  );
}

export default App;
