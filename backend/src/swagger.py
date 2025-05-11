"""
This module contains the Swagger configuration for the DevOps Lab Kit API.
"""

# Define the API documentation as a dictionary that follows the OpenAPI Specification
swagger_config = {
    "swagger": "2.0",
    "info": {
        "title": "DevOps Lab Kit API",
        "description": "API documentation for the DevOps Lab Kit backend service",
        "version": "1.0.0",
        "contact": {
            "name": "DevOps Lab Kit Team"
        }
    },
    "basePath": "/",
    "schemes": [
        "http",
        "https"
    ],
    "paths": {
        "/database/": {
            "get": {
                "summary": "Get all inventory items",
                "description": "Returns a list of all inventory items in the database",
                "produces": ["application/json"],
                "responses": {
                    "200": {
                        "description": "List of inventory items",
                        "schema": {
                            "type": "array",
                            "items": {
                                "$ref": "#/definitions/Inventory"
                            }
                        }
                    },
                    "500": {
                        "description": "Server error"
                    }
                },
                "tags": ["Inventory"]
            },
            "post": {
                "summary": "Add a new inventory item",
                "description": "Creates a new inventory item in the database",
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "item",
                        "description": "Inventory item to add",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/InventoryInput"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Item created successfully",
                        "schema": {
                            "$ref": "#/definitions/Inventory"
                        }
                    },
                    "400": {
                        "description": "Invalid input"
                    },
                    "500": {
                        "description": "Server error"
                    }
                },
                "tags": ["Inventory"]
            }
        },
        "/database/{item_id}": {
            "parameters": [
                {
                    "in": "path",
                    "name": "item_id",
                    "type": "integer",
                    "required": True,
                    "description": "The ID of the inventory item"
                }
            ],
            "put": {
                "summary": "Update an inventory item",
                "description": "Updates an existing inventory item in the database",
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "item",
                        "description": "Updated inventory item",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/InventoryUpdate"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Item updated successfully",
                        "schema": {
                            "$ref": "#/definitions/Inventory"
                        }
                    },
                    "400": {
                        "description": "Invalid input"
                    },
                    "404": {
                        "description": "Item not found"
                    },
                    "500": {
                        "description": "Server error"
                    }
                },
                "tags": ["Inventory"]
            },
            "delete": {
                "summary": "Delete an inventory item",
                "description": "Deletes an inventory item from the database",
                "produces": ["application/json"],
                "responses": {
                    "200": {
                        "description": "Item deleted successfully"
                    },
                    "404": {
                        "description": "Item not found"
                    },
                    "500": {
                        "description": "Server error"
                    }
                },
                "tags": ["Inventory"]
            }
        },
        "/healthcheck": {
            "get": {
                "summary": "Health check",
                "description": "Checks the health of the application, including database connectivity and table access",
                "produces": ["application/json"],
                "responses": {
                    "200": {
                        "description": "Application is healthy"
                    },
                    "500": {
                        "description": "Application is unhealthy"
                    }
                },
                "tags": ["System"]
            }
        },
        "/environment": {
            "get": {
                "summary": "Get environment variables",
                "description": "Returns all environment variables available to the process",
                "produces": ["application/json"],
                "responses": {
                    "200": {
                        "description": "Environment variables"
                    },
                    "500": {
                        "description": "Server error"
                    }
                },
                "tags": ["System"]
            }
        },
        "/hello": {
            "get": {
                "summary": "Hello world",
                "description": "Simple endpoint that responds with 'Hello, World!'",
                "produces": ["application/json"],
                "responses": {
                    "200": {
                        "description": "Hello world message"
                    }
                },
                "tags": ["System"]
            }
        },
        "/log": {
            "post": {
                "summary": "Trigger a log message",
                "description": "Triggers a log message at the specified level",
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "log",
                        "description": "Log details",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/LogInput"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Log created successfully"
                    },
                    "400": {
                        "description": "Invalid input"
                    }
                },
                "tags": ["System"]
            }
        },
        "/crash": {
            "post": {
                "summary": "Crash the application",
                "description": "Endpoint to intentionally crash the entire application (for testing purposes)",
                "responses": {
                    "500": {
                        "description": "Application crashed"
                    }
                },
                "tags": ["System"]
            }
        },
        "/pastebin": {
            "post": {
                "summary": "Store text in pastebin",
                "description": "Stores text in SQLite database with a 24h auto-delete policy and returns a URL",
                "consumes": ["application/json"],
                "produces": ["application/json"],
                "parameters": [
                    {
                        "in": "body",
                        "name": "paste",
                        "description": "Paste details",
                        "required": True,
                        "schema": {
                            "$ref": "#/definitions/PastebinInput"
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Paste created successfully",
                        "schema": {
                            "$ref": "#/definitions/PastebinOutput"
                        }
                    },
                    "400": {
                        "description": "Invalid input"
                    },
                    "500": {
                        "description": "Server error"
                    }
                },
                "tags": ["Pastebin"]
            }
        },
        "/pastebin/{paste_id}": {
            "parameters": [
                {
                    "in": "path",
                    "name": "paste_id",
                    "type": "string",
                    "required": True,
                    "description": "The ID of the paste"
                }
            ],
            "get": {
                "summary": "Get paste by ID",
                "description": "Retrieves a paste by its ID",
                "produces": ["text/plain"],
                "responses": {
                    "200": {
                        "description": "Paste content"
                    },
                    "404": {
                        "description": "Paste not found or expired"
                    },
                    "500": {
                        "description": "Server error"
                    }
                },
                "tags": ["Pastebin"]
            }
        },
        "/pastebin/cleanup": {
            "post": {
                "summary": "Clean up expired pastes",
                "description": "Removes all expired pastes from the database",
                "produces": ["application/json"],
                "responses": {
                    "200": {
                        "description": "Cleanup successful"
                    },
                    "500": {
                        "description": "Server error"
                    }
                },
                "tags": ["Pastebin"]
            }
        }
    },
    "definitions": {
        "Inventory": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "integer",
                    "description": "Unique identifier for the item"
                },
                "name": {
                    "type": "string",
                    "description": "Name of the item"
                },
                "quantity": {
                    "type": "integer",
                    "description": "Quantity of the item in stock"
                },
                "price": {
                    "type": "number",
                    "format": "float",
                    "description": "Price of the item"
                }
            }
        },
        "InventoryInput": {
            "type": "object",
            "required": ["name", "quantity", "price"],
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the item"
                },
                "quantity": {
                    "type": "integer",
                    "description": "Quantity of the item in stock"
                },
                "price": {
                    "type": "number",
                    "format": "float",
                    "description": "Price of the item"
                }
            }
        },
        "InventoryUpdate": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "Name of the item"
                },
                "quantity": {
                    "type": "integer",
                    "description": "Quantity of the item in stock"
                },
                "price": {
                    "type": "number",
                    "format": "float",
                    "description": "Price of the item"
                }
            }
        },
        "LogInput": {
            "type": "object",
            "required": ["level", "message"],
            "properties": {
                "level": {
                    "type": "string",
                    "description": "Log level (debug, info, warning, error, critical)",
                    "enum": ["debug", "info", "warning", "error", "critical"]
                },
                "message": {
                    "type": "string",
                    "description": "Log message"
                }
            }
        },
        "PastebinInput": {
            "type": "object",
            "required": ["text"],
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text content to store"
                },
                "content_type": {
                    "type": "string",
                    "description": "Content type of the paste",
                    "default": "text/plain"
                }
            }
        },
        "PastebinOutput": {
            "type": "object",
            "properties": {
                "id": {
                    "type": "string",
                    "description": "Unique identifier for the paste"
                },
                "url": {
                    "type": "string",
                    "description": "URL to access the paste"
                },
                "expires_at": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Expiration time of the paste"
                }
            }
        }
    },
    "tags": [
        {
            "name": "Inventory",
            "description": "Inventory management operations"
        },
        {
            "name": "System",
            "description": "System operations"
        },
        {
            "name": "Pastebin",
            "description": "Pastebin operations"
        }
    ]
}

# Function to get the swagger specs as a JSON-compatible dictionary
def get_swagger_specs():
    return swagger_config