// This file handles the HTTP calls made to the inventory API.

// Base URL is now passed as an argument, so the constant is removed.
// const API_BASE_URL = '/api'; // Removed

// Define an interface for the Inventory item structure
export interface InventoryItem {
  id: number;
  name: string;
  quantity: number;
  price: number;
}

// --- Helper Function for API Response Handling ---
/**
 * Handles the response from a fetch call, checking for errors and parsing JSON.
 * @param response The Response object from fetch.
 * @returns The parsed JSON data.
 * @throws An error if the response is not ok.
 */
const handleApiResponse = async <T>(response: Response): Promise<T> => {
  if (!response.ok) {
    // Try to get error details from response, otherwise use statusText
    let errorDetails = response.statusText;
    try {
      // Use .json().catch() to handle cases where error response is not valid JSON
      const errorData = await response.json().catch(() => null);
      if (errorData && errorData.error) {
        errorDetails = errorData.error;
      }
    } catch (jsonError) {
      // Ignore if response body is empty or not JSON, fallback to statusText is already set
      console.warn("Could not parse error response JSON:", jsonError);
    }
    throw new Error(`HTTP error! status: ${response.status} - ${errorDetails}`);
  }
  // If response is ok, parse the JSON body
  // Use .json().catch() here as well in case of empty successful responses (e.g., 204 No Content for DELETE)
  return await response.json().catch(() => null) as T; // Return null for empty body, cast to T
};

// Fetch all inventory items
// Add apiBaseUrl parameter
export const fetchInventory = async (apiBaseUrl: string): Promise<InventoryItem[]> => {
  try {
    // Use the passed apiBaseUrl
    const response = await fetch(`${apiBaseUrl}/inventory/`);
    const data = await handleApiResponse<InventoryItem[]>(response);
    console.log("Fetched inventory:", data);
    return data || [];
  } catch (error) {
    console.error("Error fetching inventory:", error);
    throw error;
  }
};

// Add a new inventory item
// Add apiBaseUrl parameter
export const addItem = async (apiBaseUrl: string, itemData: Omit<InventoryItem, 'id'>): Promise<InventoryItem> => {
  try {
    // Use the passed apiBaseUrl
    const response = await fetch(`${apiBaseUrl}/inventory/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(itemData),
    });
    const newItem = await handleApiResponse<InventoryItem>(response);
    console.log("Added item:", newItem);
    if (!newItem) {
        throw new Error("API did not return the new item.");
    }
    return newItem;
  } catch (error) {
    console.error("Error adding item:", error);
    throw error;
  }
};

// Update an existing inventory item
// Add apiBaseUrl parameter
export const updateItem = async (apiBaseUrl: string, itemId: number, itemData: Partial<Omit<InventoryItem, 'id'>>): Promise<InventoryItem> => {
    try {
        // Use the passed apiBaseUrl
        const response = await fetch(`${apiBaseUrl}/inventory/${itemId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(itemData),
        });
        const updatedItem = await handleApiResponse<InventoryItem>(response);
        console.log("Updated item:", updatedItem);
        if (!updatedItem) {
            throw new Error("API did not return the updated item.");
        }
        return updatedItem;
    } catch (error) {
        console.error(`Error updating item ${itemId}:`, error);
        throw error;
    }
};

// Delete an inventory item
// Add apiBaseUrl parameter
export const deleteItem = async (apiBaseUrl: string, itemId: number): Promise<void> => {
    try {
        // Use the passed apiBaseUrl
        const response = await fetch(`${apiBaseUrl}/inventory/${itemId}`, {
            method: "DELETE",
        });
        await handleApiResponse<void>(response);
        console.log(`Deleted item: ${itemId}`);
    } catch (error) {
        console.error(`Error deleting item ${itemId}:`, error);
        throw error;
    }
};
