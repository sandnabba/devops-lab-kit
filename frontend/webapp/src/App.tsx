import { useState, useEffect } from 'react';
import './App.css';
// Import updateItem as well
import { fetchInventory, deleteItem, addItem, updateItem, InventoryItem } from './http_handler';
// Import the modal component (ensure name matches the export)
import ItemFormModal from './AddItemModal'; // Use the potentially renamed component
// Import the modal CSS
import './Modal.css';

function App() {
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<number | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingItem, setEditingItem] = useState<InventoryItem | null>(null);
  // State for the API Base URL
  const [apiBaseUrl, setApiBaseUrl] = useState<string>('/api'); // Default to relative /api

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

  useEffect(() => {
    loadInventory();
  }, [apiBaseUrl]);

  return (
    <div>
      <h1>Inventory List</h1>

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
      </div>

      {/* Use handler to open modal for adding */}
      <button onClick={handleOpenAddModal} className="add-item-button">
        Add New Item
      </button>

      {/* Render the modal */}
      <ItemFormModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onSubmit={handleSaveItem}
        initialData={editingItem}
      />

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
