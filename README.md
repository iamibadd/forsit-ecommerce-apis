# Forsit Ecommerce APIs

## Core Features

**Sales Status**

- Endpoints to retrieve, filter, and analyze sales data.
- Endpoints to analyze revenue on a daily, weekly, monthly, and annual basis.
- Ability to compare revenue across different periods and categories.
- Provide sales data by date range, product, and category.

**Inventory Management**

- Endpoints to view current inventory status, including low stock alerts.
- Functionality to update inventory levels, and track changes over time.

# Database Schema ERD Documentation

## Entity Relationship Diagram (UML Notation)

```mermaid
erDiagram
    categories ||--o{ products : "1 to many"
    products ||--|| inventory : "1 to 1"
    inventory ||--o{ inventory_history : "1 to many"
    products ||--o{ sales : "1 to many"
    sales ||--|| revenue : "1 to 1"

    categories {
        int id PK
        varchar(255) name
    }

    products {
        int id PK
        varchar(255) name
        decimal(10,2) price
        text description
        int category_id FK
    }

    inventory {
        int id PK
        int product_id FK
        int quantity
    }

    inventory_history {
        int id PK
        int inventory_id FK
        timestamp changed_at
        int previous_quantity
        int new_quantity
        text description
    }

    sales {
        int id PK
        int product_id FK
        int quantity
        decimal(10,2) total_price
        date sale_date
    }

    revenue {
        int id PK
        int sale_id FK
        decimal(10,2) revenue_amount
        date created_at
    }

    users {
        int id PK
        varchar(255) email
        varchar(255) password
        boolean is_admin
    }
```

## Foreign Key Constraints

| Child Table         | Child Column   | Parent Table | Parent Column | On Delete | Relationship Type |
| ------------------- | -------------- | ------------ | ------------- | --------- | ----------------- |
| `products`          | `category_id`  | `categories` | `id`          | CASCADE   | Many-to-One       |
| `inventory`         | `product_id`   | `products`   | `id`          | CASCADE   | One-to-One        |
| `inventory_history` | `inventory_id` | `inventory`  | `id`          | CASCADE   | One-to-Many       |
| `sales`             | `product_id`   | `products`   | `id`          | CASCADE   | Many-to-One       |
| `revenue`           | `sale_id`      | `sales`      | `id`          | CASCADE   | One-to-One        |

### Constraint Details:

- **CASCADE**: When a referenced row is deleted, all related rows are automatically deleted

### Relationship Types:

- **Many-to-One**: Many child records reference one parent (e.g., many products per category)
- **One-to-One**: Exactly one child record per parent (e.g., one inventory per product)
- **One-to-Many**: One parent has many child records (e.g., one inventory has many history entries)

# API Endpoints

| Endpoint                                   | Method | Description                                                                  | Admin Bearer Token Required |
| ------------------------------------------ | ------ | ---------------------------------------------------------------------------- | --------------------------- |
| `/v2/users`                                | POST   | Create a user                                                                | No                          |
| `/v2/auth/login`                           | POST   | Login                                                                        | No                          |
| `/v2/products`                             | POST   | Create product                                                               | Yes                         |
| `/v2/products`                             | GET    | Get products                                                                 | No                          |
| `/v2/products/stats`                       | GET    | Get products stats                                                           | No                          |
| `/v2/products/{product_id}`                | GET    | Get product by id                                                            | No                          |
| `/v2/products/category/{category_id}`      | GET    | Get products by category                                                     | No                          |
| `/v2/sales`                                | GET    | Get sales                                                                    | No                          |
| `/v2/sales/by-date-range`                  | GET    | Get sales by date range                                                      | No                          |
| `/v2/sales/stats`                          | GET    | Get sales stats                                                              | No                          |
| `/v2/sales/{sales_id}`                     | GET    | Get sales by id                                                              | No                          |
| `/v2/sales/product/{product_id}`           | GET    | Get sales by product                                                         | No                          |
| `/v2/sales/product/{product_id}/details`   | GET    | Get sales and product details                                                | No                          |
| `/v2/sales/category/{category_id}`         | GET    | Get sales by category                                                        | No                          |
| `/v2/sales/category/{category_id}/details` | GET    | Get sales and category details                                               | No                          |
| `/v2/revenue`                              | GET    | Get revenue                                                                  | No                          |
| `/v2/revenue/by-date-range`                | GET    | Get revenue by date range                                                    | No                          |
| `/v2/revenue/by-time-period`               | GET    | Get total revenue, top N sales, and bottom N sales for the given time period | No                          |
| `/v2/revenue/compare`                      | GET    | Compare revenue between two timeframes                                       | No                          |
| `/v2/inventory`                            | GET    | Get all inventory items                                                      | No                          |
| `/v2/inventory/low-stock`                  | GET    | Get low stock items                                                          | No                          |
| `/v2/inventory/product/{product_id}`       | GET    | Get inventory by product                                                     | No                          |
| `/v2/inventory/product/{product_id}`       | PATCH  | Update product inventory                                                     | Yes                         |
| `/v2/inventory/history`                    | GET    | Get inventory history                                                        | No                          |
| `/v2/inventory/history/{inventory_id}`     | GET    | Get inventory history by id                                                  | No                          |

**Key Points:**

- APIs requiring Bearer tokens are accessible only after admin user authentication, i.e. login using `/v2/auth/login` endpoint.
- For detailed information on available parameters, refer to the `/docs` endpoint.

### Prerequisites

- Python (3.7+)
- MySQL (v8+)

# Installation

- **Clone the repository**

```bash
git clone https://github.com/iamibadd/forsit-ecommerce-apis.git
cd forsit-ecommerce-apis
```

- **Set Up MySQL**

- Ensure MySQL is installed on your system. If not, download it from [MYSQL Downloads](https://www.oracle.com/mysql/technologies/mysql-enterprise-edition-downloads.html) and complete the installation.
- Create a MySQL user and set a password if you haven’t already.
- Open a terminal and connect to MySQL:

```bash
mysql -u your-db-username -p
```

Replace your-db-username with your actual MySQL username (e.g., root, ibad, etc.).

- Create the database:

```bash
CREATE DATABASE IF NOT EXISTS forsit_ecommerce;
```

**Configure Environment Variables**

- Create a .env file in the project root and update the configuration:

Run the following command to populate the database with initial data:

```bash
DB_HOST = localhost
DB_USER = root
DB_PASSWORD = 9214s818
DB_NAME = forsit_ecommerce
JWT_SECRET_KEY = forsit_ecommerce
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 30
```

Replace your-password with your actual MySQL password.

- **Populate the Database**

```bash
 mysql -u your-db-username -p forsit_ecommerce < populate_db.sql
```

Again, replace your-db-username with your MySQL username.

- **Install Dependencies**

Use `pip` to install the required packages:

```bash
pip install -r requirements.txt
```

- **Run the Application**

Navigate to the `app` directory and start the development server:

```bash
cd app
fastapi dev main.py
```

The `app` folder structure and project template are based on the official [FastAPI Documentation](https://fastapi.tiangolo.com) and the offical [FastAPI Full-Stack Template](https://github.com/fastapi/full-stack-fastapi-template/tree/master/backend) documentation.

Happy Hacking!
