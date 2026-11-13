from playwright.sync_api import Page, expect


BASE_URL = "https://www.saucedemo.com"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
PRODUCT = "Sauce Labs Backpack"


def login(page: Page, password: str = PASSWORD) -> None:
    page.goto(f"{BASE_URL}/")
    page.locator('[data-test="username"]').fill(USERNAME)
    page.locator('[data-test="password"]').fill(password)
    page.locator('[data-test="login-button"]').click()


def test_login_page_is_displayed(page: Page) -> None:
    page.goto(f"{BASE_URL}/")
    expect(page.locator('[data-test="username"]')).to_be_visible()
    expect(page.locator('[data-test="password"]')).to_be_visible()
    expect(page.locator('[data-test="login-button"]')).to_be_visible()


def test_successful_login(page: Page) -> None:
    login(page)
    expect(page).to_have_url(f"{BASE_URL}/inventory.html")
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()


def test_catalog_is_displayed(page: Page) -> None:
    login(page)
    expect(page.locator('[data-test="title"]')).to_have_text("Products")
    product = page.locator('[data-test="inventory-item"]').filter(has_text=PRODUCT)
    expect(product.locator('[data-test="inventory-item-name"]')).to_have_text(PRODUCT)
    expect(product.get_by_role("button", name="Add to cart", exact=True)).to_be_enabled()


def test_add_product_to_cart(page: Page) -> None:
    login(page)
    expect(page.locator('[data-test="inventory-container"]')).to_be_visible()
    page.locator('[data-test="add-to-cart-sauce-labs-backpack"]').click()
    expect(page.locator('[data-test="shopping-cart-badge"]')).to_have_text("1")

    page.locator('[data-test="shopping-cart-link"]').click()
    expect(page).to_have_url(f"{BASE_URL}/cart.html")
    items = page.locator('[data-test="inventory-item"]')
    expect(items).to_have_count(1)
    expect(items.locator('[data-test="inventory-item-name"]')).to_have_text(PRODUCT)
    expect(items.locator('[data-test="item-quantity"]')).to_have_text("1")


def test_login_with_invalid_password(page: Page) -> None:
    login(page, password="wrong_password")
    error = page.locator('[data-test="error"]')
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")
    expect(page).to_have_url(f"{BASE_URL}/")
