import React, { useState, useEffect } from 'react';
import './Modal.css'; // We'll create this CSS file next
import { InventoryItem } from './http_handler';

// Define props for the modal
interface AddItemModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (itemData: Omit<InventoryItem, 'id'>) => Promise<void>;
  initialData?: InventoryItem | null;
}

const ItemFormModal: React.FC<AddItemModalProps> = ({ isOpen, onClose, onSubmit, initialData }) => {
  const [name, setName] = useState('');
  const [quantity, setQuantity] = useState('');
  const [price, setPrice] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isEditMode = !!initialData;
  const modalTitle = isEditMode ? 'Update Item' : 'Add New Item';
  const submitButtonText = isEditMode ? 'Update Item' : 'Add Item';

  useEffect(() => {
    if (initialData && isOpen) {
      setName(initialData.name);
      setQuantity(initialData.quantity.toString());
      setPrice(initialData.price.toString());
    } else if (!isOpen) {
      setName('');
      setQuantity('');
      setPrice('');
      setError(null);
      setIsSubmitting(false);
    }
  }, [initialData, isOpen]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setError(null);

    const quantityNum = parseInt(quantity, 10);
    const priceNum = parseFloat(price);

    if (!name || isNaN(quantityNum) || quantityNum < 0 || isNaN(priceNum) || priceNum < 0) {
      setError('Please enter valid details (Name, non-negative Quantity, non-negative Price).');
      return;
    }

    setIsSubmitting(true);
    try {
      await onSubmit({ name, quantity: quantityNum, price: priceNum });
    } catch (err) {
      console.error("Error submitting form:", err);
      setError(err instanceof Error ? err.message : 'An unexpected error occurred.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (!isOpen) {
    return null;
  }

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>{modalTitle}</h2>
        {error && <p className="error-message">{error}</p>}
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="itemName">Name:</label>
            <input
              id="itemName"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              disabled={isSubmitting}
            />
          </div>
          <div className="form-group">
            <label htmlFor="itemQuantity">Quantity:</label>
            <input
              id="itemQuantity"
              type="number"
              value={quantity}
              onChange={(e) => setQuantity(e.target.value)}
              required
              min="0"
              disabled={isSubmitting}
            />
          </div>
          <div className="form-group">
            <label htmlFor="itemPrice">Price:</label>
            <input
              id="itemPrice"
              type="number"
              value={price}
              onChange={(e) => setPrice(e.target.value)}
              required
              min="0"
              step="0.01"
              disabled={isSubmitting}
            />
          </div>
          <div className="modal-actions">
            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Saving...' : submitButtonText}
            </button>
            <button type="button" onClick={onClose} disabled={isSubmitting}>
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default ItemFormModal;