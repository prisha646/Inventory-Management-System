
import streamlit as st

# PAGE SETTINGS
st.set_page_config(
    page_title="Inventory Management",
    page_icon="📦",
    layout="wide"
)


# LIGHT THEME

st.markdown("""
<style>

.stApp {
    background-color: #F5F7FB;
}

[data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 1px solid #E5E7EB;
}

h1, h2, h3 {
    color: #172554;
}

p {
    color: #475569;
}

div.stButton > button {
    background-color: #2563EB;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 18px;
    font-weight: 600;
}

div.stButton > button:hover {
    background-color: #1D4ED8;
    color: white;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #E2E8F0;
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stMetricValue"] {
    color: #1D4ED8;
}

</style>
""", unsafe_allow_html=True)

# SAMPLE PRODUCTS

if "products" not in st.session_state:

    st.session_state.products = [
        {"id": 101, "name": "Laptop", "price": 45000, "quantity": 10},
        {"id": 102, "name": "Smartphone", "price": 18000, "quantity": 15},
        {"id": 103, "name": "Mouse", "price": 500, "quantity": 25},
        {"id": 104, "name": "Keyboard", "price": 1200, "quantity": 18},
        {"id": 105, "name": "Monitor", "price": 8500, "quantity": 8}
    ]


if "sales" not in st.session_state:
    st.session_state.sales = []


products = st.session_state.products
sales = st.session_state.sales


# SIDEBAR MENU

st.sidebar.title("📦 Stock Manager")
st.sidebar.caption("Inventory Management System")

st.sidebar.divider()

choice = st.sidebar.radio(
    "MAIN MENU",
    [
        "Dashboard",
        "View Products",
        "Add Product",
        "Search Product",
        "Update Stock",
        "Delete Product",
        "Sell Product",
        "Sales Report",
        "Low Stock Alert",
        "Inventory Summary"
    ]
)

st.sidebar.divider()

st.sidebar.info("Manage your business inventory easily.")

# COMMON PRODUCT DATA

total_products = len(products)

total_quantity = sum(
    product["quantity"] for product in products
)

total_value = sum(
    product["price"] * product["quantity"]
    for product in products
)

total_revenue = sum(
    sale["total"] for sale in sales
)

# DASHBOARD


if choice == "Dashboard":

    st.title("📊 Inventory Dashboard")

    st.write("Welcome to your Smart Inventory Management System.")

    st.divider()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Products",
        total_products
    )

    col2.metric(
        "Total Stock",
        total_quantity
    )

    col3.metric(
        "Inventory Value",
        f"₹{total_value:,.0f}"
    )

    col4.metric(
        "Total Revenue",
        f"₹{total_revenue:,.0f}"
    )

    st.divider()

    st.subheader("📋 Recent Inventory")

    if products:
        st.dataframe(
            products,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("No products available.")

    st.subheader("⚠️ Stock Alerts")

    low_stock = [
        product for product in products
        if product["quantity"] <= 5
    ]

    if low_stock:

        for product in low_stock:
            st.warning(
                f"{product['name']} has only "
                f"{product['quantity']} items left!"
            )

    else:
        st.success("All products have sufficient stock!")

# VIEW PRODUCTS

elif choice == "View Products":

    st.title("📦 Product Inventory")

    if products:

        st.dataframe(
            products,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("No products available!")


# ADD PRODUCT

elif choice == "Add Product":

    st.title("➕ Add New Product")

    with st.form("add_product_form"):

        product_id = st.number_input(
            "Product ID",
            min_value=1,
            step=1
        )

        name = st.text_input("Product Name")

        price = st.number_input(
            "Product Price (₹)",
            min_value=0.0
        )

        quantity = st.number_input(
            "Product Quantity",
            min_value=0,
            step=1
        )

        submit = st.form_submit_button("Add Product")

        if submit:

            if name.strip() == "":
                st.warning("Please enter product name!")

            elif any(p["id"] == product_id for p in products):
                st.error("Product ID already exists!")

            else:

                products.append({
                    "id": product_id,
                    "name": name,
                    "price": price,
                    "quantity": quantity
                })

                st.success("Product added successfully! 🎉")


# SEARCH PRODUCT


elif choice == "Search Product":

    st.title("🔍 Search Product")

    search_name = st.text_input(
        "Enter product name"
    )

    if search_name:

        found_products = [
            p for p in products
            if search_name.lower() in p["name"].lower()
        ]

        if found_products:

            st.success("Product found!")

            st.dataframe(
                found_products,
                use_container_width=True,
                hide_index=True
            )

        else:
            st.error("Product not found!")


# UPDATE STOCK

elif choice == "Update Stock":

    st.title("📦 Update Product Stock")

    if products:

        product_id = st.selectbox(
            "Select Product",
            [p["id"] for p in products],
            format_func=lambda pid: next(
                p["name"] for p in products if p["id"] == pid
            )
        )

        new_quantity = st.number_input(
            "Enter New Quantity",
            min_value=0,
            step=1
        )

        if st.button("Update Stock"):

            for product in products:

                if product["id"] == product_id:

                    product["quantity"] = new_quantity

                    st.success("Stock updated successfully!")

                    break

    else:
        st.warning("No products available!")



# DELETE PRODUCT

elif choice == "Delete Product":

    st.title("🗑️ Delete Product")

    if products:

        product_id = st.selectbox(
            "Select Product to Delete",
            [p["id"] for p in products],
            format_func=lambda pid: next(
                p["name"] for p in products if p["id"] == pid
            )
        )

        if st.button("Delete Product"):

            for product in products:

                if product["id"] == product_id:

                    products.remove(product)

                    st.success("Product deleted successfully!")

                    break

    else:
        st.warning("No products available!")


# SELL PRODUCT

elif choice == "Sell Product":

    st.title("🛒 Sell Product")

    if products:

        with st.form("sell_product_form"):

            product_id = st.selectbox(
                "Select Product",
                [p["id"] for p in products],
                format_func=lambda pid: next(
                    p["name"] for p in products if p["id"] == pid
                )
            )

            sell_quantity = st.number_input(
                "Enter Quantity",
                min_value=1,
                step=1
            )

            submit = st.form_submit_button("Sell Product")

            if submit:

                for product in products:

                    if product["id"] == product_id:

                        if product["quantity"] >= sell_quantity:

                            product["quantity"] -= sell_quantity

                            total = product["price"] * sell_quantity

                            sales.append({
                                "id": product["id"],
                                "name": product["name"],
                                "quantity": sell_quantity,
                                "total": total
                            })

                            st.success("Product sold successfully!")

                            st.write("Product:", product["name"])

                            st.write("Total Amount: ₹", total)

                        else:
                            st.error("Not enough stock available!")

                        break

    else:
        st.warning("No products available!")


# SALES REPORT

elif choice == "Sales Report":

    st.title("📈 Sales Report")

    if sales:

        st.subheader("Sales Details")

        st.dataframe(
            sales,
            use_container_width=True,
            hide_index=True
        )

        st.metric(
            "Total Sales Revenue",
            f"₹{total_revenue:,.2f}"
        )

        st.subheader("Sales Graph")

        st.bar_chart(
            [sale["total"] for sale in sales]
        )

    else:
        st.warning("No sales recorded yet!")


# LOW STOCK ALERT

elif choice == "Low Stock Alert":

    st.title("⚠️ Low Stock Alert")

    low_stock = [
        product for product in products
        if product["quantity"] <= 5
    ]

    if low_stock:

        for product in low_stock:

            st.error(
                f"{product['name']} - "
                f"Only {product['quantity']} items left!"
            )

    else:
        st.success("All products have sufficient stock!")


# INVENTORY SUMMARY

elif choice == "Inventory Summary":

    st.title("📊 Inventory Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Products", total_products)

    col2.metric("Total Stock", total_quantity)

    col3.metric("Total Value", f"₹{total_value:,.2f}")

    st.divider()

    st.subheader("Complete Inventory")

    if products:

        st.dataframe(
            products,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.warning("Inventory is empty!")

    st.success("Inventory Summary Generated!")
